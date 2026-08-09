from flask import Flask

from services.ec2_service import get_ec2_instances

app = Flask(__name__)


@app.route("/")
def home():
    instances = get_ec2_instances()

    return {
        "application": "CloudOps Monitor",
        "instances": instances,
    }


if __name__ == "__main__":
    app.run(debug=True)
