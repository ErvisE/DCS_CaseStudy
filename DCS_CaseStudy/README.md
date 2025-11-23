# ChargeNow Tweet Pipeline – Data Engineering Case Study

This repository contains the **full case study implementation**, aligned with the final PDF version including all four diagrams placed in their relevant sections.

## 1. Overview

This project describes a conceptual but realistic data pipeline that ingests tweets containing **#ChargeNow**, stores them in Snowflake, models them with **dbt**, and orchestrates everything with **Airflow**.

The goal is to show how I would structure and implement a robust, production-ready data flow aligned with the DCS Senior Data Engineer role.

## 2. High-Level Architecture

![Current Architecture](./images/architecture.png)

Core technologies:

- Python for ingestion and small transformations
- Airflow for orchestration
- Snowflake as central analytical warehouse
- dbt for modeling (staging → silver → gold)
- PostgreSQL optionally for operational/low-latency use cases

## 3. Storage Strategy – Bronze / Silver / Gold

![Data Layers – Bronze / Silver / Gold](./images/layers.png)

- **Bronze (Raw):** Full-fidelity JSON from Twitter API (Snowflake VARIANT or object storage)
- **Silver (Processed):** Parsed, cleaned, normalized models in dbt
- **Gold (Curated):** Business-ready facts/dimensions or flat tables for BI and analytics

## 4. Orchestration – Airflow

![Airflow DAG](./images/airflow_dag.png)

The Airflow DAG conceptually:

- Extracts tweets from Twitter API (#ChargeNow)
- Loads raw JSON into Snowflake
- Runs dbt models to build staging, silver, and gold layers
- Optionally syncs curated data into PostgreSQL

See `airflow/dags/tweet_pipeline_dag.py` for a simplified example DAG structure.

## 5. Dream Architecture (Future, High Scale)

![Dream Architecture – Future High Scale](./images/dream_architecture.png)

In a future scenario with much higher volume (streaming charging events, IoT, etc.), a streaming and data lake layer (Kafka/PubSub/Kinesis + Spark/Flink + Parquet) can complement Snowflake and dbt.

Snowflake remains the **gold layer** for analytics and BI, while Spark/Flink handle heavy, real-time stream processing.

## 6. Repository Structure

```text
chargenow-pipeline/
│
├── airflow/
│   └── dags/
│       └── tweet_pipeline_dag.py
│
├── src/
│   ├── extract/
│   │   └── fetch_tweets.py
│   └── utils/
│       └── hashing.py
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_tweets.sql
│   │   ├── silver/
│   │   └── gold/
│   └── tests/
│
├── images/
│   ├── architecture.png
│   ├── layers.png
│   ├── airflow_dag.png
│   └── dream_architecture.png
│
└── README.md
```

## 7. How to Run Locally (Conceptual)

This repository is **conceptual** and meant for discussion; however, a realistic local setup would look like this:

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/chargenow-pipeline.git
   cd chargenow-pipeline
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies (example)**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables for Twitter and Snowflake**
   ```bash
   export TWITTER_BEARER_TOKEN="..."
   export SNOWFLAKE_ACCOUNT="..."
   export SNOWFLAKE_USER="..."
   export SNOWFLAKE_PASSWORD="..."
   export SNOWFLAKE_WAREHOUSE="..."
   export SNOWFLAKE_DATABASE="..."
   export SNOWFLAKE_SCHEMA="..."
   ```

5. **Run the extraction script (standalone)**
   ```bash
   python src/extract/fetch_tweets.py
   ```

6. **Airflow**
   - Place the DAG file under your Airflow `dags/` folder.
   - Configure an Airflow connection/variables for credentials.
   - Trigger the DAG from the Airflow UI.

7. **dbt**
   - Place `dbt/` under a dbt project structure.
   - Configure `profiles.yml` for Snowflake.
   - Run:
     ```bash
     dbt run
     dbt test
     ```

> Note: In this case study, focus is on **architecture and design**, not on providing fully runnable production code. The structure and placeholders show how the project would be organized in a real implementation.

## 8. Technologies

- Python 3.x
- Airflow
- Snowflake
- dbt
- PostgreSQL (optional)
- Git / GitHub

## 9. License

This repository is intended as an interview case study and reference implementation.  
Use it as inspiration or reference for your own data engineering designs.
