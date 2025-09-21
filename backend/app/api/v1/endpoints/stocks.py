# app/api/v1/endpoints/stocks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.stock import PaginatedStockHistory, StockCreate, StockHistoryResponse, StockResponse, StockTransactionBase, StockUpdate
from app.services import product_service, stock_service

router = APIRouter()

from app.db.models.stock import StockTransaction

@router.get("/{product_id}/stock", response_model=StockTransactionBase, summary="Get latest stock info")
def get_stock(product_id: int, db: Session = Depends(get_db)):
    tx = db.query(StockTransaction).filter_by(product_id=product_id).order_by(StockTransaction.id.desc()).first()
    if not tx:
        raise HTTPException(status_code=404, detail="No stock transactions found")
    return tx



@router.patch("/{product_id}/stock", response_model=StockTransactionBase, summary="Update stock quantity")
def update_stock(product_id: int, stock_data: StockUpdate, db: Session = Depends(get_db)):
    transaction_type = "in" if stock_data.change > 0 else "out"
    tx = stock_service.record_stock_change(db, product_id, stock_data.change, transaction_type)
    if not tx:
        raise HTTPException(status_code=404, detail="Product not found")
    return tx



@router.get("/{id}/stock", response_model=StockResponse, summary="Check stock levels")
def get_stock(id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_stock(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product.id, "stock": product.stock}


@router.patch("/{id}/stock", response_model=StockResponse, summary="Update stock quantity")
def update_stock(id: int, stock_data: StockUpdate, db: Session = Depends(get_db)):
    product = product_service.update_product_stock(db, id, stock_data.stock)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product.id, "stock": product.stock}


@router.get("/{product_id}/stock/history", response_model=StockHistoryResponse, summary="Get stock history for a product")
def get_stock_history(product_id: int, db: Session = Depends(get_db)):
    history = stock_service.get_stock_history(db, product_id)
    if not history:
        raise HTTPException(status_code=404, detail="No stock transactions found for this product")
    return {"product_id": product_id, "history": history}


@router.post("/{product_id}/stock", response_model=StockTransactionBase, summary="Create initial stock for a product")
def create_stock(product_id: int, stock_data: StockCreate, db: Session = Depends(get_db)):
    tx = stock_service.create_stock_for_product(db, product_id, stock_data.quantity)
    if not tx:
        raise HTTPException(status_code=404, detail="Product not found")
    return tx


@router.get("/{product_id}/stock/history", response_model=PaginatedStockHistory, summary="Get paginated stock history")
def get_stock_history(
    product_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    history, total = stock_service.get_stock_history(db, product_id, skip=skip, limit=limit)
    if not history:
        raise HTTPException(status_code=404, detail="No stock transactions found for this product")
    return {
        "product_id": product_id,
        "total": total,
        "skip": skip,
        "limit": limit,
        "history": history,
    }

