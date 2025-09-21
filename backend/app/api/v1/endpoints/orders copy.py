# # app/api/v1/endpoints/orders.py

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.models.order import Order
# from app.schemas.order import BulkCancelRequest, BulkUpdateStatusRequest, OrderCreate, OrderItemAdd, OrderItemResponse, OrderItemUpdate, OrderResponse, OrderStatusUpdate, OrderUpdate
# from app.services import order_service
# from app.crud import order as order_crud
# from app.db.session import get_db

# router = APIRouter()


# @router.post("/orders/{order_id}/status", response_model=OrderResponse)
# def change_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
#     try:
#         order = order_service.update_order_status(db, order_id, payload.status)
#         return order  # assuming order response is compatible
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("", response_model=OrderResponse)
# def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
#     try:
#         return order_service.create_order(db, order_data)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.post("/orders/{order_id}/confirm")
# def confirm_order_endpoint(order_id: int, db: Session = Depends(get_db)):
#     return order_service.confirm_order(order_id, db)


# @router.get("/orders/{order_id}")
# def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
#     return order_service.get_order(order_id, db)

# @router.get("/orders")
# def list_orders_endpoint(db: Session = Depends(get_db)):
#     return order_service.list_orders(db)


# @router.put("/{order_id}", response_model=OrderResponse)
# def update_order_endpoint(
#     order_id: int,
#     update_data: OrderUpdate,
#     db: Session = Depends(get_db)
# ):
#     order = order_service.update_order(db, order_id, update_data)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     return order_service.serialize_order(order)


# @router.post("/{order_id}/cancel", response_model=OrderResponse)
# def cancel_order_endpoint(order_id: int, db: Session = Depends(get_db)):
#     order = order_service.cancel_order(db, order_id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order_service.serialize_order(order)


# @router.delete("/{order_id}", status_code=204)
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     success = order_crud.delete_order(db, order_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return

# @router.get("/{order_id}/items", response_model=list[OrderItemResponse])
# def list_order_items(order_id: int, db: Session = Depends(get_db)):
#     items = order_crud.get_order_items(db, order_id)
#     return order_service.serialize_order_items(items)


# @router.post("/orders/{order_id}/items", response_model=OrderResponse)
# def add_order_item(order_id: int, item: OrderItemAdd, db: Session = Depends(get_db)):
#     try:
#         order = order_service.add_item(db, order_id, item)
#         return order
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.patch("/orders/{order_id}/items/{item_id}", response_model=OrderItemResponse)
# def update_order_item(order_id: int, item_id: int, item_update: OrderItemUpdate, db: Session = Depends(get_db)):
#     try:
#         item = order_service.update_item(db, order_id, item_id, item_update)
#         return item
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
    
# @router.delete("/orders/{order_id}/items/{item_id}", summary="Remove an item from an order")
# def remove_order_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
#     success = order_crud.remove_order_item(db, order_id, item_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Order item not found")
#     return {"message": "Order item removed successfully"}


# @router.post("/orders/{order_id}/pay", summary="Process payment for an order")
# def process_payment(order_id: int, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     if order.status != "pending":
#         raise HTTPException(status_code=400, detail="Order is not in a payable state")

#     order.status = "paid"
#     db.commit()
#     return {"message": "Payment processed successfully", "status": order.status}


# @router.get("/users/{user_id}/orders", summary="List orders by user")
# def list_orders_by_user(user_id: int, db: Session = Depends(get_db)):
#     orders = db.query(Order).filter(Order.customer_id == user_id).all()
#     return [order_service.serialize_order(order) for order in orders]


# @router.post("/orders/bulk-cancel", summary="Cancel multiple orders")
# def bulk_cancel_orders(data: BulkCancelRequest, db: Session = Depends(get_db)):
#     updated = 0
#     for oid in data.order_ids:
#         order = db.query(Order).filter(Order.id == oid).first()
#         if order and order.status not in ["cancelled", "completed"]:
#             order.status = "cancelled"
#             updated += 1
#     db.commit()
#     return {"cancelled": updated}


# @router.post("/orders/bulk-update-status", summary="Update status of multiple orders")
# def bulk_update_order_status(data: BulkUpdateStatusRequest, db: Session = Depends(get_db)):
#     updated = 0
#     for oid in data.order_ids:
#         order = db.query(Order).filter(Order.id == oid).first()
#         if order:
#             order.status = data.status
#             updated += 1
#     db.commit()
#     return {"updated": updated, "new_status": data.status}


