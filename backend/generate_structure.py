import os

structure = [
    "fastapi_project/app/api/v1/endpoints",
    "fastapi_project/app/core",
    "fastapi_project/app/crud",
    "fastapi_project/app/db/models",
    "fastapi_project/app/schemas",
    "fastapi_project/app/services",
    "fastapi_project/tests",
]

files = [
    "fastapi_project/app/api/__init__.py",
    "fastapi_project/app/api/deps.py",
    "fastapi_project/app/api/v1/__init__.py",
    "fastapi_project/app/api/v1/api_router.py",
    "fastapi_project/app/api/v1/endpoints/__init__.py",
    "fastapi_project/app/api/v1/endpoints/auth.py",
    "fastapi_project/app/api/v1/endpoints/users.py",
    "fastapi_project/app/api/v1/endpoints/products.py",
    "fastapi_project/app/api/v1/endpoints/categories.py",
    "fastapi_project/app/api/v1/endpoints/roles.py",

    "fastapi_project/app/core/__init__.py",
    "fastapi_project/app/core/config.py",
    "fastapi_project/app/core/security.py",
    "fastapi_project/app/core/middleware.py",
    "fastapi_project/app/core/roles.py",

    "fastapi_project/app/crud/__init__.py",
    "fastapi_project/app/crud/user.py",
    "fastapi_project/app/crud/product.py",
    "fastapi_project/app/crud/category.py",
    "fastapi_project/app/crud/role.py",

    "fastapi_project/app/db/__init__.py",
    "fastapi_project/app/db/base.py",
    "fastapi_project/app/db/session.py",
    "fastapi_project/app/db/models/__init__.py",
    "fastapi_project/app/db/models/user.py",
    "fastapi_project/app/db/models/product.py",
    "fastapi_project/app/db/models/category.py",
    "fastapi_project/app/db/models/role.py",

    "fastapi_project/app/schemas/__init__.py",
    "fastapi_project/app/schemas/user.py",
    "fastapi_project/app/schemas/product.py",
    "fastapi_project/app/schemas/category.py",
    "fastapi_project/app/schemas/role.py",

    "fastapi_project/app/services/__init__.py",
    "fastapi_project/app/services/auth_service.py",
    "fastapi_project/app/services/user_service.py",
    "fastapi_project/app/services/product_service.py",
    "fastapi_project/app/services/role_service.py",

    "fastapi_project/app/main.py",
    "fastapi_project/app/logger.py",

    "fastapi_project/tests/__init__.py",
    "fastapi_project/tests/test_auth.py",
    "fastapi_project/tests/test_users.py",
    "fastapi_project/tests/test_products.py",
    "fastapi_project/tests/test_roles.py",

    "fastapi_project/requirements.txt",
    "fastapi_project/README.md",
    "fastapi_project/.env",
]

for folder in structure:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w') as f:
        pass  # Create an empty file
