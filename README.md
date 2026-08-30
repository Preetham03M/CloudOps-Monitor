# CloudOps Monitor

AWS infrastructure monitoring dashboard built with Python, Flask, and Boto3.

## Overview

A web-based dashboard that monitors EC2 instances, CPU utilization, network traffic, and S3 bucket connectivity.

The application runs on AWS EC2, pulls metrics from CloudWatch, and displays everything on a clean, auto-refreshing dashboard.

## Dashboard Preview

![CloudOps Monitor Dashboard](screenshots/dashboard.png)

## Features

- View all EC2 instances and their status
- Monitor CPU utilization with color-coded alerts
- Track network in/out traffic
- Check S3 bucket connectivity
- Auto-refresh every 60 seconds
- Deployed with Gunicorn and systemd

## Tech Stack

- Python 3.9+
- Flask 2.3.3
- Boto3 1.34.131
- Gunicorn 21.2.0
- AWS EC2, CloudWatch, S3, IAM
- HTML5, CSS3
- Git, GitHub

## Architecture

Browser -> EC2:5000 -> Gunicorn -> Flask App -> Boto3 -> AWS Services

## Deployment

The application is deployed on an AWS EC2 instance running Amazon Linux 2023.

- Gunicorn serves the Flask app
- systemd manages the service (auto-start on reboot)
- IAM role provides AWS credentials (no hardcoded keys)

## Installation

```bash
git clone https://github.com/Preetham03M/CloudOps-Monitor.git
cd CloudOps-Monitor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with your AWS region and bucket
python app.py
 ```
## Project Structure

CloudOps-Monitor/
├── app.py
├── services/
│   ├── ec2_service.py
│   ├── cloudwatch_service.py
│   └── s3_service.py
├── templates/
│   └── dashboard.html
├── requirements.txt
├── README.md
└── .gitignore

## Live Demo

The dashboard is live at: http://18.61.154.34:5000

