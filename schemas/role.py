"""
Role-related Pydantic schemas.
"""

from pydantic import BaseModel


class RoleResponse(BaseModel):
    """Schema for role response"""
    id: int
    role_name: str
    hierarchy_level: int
    
    class Config:
        from_attributes = True

