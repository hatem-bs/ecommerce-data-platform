# 🛒 E-Commerce Data Platform

> Production-ready data engineering platform for e-commerce analytics using **PySpark**, **Databricks**, **dbt** & **AWS**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20IAM-orange.svg)](https://aws.amazon.com/)
[![Databricks](https://img.shields.io/badge/Databricks-Community-red.svg)](https://databricks.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#%EF%B8%8F-architecture)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Business Metrics](#-business-metrics)
- [Documentation](#-documentation)

---

## 🎯 Project Overview

This project demonstrates **modern data engineering best practices** by building a scalable analytics platform for e-commerce data.

**Key achievements:**
- ✅ **100,000+ transactions** processed using Medallion architecture
- ✅ **Automated data quality** validation with Great Expectations
- ✅ **Infrastructure as Code** with Terraform
- ✅ **CI/CD pipeline** with GitHub Actions
- ✅ **Business-ready KPIs** for e-commerce analytics

**Dataset:** Brazilian E-Commerce Public Dataset (Olist - Kaggle)

---

## 🏗️ Architecture
```
┌─────────────┐
│   Kaggle    │
│   Dataset   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  AWS S3 Data Lake                   │
│  bronze/ → silver/ → gold/          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Databricks (PySpark)               │
│  • Bronze: Raw ingestion            │
│  • Silver: Cleaned & validated      │
│  • Gold: Business aggregations      │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Analytics Layer                    │
│  • SQL Dashboard (Databricks)       │
│  • Business KPIs                    │
└─────────────────────────────────────┘
```

**Full architecture diagram:** [See docs/architecture.md](docs/architecture.md)

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Cloud** | AWS S3 | Data Lake storage |
| **Compute** | Databricks Community | PySpark processing |
| **Transformation** | dbt-core | SQL-based modeling |
| **Orchestration** | Apache Airflow | Workflow automation |
| **Data Quality** | Great Expectations | Automated validation |
| **IaC** | Terraform | Infrastructure management |
| **CI/CD** | GitHub Actions | Automated testing & deployment |
| **Language** | Python 3.9+ | Scripting & automation |

---

## ✨ Features

### **1. Medallion Architecture (Bronze → Silver → Gold)**
- **Bronze Layer:** Raw data ingestion with schema validation
- **Silver Layer:** Cleaned, deduplicated, and enriched data
- **Gold Layer:** Business-ready aggregations and KPIs

### **2. Data Quality Framework**
- Automated data quality checks with Great Expectations
- Schema validation on ingestion
- Referential integrity tests
- Business rule validations

### **3. Infrastructure as Code**
- Fully reproducible AWS infrastructure with Terraform
- IAM roles and policies with least-privilege access
- S3 bucket lifecycle policies

### **4. CI/CD Pipeline**
- Automated testing on every commit
- Code quality checks (pylint, black)
- Automated deployment to S3

### **5. Comprehensive Documentation**
- Architecture Decision Records (ADR)
- Data lineage documentation
- Setup guides and runbooks

---

## 🚀 Getting Started

### **Prerequisites**

- Python 3.9+
- AWS Account (Free Tier)
- Databricks Community Account
- Git

### **Installation**
```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/ecommerce-data-platform.git
cd ecommerce-data-platform

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AWS credentials
aws configure

# 5. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 6. Run setup script
python scripts/setup.py
```

**Detailed setup guide:** [docs/setup.md](docs/setup.md)

---

## 📁 Project Structure
```
ecommerce-data-platform/
├── docs/                   # Documentation
├── infrastructure/         # Terraform IaC
├── notebooks/             # Databricks notebooks
├── scripts/               # Python utilities
├── sql/                   # SQL transformations
├── tests/                 # Automated tests
└── README.md
```

**Full structure explanation:** [docs/project-structure.md](docs/project-structure.md)

---

## 📈 Business Metrics Delivered

This platform generates the following KPIs:

1. **Customer Lifetime Value (CLV)**
2. **Delivery Performance SLA** (% on-time deliveries)
3. **Product Category Profitability**
4. **Customer Segmentation (RFM Analysis)**
5. **Churn Prediction Features**

---

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Setup Guide](docs/setup.md)
- [Data Model](docs/data-model.md)
- [Architecture Decision Records](docs/adr/)
- [Contributing Guide](docs/CONTRIBUTING.md)

---

## 👤 Author

**[Hatem BEN SALEM]**  
*Data Engineer | AWS | Databricks | PySpark | Python*

- 💼 LinkedIn: [hatembs](https://www.linkedin.com/in/hatembs/)
- 🐙 GitHub: [hatem-bs](https://github.com/hatem-bs)
- 📧 Email: hatem.bensalem@hotmail.com

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Dataset: [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Inspired by modern data engineering practices from Netflix, Uber, and Airbnb