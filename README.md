

# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
  
  
  
  
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
Install airflow
  
```bash
export AIRFLOW_HOME=/home/civis/git/airflow-docker/airflow_tutorial    
cd
nano .bashrc 
```  
 Добовляем в .bashrc 
```bash
export AIRFLOW_HOME=/home/civis/git/airflow-docker/airflow_tutorial
```   
Сохраняем и выходим  
 
```bash
cd ~/de_zoomcamp_project/airflow
terraform init
terraform plan
terraform apply
```  
  



