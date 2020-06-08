import argparse
import traceback
import logging.config
import pickle
import pandas as pd
import sys
import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for
from db import Reported_case

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder='app/static')

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app')

# Import Model
sys.path.append('../model/src/')
import ModelPredict

# Initialize the database
parser = argparse.ArgumentParser(description="Create defined tables in database.")
parser.add_argument("--sqlite", "-q", default=False, action="store_true",
                    help="If given, connect to local sqlite rather than mysql on RDS.")
args = parser.parse_args()

if args.sqlite:
    sqlitehost = os.environ.get("SQLITE")
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlitehost

print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)

@app.route('/')
def index():
    """Homepage of this prediction system.
    
    Returns: rendered html template
    """

    try:
        return render_template('web.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html')

@app.route('/output', methods=['POST'])
def predict():
    """View that process a POST with new lyrics
    :return: redirect to web.html page with result or error page without result
    """
    try:

        feature = { 'telecommuting':[int(request.form['Telecommuting'])],
                    'has_company_logo': [int(request.form['Has_Logo'])],
                    'has_questions':[int(request.form['Has_Questions'])],
                    'employment_type':[request.form['Employment_Type']],
                    'required_experience': [request.form['Required_Experience']],
                    'required_education': [request.form['Required_Education']],
                    'industry': [request.form['Industry']],
                    'function': [request.form['Function']],
                    'country': [request.form['Country']],
                    'salary_low': [float(request.form['Salary_Low'])],
                    'salary_high': [float(request.form['Salary_High'])],
                    'text':[request.form['Text']]
        }

        feature_df = pd.DataFrame(feature)
        print(feature)
        predict_value = ModelPredict.predict_fake_post(feature_df)[0]
            
        if predict_value < 0.5:
            result = "Real"
            predict_value = 1 - predict_value
        elif predict_value >= 0.5 :
            result = "Fake"
        else:
            result = "Invalid Input"

        #print("The predicted value is ", predict_value)
        #print("The result is ", result)

        sample = Reported_case(telecommuting=0, has_company_logo=feature['has_company_logo'][0], required_education=feature['required_education'][0],
            has_questions=feature['has_questions'][0], employment_type=feature['employment_type'][0], required_experience=feature['required_experience'][0], 
            industry=feature['industry'][0], function=feature['function'][0], country=feature['telecommuting'][0], 
            salary_low=feature['salary_low'][0], salary_high=feature['salary_high'][0], text=feature['text'][0], fraudulent=int(predict_value))

        db.session.add(sample)
        db.session.commit()
        
        return render_template('web.html', result=result, result_prob=predict_value)
    except:
        traceback.print_exc()
        logger.warning("Not able to display homepage, error page returned!")
        return render_template('error.html')

@app.route('/home')
def home():
    """For invalid input users, return to homepage if they click on the button
    
    Returns: rendered html template
    """
    try:
       # redirect to choose threshold page
       return redirect(url_for('index'))
    except:
       logger.warning("Something wrong with render web.html")
       return render_template('error.html')


if __name__ == '__main__':
    #app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
    app.run(debug=False, port=app.config["PORT"], host=app.config["HOST"], threaded=False)