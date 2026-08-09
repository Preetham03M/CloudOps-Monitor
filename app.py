from flask import Flask, render_template

from services.ec2_service import get_ec2_instances
from services.cloudwatch_service import get_cpu_utilization

app = Flask(__name__)


@app.route("/")
def home():
    instances = get_ec2_instances()

    for instance in instances:
        instance["cpu"] = get_cpu_utilization(instance["instance_id"])

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