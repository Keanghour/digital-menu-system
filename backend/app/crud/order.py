# app/crud/order.py

from typing import Tuple, Optional
from sqlalchemy.orm import Session
from app.db.models.order import Order, OrderItem
from app.db.models.product import Product
from app.schemas.order import OrderItemAdd, OrderItemUpdate


def create_order(db: Session, order_data) -> Tuple[Order, float]:
    """
    Create a new order with order items, calculate total amount.
    Raises ValueError if any product not found.
    """
    items = []
    total_amount = 0.0

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product ID {item.product_id} not found")

        price = product.price
        total_price = price * item.quantity
        total_amount += total_price

        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=price,
            total_price=total_price
        )
        items.append(order_item)

    order = Order(
        customer_id=order_data.customer_id,
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method,
        status="pending",
        items=items
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order, total_amount


def delete_order(db: Session, order_id: int) -> bool:
    """
    Delete order by ID. Returns True if deleted, False if not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True


def get_order_items(db: Session, order_id: int) -> list[OrderItem]:
    """
    Get all items of an order.
    """
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def add_item_to_order(db: Session, order_id: int, item_data: OrderItemAdd) -> Tuple[Optional[Order], Optional[str]]:
    """
    Add a new item or update quantity if product exists in order.
    Returns (order, None) on success, or (None, error message).
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None, "Order not found"

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        return None, "Product not found"

    existing_item = next((item for item in order.items if item.product_id == item_data.product_id), None)

    if existing_item:
        existing_item.quantity += item_data.quantity
        existing_item.total_price = existing_item.quantity * existing_item.price
        db.add(existing_item)
    else:
        new_item = OrderItem(
            order_id=order_id,
            product_id=product.id,
            quantity=item_data.quantity,
            price=product.price,
            total_price=product.price * item_data.quantity
        )
        db.add(new_item)

    db.commit()
    db.refresh(order)
    return order, None


def update_order_item(db: Session, order_id: int, item_id: int, item_update: OrderItemUpdate) -> Tuple[Optional[OrderItem], Optional[str]]:
    """
    Update quantity and total price of a specific order item.
    Returns (item, None) on success, or (None, error message).
    """
    item = db.query(OrderItem).filter(OrderItem.id == item_id, OrderItem.order_id == order_id).first()
    if not item:
        return None, "Order item not found"

    item.quantity = item_update.quantity
    item.total_price = item.quantity * item.price
    db.add(item)
    db.commit()
    db.refresh(item)
    return item, None


def remove_order_item(db: Session, order_id: int, item_id: int) -> bool:
    """
    Remove an item from an order. Returns True if removed, False if not found.
    """
    item = db.query(OrderItem).filter(OrderItem.id == item_id, OrderItem.order_id == order_id).first()
    if not item:
        return False

    db.delete(item)
    db.commit()
    return True
