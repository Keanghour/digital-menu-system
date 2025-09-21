# app/api/v1/api_router.py

from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, roles, categories, products, stocks, product_images, product_reviews, orders, payments

api_router = APIRouter(prefix="/api/v1")  

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])

api_router.include_router(product_images.router, prefix="/productsImages", tags=["Product Images"])
api_router.include_router(product_reviews.router, prefix="/productsReviews", tags=["Product Reviews"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])




