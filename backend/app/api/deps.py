from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core import config
from app.core.config import settings
from app.db.models.role import Role
from app.db.models.user import User
from app.db.session import get_db
from app.crud import user as user_crud
from app.schemas.product import ProductResponse
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise credentials_exception
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def serialize_user(user) -> UserResponse:
    """
    Convert SQLAlchemy User model to Pydantic UserResponse,
    with role as string (role name)
    """
    return UserResponse.model_validate({
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "role": user.role.name if user.role else None,
    })


def serialize_role(role: Role) -> dict:
    return {
        "id": role.id,
        "name": role.name,
        # If RoleResponse has other fields like permissions, map them as strings or ids
        "permissions": [p.name for p in role.permissions]  # example
    }


def serialize_product(product):
    return ProductResponse.model_validate({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "currency": product.currency,
        "category": product.category.name if product.category else None,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    })