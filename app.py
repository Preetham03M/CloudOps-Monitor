from flask import Flask, render_template
from datetime import datetime
import os
import logging
from services.ec2_service import get_ec2_instances
from services.cloudwatch_service import get_cpu_utilization, get_network_in, get_network_out
from services.s3_service import check_bucket_access

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_bytes(value):
    if value is None:
        return "N/A"
    try:
        size = float(value)
    except:
        return "Invalid"
    units = ["bytes", "KB", "MB", "GB"]
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size = size / 1024
    return f"{size:.2f} TB"

@app.route("/")
def home():
    try:
        instances = get_ec2_instances()
        logger.info(f"Fetched {len(instances)} instances")
    except Exception as e:
        logger.error(f"EC2 error: {e}")
        instances = []

    try:
        s3_status = check_bucket_access()
    except:
        s3_status = False

    for inst in instances:
        inst_id = inst["instance_id"]
        inst["cpu"] = get_cpu_utilization(inst_id)
        inst["network_in"] = format_bytes(get_network_in(inst_id))
        inst["network_out"] = format_bytes(get_network_out(inst_id))
        cpu = inst.get("cpu")
        if cpu is None:
            inst["alert"] = None
        elif cpu >= 80:
            inst["alert"] = "Critical"
        elif cpu >= 50:
            inst["alert"] = "Warning"
        else:
            inst["alert"] = None

    running_count = sum(1 for i in instances if i.get("state") == "running")
    updated_at = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

    return render_template(
        "dashboard.html",
        instances=instances,
        total_instances=len(instances),
        running_count=running_count,
        updated_at=updated_at,
        s3_status=s3_status,
        aws_region=os.getenv("AWS_REGION", "us-east-1")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)