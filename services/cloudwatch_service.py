"""
CloudWatch Service - AWS CloudWatch Metrics Integration

This module handles all CloudWatch metric operations for EC2 instances.
It provides functions to retrieve CPU utilization and network metrics.
"""

import boto3
import os
import logging
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError, BotoCoreError

# Logger setup
logger = logging.getLogger(__name__)

# Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
METRIC_LOOKBACK_MINUTES = int(os.getenv('METRIC_LOOKBACK', '5'))


def get_cloudwatch_client():
    """
    Initialize and return CloudWatch client.

    Returns:
        boto3.client: CloudWatch client instance
    """
    try:
        return boto3.client('cloudwatch', region_name=AWS_REGION)
    except Exception as e:
        logger.error(f"Failed to initialize CloudWatch client: {e}")
        raise


def get_metric_statistics(instance_id, metric_name, statistic='Average'):
    """
    Retrieve metric statistics for a specific EC2 instance.

    Args:
        instance_id (str): EC2 instance ID
        metric_name (str): CloudWatch metric name
        statistic (str): Statistic type (Average, Maximum, Minimum, Sum)

    Returns:
        float or None: Metric value or None if not available
    """
    if not instance_id:
        logger.warning("get_metric_statistics called with empty instance_id")
        return None

    try:
        cloudwatch = get_cloudwatch_client()

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=METRIC_LOOKBACK_MINUTES)

        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[
                {'Name': 'InstanceId', 'Value': instance_id}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=[statistic]
        )

        datapoints = response.get('Datapoints', [])

        if not datapoints:
            logger.debug(f"No data points found for {instance_id} - {metric_name}")
            return None

        latest = max(datapoints, key=lambda x: x['Timestamp'])
        value = latest.get(statistic)

        if value is None:
            return None

        return round(value, 2)

    except ClientError as e:
        logger.error(f"AWS ClientError for {instance_id} - {metric_name}: {e}")
        return None
    except BotoCoreError as e:
        logger.error(f"AWS Connection error for {instance_id} - {metric_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for {instance_id} - {metric_name}: {e}")
        return None


def get_cpu_utilization(instance_id):
    """
    Get average CPU utilization for an EC2 instance.

    Args:
        instance_id (str): EC2 instance ID

    Returns:
        float or None: CPU utilization percentage
    """
    return get_metric_statistics(instance_id, 'CPUUtilization')


def get_network_in(instance_id):
    """
    Get average network input traffic for an EC2 instance.

    Args:
        instance_id (str): EC2 instance ID

    Returns:
        float or None: Network In bytes
    """
    return get_metric_statistics(instance_id, 'NetworkIn')


def get_network_out(instance_id):
    """
    Get average network output traffic for an EC2 instance.

    Args:
        instance_id (str): EC2 instance ID

    Returns:
        float or None: Network Out bytes
    """
    return get_metric_statistics(instance_id, 'NetworkOut')


def get_multiple_metrics(instance_id):
    """
    Retrieve all available metrics for a single instance in one call.

    Args:
        instance_id (str): EC2 instance ID

    Returns:
        dict: Dictionary containing CPU, NetworkIn, NetworkOut metrics
    """
    return {
        'cpu': get_cpu_utilization(instance_id),
        'network_in': get_network_in(instance_id),
        'network_out': get_network_out(instance_id)
    }