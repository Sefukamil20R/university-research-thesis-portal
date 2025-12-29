"""
Token-related Pydantic schemas for JWT authentication.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data"""
    email: str | None = None
    user_id: int | None = None
    role_id: int | None = None
    clearance_level: int | None = None

