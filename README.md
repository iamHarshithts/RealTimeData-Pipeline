# High-Level Architecture Overview

## **End-to-End Data Engineering Pipeline (Data Generation → Kafka → MinIO → PySpark → PostgreSQL → Airflow)**

This architecture represents a complete **modern data engineering pipeline**, implemented using **Docker**, with orchestration, real-time streaming, fraud detection, and multi-layered storage.


### 1. Data Generation Layer (Simulated Source System)

Synthetic financial data is generated using Python + Faker, including:

* **User Profiles**
* **Merchant Information**
* **Account Balances**
* **Real-Time Transactions**

This simulates transactional data similar to real banking, e-commerce, or payment platforms.

Data is produced into **Kafka topics**:

```
user_profiles
merchant_info
account_balances
transactions
```

---

### 2. Kafka – Real-Time Message Streaming Backbone

Kafka serves as the ingestion layer.
It captures all incoming events and streams them to downstream components.

### Topics represent different data domains:

* `user_profiles` → static user data
* `merchant_info` → business data
* `account_balances` → financial balances
* `transactions` → continuous streaming data

Kafka ensures:

* decoupled producers/consumers
* buffering
* event durability
* real-time ingestion

---

### 3. MinIO – S3-Compatible Data Lake (Bronze Layer)

All Kafka-consumed data is written into MinIO as raw JSON, forming the **Bronze Layer**.

### Bronze Storage Structure:

```
bronze/
   profiles-folder/
   merchant-folder/
   account-folder/
   transactions-folder/
```

MinIO acts as:

* Object storage
* Data lake
* Checkpoint store for streaming
* Persistent raw data archive

---

### 4. PySpark Processing (Silver + Gold Layers)

PySpark reads data from MinIO using the **S3A connector** inside Docker.
This forms two major transformation layers:

---

## 4.1 Silver Layer (Cleaned & Standardized Data)

PySpark performs:

* schema enforcement
* filtering invalid IDs
* trimming & cleaning strings
* duplicate removal
* date & time extraction
* splitting names
* normalizing country/currency

Silver Layer output is stored as **Parquet** in MinIO:

```
silver/processed-profiles/
silver/processed-merchants/
silver/processed-accounts/
```

---

### 4.2 Gold Layer (PostgreSQL Warehouse)

Cleaned Silver data is written to PostgreSQL tables:

* **USERS**
* **ACCOUNTS**
* **MERCHANTS**

These are structured, relationally optimized tables for:

* analytics
* dashboards
* reporting

---

### 5. Real-Time Fraud Detection (Spark Structured Streaming)

Live transaction events from MinIO (Bronze) are processed using **Spark Streaming**.

### Fraud Rules include:

* High online amount (> 30,000)
* Suspicious merchants
* High-risk geolocations
* Unusually huge amounts

### Streaming Output:

```
FraudTransaction      → PostgreSQL
GenuineTransaction    → PostgreSQL
```

Additionally:

* Fraud events printed on console
* Checkpointing stored in MinIO

This adds real-time intelligence to the system.

---

### 6. Airflow – Orchestration Layer

Airflow automates the end-to-end pipeline inside Docker:

### Orchestrates:

* Kafka topic resets
* Data ingestion threads
* Spark Silver batch jobs
* Spark Gold ETL jobs
* Real-time streaming jobs

Airflow services:

* **Webserver (UI)** → Port 8080
* **Scheduler** → Executes DAGs
* **Metadata DB** → PostgreSQL

---

### 7. Dockerized Infrastructure

All services run as Docker containers:

* **MinIO** (object storage)
* **PostgreSQL** (database)
* **PgAdmin** (DB GUI)
* **Airflow Webserver + Scheduler + Init**
* **Spark jobs run locally but connect to MinIO/Postgres**

Volumes ensure persistence:

* `minio_data` → S3 objects
* `postgres_data` → databases

This creates a reproducible, production-like development environment.

---

### 8. End-to-End Architecture Flow

```
[Data Generators]
       ↓
    Kafka
       ↓ (Consumers)
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
       ↓
      Airflow
(Automation & Scheduling)
```

---

### 9. What This Architecture Enables

* Real-time event processing
* Batch ETL (Bronze → Silver → Gold)
* Fraud detection system
* Data warehouse in PostgreSQL
* Reproducible environment through Docker
* Full orchestration with Airflow
* Scalable and cloud-ready S3-backed storage

---

#### 10. Summary

This architecture is a **complete enterprise-grade data engineering pipeline**, integrating:

* **Real-time streaming**
* **Batch ETL**
* **Data lake + Data warehouse**
* **Fraud detection intelligence**
* **Containerized orchestration**




