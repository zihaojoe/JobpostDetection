# download data to s3
export MY_BUCKET=nw-joe-s3/data/
aws s3 cp  s3://${MY_BUCKET}jobposting.csv ./data/
aws s3 cp  s3://${MY_BUCKET}jobposting_cleaned.csv ./data/
