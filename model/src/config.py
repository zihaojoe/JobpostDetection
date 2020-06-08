import os

# Getting the parent directory of this file. That will function as the project home.
cwd = os.getcwd()
for i in range(3):
	if cwd.split('/')[-1] == 'JobpostDetection':
		PROJECT_HOME = cwd
		break;
	else:
		cwd = os.path.dirname(cwd)
print(PROJECT_HOME)

# App config
APP_NAME = "Job Posting"

# Logging
LOGGING_CONFIG = os.path.join(PROJECT_HOME, 'model/config/logging.conf')

# Path
MODEL_PATH = os.path.join(PROJECT_HOME, 'model/model_saved/')
DATA_PATH = os.path.join(PROJECT_HOME, 'model/data/jobposting.csv')
DATA_CLEANED_PATH = os.path.join(PROJECT_HOME, 'model/data/jobposting_cleaned.csv')