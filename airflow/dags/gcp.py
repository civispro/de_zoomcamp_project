from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator
import requests
import os


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
    }

def get_age():
    print(123)
    response = requests.get("https://raw.githubusercontent.com/civispro/de_zoomcamp_project/main/pldb.csv")
    open("ipldb.csv", "wb").write(response.content)

    #with open('pl2.csv', 'x') as f:
        #f.write('Create a new text file!')

with DAG(
    dag_id='gcp_v21',
    default_args=default_args,
    description='This is our gcp dag',
    start_date=datetime.today(),
    schedule_interval='@hourly'
) as dag:
    GCS_Files = GoogleCloudStorageListOperator(
    task_id='GCS_Files',
    bucket='project_data_lake_forward-cacao-374915',
    prefix='.',
    delimiter='.csv',
    gcp_conn_id="GCPCon"
    )
    task2 = BashOperator(
        task_id='second_task',
        bash_command="curl -O https://raw.githubusercontent.com/civispro/de_zoomcamp_project/main/pldb.csv"
    )
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    task4 = BashOperator(
        task_id='fourts_task',
        bash_command="pwd"
    )

    gcp_operator = FileToGoogleCloudStorageOperator(
        task_id='gcp_upload',
        src='ipldb.csv',
        dst='ipldb.csv',
        bucket='project_data_lake_forward-cacao-374915',
        gcp_conn_id="GCPCon",
        mime_type='Folder',
        dag=dag
    )
    

    task3>>task2>>task4>>GCS_Files>>gcp_operator
