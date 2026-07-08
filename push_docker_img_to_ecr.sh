#!/usr/bin/env bash
set -euo pipefail

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ACCOUNT="${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com"

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT

docker build -t cup-app .
docker tag cup-app:latest ${ACCOUNT}/cup-app:latest
docker push ${ACCOUNT}/cup-app:latest

aws ecr describe-images --repository-name cup-app