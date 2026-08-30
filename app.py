"""
CloudOps Monitor - Main Flask Application

This is the brain of the dashboard. It:
- Fetches EC2 instances from AWS
- Gets CPU and network metrics from CloudWatch
- Checks S3 bucket connectivity
- Renders the web dashboard

I know the error handling is messy. I'll clean it up later.
TODO: Move this to a proper config file someday.
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template

# Local imports - I should probably organize these better
from services.ec2_service import get_ec2_instances
from services.cloudwatch_service import (
    get_cpu_utilization,
    get_network_in,
    get_network_out
)
from services.s3_service import check_bucket_access

# Set up logging - this is better than using print() everywhere
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)

# Configuration - using environment variables so we don't hardcode things
# TODO: Move this to a config.py file if it gets bigger
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')


def format_bytes(value):
    """
    Convert bytes to human readable format.

    This took me way too long to write.
    I had a bug where it was dividing by 1000 instead of 1024.
    Don't ask how long it took me to find that.
    """
    if value is None:
        return "N/A"

    try:
        size = float(value)
    except (TypeError, ValueError):
        logger.warning(f"Invalid byte value received: {value}")
        return "Invalid"

    units = ["bytes", "KB", "MB", "GB"]

    for unit in units:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

    # If we get here, it's terabytes
    return f"{size:.2f} TB"


@app.route("/")
@app.route("/dashboard")
def home():
    """
    Main dashboard page.

    This function is getting too long. I should split it up.
    But it works, so I'm leaving it for now.
    """
    logger.info("Dashboard requested")

    # Fetch EC2 instances - this fails sometimes when AWS is slow
    try:
        instances = get_ec2_instances()
        logger.info(f"Successfully fetched {len(instances)} instances")
    except Exception as error:
        logger.error(f"Failed to fetch EC2 instances: {error}")
        instances = []

    # Check S3 connectivity - not critical but nice to have
    try:
        s3_status = check_bucket_access()
        logger.info(f"S3 bucket status: {s3_status}")
    except Exception as error:
        logger.warning(f"S3 check failed: {error}")
        s3_status = False

    # Add CloudWatch metrics to each instance
    # This loop is ugly but it works
    for instance in instances:
        instance_id = instance.get("instance_id")

        if not instance_id:
            logger.warning("Found instance without ID, skipping")
            continue

        # Get CPU and network metrics from CloudWatch
        try:
            instance["cpu"] = get_cpu_utilization(instance_id)
            instance["network_in"] = format_bytes(
                get_network_in(instance_id)
            )
            instance["network_out"] = format_bytes(
                get_network_out(instance_id)
            )
        except Exception as error:
            logger.error(f"Failed to get metrics for {instance_id}: {error}")
            instance["cpu"] = None
            instance["network_in"] = "N/A"
            instance["network_out"] = "N/A"

        # Determine alert level based on CPU
        cpu = instance.get("cpu")

        if cpu is None:
            instance["alert"] = None
            instance["health"] = "Unknown"
        elif cpu >= 80:
            instance["alert"] = "Critical"
            instance["health"] = "Critical"
        elif cpu >= 50:
            instance["alert"] = "Warning"
            instance["health"] = "Warning"
        else:
            instance["alert"] = None
            instance["health"] = "Healthy"

    # Count running instances for the stats cards
    running_count = sum(
        1 for instance in instances
        if instance.get("state") == "running"
    )

    # Current timestamp - using local time because UTC is confusing
    updated_at = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

    return render_template(
        "dashboard.html",
        instances=instances,
        total_instances=len(instances),
        running_count=running_count,
        updated_at=updated_at,
        s3_status=s3_status,
        aws_region=AWS_REGION,
        debug_mode=DEBUG_MODE
    )


@app.errorhandler(404)
def page_not_found(error):
    """Page not found error handler."""
    logger.warning(f"404 error: {error}")
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Internal server error handler."""
    logger.error(f"500 error: {error}")
    return "Something went wrong. Check the logs.", 500


if __name__ == "__main__":
    # Run the app
    # Debug mode is controlled by environment variable
    # In production, debug should ALWAYS be False
    logger.info(f"Starting CloudOps Monitor in {'debug' if DEBUG_MODE else 'production'} mode")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=DEBUG_MODE
    )
