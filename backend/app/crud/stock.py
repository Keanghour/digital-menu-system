# app/crud/stock.py

from sqlalchemy.orm import Session
from app.db.models.stock import StockTransaction
from app.db.models.product import Product


def create_initial_stock(db: Session, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    # First stock transaction
    tx = StockTransaction(
        product_id=product_id,
        old_stock=0,
        change=quantity,
        new_stock=quantity,
        transaction_type="init",
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def add_stock_transaction(db: Session, product_id: int, change: int, transaction_type: str):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    # Get latest stock transaction for old_stock
    last_tx = (
        db.query(StockTransaction)
        .filter(StockTransaction.product_id == product_id)
        .order_by(StockTransaction.created_at.desc())
        .first()
    )

    old_stock = last_tx.new_stock if last_tx else 0
    new_stock = old_stock + change

    tx = StockTransaction(
        product_id=product_id,
        old_stock=old_stock,
        change=change,
        new_stock=new_stock,
        transaction_type=transaction_type,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_latest_stock(db: Session, product_id: int):
    return (
        db.query(StockTransaction)
        .filter(StockTransaction.product_id == product_id)
        .order_by(StockTransaction.created_at.desc())
        .first()
    )


def get_stock_history(db: Session, product_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(StockTransaction)
        .filter(StockTransaction.product_id == product_id)
        .order_by(StockTransaction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_stock_history(db: Session, product_id: int):
    return db.query(StockTransaction).filter(StockTransaction.product_id == product_id).count()


def get_latest_stock_with_product(db: Session, product_id: int):
    return (
        db.query(StockTransaction, Product.name.label("product_name"))
        .join(Product, StockTransaction.product_id == Product.id)
        .filter(StockTransaction.product_id == product_id)
        .order_by(StockTransaction.created_at.desc())
        .first()
    )
