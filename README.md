# CloudOps Monitor

AWS Infrastructure Monitoring & Automation using Python, Flask, and Boto3.

## Project Overview

CloudOps Monitor is a cloud operations monitoring application designed to provide visibility into AWS infrastructure health, resource status, and monitoring metrics through a centralized web dashboard.

## Technologies

- AWS EC2
- AWS IAM
- AWS CloudWatch
- Python
- Flask
- Boto3
- Git
- GitHub

## Current Architecture

Windows Development Environment
|
v
GitHub
|
v
AWS EC2
|
+-- Flask
+-- Boto3
+-- IAM Role
|
v
AWS Services

## Security

The application uses an IAM role attached to the EC2 instance instead of storing long-lived AWS access keys in the application.

## Project Status

Day 2 - Development environment and AWS authentication completed.
