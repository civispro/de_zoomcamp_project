import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq
from airflow.models import Variable
import pathlib
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import pandas as pd
import shutil
from os import listdir
from os.path import isfile, join


PROJECT_ID = "forward-cacao-374915"
BUCKET = "project_data_lake_forward-cacao-374915"
BIGQUERY_DATASET = "project_data"

dataset_file = "pldb.csv"
dataset_url = f"https://raw.githubusercontent.com/civispro/de_zoomcamp_project/main/{dataset_file}"
path_to_local_home = os.environ.get("AIRFLOW_HOME", pathlib.Path().resolve())
parquet_file = dataset_file.replace('.csv', '.parquet')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".cred.json"


def format_to_parquet(src_file):
    spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
    df = pd.read_csv("pldb.csv", usecols = ['title','appeared','type','lastActivity','githubBigQuery.repos','country'])
    df=df.dropna(subset=['title', 'appeared', 'lastActivity', 'type'])
    values = {"country": "World", "githubBigQuery.repos": 0}
    df=df.fillna(value=values)
    df["githubBigQuery.repos"] = df["githubBigQuery.repos"].astype(int)
    df = df[(df['appeared'] >=1901) & (df['lastActivity']>=1901)]
    df = df.rename(columns={"githubBigQuery.repos": "repos"})
    df.to_csv("pldb_small.csv",index=False)

    pl_schema = types.StructType([
    types.StructField("title", types.StringType(), True),
        types.StructField("appeared", types.TimestampType(), True),
        types.StructField("type", types.StringType(), True),
        types.StructField("lastActivity", types.TimestampType(), True),
        types.StructField("repos", types.IntegerType(), True),
        types.StructField("country", types.StringType(), True)

    ])

    df_pl = spark.read \
    .option("header", "true") \
    .schema(pl_schema) \
    .csv("pldb_small.csv")

    dir_path = "pq"
    shutil.rmtree(dir_path, ignore_errors=True)
    print("Deleted '%s' directory successfully" % dir_path)

    df_pl\
    .repartition(4) \
    .write.parquet("pq/")



def upload_files(bucket):
    localFolder="pq/"
    """Upload files to GCP bucket."""
    files = [f for f in listdir(localFolder) if isfile(join(localFolder, f))]
    for file in files:
        localFile = localFolder  + file
        blob = bucket.blob(localFile)
        blob.upload_from_filename(localFile)
    return f'Uploaded {files} to bucket.'


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    #upload_local_directory_to_gcs(local_path, bucket, BUCKET_FOLDER_DIR)

    client = storage.Client()
    bucket = client.bucket(bucket)


    #bucket = client.get_bucket(bucket)
    blobs = bucket.list_blobs(prefix='pq')
    for blob in blobs:
        blob.delete()

    #blob = bucket.blob(object_name)
    #blob.upload_from_filename(local_file)
    #blob = bucket.blob("pq")
    upload_files(bucket)

    #blob.upload_from_filename("pq")


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_gcp_15",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSL {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )


    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="external_table_pldb",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table_pldb",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/pq/*.parquet"],
            },
        },
    )   


    download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task
