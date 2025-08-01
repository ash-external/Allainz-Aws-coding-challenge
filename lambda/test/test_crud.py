import pytest
import boto3
from app.crud import VpcManager

@pytest.mark.asyncio
async def test_calculate_subnets(aws_mock):
    vpc = VpcManager(region_name="us-east-1")
    subnets = vpc._calculate_subnets("10.0.0.0/16", 4)
    assert len(subnets) == 4
    assert all(s.startswith("10.0.") for s in subnets)

@pytest.mark.asyncio
async def test_create_and_get_vpc(aws_mock):
    vpc = VpcManager(region_name="us-east-1")

    result = await vpc.create_vpc(
        vpc_cidr="10.1.0.0/16",
        subnet_count=2,
        vpc_tags=[{"Key": "Name", "Value": "TestVPC"}]
    )

    assert result is not None
    assert "vpc_id" in result
    vpc_id = result["vpc_id"]

    # Test get_vpc
    fetched = await vpc.get_vpc(vpc_id)
    assert fetched["vpc_id"] == vpc_id
    assert fetched["tags"][0]["Key"] == "Name"

@pytest.mark.asyncio
async def test_list_vpcs(aws_mock):
    vpc = VpcManager(region_name="us-east-1")
    await vpc.create_vpc("10.2.0.0/16", 2)
    vpcs = await vpc.list_vpcs()
    assert isinstance(vpcs, list)
    assert len(vpcs) > 0

@pytest.mark.asyncio
async def test_update_vpc_tags(aws_mock):
    vpc = VpcManager(region_name="us-east-1")
    created = await vpc.create_vpc("10.3.0.0/16", 2)
    vpc_id = created["vpc_id"]

    updated = await vpc.update_vpc(vpc_id, tags=[{"Key": "Env", "Value": "Dev"}])
    assert updated["updated_tags"][0]["Key"] == "Env"

@pytest.mark.asyncio
async def test_delete_vpc(aws_mock):
    vpc = VpcManager(region_name="us-east-1")
    created = await vpc.create_vpc("10.4.0.0/16", 2)
    vpc_id = created["vpc_id"]

    deleted = await vpc.delete_vpc(vpc_id)
    assert "deleted" in deleted["message"].lower()

    # Verify it no longer exists
    assert await vpc.get_vpc(vpc_id) is None
