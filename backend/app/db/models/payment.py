from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum


class PaymentStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)



class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(SqlEnum(PaymentStatusEnum), default=PaymentStatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payment_method = relationship("PaymentMethod")
    order = relationship("Order", back_populates="payments")