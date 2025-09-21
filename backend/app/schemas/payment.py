from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"


class PaymentMethodCreate(BaseModel):
    name: str

class PaymentMethod(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        
class PaymentMethod(BaseModel):
    id: int
    name: str


class PaymentCreate(BaseModel):
    order_id: int
    payment_method_id: int
    amount: float = Field(gt=0)
    currency: str = "USD"
    metadata: Optional[Dict] = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    payment_method_id: int
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    updated_at: Optional[datetime]


class PaymentUpdateStatus(BaseModel):
    status: PaymentStatus


class BulkRefundRequest(BaseModel):
    payment_ids: List[int]
