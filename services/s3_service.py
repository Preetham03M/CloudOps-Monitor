import boto3


BUCKET_NAME = "cloudops-monitor-data-2026-519057264369-ap-south-2-an"


def check_bucket_access():
    try:
        s3 = boto3.client("s3", region_name="ap-south-2")
        s3.head_bucket(Bucket=BUCKET_NAME)
        return True
    except Exception as error:
        print(f"S3 error: {error}")
        return False