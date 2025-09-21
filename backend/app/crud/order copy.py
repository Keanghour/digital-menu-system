# # app/crud/order.py

# from sqlalchemy.orm import Session
# from app.db.models.order import Order, OrderItem
# from app.db.models.product import Product
# from app.schemas.order import OrderItemAdd, OrderItemUpdate

# def create_order(db: Session, order_data):
#     # Calculate prices and validate products
#     items = []
#     total_amount = 0

#     for item in order_data.items:
#         product = db.query(Product).filter(Product.id == item.product_id).first()
#         if not product:
#             raise ValueError(f"Product ID {item.product_id} not found")
#         price = product.price
#         total_price = price * item.quantity
#         total_amount += total_price

#         order_item = OrderItem(
#             product_id=item.product_id,
#             quantity=item.quantity,
#             price=price,
#             total_price=total_price
#         )
#         items.append(order_item)

#     order = Order(
#         customer_id=order_data.customer_id,
#         shipping_address=order_data.shipping_address,
#         payment_method=order_data.payment_method,
#         status="pending",
#         items=items
#     )

#     db.add(order)
#     db.commit()
#     db.refresh(order)
#     return order, total_amount


# def delete_order(db: Session, order_id: int) -> bool:
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         return False
#     db.delete(order)
#     db.commit()
#     return True


# def get_order_items(db: Session, order_id: int):
#     return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()




# def add_item_to_order(db: Session, order_id: int, item_data: OrderItemAdd):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         return None, "Order not found"

#     # Check if product already in order
#     existing_item = next((item for item in order.items if item.product_id == item_data.product_id), None)

#     product = db.query(Product).filter(Product.id == item_data.product_id).first()
#     if not product:
#         return None, "Product not found"

#     if existing_item:
#         existing_item.quantity += item_data.quantity
#         existing_item.total_price = existing_item.quantity * existing_item.price
#         db.add(existing_item)
#     else:
#         item_price = product.price  # capture price at order time
#         new_item = OrderItem(
#             order_id=order_id,
#             product_id=product.id,
#             quantity=item_data.quantity,
#             price=item_price,
#             total_price=item_price * item_data.quantity
#         )
#         db.add(new_item)

#     db.commit()
#     db.refresh(order)
#     return order, None

# def update_order_item(db: Session, order_id: int, item_id: int, item_update: OrderItemUpdate):
#     item = db.query(OrderItem).filter(OrderItem.id == item_id, OrderItem.order_id == order_id).first()
#     if not item:
#         return None, "Order item not found"

#     item.quantity = item_update.quantity
#     item.total_price = item.quantity * item.price
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item, None


# def remove_order_item(db: Session, order_id: int, item_id: int) -> bool:
#     from app.db.models.order import OrderItem

#     item = db.query(OrderItem).filter(
#         OrderItem.id == item_id,
#         OrderItem.order_id == order_id
#     ).first()

#     if not item:
#         return False

#     db.delete(item)
#     db.commit()
#     return True
