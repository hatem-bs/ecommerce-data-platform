"""
Spark schema definitions for all tables.

Defining schemas explicitly (instead of inferring) provides:
- Better performance (no schema inference overhead)
- Type safety (catch issues early)
- Documentation (schemas are self-documenting)

Author: Hatem BEN SALEM
Date: 2026-02-24
"""

from pyspark.sql.types import (
    StructType,
    StructField,
    DoubleType,
    IntegerType,
    StringType,
    TimestampType,
)


# ============================================================================
# BRONZE LAYER SCHEMAS (Raw CSV schemas)
# ============================================================================

ORDERS_SCHEMA = StructType(
    [
        StructField("order_id", StringType(), nullable=False),
        StructField("customer_id", StringType(), nullable=False),
        StructField("order_status", StringType(), nullable=True),
        StructField("order_purchase_timestamp", TimestampType(), nullable=True),
        StructField("order_approved_at", TimestampType(), nullable=True),
        StructField("order_delivered_carrier_date", TimestampType(), nullable=True),
        StructField("order_delivered_customer_date", TimestampType(), nullable=True),
        StructField("order_estimated_delivery_date", TimestampType(), nullable=True),
    ]
)

CUSTOMERS_SCHEMA = StructType(
    [
        StructField("customer_id", StringType(), nullable=False),
        StructField("customer_unique_id", StringType(), nullable=True),
        StructField("customer_zip_code_prefix", StringType(), nullable=True),
        StructField("customer_city", StringType(), nullable=True),
        StructField("customer_state", StringType(), nullable=True),
    ]
)

ORDER_ITEMS_SCHEMA = StructType(
    [
        StructField("order_id", StringType(), nullable=False),
        StructField("order_item_id", IntegerType(), nullable=False),
        StructField("product_id", StringType(), nullable=False),
        StructField("seller_id", StringType(), nullable=False),
        StructField("shipping_limit_date", TimestampType(), nullable=True),
        StructField("price", DoubleType(), nullable=True),
        StructField("freight_value", DoubleType(), nullable=True),
    ]
)

ORDER_PAYMENTS_SCHEMA = StructType(
    [
        StructField("order_id", StringType(), nullable=False),
        StructField("payment_sequential", IntegerType(), nullable=True),
        StructField("payment_type", StringType(), nullable=True),
        StructField("payment_installments", IntegerType(), nullable=True),
        StructField("payment_value", DoubleType(), nullable=True),
    ]
)

PRODUCTS_SCHEMA = StructType(
    [
        StructField("product_id", StringType(), nullable=False),
        StructField("product_category_name", StringType(), nullable=True),
        StructField("product_name_lenght", IntegerType(), nullable=True),
        StructField("product_description_lenght", IntegerType(), nullable=True),
        StructField("product_photos_qty", IntegerType(), nullable=True),
        StructField("product_weight_g", IntegerType(), nullable=True),
        StructField("product_length_cm", IntegerType(), nullable=True),
        StructField("product_height_cm", IntegerType(), nullable=True),
        StructField("product_width_cm", IntegerType(), nullable=True),
    ]
)

SELLERS_SCHEMA = StructType(
    [
        StructField("seller_id", StringType(), nullable=False),
        StructField("seller_zip_code_prefix", StringType(), nullable=True),
        StructField("seller_city", StringType(), nullable=True),
        StructField("seller_state", StringType(), nullable=True),
    ]
)

ORDER_REVIEWS_SCHEMA = StructType(
    [
        StructField("review_id", StringType(), nullable=False),
        StructField("order_id", StringType(), nullable=False),
        StructField("review_score", IntegerType(), nullable=True),
        StructField("review_comment_title", StringType(), nullable=True),
        StructField("review_comment_message", StringType(), nullable=True),
        StructField("review_creation_date", TimestampType(), nullable=True),
        StructField("review_answer_timestamp", TimestampType(), nullable=True),
    ]
)

# map table names to schema
SCHEMAS: dict = {
    "orders": ORDERS_SCHEMA,
    "customers": CUSTOMERS_SCHEMA,
    "order_items": ORDER_ITEMS_SCHEMA,
    "order_payments": ORDER_PAYMENTS_SCHEMA,
    "products": PRODUCTS_SCHEMA,
    "sellers": SELLERS_SCHEMA,
    "order_reviews": ORDER_REVIEWS_SCHEMA,
}


def get_schema(table_name: str) -> StructType:
    """
    Get SPark schema for a given table
    Args:
    table_name: name of the table
    returns:
    StrutcType schema
    Raises:
    ValueError: if table does not found
    """
    if table_name not in SCHEMAS:
        raise ValueError(f"Schema not defined for table: {table_name}")

    return SCHEMAS[table_name]


# get_schema(table_name="orders")
