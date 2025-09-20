from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, serialize_user 
from app.db.models.user import User
from app.schemas.user import ForgotPasswordRequest, LoginRequest, LoginResponse, ResetPasswordRequest, TokenPair, UserResponse
from app.services import auth_service
from app.services.auth_service import (
    authenticate_user, generate_token_pair, get_user_by_refresh_token, reset_password, send_otp, verify_refresh_token, revoke_refresh_token
)
from app.db.session import get_db
from app.crud import user as user_crud

router = APIRouter()

@router.get("/me", response_model=UserResponse, tags=["Auth"])
def get_me(current_user=Depends(get_current_user)):
    """
    Get current logged-in user information.
    """
    return serialize_user(current_user)


# @router.post("/login", response_model=TokenPair)
# def login(request: LoginRequest, db: Session = Depends(get_db)):
#     user = authenticate_user(db, request.email, request.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
#     return generate_token_pair(db, user)

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    tokens = generate_token_pair(db, user)

    return LoginResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type="bearer",
        message="Login successful",
        user=UserResponse.model_validate({
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "role": user.role.name if user.role else None
        })
    )


# @router.post("/refresh", response_model=TokenPair)
# def refresh_token(refresh_token: str, email: str, db: Session = Depends(get_db)):
#     user = user_crud.get_user_by_email(db, email)
#     if not user or not verify_refresh_token(db, user, refresh_token):
#         raise HTTPException(status_code=401, detail="Invalid refresh token")

#     return generate_token_pair(db, user)

    
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

def read_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get details of the currently authenticated user.
    """
    return UserResponse.model_validate({
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "role": current_user.role.name if current_user.role else None
    })


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return send_otp(db, request.email)

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return auth_service.reset_password(db, request.email, request.otp, request.new_password)


@router.post("/refresh-token", response_model=TokenPair)
def refresh_token_endpoint(user_id: int, refresh_token: str, db: Session = Depends(get_db)):
    user = get_user_by_refresh_token(db, user_id, refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    tokens = generate_token_pair(db, user)
    return tokens

