#!/bin/bash

cd lambda

coverage run -m pytest

coverage report -m

cd ../terraform

echo "Initializing Terraform..."
terraform init

echo "Validating Terraform configuration..."
terraform validate

echo "Planning Terraform deployment..."
terraform plan -out=tfplan

echo "Applying Terraform (Auto Approve)..."
terraform apply -auto-approve tfplan

echo "Deployment Complete!"
echo "API Gateway URL:"
terraform output api_invoke_url
