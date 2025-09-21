from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.models.order import Order, OrderItem
from app.db.models.product import Product
from app.schemas.order import (
    OrderCreate, OrderResponse, OrderUpdate,
    OrderItemAdd, OrderItemUpdate, OrderItemResponse,
    OrderStatusUpdate, BulkCancelRequest, BulkUpdateStatusRequest
)
from app.services import order_service
from app.crud import order as order_crud
from app.db.session import get_db

router = APIRouter()


# ─────────────────────────────────────────────
# ✅ Order Management
# ─────────────────────────────────────────────

@router.post("", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        return order_service.create_order(db, order_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create order: {str(e)}")


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(order_id, db)


@router.get("/orders", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return order_service.list_orders(db)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order_endpoint(order_id: int, update_data: OrderUpdate, db: Session = Depends(get_db)):
    order = order_service.update_order(db, order_id, update_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_service.serialize_order(order)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    order = order_service.cancel_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_service.serialize_order(order)



@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = order_crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} deleted successfully"}


# ─────────────────────────────────────────────
# ✅ Order Status Management
# ─────────────────────────────────────────────

@router.post("/orders/{order_id}/status", response_model=OrderResponse)
def change_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        return order_service.update_order_status(db, order_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/orders/{order_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    msg = order_service.confirm_order(order_id, db)
    return msg  # Just returns {"message": "..."}


@router.post("/orders/{order_id}/pay", summary="Process payment for an order")
def process_payment(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "confirmed":
        raise HTTPException(status_code=400, detail="Only confirmed orders can be paid.")
    
    order.status = "paid"
    db.commit()
    return {
        "message": "Payment processed successfully",
        "order_id": order.id,
        "new_status": order.status
    }


# ─────────────────────────────────────────────
# ✅ Order Items
# ─────────────────────────────────────────────

@router.get("/orders/{order_id}/items", response_model=List[OrderItemResponse])
def read_order_items(order_id: int, db: Session = Depends(get_db)):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Order items not found")

    response_items = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        response_items.append(OrderItemResponse(
            product_id=item.product_id,
            product_name=product.name if product else None,
            quantity=item.quantity,
            price=item.price,
            total_price=item.total_price,
            current_stock=product.stock if product else None
        ))

    return response_items


@router.post("/orders/{order_id}/items", response_model=OrderResponse)
def add_order_item(order_id: int, item: OrderItemAdd, db: Session = Depends(get_db)):
    try:
        return order_service.add_item(db, order_id, item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add item: {str(e)}")


@router.patch("/orders/{order_id}/items/{item_id}", response_model=OrderItemResponse)
def update_order_item(order_id: int, item_id: int, item_update: OrderItemUpdate, db: Session = Depends(get_db)):
    try:
        return order_service.update_item(db, order_id, item_id, item_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update item: {str(e)}")


@router.delete("/orders/{order_id}/items/{item_id}", summary="Remove an item from an order")
def remove_order_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
    success = order_crud.remove_order_item(db, order_id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"message": "Order item removed successfully"}


# ─────────────────────────────────────────────
# ✅ Bulk Actions
# ─────────────────────────────────────────────

@router.post("/orders/bulk-cancel", summary="Cancel multiple orders")
def bulk_cancel_orders(data: BulkCancelRequest, db: Session = Depends(get_db)):
    updated = 0
    for oid in data.order_ids:
        order = db.query(Order).filter(Order.id == oid).first()
        if order and order.status not in ["cancelled", "completed"]:
            order.status = "cancelled"
            updated += 1
    db.commit()
    return {"cancelled_count": updated}


@router.post("/orders/bulk-update-status", summary="Update status of multiple orders")
def bulk_update_order_status(data: BulkUpdateStatusRequest, db: Session = Depends(get_db)):
    updated = 0
    for oid in data.order_ids:
        order = db.query(Order).filter(Order.id == oid).first()
        if order:
            order.status = data.status
            updated += 1
    db.commit()
    return {"updated_count": updated, "new_status": data.status}


# ─────────────────────────────────────────────
# ✅ User-specific
# ─────────────────────────────────────────────

@router.get("/users/{user_id}/orders", summary="List orders by user", response_model=list[OrderResponse])
def list_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.customer_id == user_id).all()
    return [order_service.serialize_order(order) for order in orders]
