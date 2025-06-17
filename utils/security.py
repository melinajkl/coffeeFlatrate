"""Utility functions for hashing and verifying passwords, 
as well as creating access tokens using JWT."""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# SECRET + settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifies a plaintext password against its hashed version.

    Args:
        plain (str): The plaintext password.
        hashed (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT access token with optional expiration.

    Args:
        data (dict): The payload data to encode into the token.
        expires_delta (timedelta, optional): The duration until expiration. Defaults to 20 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
