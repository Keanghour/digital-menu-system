from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine, SessionLocal, init_default_roles_and_permissions

# Import models so SQLAlchemy knows about them
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.permission import Permission

from app.api.v1.api_router import api_router

# Auto-create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_default_roles_and_permissions(db)
    finally:
        db.close()

# Include main API router
app.include_router(api_router)  # prefix handled inside router
