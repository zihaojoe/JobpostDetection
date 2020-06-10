import os

DEBUG = False
LOGGING_CONFIG = "config/logging.conf"
PORT = 5000
APP_NAME = "JobPosting"


SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
#host = os.environ.get("MYSQL_HOST")
#port = os.environ.get("MYSQL_PORT")
#database = os.environ.get("DATABASE_NAME")

host = "nw-msia423-joe.c7e9ftl52ogd.us-east-2.rds.amazonaws.com"
port = 3306
database = "msia423_project_db"

#SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=db_name)
SQLALCHEMY_DATABASE_URI="{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)
#SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423_project_db.db'
