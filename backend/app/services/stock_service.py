from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import stock as stock_crud
from app.db.models.order import Order
from app.db.models.product import Product
from app.db.models.stock import StockTransaction
from datetime import datetime


# 🔹 Create initial stock for a product
def create_stock_for_product(db: Session, product_id: int, quantity: int):
    return stock_crud.create_initial_stock(db, product_id, quantity)


# 🔹 Record stock change (in/out)
def record_stock_change(db: Session, product_id: int, change: int, transaction_type: str):
    return stock_crud.add_stock_transaction(db, product_id, change, transaction_type)


# 🔹 Get latest stock transaction
def get_latest_stock(db: Session, product_id: int):
    return stock_crud.get_latest_stock(db, product_id)


# 🔹 Get paginated stock history
def get_stock_history(db: Session, product_id: int, skip: int = 0, limit: int = 10):
    items = stock_crud.get_stock_history(db, product_id, skip=skip, limit=limit)
    total = stock_crud.count_stock_history(db, product_id)
    return items, total



def consume_stock_for_order(db: Session, product_id: int, quantity: int):
    """
    Deduct stock using FIFO (oldest stock first).
    """
    transactions = (
        db.query(StockTransaction)
        .filter(StockTransaction.product_id == product_id, StockTransaction.new_stock > 0)
        .order_by(StockTransaction.created_at.asc())
        .all()
    )

    remaining = quantity
    for tx in transactions:
        if remaining <= 0:
            break

        if tx.new_stock >= remaining:
            tx.new_stock -= remaining
            remaining = 0
        else:
            remaining -= tx.new_stock
            tx.new_stock = 0

        db.add(tx)

    if remaining > 0:
        raise HTTPException(status_code=400, detail="Not enough stock")

    db.commit()
    return True


def confirm_order(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Order is not in a pending state")

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        old_stock = product.stock
        if old_stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'. Available: {old_stock}, Required: {item.quantity}"
            )

        new_stock = old_stock - item.quantity

        # Create a stock transaction for the deduction
        txn = StockTransaction(
            product_id=product.id,
            old_stock=old_stock,
            change=-item.quantity,
            new_stock=new_stock,
            transaction_type="out",
            created_at=datetime.utcnow()
        )

        db.add(txn)

    # Update order status
    order.status = "confirmed"
    db.commit()

    return {"message": f"Order #{order.id} confirmed and stock updated successfully"}
