# app/services/auth_service.py

from datetime import datetime, timedelta
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.crud import user as user_crud
import secrets

from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import TokenPair, UserResponse

otp_store: dict[str, dict] = {}

OTP_EXPIRE_MINUTES = 10  # OTP validity


# ----------------------------
# JWT Access Token
# ----------------------------
def create_access_token(data: dict, expires_delta: int = None):
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ----------------------------
# Refresh Token (random string)
# ----------------------------
def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


# ----------------------------
# Authenticate user
# ----------------------------
def authenticate_user(db: Session, email: str, password: str):
    user = user_crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# ----------------------------
# Generate Tokens
# ----------------------------
# def generate_token_pair(db: Session, user: User) -> TokenPair:
#     access_token = create_access_token({"sub": str(user.id)})
#     refresh_token = create_refresh_token()

#     # 🔑 store a hashed version of the refresh token in DB
#     user.refresh_token = get_password_hash(refresh_token)
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return TokenPair(
#         access_token=access_token,
#         refresh_token=refresh_token,  # raw token returned to client
#         message="Login successful"
#     )

def generate_token_pair(db: Session, user: User) -> TokenPair:
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_active": user.is_active,
        "role": user.role.name if user.role else None
    }
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token()

    # Store hashed refresh token
    user.refresh_token = get_password_hash(refresh_token)
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        message="Login successful"
    )


# ----------------------------
# Verify Refresh Token
# ----------------------------
def verify_refresh_token(db: Session, user: User, refresh_token: str):
    if not user.refresh_token:
        return False
    return verify_password(refresh_token, user.refresh_token)


# ----------------------------
# Revoke Refresh Token
# ----------------------------
def revoke_refresh_token(db: Session, user: User):
    user.refresh_token = None
    db.add(user)
    db.commit()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = user_crud.get_user_by_id(db, int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user



def send_otp(db: Session, email: str) -> dict:
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = f"{secrets.randbelow(1000000):06}"  # 6-digit OTP
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)

    # Store OTP (in-memory for demo)
    otp_store[email] = {"otp": otp, "expires_at": expires_at}

    # In real system, send email here
    print(f"Send OTP to {email}: {otp}")

    return {"message": "OTP sent successfully", "otp": otp, "expires_at": expires_at}



def reset_password(db: Session, email: str, otp: str, new_password: str) -> dict:
    record = otp_store.get(email)
    if not record:
        raise HTTPException(status_code=400, detail="OTP not requested")

    if record["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Remove used OTP
    otp_store.pop(email, None)

    return {"message": "Password reset successfully"}


def get_user_by_refresh_token(db: Session, user_id: int, refresh_token: str):
    """Verify refresh token for a given user ID"""
    user = user_crud.get_user_by_id(db, user_id)
    if user and user.refresh_token and verify_password(refresh_token, user.refresh_token):
        return user
    return None
