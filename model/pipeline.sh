# run the model build pipeline
aws s3 cp  s3://${MY_BUCKET}jobposting.csv ./data/
python3 src/DataCleaning.py
python3 src/ModelTraining.py 
python3 src/ModelDump.py 
