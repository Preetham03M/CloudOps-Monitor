# CloudOps Monitor

AWS infrastructure monitoring dashboard built with Python, Flask, Boto3, and Amazon CloudWatch.

## Project Overview

CloudOps Monitor is a web-based monitoring application that provides visibility into AWS EC2 infrastructure through a centralized dashboard.

The application retrieves EC2 instance information and CloudWatch metrics, processes the data with Python, and displays the results through a Flask web interface.

## Features

- Monitor EC2 instance status
- Display running instance count
- Monitor CPU utilization
- Monitor Network In and Network Out
- Display instance health
- CPU-based warning and critical alerts
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
     +------------------+
     |                  |
     v                  v
   Boto3            Dashboard
     |
     v
IAM Role
     |
     +------------------+
     |                  |
     v                  v
   EC2             CloudWatch
                         |
                         v
                CPU / Network Metrics.
