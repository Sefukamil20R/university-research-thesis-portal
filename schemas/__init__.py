"""
Pydantic schemas for request/response validation.
"""

from .user import UserCreate, UserResponse, UserLogin
from .role import RoleResponse
from .department import DepartmentResponse
from .thesis import ThesisCreate, ThesisResponse, ThesisUpdate
from .token import Token, TokenData

__all__ = [
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "RoleResponse",
    "DepartmentResponse",
    "ThesisCreate",
    "ThesisResponse",
    "ThesisUpdate",
    "Token",
    "TokenData",
]

