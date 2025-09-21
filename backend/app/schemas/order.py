# app/schemas/order.py

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")


class OrderCreate(BaseModel):
    customer_id: int
    shipping_address: str
    payment_method: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    product_name: Optional[str]
    quantity: int
    price: float
    total_price: float
    current_stock: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True  # works with SQLAlchemy model attributes


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    shipping_address: str
    payment_method: str      # <-- required
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    items: List[OrderItemResponse]   # <-- required
    total_amount: float


    class Config:
        orm_mode = True
        from_attributes = True


class OrderUpdate(BaseModel):
    shipping_address: Optional[str] = None
    payment_method: Optional[str] = None
    # You could extend this with validation or allow updating items carefully.


class OrderItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")


class OrderItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")


class BulkCancelRequest(BaseModel):
    order_ids: List[int] = Field(..., min_items=1, description="List of order IDs cannot be empty")


class BulkUpdateStatusRequest(BaseModel):
    order_ids: List[int] = Field(..., min_items=1, description="List of order IDs cannot be empty")
    status: OrderStatusEnum  # Use enum for stricter validation

    # Optional validator to ensure the status is valid - Pydantic will enforce enum automatically
    # @validator('status')
    # def validate_status(cls, v):
    #     if v not in OrderStatusEnum:
    #         raise ValueError('Invalid status value')
    #     return v
