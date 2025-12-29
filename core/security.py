"""
Security utilities for password hashing and verification.
"""

import bcrypt
from core.config import settings

# Bcrypt maximum password length in bytes
BCRYPT_MAX_PASSWORD_LENGTH = 72


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The bcrypt hash to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Bcrypt has a 72-byte limit. Passwords exceeding this will be rejected.
    
    Args:
        password: The plain text password to hash (max 72 bytes)
        
    Returns:
        The bcrypt hash of the password (as string)
        
    Raises:
        ValueError: If password is empty, None, or exceeds 72 bytes
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Convert to bytes to check length
    password_bytes = password.encode('utf-8')
    
    # Bcrypt has a 72-byte limit - reject if too long
    if len(password_bytes) > BCRYPT_MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password is too long. Maximum {BCRYPT_MAX_PASSWORD_LENGTH} bytes allowed "
            f"(approximately {BCRYPT_MAX_PASSWORD_LENGTH} ASCII characters)."
        )
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string (bcrypt returns bytes)
    return hashed.decode('utf-8')

