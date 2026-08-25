from flask import Flask, render_template
from datetime import datetime
from services.ec2_service import get_ec2_instances
from services.cloudwatch_service import (
    get_cpu_utilization, get_network_in, get_network_out
)

from services.s3_service import check_bucket_access

app = Flask(__name__)

def format_bytes(value):
    if value is None:
        return "N/A"

    units = ["bytes", "KB", "MB", "GB"]
    size = float(value)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} TB"

@app.route("/")
def home():
    try:
        instances = get_ec2_instances()
    except Exception as error:
        print(f"EC2 error: {error}")
        instances = []

    s3_status = check_bucket_access()

    for instance in instances:
        instance_id = instance["instance_id"]
        instance["cpu"] = get_cpu_utilization(instance_id)
        instance["network_in"] = format_bytes(
            get_network_in(instance_id)
        )
        instance["network_out"] = format_bytes(
            get_network_out(instance_id)
        )
        cpu = instance["cpu"]

        if cpu is None:
            instance["alert"] = None
        elif cpu >= 80:
            instance["alert"] = "Critical"
        elif cpu >= 50:
            instance["alert"] = "Warning"
        else:
            instance["alert"] = None

    running_count = sum(
        1 for instance in instances if instance["state"] == "running"
    )
    updated_at = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

    return render_template(
        "dashboard.html",
        instances=instances,
        total_instances=len(instances),
        running_count=running_count,
        updated_at=updated_at,
        s3_status=s3_status,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
