# 🔢 History of programming languages

Data Engineering project to demonstrate pipelines for Data Engineering Zoomcamp. 



## Problem

This project aims to show some interesting statistics of the Stack-Overflow's public dataset in BigQuery.

Some of the questions answered (taken from google cloud page):

    What is the percentage of questions that have been answered over the years?
    What is the reputation and badge count of users across different tenures on StackOverflow?
    What are 10 of the “easier” gold badges to earn?
    Which day of the week has most questions answered within an hour?



## Dataset

The dataset contains information on over 4000 programming languages. Which include facts about the language such as what year it was created, What is its rank, and other parameters that you will come to know once you explore the dataset.

[Kaggle](https://www.kaggle.com/datasets/sujaykapadnis/programming-language-database) 

## Conclusion



## Dashboard

![Dashboard](https://user-images.githubusercontent.com/123605185/227710734-0ea83474-41fc-40d7-906f-2d997486ee42.png)



## Tech Stack

Python, Apache Airflow, Apache Spark with PySpark, dbt, Google Cloud Platform, Metabase

## Installation

#### Clone repo to your computer
  ```bash
  git clone https://github.com/civispro/de_zoomcamp_project.git
  cd de_zoomcamp_project
```
#### Setup [connection to google cloud](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup) and aplly terraform  
```bash
gcloud auth application-default login
terraform init
terraform plan
terraform apply
```
#### [Install Apache Spark with PySpark](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md)  
```bash
conda install  setuptools  
```  
   
#### Install Apache Spark
  
```bash
export AIRFLOW_HOME=/de_zoomcamp_project/airflow    
cd
nano .bashrc 
```  
###### add to .bashrc 
```bash
export AIRFLOW_HOME=/de_zoomcamp_project/airflow
```   
###### save and exit 
```bash
cd /de_zoomcamp_project/airflow
pip install 'apache-airflow==2.5.1'  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.9.txt"
airflow db init
airflow users create \	
    --username airflow \
    --firstname airflow \
    --lastname airflow \
    --role Admin \
    --email li@li.ru  
airflow webserver -p 8080
airflow scheduler

```   
###### Put GCP credentials "cred.json" to the folder named airflow

#### Sign up on [dbt cloud](https://www.getdbt.com/) and use dbt folder from this repo
```bash
dbt build
```   
#### Run Metabase in docker to vizualize data
```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

## Dashboard

![Dashboard](https://user-images.githubusercontent.com/123605185/227710734-0ea83474-41fc-40d7-906f-2d997486ee42.png)

