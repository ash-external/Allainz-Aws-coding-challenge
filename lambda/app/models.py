from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Tag(BaseModel):
    """
    Represents an AWS resource tag.

    Attributes:
        Key (str): The tag key (e.g., "Name").
        Value (str): The tag value associated with the key.
    """
    Key: str
    Value: str

class VpcResponse(BaseModel):
    """
    Response model representing metadata of a created or fetched VPC.

    Attributes:
        vpc_id (str): The unique identifier of the VPC (e.g., vpc-123abc456def).
        subnet_ids (List[str]): List of subnet IDs associated with the VPC.
        tags (Optional[List[Tag]]): Optional list of tags applied to the VPC.
        region (str): AWS region where the VPC exists (e.g., ap-south-1).
        igw (str): Internet Gateway ID attached to the VPC.
        route_tables (Dict): Dictionary containing route table IDs (public/private).
    """
    vpc_id: str
    subnet_ids: List[str]
    tags: Optional[List[Tag]] = None
    region: str
    igw: str
    route_tables: Dict

class CreateVpcRequest(BaseModel):
    """
    Request model for creating a new VPC with associated resources.

    Attributes:
        vpc_cidr (str): CIDR block for the VPC (e.g., 10.0.0.0/16).
        subnet_count (int): Total number of subnets to create in the VPC.
        public_subnet_count (Optional[int]): Number of subnets to mark as public.
            Defaults to half of the total subnet count if not provided.
        vpc_tags (Optional[List[Dict[str, str]]]): Tags to apply to the VPC.
        subnet_tags (Optional[List[Dict[str, str]]]): Tags for individual subnets.
            Used to identify whether a subnet is public/private based on tag values.
        region (str): AWS region where the VPC will be created (e.g., ap-south-1).
    """
    vpc_cidr: str = Field(..., description="CIDR block for the VPC, e.g., 10.0.0.0/16")
    subnet_count: int = Field(..., description="Total number of subnets to create")
    public_subnet_count: Optional[int] = Field(None, description="Number of subnets to be public (defaults to half)")
    vpc_tags: Optional[List[Dict[str, str]]] = Field(None, description="Tags for the VPC")
    subnet_tags: Optional[List[Dict[str, str]]] = Field(None, description="Tags for the subnets (used to detect public/private if contains 'Public')")
    region: str = Field(..., description="AWS region, e.g., ap-south-1")


class UpdateVpcTagsRequest(BaseModel):
    """
    Request model for updating tags of an existing VPC.

    Attributes:
        vpc_tags (Optional[List[Dict[str, str]]]): New or updated tags to apply to the VPC.
        region (str): AWS region where the VPC resides (e.g., ap-south-1).
    """
    vpc_tags: Optional[List[Dict[str, str]]] = Field(None, description="Tags to update for the VPC")
    region: str = Field(..., description="AWS region, e.g., ap-south-1")