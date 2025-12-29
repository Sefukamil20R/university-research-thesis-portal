"""
Department-related Pydantic schemas.
"""

from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    """Schema for department response"""
    id: int
    name: str
    code: str
    
    class Config:
        from_attributes = True

