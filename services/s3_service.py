"""
S3 Service - Amazon S3 Bucket Connectivity Check

This module verifies connectivity to a configured S3 bucket
using the HeadBucket operation.
"""

import boto3
import os
import logging
from botocore.exceptions import ClientError, BotoCoreError

# Logger setup
logger = logging.getLogger(__name__)

# Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = os.getenv('S3_BUCKET', 'cloudops-monitor-data')


def get_s3_client():
    """
    Initialize and return S3 client.

    Returns:
        boto3.client: S3 client instance
    """
    try:
        return boto3.client('s3', region_name=AWS_REGION)
    except Exception as e:
        logger.error(f"Failed to initialize S3 client: {e}")
        raise


def check_bucket_access(bucket_name=None):
    """
    Check if the configured S3 bucket is accessible.

    Args:
        bucket_name (str, optional): Override default bucket name

    Returns:
        bool: True if bucket is accessible, False otherwise
    """
    bucket = bucket_name or S3_BUCKET_NAME

    if not bucket:
        logger.warning("No S3 bucket name configured")
        return False

    try:
        s3 = get_s3_client()
        s3.head_bucket(Bucket=bucket)
        logger.info(f"S3 bucket '{bucket}' is accessible")
        return True

    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')

        if error_code == '404':
            logger.error(f"S3 bucket '{bucket}' does not exist")
        elif error_code == '403':
            logger.error(f"Access denied to S3 bucket '{bucket}'")
        else:
            logger.error(f"S3 ClientError for bucket '{bucket}': {e}")

        return False

    except BotoCoreError as e:
        logger.error(f"AWS connection error for S3 bucket '{bucket}': {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error checking S3 bucket '{bucket}': {e}")
        return False


def get_bucket_region(bucket_name=None):
    """
    Get the region of the configured S3 bucket.

    Args:
        bucket_name (str, optional): Override default bucket name

    Returns:
        str or None: Region name or None if not found
    """
    bucket = bucket_name or S3_BUCKET_NAME

    if not bucket:
        logger.warning("No S3 bucket name configured")
        return None

    try:
        s3 = get_s3_client()
        response = s3.get_bucket_location(Bucket=bucket)
        region = response.get('LocationConstraint')

        if region is None:
            region = 'us-east-1'

        logger.info(f"S3 bucket '{bucket}' is in region: {region}")
        return region

    except Exception as e:
        logger.error(f"Failed to get region for bucket '{bucket}': {e}")
        return None


def list_bucket_objects(bucket_name=None, prefix='', max_keys=10):
    """
    List objects in the configured S3 bucket.

    Args:
        bucket_name (str, optional): Override default bucket name
        prefix (str): Filter objects by prefix
        max_keys (int): Maximum number of objects to return

    Returns:
        list: List of object keys or empty list on failure
    """
    bucket = bucket_name or S3_BUCKET_NAME

    if not bucket:
        logger.warning("No S3 bucket name configured")
        return []

    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys
        )

        objects = response.get('Contents', [])
        keys = [obj.get('Key') for obj in objects if obj.get('Key')]

        logger.info(f"Found {len(keys)} objects in bucket '{bucket}'")
        return keys

    except Exception as e:
        logger.error(f"Failed to list objects in bucket '{bucket}': {e}")
        return []