# app/db/models/product.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

UTC_NOW = lambda: datetime.utcnow()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")  # USD or KHR
    is_active = Column(Boolean, default=True)  # Track active/deleted products
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=UTC_NOW)
    updated_at = Column(DateTime(timezone=True), default=UTC_NOW, onupdate=UTC_NOW)


    category = relationship("Category", backref="products")

    transactions = relationship("StockTransaction", back_populates="product", cascade="all, delete-orphan")

    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")



    @property
    def stock(self):
        if not self.transactions:
            return 0
        return self.transactions[-1].new_stock



class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Float, nullable=False)  # e.g. 1.0 to 5.0
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="images")

    
    