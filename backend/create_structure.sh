#!/bin/bash

BASE_DIR=~/Desktop/digital-menu-system/backend

mkdir -p "$BASE_DIR"

# Create directories
dirs=(
  "app/api/v1/endpoints"
  "app/core"
  "app/crud"
  "app/db/models"
  "app/schemas"
  "app/services"
  "tests"
)

for dir in "${dirs[@]}"; do
  mkdir -p "$BASE_DIR/$dir"
done

# Create __init__.py files
init_files=(
  "app/api/__init__.py"
  "app/api/v1/__init__.py"
  "app/api/v1/endpoints/__init__.py"
  "app/core/__init__.py"
  "app/crud/__init__.py"
  "app/db/__init__.py"
  "app/db/models/__init__.py"
  "app/schemas/__init__.py"
  "app/services/__init__.py"
  "tests/__init__.py"
)

for file in "${init_files[@]}"; do
  touch "$BASE_DIR/$file"
done

# Create files with comments inside
declare -A files_and_comments=(
  ["app/api/deps.py"]="# Dependency overrides and common deps"
  ["app/api/v1/endpoints/auth.py"]="# /login, /logout"
  ["app/api/v1/endpoints/users.py"]="# /users routes"
  ["app/api/v1/endpoints/products.py"]="# /products routes"
  ["app/api/v1/endpoints/categories.py"]="# /categories routes"
  ["app/api/v1/endpoints/roles.py"]="# /roles routes & user-role assignment"
  ["app/api/v1/api_router.py"]="# Aggregates all routes in v1"

  ["app/core/config.py"]="# Configurations, env variables"
  ["app/core/security.py"]="# JWT, password hashing"
  ["app/core/middleware.py"]="# Custom middleware (auth, logging)"
  ["app/core/roles.py"]="# Role definitions & permissions"

  ["app/crud/user.py"]="# CRUD ops for user model"
  ["app/crud/product.py"]="# CRUD ops for product model"
  ["app/crud/category.py"]="# CRUD ops for categories"
  ["app/crud/role.py"]="# CRUD ops for roles"

  ["app/db/base.py"]="# Base class for models"
  ["app/db/session.py"]="# DB session management"
  ["app/db/models/user.py"]=""
  ["app/db/models/product.py"]=""
  ["app/db/models/category.py"]=""
  ["app/db/models/role.py"]=""

  ["app/schemas/user.py"]=""
  ["app/schemas/product.py"]=""
  ["app/schemas/category.py"]=""
  ["app/schemas/role.py"]=""

  ["app/services/auth_service.py"]="# Login, logout, token handling"
  ["app/services/user_service.py"]="# Business logic for users"
  ["app/services/product_service.py"]="# Business logic for products"
  ["app/services/role_service.py"]="# Business logic for roles"

  ["app/main.py"]="# FastAPI app entrypoint"
  ["app/logger.py"]="# Centralized logging setup"

  ["tests/test_auth.py"]=""
  ["tests/test_users.py"]=""
  ["tests/test_products.py"]=""
  ["tests/test_roles.py"]=""
  ["requirements.txt"]=""
  ["README.md"]=""
  [".env"]=""
)

for file in "${!files_and_comments[@]}"; do
  echo "${files_and_comments[$file]}" > "$BASE_DIR/$file"
done

echo "Folder structure with placeholder files created successfully at $BASE_DIR"

