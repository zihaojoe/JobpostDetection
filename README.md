# MSiA 423 Project: Fake Job Posting Detection App
- **Author: Joe Zhang**    
- **QA: Zach Zhu**
- [Charter](#project-charter)
- [Backlog](#backlog)

## Project charter
### Vision
It is very difficult for students who have just graduated to judge the authenticity of a job posting because they lack experiences in the industry and are disadvantaged under the information asymmetry. Unlike illegal recruitment, fake recruitment often involves a legitimate company, who wants to gather wealth of information about the applicants and the job market as a whole, which can be monetized in multiple ways. This would leak the applicant's information and also waste much of their time. 
Therefore, in the project, I am going to develop an app which can help the applicants to determine whether a job posting is fake or real. (Assume that this is an extra function or app for job information providers such Glassdoor or LinkedIn)

### Mission
To design a web app, which allows users to input the information they have got regarding a job posting and gives them information for their decision based on a machine learning model.

The model will be trained in advance on a dataset that can be find on Kaggle. This link of the dataset is as follows:
<https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction>

### Success criteria
The success criteria can be divided into business measures and model performance measures.  

**Business criteria:**  
* User engagement: number of users using the app / visits in an interval of time  
* Conversion rate: number of users registering as membership / subscribing the company's service     

**Model criteria:**  
* The accuracy should be greater than 80%  
* The recall and precision should be both larger than 0.8

## Backlog

**Size of story**.
-   The magnitude of work planned. 
    -   0 points - quick chore
    -   1 point ~ 1 hour (small)
    -   2 points ~ 1/2 day (medium)
    -   4 points ~ 1 day (large)
    -   8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)

### Initiative 1: Help applicants precisely judge whether a job posting is fake or real
* Epic 1: Construct solid machine learning model candidates which satisfy the performance metrics
	- Story 1: Plan whether or not to / how to segement the job postings 
	- Story 2: Engineer features of the posting descriptions
	- Story 3: Verify segmentation and analyze the distributions of the features
	- Story 4: Build machine learning models to train the model
* Epic 2: Select and improve models
	- Story 1: Define major metrics of the model performance
	- Story 2: Determine 'best' models based on metrics defined
	- Story 3: Test segmentation and see if segmentation can improve the model
* Epic 3: Scripts and documentations
* Epic 4: Application deployment
	- Story 1: Encapsulate the model application into docker
	- Story 2: Use could service like RDS and S3 to deploy the application and data
	
### Initiative 2: Increase user engagement and app interactivity
* Epic 1: Build user-friendly web app page that reads users' inputs (frontend)
	- Story 1: Design structure and framework of the web app
	- Story 2: Define interface to connect to other application (Model Docker)
	- Story 3: Finalize the web page on the host
	- Story 4: Design and finalize web page style and layout
* Epic 2: Realize collection of new data
	- Story 1: Build interface that allows users to update new finds of fake or real job postings to the database
* Epic 3: Build a user report system that collects users' feedback
	- Story 1: Build interface that allows users to report whether a prediction is right
	- Story 2: Build interface that allows users to give feedback to the utility of the app
* Epic 4: Scripts and documentations
* Epic 5: Application deployment (backend)
	- Story 1: Encapsulate the model application into docker
	- Story 2: Use could service like RDS and S3 to deploy the application and data
	- Story 3: Finalize connection with model docker and database
* Epic 6: Test application and release
	- Story 1: Test the multiple components of the project
	- Story 2: Fix bugs
	- Story 3: Release application

### Backlog

* Initiative1.epic1.story1 (1 of story points) - PLANNED  
* Initiative1.epic1.story2 (4 of story points) - PLANNED  
* Initiative1.epic1.story3 (2 of story points) - PLANNED  
* Initiative1.epic1.story4 (2 of story points) - PLANNED  
* Initiative1.epic2.story1 (1 of story points) - PLANNED  
* Initiative1.epic2.story2 (2 of story points) - PLANNED  
* Initiative1.epic2.story3 (4 of story points) - PLANNED  
* Initiative1.epic3(2 of story points)  
* Initiative1.epic4.story1 (2 of story points)  
* Initiative1.epic4.story2 (8 of story points)  
* Initiative2.epic1.story1 (2 of story points)  
* Initiative2.epic1.story2 (1 of story points)  
* Initiative2.epic1.story3 (4 of story points)  
* Initiative2.epic1.story4 (4 of story points)  
* Initiative2.epic5 (2 of story points)  
* Initiative2.epic5.story1 (2 of story points)  
* Initiative2.epic5.story2 (4 of story points)  
* Initiative2.epic5.story3 (2 of story points)  
* Initiative2.epic6.story1 (2 of story points)  
* Initiative2.epic6.story2 (2 of story points)  
* Initiative2.epic6.story3 (0 of story points)  

### Icebox
* Initiative2.epic2.story1  
* Initiative2.epic3.story1  
* Initiative2.epic3.story2

## Documentation

## How to run?

### Module 1: Data Ingestion
#### 1. Set up environment: 

Go to the root directory of the project, and run:
```bash
cd model/config/
vi s3.env
```
* Set `MY_BUCKET` to the name of the bucket you want to put files in.
* Set `AWS_ACCESS_KEY_ID` to the access ID of your AWS.
* Set `AWS_SECRET_ACCESS_KEY` to the secret access ID of your AWS.
* Set `AWS_DEFAULT_REGION` to the default region of your AWS.

#### 2. Run the Docker to upload data to S3 bucket  

##### 2.1 Build Docker file 
Go to the root directory of the project, and run:   
```bash
cd model/
docker build -f Dockerfile -t jobpostmodel .
```
##### 2.2 Run Docker Container
Go to the root directory of the project, and run the following to upload data to S3:   
```bash
cd model/
docker run --mount type=bind,source="$(pwd)"/data,target=/JobpostDetection/model/data --env-file config/s3.env jobpostmodel upload_data.sh
```

### Module 2: Data Base Set up
#### 1. Set up environment:   

Go to the root directory of the project, and run:
```bash
cd web/config/
vi database.env
```
* Set `MYSQL_USER` to the "master username" that you used to create the database server.
* Set `MYSQL_PASSWORD` to the "master password" that you used to create the database server.
* Set `MYSQL_HOST` to be the RDS instance endpoint from the console.
* Set `MYSQL_HOST` to be `3306`.
* Set `DATABASE_NAME` to the name of the database you want to operate in.
* Set `SQLITE` to the host name for the sqlite base. 

**Notice:** 
* If you want to use MySQL, ignore the `SQLITE` variable. On the contrast, if you want to use SQLite, just set `SQLITE` and ignore all the others.
* Verify that you are on the northwestern vpn before you continue on with MySQL

#### 2. Run the Docker to upload data to S3 bucket  

##### 2.1 Build Docker file 
Go to the root directory of the project, and run:   
```bash
cd web/
docker build -f Dockerfile -t jobpostweb .
```
##### 2.2 Run Docker Container   
Go to the root directory of the project, and run the following to set up datebase withe the table reported_case:   
```bash
cd web/
docker run --mount type=bind,source="$(pwd)"/data,target=/JobpostDetection/web/data --env-file config/database.env jobpostweb db.py
```
**Notice: you can provide up to 3 parameters to the docker run command**     
--truncate: If given, delete current records from reported_case table before creating reported_case table.  
--sampledata:  If given, add a sample record after creating the reported_case table.  
--sqlite: If given, connect to local sqlite rather than mysql on RDS.  

For example, run the following to create database and truncate table in sqlite:
```bash
docker run --mount type=bind,source="$(pwd)"/data,target=/JobpostDetection/web/data --env-file config/database.env jobpostweb db.py --truncate --sqlite
```

## Repo Structure
```
JobpostDetection
├─ .DS_Store
├─ README.md
├─ model
│    ├─ .DS_Store
│    ├─ Dockerfile
│    ├─ config
│    │    ├─ logging.conf
│    │    └─ s3.env
│    ├─ data
│    │    ├─ .DS_Store
│    │    ├─ jobposting.csv
│    │    └─ jobposting_cleaned.csv
│    ├─ model
│    │    ├─ .DS_Store
│    │    ├─ OH_file.pickle
│    │    ├─ SD_file.pickle
│    │    ├─ model_file.pickle
│    │    └─ vec_file.pickle
│    ├─ nltk_data
│    │    ├─ .DS_Store
│    │    ├─ corpora
│    │    └─ taggers
│    ├─ notes.txt
│    ├─ requirements copy.txt
│    ├─ requirements.txt
│    ├─ src
│    │    ├─ .DS_Store
│    │    ├─ DataCleaning.py
│    │    ├─ FeatureEngineering.py
│    │    ├─ FeatureEngineeringPred.py
│    │    ├─ ModelDump.py
│    │    ├─ ModelPredict.py
│    │    ├─ ModelTraining.py
│    │    ├─ __pycache__
│    │    ├─ config.py
│    │    ├─ model_config.yml
│    │    └─ model_training.log
│    └─ upload_data.sh
└─ web
       ├─ .DS_Store
       ├─ .mysqlconfig
       ├─ Dockerfile
       ├─ config
       │    ├─ .DS_Store
       │    ├─ database.env
       │    └─ logging.conf
       ├─ data
       │    ├─ .DS_Store
       │    └─ data.db
       ├─ db.py
       ├─ mysql_database.log
       ├─ notes.txt
       ├─ requirements.txt
       └─ run_mysql_client.sh
```