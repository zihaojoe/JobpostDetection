# source .mysqlconfig
import os
import logging
import sqlalchemy as sql
import argparse
import logging
import logging.config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData, Float, Text

Base = declarative_base()  
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('mysql_database')

class Reported_case(Base):
	"""Create a data model for the database to be set up for capturing songs """
	__tablename__ = 'reported_case'
	id = Column(Integer, primary_key=True)
	telecommuting = Column(Integer, unique=False, nullable=True)
	has_company_logo  = Column(Integer, unique=False, nullable=True)
	has_questions = Column(Integer, unique=False, nullable=True)
	employment_type = Column(String(100), unique=False, nullable=True)
	required_experience = Column(String(100), unique=False, nullable=True)
	required_education = Column(String(100), unique=False, nullable=True)
	industry = Column(String(100), unique=False, nullable=True)
	function = Column(String(100), unique=False, nullable=True)
	fraudulent = Column(Integer, unique=False, nullable=True)
	country = Column(String(100), unique=False, nullable=True)
	salary_low = Column(Float, unique=False, nullable=True)
	salary_high = Column(Float, unique=False, nullable=True)
	text = Column(Text(2048), unique=False, nullable=False)
  	  
	def __repr__(self):
		return '<Job posting object>'

if __name__ == "__main__":
	# parser the command line params
	parser = argparse.ArgumentParser(description="Create defined tables in database.")
	parser.add_argument("--truncate", "-t", default=False, action="store_true",
	                    help="If given, delete current records from reported_case table before creating reported_case table."
	                         "so that table can be recreated without unique id issues.")
	parser.add_argument("--sampledata", "-s", default=False, action="store_true",
	                    help="If given, add a sample record after creating the reported_case table.")
	parser.add_argument("--sqlite", "-q", default=False, action="store_true",
	                    help="If given, connect to local sqlite rather than mysql on RDS.")
	args = parser.parse_args()

	conn_type = "mysql+pymysql"
	user = os.environ.get("MYSQL_USER")
	password = os.environ.get("MYSQL_PASSWORD")
	host = os.environ.get("MYSQL_HOST")
	port = os.environ.get("MYSQL_PORT")
	database = os.environ.get("DATABASE_NAME")
	sqlitehost = os.environ.get("SQLITE")

	if args.sqlite:
		engine_string = sqlitehost
	else:
		engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

	# set up mysql connection
	engine = sql.create_engine(engine_string)

	# create the reported_case table
	Base.metadata.create_all(engine)

	# create a db session
	Session = sessionmaker(bind=engine)  
	session = Session()

	# If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the reported_case table)
	if args.truncate:
	    try:
	        logger.info("Attempting to truncate reported_case table.")
	        session.execute('''DELETE FROM reported_case''')
	        session.commit()
	        logger.info("reported_case truncated.")
	    except Exception as e:
	        logger.error("Error occurred while attempting to truncate reported_case table.")
	        logger.error(e)
	    finally:
	        session.close()

	# If "sampledata" is given as an argument (i.e. python models.py --sampledata), then empty the reported_case table)
	if args.sampledata:
		# add a sample record
		sample = Reported_case(telecommuting=0, has_company_logo=1, has_questions=0, employment_type="Full-time", 
			required_experience="Bachelor", industry="Other", function="Other", fraudulent=0, country="Other", 
			salary_low=500, salary_high=1000, text="This is a good company!")
		session.add(sample)
		session.commit()







