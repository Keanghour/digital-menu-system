from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.crud import user as user_crud
import secrets

from app.schemas.user import UserResponse

def create_access_token(data: dict, expires_delta: int = None):
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token() -> str:
    # Refresh tokens are long random strings (JWT is optional here)
    return secrets.token_urlsafe(64)

def authenticate_user(db: Session, email: str, password: str):
    user = user_crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token_pair(db: Session, user):
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    refresh_token = create_refresh_token()
    user.refresh_token = get_password_hash(refresh_token)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "Login successful",
        "user": UserResponse.model_validate(user)   # ✅
    }

def verify_refresh_token(db: Session, user, refresh_token: str):
    if not user.refresh_token:
        return False
    return verify_password(refresh_token, user.refresh_token)

def revoke_refresh_token(db: Session, user):
    user.refresh_token = None
    db.add(user)
    db.commit()

