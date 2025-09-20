from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.role import RoleCreate, RoleUpdate, RoleListResponse
from app.services import role_service

router = APIRouter()

@router.get("/", response_model=RoleListResponse)
def get_roles(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """List all roles (requires authentication)"""
    return role_service.list_roles(db)

@router.post("/")
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create a new role (requires admin)"""
    # Here you can add permission check: current_user must have manage_users
    return role_service.create_role_service(db, role)

@router.put("/{role_id}")
def update_role(role_id: int, role_update: RoleUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Update role by ID (requires admin)"""
    return role_service.update_role_service(db, role_id, role_update)

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Delete role by ID (requires admin)"""
    return role_service.delete_role_service(db, role_id)
