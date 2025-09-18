from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user 
from app.schemas.user import LoginRequest, TokenPair
from app.services.auth_service import (
    authenticate_user, generate_token_pair, verify_refresh_token, revoke_refresh_token
)
from app.db.session import get_db
from app.crud import user as user_crud

router = APIRouter()

@router.post("/login", response_model=TokenPair)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return generate_token_pair(db, user)

@router.post("/refresh", response_model=TokenPair)
def refresh_token(refresh_token: str, email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user or not verify_refresh_token(db, user, refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return generate_token_pair(db, user)

# @router.post("/logout")
# def logout(email: str, db: Session = Depends(get_db)):
#     user = user_crud.get_user_by_email(db, email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     revoke_refresh_token(db, user)
#     return {"message": "Logout successful. Refresh token revoked."}

@router.post("/logout")
def logout(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    revoke_refresh_token(db, current_user)
    return {"message": "Logout successful. Refresh token revoked."}
