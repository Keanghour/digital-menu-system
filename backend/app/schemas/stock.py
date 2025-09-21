# app/schemas/stock.py

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime



# 🔹 Transaction representation
class StockTransactionBase(BaseModel):
    id: int
    product_id: int
    old_stock: int
    change: int
    new_stock: int
    transaction_type: str
    created_at: datetime

    class Config:
        orm_mode = True


# 🔹 Create initial stock
class StockCreate(BaseModel):
    quantity: int


# 🔹 Update stock (in/out change)
class StockUpdate(BaseModel):
    change: int  # e.g. +10 for in, -5 for out


# 🔹 Response for current stock
class StockResponse(BaseModel):
    product_id: int
    stock: int

    class Config:
        orm_mode = True


# 🔹 Full history (no pagination)
class StockHistoryResponse(BaseModel):
    product_id: int
    history: List[StockTransactionBase]


# 🔹 Paginated history
class PaginatedStockHistory(BaseModel):
    product_id: int
    total: int
    skip: Optional[int] = None
    limit: Optional[int] = None
    history: List[StockTransactionBase]


class StockTransactionWithProduct(BaseModel):
    id: int
    product_id: int
    product_name: str
    old_stock: int
    change: int
    new_stock: int
    transaction_type: str
    created_at: datetime

    class Config:
        orm_mode = True
