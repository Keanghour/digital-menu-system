from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict

from app.api.deps import serialize_user
from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.crud import user as user_crud
from app.db.models.user import User



# ------------------------------
# Register User
# ------------------------------
def register_user(db: Session, user_data: UserCreate) -> Dict[str, object]:
    # Password validation
    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    # Check duplicate email
    existing_user = user_crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    new_user = user_crud.create_user(db, user_data)

    # Return validated response
    return {
        "message": "User registered successfully",
        "user": UserResponse.model_validate(serialize_user(new_user)),
    }


# ------------------------------
# List Users
# ------------------------------
def list_users(db: Session, skip: int = 0, limit: int = 10) -> UserListResponse:
    total, users = user_crud.get_users(db, skip=skip, limit=limit)
    return UserListResponse(
        total=total,
        users=[UserResponse.model_validate(serialize_user(u)) for u in users],
    )


# ------------------------------
# Edit User
# ------------------------------
def edit_user(db: Session, user_id: int, user_update: UserUpdate) -> Dict[str, object]:
    user = user_crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {
        "message": "User updated successfully",
        "user": UserResponse.model_validate(serialize_user(user)),
    }


# ------------------------------
# Delete User
# ------------------------------
def remove_user(db: Session, user_id: int) -> Dict[str, str]:
    user = user_crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {"message": "User deleted successfully"}
