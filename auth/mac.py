"""
Mandatory Access Control (MAC) dependencies.
Enforces clearance levels for data access.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from .dependencies import get_current_active_user


def require_clearance(required_clearance_level: int):
    """
    Dependency factory for requiring minimum clearance level (MAC).
    
    Clearance levels:
    - 1 = Public
    - 2 = Internal
    - 3 = Confidential
    
    Users can only access data at or below their clearance level.
    
    Args:
        required_clearance_level: Minimum clearance level required (1-3)
        
    Returns:
        Dependency function that checks user clearance level
    """
    def clearance_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        if current_user.clearance_level < required_clearance_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required clearance level: {required_clearance_level}. "
                       f"Your clearance level: {current_user.clearance_level}"
            )
        
        return current_user
    
    return clearance_checker

