import boto3
from datetime import datetime, timedelta, timezone


REGION = "ap-south-2"


def get_cloudwatch_client():
    return boto3.client("cloudwatch", region_name=REGION)


def get_metric_statistics(instance_id, metric_name, statistic="Average"):
    try:
        cloudwatch = get_cloudwatch_client()

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=10)

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName=metric_name,
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=[statistic],
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            return None

        latest = max(datapoints, key=lambda x: x["Timestamp"])
        return round(latest[statistic], 2)

    except Exception as error:
        print(f"CloudWatch error ({metric_name}): {error}")
        return None


def get_cpu_utilization(instance_id):
    return get_metric_statistics(instance_id, "CPUUtilization")


def get_network_in(instance_id):
    return get_metric_statistics(instance_id, "NetworkIn")


def get_network_out(instance_id):
    return get_metric_statistics(instance_id, "NetworkOut")