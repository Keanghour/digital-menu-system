# digital-menu-system
A digital menu system that enables restaurants to showcase their menu items interactively on tablets or smartphones, allowing customers to browse, customize orders, and place them directly. It improves order accuracy, enhances user experience, and streamlines restaurant operations.

---
# Backend
---

# FastAPI Digital Menu System

A **FastAPI-based backend project** for managing users, roles, categories, products, and authentication.
Supports JWT-based authentication, role management, product-category assignment, and multiple product operations.

---

## Table of Contents

* [Features](#features)
* [Folder Structure](#folder-structure)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Running the App](#running-the-app)
* [API Endpoints](#api-endpoints)
* [Testing with Postman](#testing-with-postman)
* [License](#license)

---

## Features

* User management: create, read, update, delete (CRUD)
* Role & permission management
* JWT authentication (access & refresh tokens)
* Password reset via OTP
* Category & product management
* Assign products to categories
* Single and multiple product deletion
* Logging & request tracking
* CORS and middleware support

---

## Folder Structure

```
fastapi_project/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── roles.py
│   │   │   │   ├── categories.py
│   │   │   │   └── products.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── middleware.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── category.py
│   │   └── product.py
│   ├── db/
│   │   ├── base.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── category.py
│   │   │   └── product.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── category.py
│   │   └── product.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── product_service.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Keanghour/digital-menu-system.git
cd fastapi_project
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```
# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Database (SQLite for local dev)
DATABASE_URL=sqlite:///./app.db

# App Settings
APP_NAME=FastAPI Project
APP_ENV=development
APP_DEBUG=True
```

---

## Running the App

```bash
uvicorn app.main:app --reload
```

Visit the **Swagger UI** at:

```
http://127.0.0.1:8000/docs
```

or **OpenAPI JSON** at:

```
http://127.0.0.1:8000/openapi.json
```

---

## API Endpoints

### Auth

| Endpoint                       | Method | Description                              |
| ------------------------------ | ------ | ---------------------------------------- |
| `/api/v1/auth/login`           | POST   | Login and get JWT access & refresh token |
| `/api/v1/auth/refresh-token`   | POST   | Refresh access token using refresh token |
| `/api/v1/auth/logout`          | POST   | Logout and revoke refresh token          |
| `/api/v1/auth/forgot-password` | POST   | Send OTP to reset password               |
| `/api/v1/auth/reset-password`  | POST   | Reset password using OTP                 |

### Users

| Endpoint             | Method | Description      |
| -------------------- | ------ | ---------------- |
| `/api/v1/users`      | POST   | Create user      |
| `/api/v1/users/{id}` | GET    | Get user profile |
| `/api/v1/users/{id}` | PUT    | Update user      |
| `/api/v1/users/{id}` | DELETE | Delete user      |

### Roles

CRUD operations for roles and permissions.

### Categories

| Endpoint                  | Method | Description                          |
| ------------------------- | ------ | ------------------------------------ |
| `/api/v1/categories`      | POST   | Create category                      |
| `/api/v1/categories`      | GET    | List all categories (optional limit) |
| `/api/v1/categories/{id}` | GET    | Get category by ID                   |
| `/api/v1/categories/{id}` | PUT    | Update category                      |
| `/api/v1/categories/{id}` | DELETE | Delete category                      |

### Products

| Endpoint                         | Method | Description                                          |
| -------------------------------- | ------ | ---------------------------------------------------- |
| `/api/v1/products`               | POST   | Create product                                       |
| `/api/v1/products`               | GET    | List products (optional limit)                       |
| `/api/v1/products/{id}`          | GET    | Get product by ID                                    |
| `/api/v1/products/{id}/category` | POST   | Assign product to a category                         |
| `/api/v1/products/{id}`          | DELETE | Delete a single product                              |
| `/api/v1/products/multiple`      | DELETE | Delete multiple products (query param `product_ids`) |

---

## Testing with Postman

### Login

* Method: POST
* URL: `http://127.0.0.1:8000/api/v1/auth/login`
* Body (JSON):

```json
{
  "email": "admin@gmail.com",
  "password": "password123"
}
```

### Delete Multiple Products

* Method: DELETE
* URL: `http://127.0.0.1:8000/api/v1/products/multiple?product_ids=1&product_ids=2&product_ids=3`
* Body: empty

---

## License

MIT License

