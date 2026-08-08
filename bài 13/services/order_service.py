from sqlalchemy.orm import Session
from models.order import OrderModel
from models.order_item import OrderItemModel
from models.product import ProductModel
from schemas.order import OrderCreate
import uuid

def create_order_transaction(db: Session, order_in: OrderCreate):
    try:
        total_amount = 0.0
        order_items_to_create = []

        for item in order_in.items:
            product = db.query(ProductModel).filter(ProductModel.id == item.product_id).with_for_update().first()

            if not product:
                db.rollback()
                return None, f"Sản phẩm ID {item.product_id} không tồn tại!"

            if product.stock_quantity < item.quantity:
                db.rollback()
                return None, f"Sản phẩm '{product.name}' không đủ tồn kho (Còn {product.stock_quantity}, yêu cầu {item.quantity})!"

            item_total = product.price * item.quantity
            total_amount += item_total

            product.stock_quantity -= item.quantity

            order_items_to_create.append({
                "product_id": product.id,
                "quantity": item.quantity,
                "unit_price": product.price
            })

        order_code = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        new_order = OrderModel(
            order_code=order_code,
            customer_name=order_in.customer_name,
            total_amount=total_amount,
            status="COMPLETED"
        )
        db.add(new_order)
        db.flush() 

        for item_data in order_items_to_create:
            order_item = OrderItemModel(
                order_id=new_order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"]
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        return new_order, None

    except Exception as e:
        db.rollback()
        return None, str(e)

def get_order_by_id(db: Session, order_id: int):
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()