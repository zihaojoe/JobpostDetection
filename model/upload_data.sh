# update data to the 
aws s3 cp ./data/jobposting.csv s3://${MY_BUCKET}/data/
aws s3 cp ./data/jobposting_cleaned.csv s3://${MY_BUCKET}/data/
