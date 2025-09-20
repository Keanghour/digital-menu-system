# app/main.py

from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine, SessionLocal, init_default_roles_and_permissions
from app.core.logging import log_requests

from app.core.middleware import setup_cors

from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.permission import Permission

from app.api.v1.api_router import api_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")

# Apply CORS
setup_cors(app)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_default_roles_and_permissions(db)
    finally:
        db.close()


# Apply request/response logging
app.middleware("http")(log_requests)


# Include API
app.include_router(api_router)




# ------------------------------
# Swagger UI /docs Authorize setup
# ------------------------------


from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Project",
        version="1.0.0",
        # description="API documentation with JWT auth",
        description="""
A modular and scalable **FastAPI** application following a clean architecture with clear separation of concerns:
""",
        routes=app.routes,
    )
    # Add Bearer auth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
        "LoginAuth": {
            "type": "http",
            "scheme": "basic",  # for email/password testing
        }
    }
    # Apply BearerAuth globally
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
