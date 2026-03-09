"""
SparkSession factory with optimized configurations.

This module provides a centralized way to create SparkSession instances
with consistent configurations across all pipelines.

Author: Hatem BEN SALEM
Date: 2026-02-24
"""

import logging
from typing import Optional

from pyspark.sql import SparkSession
from src.config.settings import SPARK_APP_NAME, SPARK_MASTER, SPARK_CONFIGS


logger = logging.getLogger(__name__)


def get_spark_session(
    app_name: Optional[str] = None,
    master: Optional[str] = None,
    additional_configs: Optional[dict[str, str]] = None,
) -> SparkSession:
    """
    Create or get existing SparkSession with optimized configurations.

    Args:
        app_name: Spark application name (default: from config)
        master: Spark master URL (default: from config)
        additional_configs: Additional Spark configurations

    Returns:
        Configured SparkSession

    Example:
        >>> spark = get_spark_session()
        >>> df = spark.read.csv("s3a://bucket/data.csv")

    Best Practice:
    - Reuse the same SparkSession across an application (singleton pattern)
    - Configure S3 access at session level (not per-read)
    - Enable adaptive query execution for performance
    """
    app_name = app_name or SPARK_APP_NAME
    master = master or SPARK_MASTER

    logger.info(f"Creating SparkSession: {app_name}")
    builder = SparkSession.builder.appName(app_name).master(master)

    for k, v in SPARK_CONFIGS.items():
        if v is not None:
            builder = builder.config(k, v)

    if additional_configs:
        for k, v in additional_configs.items():
            builder = builder.config(k, v)

    spark = builder.getOrCreate()

    # Set log level to reduce verbosity
    spark.sparkContext.setLogLevel("WARN")

    logger.info(f"   SparkSession created: {spark.version}")
    logger.info(f"   Master: {spark.sparkContext.master}")
    logger.info(f"   App ID: {spark.sparkContext.applicationId}")

    return spark


def stop_spark_session(spark: SparkSession) -> None:
    """
    Stop SparkSession.

    Args:
        spark: SparkSession to stop

    Best Practice: Always stop SparkSession at end of application to release resources.
    """
    if spark:
        logger.info("Stopping SparkSession...")
        spark.stop()
        logger.info("✅ SparkSession stopped")
