"""
Role-Based Access Control (RBAC) dependencies.
Implements role hierarchy for access control.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.role import Role
from .dependencies import get_current_active_user


def require_role(allowed_roles: list[str]):
    """
    Dependency factory for requiring specific roles.
    
    Args:
        allowed_roles: List of role names that can access the endpoint
        
    Returns:
        Dependency function that checks user role
    """
    def role_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        
        if role is None or role.role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        
        return current_user
    
    return role_checker


def require_minimum_role(minimum_hierarchy_level: int):
    """
    Dependency factory for requiring minimum role hierarchy level.
    Higher hierarchy level = more privileges.
    
    Args:
        minimum_hierarchy_level: Minimum hierarchy level required (1-4)
        
    Returns:
        Dependency function that checks user role hierarchy
    """
    def hierarchy_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        
        if role is None or role.hierarchy_level < minimum_hierarchy_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required minimum hierarchy level: {minimum_hierarchy_level}"
            )
        
        return current_user
    
    return hierarchy_checker

