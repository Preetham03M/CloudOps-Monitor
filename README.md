# CloudOps Monitor

AWS infrastructure monitoring dashboard built with Python, Flask, Boto3, Amazon EC2, Amazon CloudWatch, and Amazon S3.

## Project Overview

CloudOps Monitor is a web-based monitoring application that provides visibility into AWS EC2 infrastructure and S3 storage connectivity through a centralized dashboard.

The application retrieves EC2 instance information and CloudWatch metrics, processes the data with Python and Boto3, and displays the results through a Flask web interface.

The dashboard also verifies connectivity to a configured Amazon S3 bucket using the S3 `HeadBucket` operation.

## Dashboard Preview

![CloudOps Monitor Dashboard](screenshots/dashboard.png)

The dashboard provides a centralized view of EC2 instances, CPU utilization, network traffic, instance health, current instance status, AWS region, and S3 bucket connectivity.

## Features

- Monitor EC2 instance status
- Display running instance count
- Monitor CPU utilization
- Monitor Network In and Network Out
- Display instance health
- CPU-based warning and critical alerts
- Monitor S3 bucket connectivity
- Verify access to the configured S3 bucket
- Automatic dashboard refresh every 60 seconds
- Last updated timestamp
- CloudWatch error handling
- Persistent deployment using Gunicorn and systemd
- Automatic application restart after EC2 reboot

## Architecture

User Browser
|
v
EC2 Public IP :5000
|
v
Gunicorn
|
v
Flask Application
|
+-----------------------+
| |
v v
Boto3 Dashboard
|
+-----------------------+
| |
v v
EC2 CloudWatch
|
v
CPU / Network Metrics

Boto3
|
v
S3
|
v
Configured Bucket
Connectivity Check

## Technologies

- Python 3.9+
- Flask 2.3.3
- Boto3 1.34.131
- Gunicorn 21.2.0
- Amazon EC2
- Amazon CloudWatch
- Amazon S3
- AWS IAM
- systemd
- HTML5
- CSS3
- Git
- GitHub

## Monitoring

The dashboard currently displays:

- EC2 Instance ID
- Instance Type
- Instance Status
- CPU Utilization
- Network In
- Network Out
- Instance Health
- AWS Region
- S3 Bucket Connectivity

CPU usage is classified as:

| CPU Usage     | Status   |
| ------------- | -------- |
| Below 50%     | Healthy  |
| 50% - 79%     | Warning  |
| 80% or higher | Critical |

S3 connectivity is verified by checking access to the configured S3 bucket using the S3 HeadBucket operation.

The dashboard refreshes automatically every 60 seconds.

## AWS Authentication

The deployed application uses an IAM role attached to the EC2 instance for AWS authentication.

Boto3 is used to access EC2, CloudWatch, and the configured S3 bucket.

AWS access keys and secret keys are not stored in the application source code.

The S3 bucket access follows a least-privilege approach by checking a specific configured bucket rather than listing all S3 buckets.

## Deployment

The application is hosted on an AWS EC2 instance.

Gunicorn is used as the production application server and systemd is used to manage the application.

The systemd service is configured to:

- Start automatically when the EC2 instance starts
- Restart the application if the process stops
- Run the application using the Python virtual environment

The deployment was tested by rebooting the EC2 instance and verifying that the application started automatically.

## Installation

### Prerequisites

- Python 3.9 or higher
- AWS account with appropriate permissions
- AWS CLI configured with credentials

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Preetham03M/CloudOps-Monitor.git
   cd CloudOps-Monitor
   ```
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt

   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

# Edit .env with your AWS credentials and region

5. Run the application:

   ```bash
   python app.py

   ```

6. Access the dashboard:
   Open your browser and navigate to http://localhost:5000

## Project Structure

CloudOps-Monitor/
├── app.py # Main Flask application
├── services/
│ ├── ec2_service.py # EC2 instance operations
│ ├── cloudwatch_service.py # CloudWatch metrics
│ └── s3_service.py # S3 connectivity check
├── templates/
│ └── dashboard.html # Dashboard HTML template
├── screenshots/
│ └── dashboard.png # Dashboard screenshot
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .gitignore # Git ignore file

## Error Handling

The application handles AWS and CloudWatch errors gracefully:

- If EC2 instances cannot be fetched, the dashboard displays an empty state
- If CloudWatch metrics are unavailable, N/A is displayed
- If S3 bucket access fails, the dashboard shows Unavailable
- All errors are logged for troubleshooting

## Security

- IAM roles are used for AWS authentication (no hardcoded credentials)
- Flask debug mode is disabled in production
- Ec2 security group restrict access to specific IPs
- .env files are excluded from version control
- S3 bucket access follows least-privilege principles

## future Improvements

- HTTPS using Nginx
- CloudWatch alarms integration
- Email or SNS notifications for alerts
- Historical monitoring charts
- Multiple EC2 instance support
- Docker containerization
- Terraform infrastructure as code
- CI/CD pipeline with GitHub Actions

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
   For major changes, please open an issue first to discuss.
