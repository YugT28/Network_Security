from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
load_dotenv()

with DAG(
    dag_id = 'network_security',
    default_args = {'retires':2},
    description='network security pipeline',
    schedule_interval='@weekly',
    start_date=pendulum.datetime(year=2024,month=8,day=31,tz='UTC'),
    catchup=False,
    tags=['example'],
) as dag:
    def training(**kwargs):
        from network_security.pipeline.training_pipeline import TrainingPipeline
        training_obj=TrainingPipeline()
        training_obj.run_pipeline()

    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = "mynetworksecurity"
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models ")

    training_pipeline = PythonOperator(
        task_id='Train_pipeline',
        python_callable=training
    )

    sync_data_to_s3 = PythonOperator(
        task_id="sync_data_to_s3",
        python_callable=sync_artifact_to_s3_bucket
    )

    training_pipeline >> sync_data_to_s3