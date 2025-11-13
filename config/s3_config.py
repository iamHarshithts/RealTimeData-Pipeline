import boto3
from botocore.client import Config

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url="http://localhost:9000",
        aws_access_key_id="minio",
        aws_secret_access_key="minio123",
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
