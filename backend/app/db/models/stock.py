# app/db/models/stock.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    old_stock = Column(Integer, nullable=False)
    change = Column(Integer, nullable=False)  # + for stock-in, - for stock-out
    new_stock = Column(Integer, nullable=False)
    
    transaction_type = Column(String, nullable=False)  # "in" or "out"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="transactions")
