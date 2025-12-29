"""
Role model for RBAC (Role-Based Access Control).
Implements role hierarchy for access control decisions.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Role(Base):
    """
    Role model with hierarchy levels.
    
    Hierarchy levels (higher = more privileges):
    - 1: Student
    - 2: Advisor/Reviewer
    - 3: Department Head
    - 4: Admin
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), unique=True, nullable=False, index=True)
    hierarchy_level = Column(Integer, nullable=False, index=True)
    
    # Relationships
    users = relationship("User", back_populates="role")

