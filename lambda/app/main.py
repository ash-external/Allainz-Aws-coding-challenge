import logging
import os
from mangum import Mangum
from fastapi import FastAPI, HTTPException, Request, Query
from app.crud import VpcManager
from app.models import VpcResponse, CreateVpcRequest, UpdateVpcTagsRequest

# Configure global logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("FastAPI")

# Initialize FastAPI app
app = FastAPI(title="AWS VPC CRUD API", version="1.0.0")

handler = Mangum(app)

DB_REGION = os.environ["DB_REGION"]

# CRUD Endpoints

@app.post("/create-vpc", response_model=VpcResponse)
async def create_vpc_endpoint(payload: CreateVpcRequest):
    """Create a new VPC with subnets and optional tags."""
    logger.info("API Call: Create VPC with CIDR %s and %s subnets", payload.vpc_cidr , payload.subnet_count)
    vpc_manager = VpcManager(region_name=payload.region)
    return await vpc_manager.create_vpc(payload.vpc_cidr, payload.subnet_count, payload.public_subnet_count, payload.vpc_tags, payload.subnet_tags)

@app.get("/get-vpc/{vpc_id}", response_model=VpcResponse)
async def get_vpc_endpoint(vpc_id: str):
    """Retrieve a VPC by ID."""
    logger.info("API Call: Get VPC %s", vpc_id)
    vpc_manager = VpcManager(region_name=DB_REGION)
    data = await vpc_manager.get_vpc(vpc_id)
    if not data:
        logger.warning("VPC %s not found", vpc_id)
        raise HTTPException(status_code=404, detail="VPC not found")
    return data

@app.get("/list-vpcs")
async def list_vpcs_endpoint():
    """List all VPCs."""
    logger.info("API Call: List VPCs")
    vpc_manager = VpcManager(region_name=DB_REGION)
    return await vpc_manager.list_vpcs()

@app.put("/update-vpc/{vpc_id}")
async def update_vpc_endpoint(vpc_id: str, payload: UpdateVpcTagsRequest):
    """Update tags for a VPC."""
    logger.info("API Call: Update VPC %s with tags %s", vpc_id, payload.vpc_tags)
    vpc_manager = VpcManager(region_name=payload.region)
    try:
        return await vpc_manager.update_vpc(vpc_id, payload.vpc_tags)
    except Exception as e:
        logger.error("Failed to update VPC %s: %s", vpc_id, e)
        raise HTTPException(status_code=500, detail="Internal server error while updating VPC.")

@app.delete("/delete-vpc/{vpc_id}")
async def delete_vpc_endpoint(vpc_id: str,
    region: str = Query(..., description="AWS region, e.g., ap-south-1")):
    """Delete a VPC and its subnets."""
    logger.info("API Call: Delete VPC %s", vpc_id)
    vpc_manager = VpcManager(region_name=region)
    result = await vpc_manager.delete_vpc(vpc_id)
    if not result:
        logger.warning("VPC %s not found or could not be deleted", vpc_id)
        raise HTTPException(status_code=404, detail="VPC not found or could not be deleted")
    return result