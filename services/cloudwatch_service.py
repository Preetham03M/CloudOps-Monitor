import boto3
import os
import logging
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
METRIC_LOOKBACK_MINUTES = int(os.getenv('METRIC_LOOKBACK', '5'))

def get_metric_statistics(instance_id, metric_name, statistic='Average'):
    if not instance_id:
        logger.warning("get_metric_statistics called with empty instance_id")
        return None

    try:
        cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION)
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=METRIC_LOOKBACK_MINUTES)

        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
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
    return get_metric_statistics(instance_id, 'CPUUtilization')

def get_network_in(instance_id):
    return get_metric_statistics(instance_id, 'NetworkIn')

def get_network_out(instance_id):
    return get_metric_statistics(instance_id, 'NetworkOut')