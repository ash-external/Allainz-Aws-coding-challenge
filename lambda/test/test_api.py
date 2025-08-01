import pytest

@pytest.mark.asyncio
async def test_create_vpc_api(test_client):
    payload = {
        "vpc_cidr": "10.10.0.0/16",
        "subnet_count": 2,
        "region": "us-east-1",
        "vpc_tags": [{"Key": "Name", "Value": "API-VPC"}]
    }
    response = test_client.post("/create-vpc", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["vpc_id"].startswith("vpc-")

@pytest.mark.asyncio
async def test_list_vpcs_api(test_client):
    response = test_client.get("/list-vpcs")
    assert response.status_code == 200
    vpcs = response.json()
    assert isinstance(vpcs, list)

@pytest.mark.asyncio
async def test_get_vpc_api(test_client):
    # First create a VPC
    payload = {
        "vpc_cidr": "10.20.0.0/16",
        "subnet_count": 2,
        "region": "us-east-1"
    }
    create_resp = test_client.post("/create-vpc", json=payload)
    vpc_id = create_resp.json()["vpc_id"]

    # Fetch via GET API
    resp = test_client.get(f"/get-vpc/{vpc_id}")
    assert resp.status_code == 200
    assert resp.json()["vpc_id"] == vpc_id

@pytest.mark.asyncio
async def test_update_vpc_api(test_client):
    # Create VPC
    payload = {
        "vpc_cidr": "10.30.0.0/16",
        "subnet_count": 2,
        "region": "us-east-1"
    }
    vpc_id = test_client.post("/create-vpc", json=payload).json()["vpc_id"]

    # Update tags
    update_payload = {"vpc_tags": [{"Key": "Env", "Value": "QA"}], "region": "us-east-1"}
    resp = test_client.put(f"/update-vpc/{vpc_id}", json=update_payload)
    assert resp.status_code == 200
    assert resp.json()["updated_tags"][0]["Value"] == "QA"

@pytest.mark.asyncio
async def test_delete_vpc_api(test_client):
    # Create VPC
    payload = {
        "vpc_cidr": "10.40.0.0/16",
        "subnet_count": 2,
        "region": "us-east-1"
    }
    vpc_id = test_client.post("/create-vpc", json=payload).json()["vpc_id"]

    # Delete VPC
    resp = test_client.delete(f"/delete-vpc/{vpc_id}?region=us-east-1")
    assert resp.status_code == 200
    assert "deleted" in resp.json()["message"].lower()
