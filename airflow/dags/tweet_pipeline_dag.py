"""
ChargeNow Case Study – Airflow DAG

This DAG demonstrates:
- Orchestration of tweet extraction
- Retry logic for robustness
- Parameterized date windows (support for reprocessing past intervals)
- dbt transformation step placeholder
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract.fetch_tweets import fetch_tweets


def extract_tweets(**context):
    start = context["data_interval_start"].isoformat()
    end = context["data_interval_end"].isoformat()

    print(f"[INFO] Extracting tweets from {start} → {end}")
    data = fetch_tweets(start, end)

    # save raw JSON to disk/S3/Snowflake stage - placeholder
    print(f"[INFO] Raw extraction complete. Records: {len(data.get('data', []))}")


def run_dbt_models(**context):
    print("[INFO] Running dbt models (mock placeholder).")
    # dbt run --models stg_* silver_* gold_*  (placeholder)


default_args = {
    "owner": "data-engineering",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="chargenow_tweet_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    default_args=default_args,
    description="ChargeNow ELT pipeline for #ChargeNow tweets",
) as dag:

    extract = PythonOperator(
        task_id="extract_tweets",
        python_callable=extract_tweets,
    )

    dbt_run = PythonOperator(
        task_id="run_dbt_models",
        python_callable=run_dbt_models,
    )

    extract >> dbt_run
