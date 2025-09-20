# app/services/role_service.py

from fastapi import HTTPException, status
from app.api.deps import serialize_role
from app.crud import role as role_crud
from app.schemas.role import RoleResponse, RoleListResponse, RoleCreate, RoleUpdate

def list_roles(db, skip: int = 0, limit: int = 100) -> RoleListResponse:
    total, roles = role_crud.get_roles(db, skip=skip, limit=limit)
    return RoleListResponse(
        total=total,
        roles=[RoleResponse.model_validate(serialize_role(r)) for r in roles]
    )

def get_role_by_id(db, role_id: int) -> RoleResponse:
    role = role_crud.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return RoleResponse.model_validate(serialize_role(role))

def create_role_service(db, role_data: RoleCreate):
    role = role_crud.create_role(db, role_data)
    return {"message": "Role created successfully", "role": RoleResponse.model_validate(serialize_role(role))}

def update_role_service(db, role_id: int, role_update: RoleUpdate):
    role = role_crud.update_role(db, role_id, role_update)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return {"message": "Role updated successfully", "role": RoleResponse.model_validate(serialize_role(role))}


def delete_role_service(db, role_id: int):
    role = role_crud.delete_role(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return {"message": "Role deleted successfully"}
