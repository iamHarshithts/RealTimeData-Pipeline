# End-to-End Data Engineering Pipeline

## Overview
## **End-to-End Data Engineering Pipeline (Data Generation → Kafka → MinIO → PySpark → PostgreSQL)**
This project implements a complete **modern data engineering pipeline** using Docker, real-time streaming, batch processing, a data lake, and a data warehouse.


---

## High-Level Architecture

```
[Data Generators]
       ↓
   Kafka (Docker)
       ↓
   MinIO (Bronze JSON)
       ↓
   PySpark Cleaning
       ↓
 MinIO (Silver Parquet)
       ↓
 PySpark → PostgreSQL
  (Gold Tables)
       ↓
 Real-time Spark Streaming
       ↓
 PostgreSQL Fraud Tables
```

---

## 1. Data Generation Layer

Synthetic financial data is generated using **Python + Faker**:

* User profiles
* Merchant information
* Account balances
* Real-time transactions

Data is produced to Kafka topics:

```
user_profiles
merchant_info
account_balances
transactions
```

---

## 2. Kafka – Real-Time Streaming (Dockerized)

Kafka runs fully inside Docker and serves as the event streaming backbone.

Responsibilities:

* Decoupled producers and consumers
* Message durability
* Real-time ingestion
* Topic-based domain separation

Topics:

* `user_profiles`
* `merchant_info`
* `account_balances`
* `transactions`

---

## 3. MinIO – Data Lake (Bronze Layer)

Kafka consumers persist all raw messages into MinIO as JSON objects.

Directory structure:

```
bronze/
   profiles-folder/
   merchant-folder/
   account-folder/
   transactions-folder/
```

MinIO is used as:

* Object store
* Data lake
* Streaming checkpoints
* Raw data archive

---

## 4. PySpark Processing

### 4.1 Silver Layer – Cleaned & Standardized

PySpark reads JSON from MinIO and performs:

* Schema enforcement
* Deduplication
* Data cleansing
* Date normalization
* Currency/country normalization

Output stored in Parquet format:

```
silver/processed-profiles/
silver/processed-merchants/
silver/processed-accounts/
```

---

### 4.2 Gold Layer – PostgreSQL Warehouse

Silver layer outputs are loaded into PostgreSQL:

Tables:

* USERS
* ACCOUNTS
* MERCHANTS

Use cases:

* Data analytics
* Reporting
* Business intelligence

---

## 5. Real-Time Fraud Detection

Spark Structured Streaming processes transactions from MinIO.

Fraud rules:

* Amount > 30,000
* Suspicious merchants
* High-risk locations
* Abnormal spending patterns

Results:

```
FraudTransaction   → PostgreSQL
GenuineTransaction → PostgreSQL
```

Additional features:

* Console logging for fraud alerts
* Checkpointing in MinIO

---

## 6. Dockerized Infrastructure

All services run inside Docker containers:

* Kafka
* MinIO
* PostgreSQL
* pgAdmin

Volumes ensure persistence:

* `minio_data` → data lake
* `postgres_data` → warehouse

---

## 7. What This Enables

* End-to-end streaming + batch
* Data lake + data warehouse
* Real-time fraud detection
* Fully reproducible local environment


---

## 8. Summary

This project demonstrates a production-style data engineering pipeline without orchestration frameworks, focusing on:

* Kafka-based ingestion
* S3-backed data lake
* Spark transformations
* PostgreSQL analytics layer
* Dockerized architecture
