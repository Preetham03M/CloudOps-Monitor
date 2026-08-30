import boto3
import os
import logging
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = os.getenv('S3_BUCKET', 'cloudops-monitor-data')

def check_bucket_access():
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        s3.head_bucket(Bucket=S3_BUCKET_NAME)
        logger.info(f"S3 bucket '{S3_BUCKET_NAME}' is accessible")
        return True
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == '404':
            logger.error(f"S3 bucket '{S3_BUCKET_NAME}' does not exist")
        elif error_code == '403':
            logger.error(f"Access denied to S3 bucket '{S3_BUCKET_NAME}'")
        else:
            logger.error(f"S3 ClientError for bucket '{S3_BUCKET_NAME}': {e}")
        return False
    except BotoCoreError as e:
        logger.error(f"AWS connection error for S3 bucket '{S3_BUCKET_NAME}': {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking S3 bucket '{S3_BUCKET_NAME}': {e}")
        return False