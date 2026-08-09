import boto3
from datetime import datetime, timedelta, timezone


def get_cpu_utilization(instance_id):
    cloudwatch = boto3.client(
        "cloudwatch",
        region_name="ap-south-2",
    )

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id,
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )

    datapoints = response.get("Datapoints", [])

    if not datapoints:
        return None

    latest_datapoint = max(
        datapoints,
        key=lambda datapoint: datapoint["Timestamp"],
    )

    return round(latest_datapoint["Average"], 2)