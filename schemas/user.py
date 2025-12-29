"""
User-related Pydantic schemas for validation.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)  # Bcrypt 72-byte limit
    role_id: int = Field(..., ge=1)
    department_id: Optional[int] = None
    clearance_level: int = Field(default=1, ge=1, le=3)
    
    @validator("password")
    def validate_password(cls, v):
        """Basic password strength validation"""
        if not v:
            raise ValueError("Password cannot be empty")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Check byte length (bcrypt has 72-byte limit)
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError("Password is too long. Maximum 72 bytes allowed (approximately 72 characters for ASCII).")
        # TODO: Add more password complexity requirements
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (excludes sensitive data)"""
    id: int
    email: str
    role_id: int
    department_id: Optional[int]
    clearance_level: int
    is_locked: bool
    is_email_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

