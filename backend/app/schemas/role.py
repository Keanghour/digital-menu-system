from pydantic import BaseModel
from typing import List, Optional

class RoleBase(BaseModel):
    name: str
    permissions: List[str] = []

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permissions: Optional[List[str]] = None

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True

class RoleListResponse(BaseModel):
    total: int
    roles: List[RoleResponse]
