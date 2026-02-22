# ADR 001: Adoption de la Medallion Architecture

**Status:** Accepted  
**Date:** 2026-02-21  
**Author:** [Hatem BEN SALEM]  
**Deciders:** [Hatem BEN SALEM]   

---

## Context

This project requires a scalable and maintenable data architecture, using modern data engineering best practices. 

### Requirements

- 100k+ transactions e-commerce
- Reproductable and testable Pipeline
- Segregation of raw data and business data
- Idempotent data reprocessing capabilities without raw data re-integration

---

## Decision

Use **Medallion Architecture** (Bronze → Silver → Gold) to structure our Data Lake and pipelines.

### Architecture Layers

**Bronze (Raw Zone):**
- Raw data, immutable
- Parquet format
- Immutable (append-only)
- Schema minimal validation

**Silver (Refined Zone):**
- Data cleaned and validated
- Déduplication, type-checked
- Enrich with dimensions
- Great Expectations validation gates

**Gold (Curated Zone):**
- Agregation business-ready
- KPIs
- Optimized for BI queries
- Star schema / Data Marts

---

## Consequences

### Positive

✅ **Separation of concerns:** Each layer has a well-defined responsibility
✅ **Reproducibility:** Immutable Bronze enables deterministic reprocessing of Silver/Gold
✅ **Performance:** Pre-aggregated Gold tables → low-latency BI dashboards
✅ **Quality gates:** Data validation enforced at every promotion stage
✅ **Industry standard:** Pattern widely adopted (Netflix, Uber, LinkedIn)
✅ **Collaboration:** Data engineers operate on Bronze/Silver, analysts consume Gold

### Negative

⚠️ **Initial complexity:** Three-tier pipeline instead of a single-layer model
⚠️ **Storage cost:** Data duplication across Bronze + Silver + Gold
⚠️ **Latency:** Multi-hop processing (bronze → silver → gold) compared to single-hop

### Mitigation

**Complexity:** Mitigated through clear documentation and reusable pipeline templates
**Storage:** S3 lifecycle policies (archive Bronze after 90 days to Glacier)
**Latency:** Acceptable for daily batch workloads (non-real-time use cases)

---

## Alternatives Considered

### Alternative 1: Single Layer (Bronze only)

**Rejected because:**
- No separation between raw and business data
- Transformations coupled with ingestion logic
- Hard to maintain and test
- Not scalable for multi-team environments

### Alternative 2: Lambda Architecture (Batch + Streaming)

**Rejected because:**
- Over-engineering in this use case : daily batch processing is sufficient
- Operational complexity too high
- Dataset Kaggle is not streaming-based

### Alternative 3: Data Vault 2.0

**Rejected because:**
- Too complex for a solo/portfolio project
- Better suited for long-term historical data warehousing
- Significant modeling overhead (hubs, links, satellites)

---

## Implementation Notes

### File Structure
```
s3://kaggle-e-commerce-datalake-us-east-1/
├── bronze/
│   ├── orders/date=2024-02-19/orders.parquet
│   └── customers/date=2024-02-19/customers.parquet
├── silver/
│   ├── orders_cleaned/date=2024-02-19/
│   └── customers_enriched/date=2024-02-19/
└── gold/
    ├── daily_revenue/date=2024-02-19/
    └── customer_lifetime_value/date=2024-02-19/
```

### Processing Pattern
```python
# Bronze: Minimal transformation
df_bronze = spark.read.csv("source.csv")
df_bronze.write.parquet("s3://bucket/bronze/")

# Silver: Clean & enrich
df_silver = (
    spark.read.parquet("s3://bucket/bronze/")
    .dropDuplicates()
    .withColumn("clean_field", clean_udf("raw_field"))
)
validate_expectations(df_silver)  # Great Expectations
df_silver.write.parquet("s3://bucket/silver/")

# Gold: Aggregate
df_gold = (
    spark.read.parquet("s3://bucket/silver/")
    .groupBy("customer_id")
    .agg(sum("revenue").alias("lifetime_value"))
)
df_gold.write.parquet("s3://bucket/gold/")
```

---

## References

- [Databricks: Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [Delta Lake: Multi-hop Architecture](https://docs.delta.io/latest/best-practices.html)
- [Data Engineering Best Practices - Netflix](https://netflixtechblog.com/)

---

## Change History

| Date | Author | Change |
|------|--------|--------|
| 2024-02-22 | Hatem BEN SALEM | Initial version |