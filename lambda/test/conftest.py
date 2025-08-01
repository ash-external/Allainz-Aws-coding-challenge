import os
import pytest
import boto3
from moto import mock_aws
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def set_env():
    """Set environment variables before tests."""
    os.environ["TABLE_NAME"] = "TestVpcTable"
    os.environ["DB_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def aws_mock():
    """Mock AWS services EC2 & DynamoDB."""
    with mock_aws():
        # Create DynamoDB table for VpcManager
        dynamodb = boto3.client("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName=os.environ["TABLE_NAME"],
            KeySchema=[{"AttributeName": "VpcId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "VpcId", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        yield  # AWS mocks are active
        # Moto automatically cleans up after exit

@pytest.fixture(scope="function")
def test_client(aws_mock):
    """FastAPI TestClient with AWS mocks applied."""
    return TestClient(app)
