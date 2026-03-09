"""
S3 utilities for Spark-based data pipelines.

These functions provide high-level abstractions for common S3 operations

Author: Hatem BEN SALEM
Date: 2026-02-24
"""

import logging
from datetime import datetime
from typing import Optional
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import current_timestamp, lit
from src.config.settings import (
    S3_BUCKET_NAME,
    PARTITION_FORMAT,
    OUTPUT_FORMAT,
    WRITE_MODE,
)

logger = logging.getLogger(__name__)


def build_s3_path(
    prefix: str, table_name: str, partition_date: Optional[str] = None
) -> str:
    """
    Build S3 path following Medallion architecture conventions.

    Args:
        prefix: S3 prefix (bronze/silver/gold)
        table_name: Table name
        partition_date: Date partition (YYYY-MM-DD). If None, no partition.

    Returns:
        Full S3 path (s3a://bucket/prefix/table/date=YYYY-MM-DD/)

    Example:
        >>> build_s3_path("bronze", "orders", "2024-02-19")
        's3a://my-bucket/bronze/orders/date=2024-02-19/'

    Best Practice:
    - Use s3a:// (not s3://) for better performance with Spark
    - Always include trailing slash for directories
    - Use partitioning for incremental processing
    """

    base_path = f"s3a://{S3_BUCKET_NAME}/{prefix}/{table_name}"

    return f"{base_path}/{partition_date}/" if partition_date else f"{base_path}"


def write_to_s3(
    df: DataFrame,
    s3_prefix: str,
    table_name: str,
    partition_date: Optional[str] = None,
    partition_cols: Optional[str] = None,
    mode: str = WRITE_MODE,
) -> bool:
    """
    Write Spark DataFrame to S3 as Parquet with metadata.

    Args:
        df: Spark DataFrame to write
        s3_prefix: S3 prefix (bronze/silver/gold)
        table_name: Table name
        partition_date: Date partition (YYYY-MM-DD)
        partition_cols: Columns to partition by (in addition to date)
        mode: Write mode (overwrite/append)

    Returns:
        True if successful, False otherwise

    Example:
        >>> df_orders = spark.read.csv("orders.csv", header=True)
        >>> write_to_s3(df_orders, "bronze", "orders", "2024-02-19")

    Best Practice:
    - Always add ingestion metadata (timestamp, date)
    - Use partitioning for efficient querying
    - Overwrite mode for daily batches, append for streaming
    """

    try:
        df_with_metadata = df.withColumn(
            "ingestion_date", current_timestamp()
        ).withColumn(
            "ingestion_date",
            lit(partition_date or datetime.now().strftime(PARTITION_FORMAT)),
        )

        s3_path = build_s3_path(s3_prefix, table_name, partition_date)

        # Count rows before write
        row_count = df_with_metadata.count()
        logger.info(f"📊 Writing {row_count:,} rows to {s3_path}")

        # Prepare writer
        writer = df_with_metadata.write.format(OUTPUT_FORMAT).mode(mode)

        if partition_cols:
            writer = writer.partitionBy(partition_cols)

        writer.save(s3_path)
        logger.info(f"✅ Successfully write {row_count:,} rows to {s3_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Error writing to S3: {e}")
        return False


def read_from_s3(
    spark: SparkSession,
    s3_prefix: str,
    table_name: str,
    partition_date: Optional[str] = None,
) -> Optional[DataFrame]:
    """
    Read parquet data from S3 into Dataframe
    Args:
        spark: SparkSession
        s3_prefix: S3 prefix (bronze/silver/gold)
        table_name: Table name
        partition_date: Date partition (if None, reads all partitions)
    
    Returns:
        Spark DataFrame or None if error
    
    Example:
        >>> df = read_from_s3(spark, "bronze", "orders", "2024-02-19")
    
    Best Practice:
    - Use partition for better performance
    - Cache DataFrame if used multiple times 
    """

    try:
        s3_path = build_s3_path(s3_prefix,table_name,partition_date)

        logger.info(f"📖 Reading from {s3_path}")
        df = spark.read.parquet(s3_path)
        
        row_count = df.count()
        logger.info(f"✅ Read {row_count:,} rows from {s3_path}")
        
        return df
    except Exception as e:
        logger.error(f"❌ Error reading from S3: {e}")
        return None
