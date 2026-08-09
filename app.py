from flask import Flask, render_template
from services.ec2_service import get_ec2_instances
from services.cloudwatch_service import (
    get_cpu_utilization, get_network_in, get_network_out
)

app = Flask(__name__)


@app.route("/")
def home():
    try:
        instances = get_ec2_instances()
    except Exception as error:
        print(f"EC2 error: {error}")
        instances = []

    for instance in instances:
        instance_id = instance["instance_id"]
        instance["cpu"] = get_cpu_utilization(instance_id)
        instance["network_in"] = get_network_in(instance_id)
        instance["network_out"] = get_network_out(instance_id)
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

    return render_template(
        "dashboard.html",
        instances=instances,
        total_instances=len(instances),
        running_count=running_count,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)