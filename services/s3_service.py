import boto3


def check_bucket_access():
    try:
        s3 = boto3.client("s3", region_name="ap-south-2")
        s3.list_buckets()
        return True
    except Exception as error:
        print(f"S3 error: {error}")
        return False