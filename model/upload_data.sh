# upload data to s3
aws s3 cp ./data/jobposting.csv s3://${MY_BUCKET}
aws s3 cp ./data/jobposting_cleaned.csv s3://${MY_BUCKET}
