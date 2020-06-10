# run the model build pipeline
export MY_BUCKET=nw-joe-s3/data/
sh download_data.sh
python3 src/ModelDump.py 