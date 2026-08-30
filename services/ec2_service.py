import boto3
import os
import logging
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

def get_ec2_instances():
    try:
        ec2 = boto3.client("ec2", region_name=AWS_REGION)
        response = ec2.describe_instances()
    except (ClientError, BotoCoreError) as e:
        logger.error(f"AWS error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

    instances = []
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            inst_id = instance.get("InstanceId", "unknown")
            inst_type = instance.get("InstanceType", "unknown")
            state = instance.get("State", {}).get("Name", "unknown")
            tags = instance.get("Tags", [])
            name = inst_id
            for tag in tags:
                if tag.get("Key") == "Name":
                    name = tag.get("Value", inst_id)
                    break
            instances.append({
                "instance_id": inst_id,
                "instance_type": inst_type,
                "state": state,
                "name": name,
            })

    instances.sort(key=lambda x: x["instance_id"])
    logger.info(f"Found {len(instances)} instances")
    return instances