import os

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = os.path.abspath(os.path.dirname(os.getcwd()))

# App config
APP_NAME = "Job Posting"

# Logging
LOGGING_CONFIG = os.path.join(PROJECT_HOME, 'config/logging.conf')

# Model
MODEL_PATH = os.path.join(PROJECT_HOME, 'model/')