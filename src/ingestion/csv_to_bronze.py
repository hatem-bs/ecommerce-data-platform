"""
Ingest Kaggle CSV files to S3 bronze layer using PySpark.

This script reads CSV files, applies schema validation, and writes to S3
as Parquet with date partitioning.

Usage:
    spark-submit src/ingestion/csv_to_bronze.py --date 2026-02-19
    python src/ingestion/csv_to_bronze.py --tables orders customers

Author: Hatem BEN SALEM
Date: 2024-02-19
"""

import datetime
import logging
import argparse
from pathlib import Path
import sys
from pyspark.sql import SparkSession

from src.config.settings import (
    RAW_DATA_DIR,
    CSV_FILES,
    S3_BRONZE_PREFIX,
    PARTITION_FORMAT,
    LOG_LEVEL,
)
from src.config.schemas import get_schema, SCHEMAS
from src.utils.spark_session import get_spark_session, stop_spark_session
from src.utils.s3_utils import write_to_s3

logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Kaggle ecommerce data ingestion to S3 using PySpark"
    )

    parser.add_argument(
        "--date",
        type=str,
        default=datetime.datetime.now().strftime(PARTITION_FORMAT),
        help=f"Partition date (format: {PARTITION_FORMAT}). Default: today",
    )

    parser.add_argument(
        "--tables",
        nargs="+",
        choices=list(CSV_FILES.keys()),
        default=list(CSV_FILES.keys()),
        help="Specific tables to process (default: all)",
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without writing to S3"
    )

    return parser.parse_args()


def ingest_table(
    spark: SparkSession,
    table_name: str,
    partition_date: str,
    dry_run: bool = False,
) -> bool:
    """
    Ingest a single CSV table to S3 bronze layer.

    Args:
        spark: SparkSession
        table_name: Table name
        partition_date: Date partition (YYYY-MM-DD)
        dry_run: If True, don't write to S3

    Returns:
        True if successful, False otherwise
    """

    logger.info("=" * 80)
    logger.info(f"📊 Processing table: {table_name}")
    logger.info("=" * 80)

    filename = CSV_FILES[table_name]
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        logger.error(f"❌ File not found: {file_path}")
        return False
    try:
        schema = get_schema(table_name) if table_name in SCHEMAS else None

        logger.info(f"📖 Reading CSV: {file_path}")
        df_reader = spark.read.option("header", "true").option(
            "infer_schema", "false" if schema else "true"
        )
        if schema:
            df_reader = df_reader.schema(schema)
        df = df_reader.csv(str(file_path))

        row_count = df.count()
        col_count = len(df.columns)
        logger.info(f"Loaded {row_count} rows, {col_count} columns")

        logger.info(f"Schema: {df.printSchema()}")

        if dry_run:
            logger.info("🔍 DRY RUN: Skipping S3 write")
            return True

        success: bool = write_to_s3(
            df=df,
            s3_prefix=S3_BRONZE_PREFIX,
            table_name=table_name,
            partition_date=partition_date,
        )
        return success

    except Exception as e:
        logger.error(f"❌ Error processing {table_name}: {e}")
        return False


def main() -> int:
    """
    Main Execution function

    Returns: 0 on success, 1 on error
    """
    print("call main")
    logger.info("=" * 80)
    logger.info("🚀 Starting Bronze Ingestion Pipeline ")
    logger.info("=" * 80)

    args = parse_args()
    partition_date = args.date
    tables_to_process = args.tables
    dry_run = args.dry_run

    logger.info(f"📅 Partition date: {partition_date}")
    logger.info(f"📋 Tables to process: {', '.join(tables_to_process)}")

    if dry_run:
        logger.info("🔍 DRY RUN MODE - No data will be written to S3")

    spark = get_spark_session()

    results: dict[str, bool] = {}
    start_time = datetime.datetime.now()

    for table_name in tables_to_process:
        success = ingest_table(spark, table_name, partition_date, dry_run)
        results[table_name] = success

    # Summary
    logger.info("=" * 80)
    logger.info("📈 INGESTION SUMMARY")
    logger.info("=" * 80)

    successful: int = sum(1 for v in results.values() if v)
    failed: int = len(results) - successful
    total_execution = (datetime.datetime.now() - start_time).total_seconds()

    logger.info(f"✅ Successful: {successful}/{len(results)}")
    logger.info(f"❌ Failed: {failed}/{len(results)}")
    logger.info(f"⏱️ Total execution time: {total_execution:.2f} seconds")

    logger.info("📋 Detailed Results:")
    for table, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"  {table:30s} {status}")

    stop_spark_session(spark)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
