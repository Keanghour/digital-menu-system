from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# SQLite database URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Init default roles and permissions
def init_default_roles_and_permissions(db: Session):
    from app.db.models.role import Role
    from app.db.models.permission import Permission

    default_permissions = [
        "manage_users",
        "manage_products",
        "view_reports",
        "view_products",
    ]

    permissions_map = {}
    for perm_name in default_permissions:
        perm = db.query(Permission).filter(Permission.name == perm_name).first()
        if not perm:
            perm = Permission(name=perm_name)
            db.add(perm)
            db.flush()
        permissions_map[perm_name] = perm

    roles_permissions = {
        "admin": ["manage_users", "manage_products", "view_reports"],
        "editor": ["manage_products"],
        "viewer": ["view_products"],
    }

    for role_name, perm_names in roles_permissions.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.flush()
        role.permissions = [permissions_map[p] for p in perm_names]

    db.commit()
