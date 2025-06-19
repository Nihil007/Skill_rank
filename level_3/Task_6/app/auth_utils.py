from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret key to encode JWT (keep this secure in production)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable must be set for security!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context (bcrypt)
PasswordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the password using bcrypt
def HashPassword(password: str) -> str:
    # Takes a plain text password and returns a hashed version using bcrypt
    return PasswordContext.hash(password)


# Verify input password against stored hashed password
def VerifyPassword(plain_password: str, hashed_password: str) -> bool:
    # Compares a plain text password with a hashed password, returns True if they match
    return PasswordContext.verify(plain_password, hashed_password)


# Generate a JWT token for the user
def CreateAccessToken(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Creates a JWT token with user data and optional custom expiry time
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Decode and verify JWT token
def DecodeAccessToken(token: str) -> Optional[dict]:
    # Decodes a JWT token and returns the payload, or None if token is invalid
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
