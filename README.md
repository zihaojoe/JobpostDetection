# Fake Job Posting Detection App
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

* Epic 3: Application deployment
	- Story 1: Encapsulate the model application into docker
	- Story 2: Use could service like RDS and S3 to deploy the application and data
	
### Initiative 2: Increase user engagement and app interactivity
* Epic 1: Build user-friendly web app page that reads users' inputs
	- Story 1: Design structure and framework of the web app
	- Story 2: Define interface to connect to other application (Model Docker)
	- Story 3: Finalize the web page on the host
	- Story 4: Design and finalize web page style and layout
* Epic 2: Realize collection of new data
	- Story 1: Build interface that allows users to update new finds of fake or real job postings to the database
* Epic 3: Build a user report system that collects users' feedback
	- Story 1: Build interface that allows users to report whether a prediction is right
	- Story 2: Build interface that allows users to give feedback to the utility of the app
* Epic 4: Application deployment
	- Story 1: Encapsulate the model application into docker
	- Story 2: Use could service like RDS and S3 to deploy the application and data
	- Story 3: Finalize connection with model docker and database
* Epic 5: Test application and release
	- Story 1: Test the multiple components of the project
	- Story 2: Fix bugs
	- Story 3: Release application

### Backlog

Initiative1.epic1.story1 (1 of story points) - PLANNED  
Initiative1.epic1.story2 (4 of story points) - PLANNED  
Initiative1.epic1.story3 (2 of story points) - PLANNED  
Initiative1.epic1.story4 (2 of story points) - PLANNED  

Initiative1.epic2.story1 (1 of story points) - PLANNED  
Initiative1.epic2.story2 (2 of story points) - PLANNED  
Initiative1.epic2.story3 (4 of story points) - PLANNED  

Initiative1.epic3.story1 (2 of story points)  
Initiative1.epic3.story2 (8 of story points)  


Initiative2.epic1.story1 (2 of story points)  
Initiative2.epic1.story2 (1 of story points)  
Initiative2.epic1.story3 (4 of story points)  
Initiative2.epic1.story4 (4 of story points)  

Initiative2.epic4.story1 (2 of story points)  
Initiative2.epic4.story2 (4 of story points)  
Initiative2.epic4.story3 (2 of story points)  

Initiative2.epic5.story1 (2 of story points)  
Initiative2.epic5.story2 (2 of story points)  
Initiative2.epic5.story3 (0 of story points)  

### Icebox
Initiative2.epic2.story1  
Initiative2.epic3.story1  
Initiative2.epic3.story2  



