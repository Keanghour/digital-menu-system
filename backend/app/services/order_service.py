# app/services/order_service.py

from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.order import Order
from app.db.models.product import Product
from app.db.models.stock import StockTransaction
from app.schemas.order import OrderCreate, OrderItemAdd, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderUpdate
from app.crud import order as order_crud
from datetime import datetime


def get_current_stock(db: Session, product_id: int) -> int:
    """
    Calculate current stock for a product by summing all stock transaction changes.
    """
    stock_sum = db.query(func.sum(StockTransaction.change)).filter(
        StockTransaction.product_id == product_id
    ).scalar()
    return stock_sum or 0


# def serialize_order(order: Order) -> OrderResponse:
#     items = []
#     total_amount = 0
#     for item in order.items:
#         product = item.product  # relationship
#         item_total = item.price * item.quantity
#         total_amount += item_total
#         items.append(OrderItemResponse(
#             product_id=item.product_id,
#             product_name=product.name if product else None,
#             quantity=item.quantity,
#             price=item.price,
#             total_price=item_total,
#             current_stock=get_current_stock(order.items[0].__dict__.get('_sa_instance_state').session, item.product_id) if product else None
#         ))

#     return OrderResponse(
#         order_id=order.id,
#         customer_id=order.customer_id,
#         shipping_address=order.shipping_address,
#         payment_method=order.payment_method,
#         status=order.status,
#         created_at=order.created_at,
#         items=items,
#         total_amount=total_amount
#     )


def serialize_order(order: Order, db: Session) -> OrderResponse:
    items = []
    total_amount = 0
    for item in order.items:
        product = item.product
        item_total = item.price * item.quantity
        total_amount += item_total
        items.append(OrderItemResponse(
            product_id=item.product_id,
            product_name=product.name if product else None,
            quantity=item.quantity,
            price=item.price,
            total_price=item_total,
            current_stock=get_current_stock(db, item.product_id) if product else None
        ))

    return OrderResponse(
        order_id=order.id,
        customer_id=order.customer_id,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        status=order.status,
        created_at=order.created_at,
        updated_at=getattr(order, "updated_at", None),
        confirmed_at=getattr(order, "confirmed_at", None),
        items=items,
        total_amount=total_amount
    )


def create_order(db: Session, data: OrderCreate) -> OrderResponse:
    try:
        order, total_amount = order_crud.create_order(db, data)
    except ValueError as e:
        raise Exception(str(e))

    # Prepare response items with product names
    items_response = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product_name = product.name if product else None
        current_stock = get_current_stock(db, item.product_id)

        items_response.append({
            "product_id": item.product_id,
            "product_name": product_name,
            "quantity": item.quantity,
            "price": item.price,
            "total_price": item.total_price,
            "current_stock": current_stock
        })

    return OrderResponse(
        order_id=order.id,
        customer_id=order.customer_id,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        status=order.status,
        created_at=order.created_at,
        items=items_response,
        total_amount=total_amount
    )


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

        current_stock = get_current_stock(db, product.id)
        if current_stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'. Available: {current_stock}, Required: {item.quantity}"
            )

        new_stock = current_stock - item.quantity

        # Create a stock transaction for the deduction
        txn = StockTransaction(
            product_id=product.id,
            old_stock=current_stock,
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


def get_order(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = []
    total_amount = 0

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        current_stock = get_current_stock(db, item.product_id)
        items.append({
            "product_id": item.product_id,
            "product_name": product.name if product else "Unknown",
            "quantity": item.quantity,
            "price": item.price,
            "total_price": item.total_price,
            "current_stock": current_stock
        })
        total_amount += item.total_price

    return {
        "order_id": order.id,
        "customer_id": order.customer_id,
        "shipping_address": order.shipping_address,
        "payment_method": order.payment_method,
        "status": order.status,
        "created_at": order.created_at,
        "items": items,
        "total_amount": total_amount
    }


def list_orders(db: Session):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()

    result = []
    for order in orders:
        total_amount = sum(item.total_price for item in order.items)
        
        # serialize items
        items = []
        for item in order.items:
            product = item.product  # assuming relationship exists
            items.append({
                "product_id": item.product_id,
                "product_name": product.name if product else None,
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.total_price,
                # optionally add current_stock or other fields if needed
            })

        result.append({
            "order_id": order.id,
            "customer_id": order.customer_id,
            "shipping_address": order.shipping_address,
            "payment_method": order.payment_method,
            "status": order.status,
            "created_at": order.created_at,
            "items": items,
            "total_amount": total_amount
        })

    return result



def update_order(db: Session, order_id: int, update_data: OrderUpdate) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order_id: int) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    if order.status == "cancelled":
        return order  # Already cancelled

    order.status = "cancelled"
    db.commit()
    db.refresh(order)

    # (Optional) Restore stock for each item
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            current_stock = get_current_stock(db, product.id)
            change = item.quantity
            new_stock = current_stock + change

            transaction = StockTransaction(
                product_id=item.product_id,
                old_stock=current_stock,
                change=change,
                new_stock=new_stock,
                transaction_type="in",
                created_at=datetime.utcnow()
            )
            db.add(transaction)
    db.commit()

    return order


def add_item(db: Session, order_id: int, item_data: OrderItemAdd) -> OrderResponse:
    order, error = order_crud.add_item_to_order(db, order_id, item_data)
    if error:
        raise Exception(error)
    # serialize order or just items depending on your response design
    return serialize_order(order)


def update_item(db: Session, order_id: int, item_id: int, item_data: OrderItemUpdate):
    item, error = order_crud.update_order_item(db, order_id, item_id, item_data)
    if error:
        raise Exception(error)
    # serialize item response or return updated item info
    return item
