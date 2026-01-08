"""
Better Auth Integration for FastAPI
Provides JWT-based authentication compatible with Better Auth frontend
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
from fastapi import HTTPException, status, Header, Depends
from sqlmodel import Session
from .database import get_session
from .models import User, TokenData
from . import crud
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Better Auth configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class BetterAuth:
    """
    Better Auth implementation for FastAPI backend
    Provides JWT-based authentication compatible with Better Auth frontend
    """

    def __init__(self, secret: str):
        self.secret = secret
        self.algorithm = ALGORITHM

    def create_token(self, user_id: str, email: str) -> str:
        """
        Create a JWT token for a user (compatible with Better Auth sessions)
        """
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        encoded_jwt = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[TokenData]:
        """
        Verify a JWT token and return user data
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            if user_id is None or email is None:
                return None
            return TokenData(user_id=user_id, email=email)
        except jwt.exceptions.PyJWTError:
            return None


# Global Better Auth instance
better_auth = BetterAuth(BETTER_AUTH_SECRET)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# Dependency to extract and verify token from Authorization header
async def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_session)
) -> User:
    """
    Get current authenticated user by verifying JWT token from Authorization header.
    Compatible with Better Auth frontend token storage.
    """
    # Extract token from "Bearer <token>" format
    try:
        token = authorization.replace("Bearer ", "")
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
        )

    # Verify token
    token_data = better_auth.verify_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    user = crud.get_user_by_id(session, token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# Better Auth endpoint handlers
def register_better_auth_user(email: str, password: str, session: Session) -> dict:
    """
    Register a new user using Better Auth protocol
    Returns user ID and session token
    """
    # Check if user already exists
    existing_user = crud.get_user_by_email(session, email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Create new user with hashed password
    user = crud.create_user(session, email, password)
    token = better_auth.create_token(str(user.id), email)

    return {
        "user": {
            "id": str(user.id),
            "email": email,
            "createdAt": user.created_at.isoformat() if user.created_at else None
        },
        "token": token
    }


def login_better_auth_user(email: str, password: str, session: Session) -> dict:
    """
    Login a user using Better Auth protocol
    Returns user ID and session token
    """
    user = crud.get_user_by_email(session, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    token = better_auth.create_token(str(user.id), email)

    return {
        "user": {
            "id": str(user.id),
            "email": email,
            "createdAt": user.created_at.isoformat() if user.created_at else None
        },
        "token": token
    }
