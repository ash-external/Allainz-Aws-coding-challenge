AWS VPC CRUD API
FastAPI | AWS Lambda | API Gateway | Cognito | DynamoDB | Terraform

This project provides an API to manage AWS VPC resources (Create, Read, Update, Delete) using a serverless architecture.
The solution leverages FastAPI deployed on AWS Lambda, exposed via API Gateway v2 (HTTP API), secured by Amazon Cognito JWT Authorizer, and stores metadata in DynamoDB.
Infrastructure is provisioned and managed using Terraform.

## Features

Full CRUD Support: Create, Retrieve, List, Update, Delete VPCs

Automated Resource Management:

Public & Private Subnets
Public & Private Route Tables
Internet Gateway
Failure Handling: Rollback on failures
Infrastructure as Code: Managed using Terraform

## Project Structure
```
├── app/
│   ├── main.py        # FastAPI Lambda entrypoint
│   ├── crud.py        # VPC CRUD logic
│   └── models.py      # Pydantic models
├── lambda.zip         # Packaged Lambda function
├── layer.zip          # Lambda dependencies
├── main.tf            # Terraform configuration
├── variables.tf       # Terraform variables
├── outputs.tf         # Terraform outputs
├── deploy.sh          # Deployment script
└── README.md          # Documentation
```
## Prerequisites
AWS CLI installed and configured
Terraform (≥ 1.5.0)
AWS Access Key & Secret Key with required IAM permissions

## Deployment Steps

Configure AWS Credentials

```
aws configure
```
Deploy Infrastructure and Application

```
This script will:
Initialize Terraform
Plan and Apply infrastructure automatically

./deploy.sh

```

## Authentication (Cognito JWT)

Authentication is handled by Amazon Cognito. You need to retrieve a JWT Token before calling API endpoints.

Before requesting a JWT token, ensure that:
A user is created and confirmed in the Cognito User Pool.

#### Steps to Retrieve JWT Using Postman:

1st way:

Set environment variables for CLIENT_ID (Cognito App client id), CLIENT_SECRET (Cognito app client secret), USERNAME (Cognito user from user pool), USER_PASSWD (Password for cognito user)

```
export CLIENT_ID = <Replace with cognito app client id>
export CLIENT_SECRET = <Replace with cognito app client secret>
export USERNAME = <Replace with user name>
export USER_PASSWD = <Replace with user password>
pip install requests
python retrieve_token.py

```
copy id token from printed output.

2nd Way:

Go to Authorization → Select OAuth 2.0
Set the following values:
Callback URL → Configured in Cognito App Client
Auth URL → https://<your-domain>.auth.<region>.amazoncognito.com/oauth2/authorize
Access Token URL → https://<your-domain>.auth.<region>.amazoncognito.com/oauth2/token
Client ID → Cognito App Client ID
Client Secret → Cognito App Client Secret
Click Get New Access Token and copy the JWT.

Use the token in the request header:

Authorization: Bearer <JWT_TOKEN>

## Testing the API (Curl Examples)

Replace <API_INVOKE_URL> with the actual API Gateway endpoint and <JWT_TOKEN> with the retrieved token.

### Create VPC

```
curl -X POST "<API_INVOKE_URL>/create-vpc" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "vpc_cidr": "10.0.0.0/16",
    "subnet_count": 4,
    "public_subnet_count": 2,
    "vpc_tags": [{"Key": "Name", "Value": "MyVpc"}],
    "subnet_tags": [{"Key": "Type", "Value": "Public"}, {"Key": "Type", "Value": "Private"}],
    "region": "us-east-1"
  }'
```

### Get VPC by ID

```
curl -X GET "<API_INVOKE_URL>/get-vpc/vpc-123abc456def" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### List All VPCs
```
curl -X GET "<API_INVOKE_URL>/list-vpcs" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### Update VPC Tags

```
curl -X PUT "<API_INVOKE_URL>/update-vpc/vpc-123abc456def" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "vpc_tags": [{"Key": "Environment", "Value": "Production"}],
    "region": "us-east-1"
  }'
```

### Delete VPC

```
curl -X DELETE "<API_INVOKE_URL>/delete-vpc/vpc-123abc456def?region=us-east-1" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```