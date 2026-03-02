"""
Configuration management for the data platform.

This module centralizes all configuration, loading from environment variables
with sensible defaults. All settings are validated at import time.

Author: Hatem BEN SALEM
Date: 2026-02-22
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# load env variables from .env
load_dotenv()


# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
LOGS_DIR = PROJECT_ROOT / "logs"

# ensure directories exists
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# AWS CONFIGURATION
# ============================================================================
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

# ============================================================================
# S3 STRUCTURE (Medallion Architecture)
# ============================================================================

S3_BRONZE_PREFIX = "bronze"
S3_SILVER_PREFIX = "silver"
S3_GOLD_PREFIX = "gold"
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# ============================================================================
# SPARK CONFIGURATION
# ============================================================================

SPARK_APP_NAME = "ecommerce-data-platform"
# Spark master (local for development, yarn/k8s for production)
SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
SPARK_CONFIGS: dict = {
    # AWS S3 access
    "spark.hadoop.fs.s3a.access.key": AWS_ACCESS_KEY_ID,
    "spark.hadoop.fs.s3a.secret.key": AWS_SECRET_ACCESS_KEY,
    "spark.hadoop.fs.s3a.endpoint": f"s3.{AWS_REGION}.amazonaws.com",
    "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
    # Optimization
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    # Parquet optimization
    "spark.sql.parquet.compression.codec": "snappy",
    "spark.sql.parquet.mergeSchema": "false",
    # Memory
    "spark.driver.memory": "4g",
    "spark.executor.memory": "4g",
}


# ============================================================================
# DATA SOURCES (Kaggle Dataset)
# ============================================================================

CSV_FILES: dict[str, str] = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_categories": "product_category_name_translation.csv",
}


# ============================================================================
# PROCESSING CONFIGURATION
# ============================================================================

# Date partition format
PARTITION_FORMAT = "%Y-%m-%d"  # Date partition format
OUTPUT_FORMAT = "parquet"
WRITE_MODE = "overwrite"  # or "append" for incremental

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# VALIDATION
# ============================================================================


def validate_config() -> None:
    """
    Validate required configuration.

    Raises:
        ValueError: If required config is missing
    """
    required: dict = {
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        "S3_BUCKET_NAME": S3_BUCKET_NAME,
    }

    missing = [k for k, v in required.items() if not v]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please set them in your .env file."
        )


# Auto-validate on import
validate_config()
