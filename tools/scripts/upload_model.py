import os

import boto3
from botocore.exceptions import ClientError


def upload_model(bucket_name, model_path="data/models/rf.pkl", s3_key="models/rf.pkl"):
    
    if not os.path.exists(model_path):
        print(f"Model file not found at: {model_path}")
        return

    s3 = boto3.client("s3")

    try:
        print(f"Uploading {model_path} to s3://{bucket_name}/{s3_key} ...")
        s3.upload_file(model_path, bucket_name, s3_key)
        print("✅ Upload successful.")
    except ClientError as e:
        print("❌ Upload failed:", e)


if __name__ == "__main__":
    
    upload_model("wgucapstonestack-modelbucketb33d855b-ypkd3meauwwq")
