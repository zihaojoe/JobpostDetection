# MSiA 423 Project: Fake Job Posting Detection App
- **Author: Joe Zhang**    
- **QA: Zach Zhu**
- [Charter](#project-charter)
- [Backlog](#backlog)
- [How to run?](#how-to-run?)

## Project charter
### Vision
It is very difficult for students who have just graduated to judge the authenticity of a job posting because they lack experiences in the industry and are disadvantaged under the information asymmetry. Unlike illegal recruitment, fake recruitment often involves a legitimate company, who wants to gather wealth of information about the applicants and the job market as a whole, which can be monetized in multiple ways. This would leak the applicant's information and also waste much of their time. 
Therefore, in the project, I am going to develop an app which can give prediction of whether a job posting is fake or real for the applicants. This is can be integrated as an extra function or app for job information providers such Glassdoor or LinkedIn.

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
* The accuracy should be greater than 90%  
* The precision should be larger than 0.8
* The recall should be larger than 0.5

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

## How to run?
* For midpoint, please check Module 1 and Module 2
* For final, please check Module 3 and Module 4

- [Module 1: Data Ingestion](#module-1)
- [Module 2: Database Set up](#module-2)
- [Module 3: Build the model](#module-3)
- [Module 4: Run the App](#module-4)

### Module 1: Data Ingestion
The dataset can be downloaded from [Kaggle](https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction). It contains 17880 job posting records and is around 50MB in size. The dataset is downloaded to JobpostDetection/model/jobposting.csv

#### 1. Set up environment: 

Go to the root directory of the project, and run:
```bash
cd model/config/
vi s3.env
```
* Set `MY_BUCKET` to the name of the bucket you want to connect. You can also add path to the bucket name where you want to save your data, such as `bucketname/path/data.csv`. Defaults to `nw-joe-s3/data/`.
* Set `AWS_ACCESS_KEY_ID` to the access ID of your AWS.
* Set `AWS_SECRET_ACCESS_KEY` to the secret access ID of your AWS.
* Set `AWS_DEFAULT_REGION` to the default region of your AWS. Defaults to `us-east-2`. 

#### 2. Run the Docker to upload data to S3 bucket  

##### 2.1 Build Docker image 
Go to the root directory of the project, and run:   
```bash
cd model/
docker build -f Dockerfile -t jobpostmodel .
```
##### 2.2 Run Docker Container
Go to the root directory of the project, and run the following to upload data to S3:   
```bash
cd model/
docker run --mount type=bind,source="$(pwd)"/data,target=/JobpostDetection/model/data --env-file config/s3.env jobpostmodel sh upload_data.sh
```

### Module 2: Database Set up
#### 1. Set up environment:   

Go to the root directory of the project, and run:
```bash
cd web/config/
vi database.env
```
* Set `MYSQL_USER` to the "master username" that you used to create the database server.
* Set `MYSQL_PASSWORD` to the "master password" that you used to create the database server.
* Set `MYSQL_HOST` to be the RDS instance endpoint from the console. Defaults to `nw-msia423-joe.c7e9ftl52ogd.us-east-2.rds.amazonaws.com`.
* Set `MYSQL_HOST` to be `3306`.
* Set `DATABASE_NAME` to the name of the database you want to operate in. Defaults to `msia423_project_db`. 
* Set `SQLITE` to the host name for the sqlite base. Defaults to `///data/msia423_project_db.db`.

**Notice:** 
* If you want to use MySQL, you can ignore the `SQLITE` variable. On the contrast, if you want to use SQLite, just set `SQLITE` and ignore all the others.
* Verify that you are on the northwestern vpn before you continue on with MySQL.
* Follow the docker commands to differentiate between local SQLite and MySQL.

#### 2. Run the Docker to upload data to S3 bucket  

##### 2.1 Build Docker image 
Go to the root directory of the project, and run:   
```bash
docker build -f Dockerfile -t jobpostweb .
```
##### 2.2 Run Docker Container   
Stay in the root directory, and run the following to set up datebase withe the table reported_case:   
```bash
docker run --mount type=bind,source="$(pwd)"/web/data,target=/JobpostDetection/web/data --env-file web/config/database.env jobpostweb python3 db.py
```
**Notice: you can provide up to 3 parameters to the docker run command**     
--truncate: If given, delete current records from reported_case table before creating reported_case table.  
--sampledata:  If given, add a sample record after creating the reported_case table.  
--sqlite: If given, connect to local sqlite rather than mysql on RDS.  

For example, run the following to create database and truncate table in sqlite:    
```bash
docker run --mount type=bind,source="$(pwd)"/web/data,target=/JobpostDetection/web/data --env-file web/config/database.env jobpostweb python3 db.py --truncate --sqlite
```

##### 2.3 Query data
* For instructor, you can use `MYSQL_USER=msia423instructor` and `MYSQL_PASSWORD=zzu8431` to perform queries to the table. 
* For QA, you can use `MYSQL_USER=msia423qa` and `MYSQL_PASSWORD=zzu8431` to perform queries to the table. 
* The insturctor user and qa user account can only select from the current RDS instance. If you are running the app in a development environment, you have to set the MySQL database with your own RDS instance. 

### Module 3: Build the model
#### 1. Follow Module 1 Part 1 to set up AWS environment. (If you are using -e to pass environment variables to docker run instead of env file, just skip this.)

#### 2. Build Docker image (If you have built it in Module 1, just skip this step).
Go to the root directory of the project, and run: 
```bash
cd model/
```
**Notice**: All the following command of this part should be run under `model` 
```bash
docker build -f Dockerfile -t jobpostmodel .
```

#### 3. Run the model generation pipeline
##### 3.1 The demo pipeline (Recommended, skipping data cleaning and grid search)
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY jobpostmodel sh pipeline_demo.sh
```

##### 3.2 The full pipeline
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY jobpostmodel sh pipeline.sh
```

#### 4. Build the model step-by-step (Reference Only)
##### 4.1 Download data
Run the following command to download data from S3 (previously uploaded in module 1). You can skip this if you've already had the data in the data folder. 
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY jobpostmodel sh download_data.sh
```

##### 4.2 Data Cleaning
Run the following command to clean the data. Since it may take hours to parse the text, the cleaned data has been uploaded to S3 and you want to download it using the command in 3.2. Once you have downloaded, you can skip the following command.
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model/ jobpostmodel python3 src/DataCleaning.py 
```

##### 4.3 Model Training
Run the following command to train the models (model parameters are in model_config.yml), and find the best model. Model performance is saved to src/model_training.log.
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model/ jobpostmodel python3 src/ModelTraining.py 
```

##### 4.4 Model Dumping
Run the following command to train the best model (model parameters are in model_config.yml) and save it to file.
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model/ jobpostmodel python3 src/ModelDump.py 
```

#### 5. Model Unit Test
Run the following command to conduct unit test.
```bash
docker run --mount type=bind,source="$(pwd)",target=/JobpostDetection/model/ jobpostmodel pytest unit_test/
```

### Module 4: Run the App
#### 1. Follow Module 2 Part 1 to set up RDS environment.(If you are using -e to pass environment variables to docker run instead of env file, just skip this.)
#### 2. Build Docker image (If you have built it in Module 2, just skip this step).
Go to the root directory of the project, and run:
```bash
docker build -f Dockerfile -t jobpostweb .
```
#### 3. Run the app in the backend 
Stay in the root directory of the project, and run:
```bash
docker run -p 5000:5000 -e MYSQL_USER -e MYSQL_PASSWORD jobpostweb python3 app.py
```
or 
```bash
docker run -p 5000:5000 --mount type=bind,source="$(pwd)"/web/data,target=/JobpostDetection/web/data jobpostweb python3 app.py --sqlite
```
**Notice: you can provide up to 1 parameters to the docker run command**   
--sqlite: If given, connect to local sqlite rather than mysql on RDS. If not given, connect to RDS MySQL. 
* If you are using MySQL, you have to need to be connected to Northwestern VPN.


##### 3. Check the web app
You should now be able to access the app at <http://0.0.0.0:5000/> in your browser.

### Module 5: Kill the container

Once finished with the app, you will need to kill the container. To do so: 
```bash
docker kill test 
```
where `test` is the name given in the `docker run` command.

## Repo Structure
```
├─ Dockerfile
├─ README.md
├─ backup
│    ├─ code
│    │    ├─ DataCleaning-v1.py
│    │    └─ DataCleaning-v2.py
│    ├─ jobposting.csv
│    ├─ jobposting_cleaned.csv
│    └─ model
│           ├─ OH_file.pickle
│           ├─ SD_file.pickle
│           ├─ input_size.txt
│           ├─ model_file.ckpt
│           └─ vec_file.pickle
├─ deliverable
│    └─ FinalPre_MSiA423.pptx
├─ model
│    ├─ Dockerfile
│    ├─ config
│    │    ├─ logging.conf
│    │    └─ s3.env
│    ├─ data
│    │    ├─ jobposting.csv
│    │    └─ jobposting_cleaned.csv
│    ├─ download_data.sh
│    ├─ model_saved
│    │    ├─ OH_file.pickle
│    │    ├─ SD_file.pickle
│    │    ├─ input_size.txt
│    │    ├─ model_file.ckpt
│    │    ├─ result.txt
│    │    └─ vec_file.pickle
│    ├─ nltk_data
│    │    ├─ corpora
│    │    └─ taggers
│    ├─ pipeline.sh
│    ├─ pipeline_demo.sh
│    ├─ requirements.txt
│    ├─ src
│    │    ├─ DataCleaning.py
│    │    ├─ FeatureEngineering.py
│    │    ├─ FeatureEngineeringPred.py
│    │    ├─ ModelDump.py
│    │    ├─ ModelPredict.py
│    │    ├─ ModelTraining.py
│    │    ├─ __init__.py
│    │    ├─ config.py
│    │    ├─ model_config.yml
│    │    └─ model_training.log
│    ├─ unit_test
│    │    ├─ __pycache__
│    │    ├─ input
│    │    ├─ target
│    │    └─ test_model.py
│    └─ upload_data.sh
├─ requirements.txt
└─ web
       ├─ app
       │    ├─ static
       │    └─ templates
       ├─ app.py
       ├─ config
       │    ├─ database.env
       │    ├─ flaskconfig.py
       │    └─ logging.conf
       ├─ data
       │    └─ msia423_project_db.db
       ├─ db.py
       ├─ mysql_database.log
       └─ run_mysql_client.sh
```
