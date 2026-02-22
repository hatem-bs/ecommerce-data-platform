"""
Architecture Diagram Generator
Generates modern, production-ready architecture diagrams for the e-commerce data platform.

Author: [Hatem BEN SALEM]
Date: 2024-02-19
"""

from pathlib import Path
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.custom import Custom
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Spark
from diagrams.programming.language import Python
from diagrams.programming.framework import React

ICONS_DIR = Path(__file__).parent.parent / "icons"

# Configuration du style
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "ortho",  # Lignes orthogonales (plus propres)
}

node_attr = {
    "fontsize": "12",
    "height": "1.2",
    "width": "1.2",
}

edge_attr = {
    "fontsize": "10",
}

with Diagram(
    "E-Commerce Data Platform - Modern Architecture",
    filename="docs/diagrams/architecture",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
):
    
    # ====================
    # DATA SOURCES
    # ====================
    with Cluster("Data Sources"):
        kaggle = Custom("Kaggle Dataset\n(100k orders)", str(ICONS_DIR / "kaggle.png")) \
                 if True else Python("Kaggle\nDataset")
    
    # ====================
    # INGESTION LAYER
    # ====================
    with Cluster("Ingestion Layer"):
        upload_script = Python("Upload Script\n(boto3)")
    
    # ====================
    # STORAGE LAYER (AWS S3)
    # ====================
    with Cluster("Data Lake (AWS S3)"):
        with Cluster("Bronze Layer"):
            bronze_s3 = S3("Raw Data\n(Immutable)")
        
        with Cluster("Silver Layer"):
            silver_s3 = S3("Cleaned Data\n(Validated)")
        
        with Cluster("Gold Layer"):
            gold_s3 = S3("Business Metrics\n(Aggregated)")
    
    # ====================
    # PROCESSING LAYER
    # ====================
    with Cluster("Processing (Databricks)"):
        with Cluster("Bronze Processing"):
            bronze_spark = Spark("PySpark\nIngestion")
        
        with Cluster("Silver Processing"):
            silver_spark = Spark("PySpark\nTransformations")
        
        with Cluster("Gold Processing"):
            gold_spark = Spark("PySpark\nAggregations")
    
    # ====================
    # DATA QUALITY
    # ====================
    with Cluster("Data Quality & Governance"):
        great_expectations = Python("Great\nExpectations")
        iam = IAM("IAM Roles\n(RBAC)")
        monitoring = Cloudwatch("CloudWatch\nLogs")
    
    # ====================
    # ORCHESTRATION
    # ====================
    with Cluster("Orchestration"):
        airflow = Airflow("Apache Airflow\n(DAGs)")
    
    # ====================
    # ANALYTICS LAYER
    # ====================
    with Cluster("Analytics & Consumption"):
        databricks_sql = Custom("Databricks SQL", str(ICONS_DIR / "databricks.png")) \
                        if True else React("Dashboard")
    
    # ====================
    # FLOW CONNECTIONS
    # ====================
    
    # Data flow
    kaggle >> Edge(label="CSV files") >> upload_script
    upload_script >> Edge(label="boto3 upload") >> bronze_s3
    
    # Bronze to Silver
    bronze_s3 >> Edge(label="read") >> bronze_spark
    bronze_spark >> Edge(label="validate") >> great_expectations
    bronze_spark >> Edge(label="write") >> silver_s3
    
    # Silver to Gold
    silver_s3 >> Edge(label="read") >> silver_spark
    silver_spark >> Edge(label="quality checks") >> great_expectations
    silver_spark >> Edge(label="write") >> gold_s3
    
    # Gold aggregations
    gold_s3 >> Edge(label="read") >> gold_spark
    gold_spark >> Edge(label="write") >> gold_s3
    
    # Analytics consumption
    gold_s3 >> Edge(label="query") >> databricks_sql
    
    # Orchestration
    airflow >> Edge(label="trigger", style="dashed") >> bronze_spark
    airflow >> Edge(label="trigger", style="dashed") >> silver_spark
    airflow >> Edge(label="trigger", style="dashed") >> gold_spark
    
    # Security & Monitoring
    iam >> Edge(label="access control", style="dotted") >> bronze_s3
    iam >> Edge(label="access control", style="dotted") >> silver_s3
    iam >> Edge(label="access control", style="dotted") >> gold_s3
    
    monitoring >> Edge(label="logs", style="dotted") >> bronze_spark
    monitoring >> Edge(label="logs", style="dotted") >> silver_spark
    monitoring >> Edge(label="logs", style="dotted") >> gold_spark

print("✅ Architecture diagram generated: docs/diagrams/architecture.png")