# app/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserCreateResponse, UserResponse, UserUpdate, UserListResponse
from app.services.user_service import register_user, list_users, edit_user, remove_user
from app.db.session import get_db
from app.api.deps import get_current_user

router = APIRouter()  # ✅ must be called 'router'

# POST /users/ → create user
@router.post("/", response_model=UserCreateResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)



# GET /users/ → list users
@router.get("/", response_model=UserListResponse)
def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_users(db)

# PUT /users/{user_id} → edit user
@router.put("/{user_id}", response_model=dict)
def update_user_endpoint(user_id: int, user_update: UserUpdate,
                         db: Session = Depends(get_db),
                         current_user=Depends(get_current_user)):
    return edit_user(db, user_id, user_update)

# DELETE /users/{user_id} → delete user
@router.delete("/{user_id}", response_model=dict)
def delete_user_endpoint(user_id: int,
                         db: Session = Depends(get_db),
                         current_user=Depends(get_current_user)):
    return remove_user(db, user_id)
