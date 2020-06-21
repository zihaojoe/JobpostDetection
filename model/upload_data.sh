# upload data to s3
export MY_BUCKET=nw-joe-s3/data/
aws s3 cp ./data/jobposting.csv s3://${MY_BUCKET}
aws s3 cp ./data/jobposting_cleaned.csv s3://${MY_BUCKET}
