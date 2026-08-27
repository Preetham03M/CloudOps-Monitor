# CloudOps Monitor

AWS infrastructure monitoring dashboard built with Python, Flask, Boto3, Amazon EC2, Amazon CloudWatch, and Amazon S3.

## Project Overview

CloudOps Monitor is a web-based monitoring application that provides visibility into AWS EC2 infrastructure and S3 storage connectivity through a centralized dashboard.

The application retrieves EC2 instance information and CloudWatch metrics, processes the data with Python and Boto3, and displays the results through a Flask web interface.

The dashboard also verifies connectivity to a configured Amazon S3 bucket using the S3 `HeadBucket` operation.

## Dashboard Preview

![CloudOps Monitor Dashboard](screenshots/dashboard.png?v=2)

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

```text
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
     |                       |
     v                       v
   Boto3                 Dashboard
     |
     +-----------------------+
     |                       |
     v                       v
    EC2                 CloudWatch
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
```
## Technologies

- Python
- Flask
- Boto3
- Amazon EC2
- Amazon CloudWatch
- Amazon S3
- AWS IAM
- Gunicorn
- systemd
- HTML
- CSS
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
- AWS REgion
- S3 Bucket Connectivity

CPU usage is classified as:

| CPU Usage | Status |
|---|---|
| Below 50% | Healthy |
| 50% - 79% | Warning |
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

## Error Handling

The application handles AWS and CloudWatch errors so that unavailable monitoring data does not immediately stop the dashboard.

When a metric is unavailable, the dashboard can display `N/A` instead of treating the missing value as zero.

S3 access errors are also handled so that the dashboard can display Unavailable when the configured bucket cannot be accessed.

## Security

- EC2 IAM role is used for AWS authentication
- AWS credentials are not stored in the application
- Private key files are excluded using `.gitignore`
- `.env` files are excluded from Git
- Flask debug mode is disabled for deployment
- EC2 Security Group access is restricted to the configured source IP
- S3 access is limited to the configured bucket

## Project Structure

```text
CloudOps-Monitor/
├── app.py
├── services/
│   ├── ec2_service.py
│   ├── cloudwatch_service.py
│   └── s3_service.py
├── templates/
│   └── dashboard.html
├── screenshots/
│   └── dashboard.png
├── requirements.txt
├── README.md
└── .gitignore
```
## Future Improvements

- HTTPS using Nginx
- CloudWatch alarms
- Email or SNS notifications
- Historical monitoring charts
- Multiple EC2 instance support
- Docker deployment
- Terraform infrastructure

## Project Status

Core monitoring, alerting, error handling, S3 connectivity monitoring, and AWS deployment functionality are complete.

Final JD alignment, documentation review, and portfolio preparation are in progress.
