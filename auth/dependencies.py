"""
Authentication dependencies for FastAPI routes.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.user import User
from core.config import settings
from .jwt import verify_token
from schemas.token import TokenData


def get_current_user(
    token_data: TokenData = Depends(verify_token),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from the database.
    
    Args:
        token_data: Decoded token data from verify_token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user not found or account is locked
    """
    user = db.query(User).filter(User.email == token_data.email).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Check if account is locked
    if user.is_locked:
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is locked. Please try again later."
            )
        else:
            # Lock expired, unlock the account
            user.is_locked = False
            user.failed_login_attempts = 0
            user.locked_until = None
            db.commit()
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active (non-locked) user.
    
    Args:
        current_user: User from get_current_user
        
    Returns:
        Active User object
        
    Raises:
        HTTPException: If account is locked
    """
    if current_user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked"
        )
    
    # TODO: Add email verification check when implemented
    # if not current_user.is_email_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Email not verified"
    #     )
    
    return current_user

