# Installation & Setup Guide

> Step-by-step guide to set up the E-Commerce Data Platform on **Windows**.

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Application runtime |
| Java (JDK) | 17 (64-bit) | Spark runtime (JVM) |
| Apache Spark | 3.5.x | Data processing engine |
| AWS CLI | v2 | AWS credential management |
| Git | 2.x+ | Version control |

---

## 1. Java JDK 17 (64-bit)

Spark requires a **64-bit JDK** (not JRE).

### Install Amazon Corretto 17

1. Download from [Amazon Corretto 17](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/downloads-list.html)
2. Install to `D:\Tools\jdk17.x.x_x` (or your preferred path)

### Configure environment variable

```
JAVA_HOME = D:\Tools\jdk17.0.18_9
```

Add `%JAVA_HOME%\bin` to the system `Path`.

### Verify

```bash
java -version
# Expected: OpenJDK 64-Bit Server VM (NOT Client VM)
```

> **Important:** A 32-bit JRE will cause `JAVA_GATEWAY_EXITED` errors in PySpark.

---

## 2. Apache Spark 3.5.x

### Install

1. Download [Spark 3.5.x pre-built for Hadoop 3](https://spark.apache.org/downloads.html)
2. Extract to `D:\Tools\spark-3.5.x-bin-hadoop3`

### Configure environment variables

```
SPARK_HOME  = D:\Tools\spark-3.5.x-bin-hadoop3
HADOOP_HOME = D:\Tools\spark-3.5.x-bin-hadoop3
```

Add to the system `Path`:
- `%SPARK_HOME%\bin`
- `%HADOOP_HOME%\bin`

### Hadoop Windows binaries (winutils.exe)

Spark on Windows requires native Hadoop binaries.

1. Download `winutils.exe` and `hadoop.dll` matching your Hadoop version from
   [github.com/cdarlint/winutils](https://github.com/cdarlint/winutils) (branch `hadoop-3.3.x`)
2. Copy both files to `%HADOOP_HOME%\bin\`

> **Note:** Make sure both files are **64-bit** (`PE32+ executable`).
> If you still get `NativeIO$Windows.access0` errors, the `hadoop.dll` may be
> incompatible. The project is configured with `fs.s3a.fast.upload.buffer=bytebuffer`
> and `io.native.lib.available=false` to work around this on Windows.

### Verify

```bash
spark-submit --version
```

---

## 3. AWS CLI & Credentials

### Install AWS CLI v2

Download from [AWS CLI v2 for Windows](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

### Configure credentials

```bash
aws configure
```

```
AWS Access Key ID:     YOUR_ACCESS_KEY
AWS Secret Access Key: YOUR_SECRET_KEY
Default region name:   us-east-1
Output format:         json
```

This creates `~/.aws/credentials` and `~/.aws/config`.

### Required IAM permissions

The IAM user needs the following S3 permissions on the data lake bucket:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:Gekaggle-e-commerce-datalake-us-east-1tObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR_BUCKET_NAME",
                "arn:aws:s3:::YOUR_BUCKET_NAME/*"
            ]
        }
    ]
}
```

Or attach the managed policy `AmazonS3FullAccess` for development.

### Verify

```bash
aws s3 ls s3://YOUR_BUCKET_NAME/
```

---

## 4. Project Setup

### Clone & create virtual environment

```bash
git clone https://github.com/hatem-bs/ecommerce-data-platform.git
cd ecommerce-data-platform

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

### Environment variables (.env)

Create a `.env` file at the project root:

```dotenv
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION="us-east-1"
AWS_DEFAULT_REGION="us-east-1"
S3_BUCKET_NAME="your-bucket-name"
```

> **Tip:** Make sure the `AWS_SECRET_ACCESS_KEY` is the complete key — a truncated
> key will cause `SignatureDoesNotMatch` errors.

### Download the Kaggle dataset

1. Download [Brazilian E-Commerce (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Extract all CSV files into `data/raw/`

---

## 5. Run the Pipeline

### Bronze ingestion (CSV → S3 Parquet)

```bash
# All tables
python -m src.ingestion.csv_to_bronze

# Specific tables
python -m src.ingestion.csv_to_bronze --tables orders customers

# Dry run (preview without writing to S3)
python -m src.ingestion.csv_to_bronze --dry-run
```

---

## Troubleshooting

### `JAVA_GATEWAY_EXITED`

**Cause:** Java is 32-bit, missing, or `JAVA_HOME` is not set.

**Fix:** Install a 64-bit JDK and set `JAVA_HOME`. Verify with:
```bash
java -version
# Must show "64-Bit Server VM"
```

### `SignatureDoesNotMatch` on S3

**Cause:** The `AWS_SECRET_ACCESS_KEY` in `.env` is incorrect or truncated.

**Fix:** Compare with `~/.aws/credentials` and ensure they match exactly:
```bash
aws configure list
```

### `403 Forbidden` on S3

**Cause:** IAM user lacks S3 write permissions, or the S3 endpoint is wrong.

**Fix:**
1. Verify IAM permissions (see section 3)
2. Check `AWS_REGION` matches your bucket's actual region

### `NativeIO$Windows.access0` UnsatisfiedLinkError

**Cause:** `hadoop.dll` is missing or incompatible with your Hadoop version.

**Fix:** The project config already includes workarounds:
- `spark.hadoop.io.native.lib.available=false`
- `spark.hadoop.fs.s3a.fast.upload.buffer=bytebuffer`

If the error persists, download the matching `hadoop.dll` from
[cdarlint/winutils](https://github.com/cdarlint/winutils) and place it in `%HADOOP_HOME%\bin\`.

### Spark hangs when writing to S3

**Cause:** Invalid S3 endpoint (e.g., `s3.None.amazonaws.com`).

**Fix:** Ensure `AWS_REGION` is set in `.env`. Verify:
```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('AWS_REGION'))"
```

---

## Environment Variables Summary

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `JAVA_HOME` | Yes | `D:\Tools\jdk17.0.18_9` | Path to 64-bit JDK |
| `SPARK_HOME` | Yes | `D:\Tools\spark-3.5.8-bin-hadoop3` | Spark installation |
| `HADOOP_HOME` | Yes | `D:\Tools\spark-3.5.8-bin-hadoop3` | Same as SPARK_HOME |
| `AWS_ACCESS_KEY_ID` | Yes | `AKIA...` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | `wJal...` | AWS IAM secret key |
| `AWS_REGION` | Yes | `us-east-1` | AWS region |
| `S3_BUCKET_NAME` | Yes | `my-datalake-bucket` | S3 bucket name |
| `SPARK_MASTER` | No | `local[*]` | Spark master (default: local) |
| `LOG_LEVEL` | No | `INFO` | Logging level (default: INFO) |

### System Path entries

```
%JAVA_HOME%\bin
%SPARK_HOME%\bin
%HADOOP_HOME%\bin
```
