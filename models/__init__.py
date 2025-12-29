"""
Database models package.
"""

from .user import User
from .role import Role
from .department import Department
from .thesis import Thesis

__all__ = ["User", "Role", "Department", "Thesis"]

