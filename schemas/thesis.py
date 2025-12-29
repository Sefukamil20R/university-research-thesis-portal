"""
Thesis-related Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.thesis import ThesisStatus


class ThesisCreate(BaseModel):
    """Schema for creating a thesis"""
    title: str = Field(..., min_length=1, max_length=500)
    abstract: Optional[str] = None
    classification_level: int = Field(default=1, ge=1, le=3)
    department_id: int


class ThesisUpdate(BaseModel):
    """Schema for updating a thesis (only admin can change classification)"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    abstract: Optional[str] = None
    classification_level: Optional[int] = Field(None, ge=1, le=3)
    status: Optional[ThesisStatus] = None


class ThesisResponse(BaseModel):
    """Schema for thesis response"""
    id: int
    title: str
    abstract: Optional[str]
    classification_level: int
    status: ThesisStatus
    student_id: int
    department_id: int
    file_path: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

