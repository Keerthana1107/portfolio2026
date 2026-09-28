"""
auth.py
Password hashing, JWT creation/validation, in-memory "database" of users and
active sessions, and the FastAPI dependency used to protect routes.

NOTE: users_db / active_sessions / blacklisted_tokens / user_recommendations
are plain in-memory dicts (as in the original project) -- fine for a demo /
college project, but everything resets when the server restarts and none of
it is shared across multiple worker processes. Swap for a real database
(SQLite/Postgres) before deploying for real users.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from models import UserInDB, TokenData, UserSession, RecommendationHistoryItem

# ---------- Config ----------

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)  # Allow optional token

# ---------- In-memory "database" ----------

users_db: Dict[str, UserInDB] = {}
active_sessions: Dict[str, UserSession] = {}
blacklisted_tokens: set = set()
user_recommendations: Dict[str, List[RecommendationHistoryItem]] = {}


# ---------- Password helpers ----------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ---------- User helpers ----------

def get_user(db: Dict[str, UserInDB], username: str) -> Optional[UserInDB]:
    return db.get(username)


def authenticate_user(db: Dict[str, UserInDB], username: str, password: str):
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ---------- JWT helpers ----------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_token(request: Request) -> Optional[str]:
    """Pull the JWT out of the access_token cookie (falls back to Authorization header)."""
    token = request.cookies.get("access_token")
    if token:
        return token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        return auth_header.split(" ", 1)[1]
    return None


async def get_current_user(request: Request, token: Optional[str] = None) -> Optional[UserInDB]:
    if token is None:
        token = await get_token(request)
    if not token or token in blacklisted_tokens:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None

    user = get_user(users_db, username=token_data.username)
    return user


async def get_current_active_user(request: Request) -> UserInDB:
    """FastAPI dependency: protects a route, 401s if not logged in."""
    user = await get_current_user(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
