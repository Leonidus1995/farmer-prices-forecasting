from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.ingestion.download_faostat_bulk import main as download_faostat_bulk_main

with DAG(
    dag_id="faostat_ppi_pipeline",
    description="End-to-end pipeline for FAOSTAT-based PPI forecasting",
    start_date=datetime(2026, 5, 5),
    schedule="@daily",
    catchup=False,
    tags=["faostat", "ppi", "etl", "ml"],
) as dag:
    faostat_data_ingestion = PythonOperator(
        task_id="faostat_data_ingestion",
        python_callable=download_faostat_bulk_main,
    )