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
