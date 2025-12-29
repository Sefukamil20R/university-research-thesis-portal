"""
Authentication router - Registration, login, and account management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models.user import User
from models.role import Role
from core.config import settings
from core.security import verify_password, get_password_hash
from auth.jwt import create_access_token
from auth.dependencies import get_current_active_user
from schemas.user import UserCreate, UserLogin, UserResponse
from schemas.token import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])
templates = Jinja2Templates(directory="templates")


def lock_account(user: User, db: Session):
    """
    Lock user account after too many failed login attempts.
    
    Args:
        user: User object to lock
        db: Database session
    """
    user.is_locked = True
    user.locked_until = datetime.utcnow() + timedelta(
        minutes=settings.LOCKOUT_DURATION_MINUTES
    )
    user.failed_login_attempts = 0
    db.commit()


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)):
    """Registration page"""
    roles = db.query(Role).all()
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "roles": roles}
    )


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint.
    
    Security:
    - Password hashing with bcrypt
    - Email uniqueness check
    - Input validation via Pydantic
    """
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Verify role exists
        role = db.query(Role).filter(Role.id == user_data.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role"
            )
        
        # Create new user
        new_user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role_id=user_data.role_id,
            department_id=user_data.department_id,
            clearance_level=user_data.clearance_level,
            is_email_verified=False  # TODO: Implement email verification
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # TODO: Send email verification token
        # generate_verification_token(new_user)
        # send_verification_email(new_user.email, token)
        
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Registration error: {error_details}")  # Print to console for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint with account lockout protection.
    
    Security:
    - Password verification
    - Account lockout after multiple failed attempts
    - JWT token generation
    """
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    # Security: Don't reveal if email exists or not
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
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
    
    # Verify password
    if not verify_password(user_credentials.password, user.password_hash):
        user.failed_login_attempts += 1
        
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            lock_account(user, db)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account locked due to too many failed login attempts"
            )
        
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Successful login - reset failed attempts
    user.failed_login_attempts = 0
    db.commit()
    
    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role_id": user.role_id,
            "clearance_level": user.clearance_level
        }
    )
    
    # Return token (client should store in localStorage and/or cookie)
    # TODO: Set HTTP-only cookie for better security
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.post("/logout")
async def logout():
    """
    Logout endpoint (client-side token removal).
    TODO: Implement token blacklisting if needed.
    """
    return {"message": "Logged out successfully"}

