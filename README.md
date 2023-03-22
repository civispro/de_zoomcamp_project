# ✨ Welcome to my data engenering zoomcamp project

This project analyze popularity of prrogramming languages


## Tech Stack

**Client:** React, Redux, TailwindCSS

**Server:** Node, Express


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Installation

Clone repo to your computer
  ```bash
  git clone https://github.com/civispro/de_zoomcamp_project.git
  cd de_zoomcamp_project
```
Setup [connection to google cloud](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup)  and aplly terraform  

```bash
gcloud auth application-default login
terraform init
terraform plan
terraform apply
```

[Install spark](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md) 
  
    
  
  
  
```bash
conda install  setuptools  

```  
  
  
  
  
Install airflow
  
```bash
export AIRFLOW_HOME=/de_zoomcamp_project/airflow    
cd
nano .bashrc 
```  
 Добовляем в .bashrc 
```bash
export AIRFLOW_HOME=/de_zoomcamp_project/airflow
```   
Сохраняем и выходим  
 
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
  
Кладем ключ гугла cred.json в папку airflow
  



