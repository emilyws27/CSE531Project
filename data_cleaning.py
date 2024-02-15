import boto3
import gzip
from io import BytesIO
import os 


#add them to your computer's env variables lsit for security
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

# Create an S3 client
s3 = boto3.client("s3", aws_access_key_id, aws_secret_access_key)

# Specify the bucket names and file keys
bucket_name = 'cse531bucket'
file_keys = ['DIAGNOSES_ICD.csv.gz', 'ICUSTAYS.csv.gz']

data = []
for file_key in file_keys:
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    gzipped_file_data = response['Body'].read()
    
    # Decompress the data
    with gzip.GzipFile(fileobj=BytesIO(gzipped_file_data)) as file:
        decompressed_data = file.read()
    
    data.append(decompressed_data)

# Print the contents of the files
for file_data in data:
    print(file_data.decode('utf-8'))  # Assuming the file content is in UTF-8