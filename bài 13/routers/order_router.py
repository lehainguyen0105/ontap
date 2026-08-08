from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import StandardResponse
from schemas.order import OrderCreate, OrderResponse, OrderItemResponse
import services.order_service as order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=StandardResponse)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    order, err_msg = order_service.create_order_transaction(db, order_in)
    if err_msg:
        return StandardResponse(statusCode=400, error="Out of Stock / Bad Request", message=err_msg, data=None)

    return StandardResponse(
        statusCode=201,
        error=None,
        message="Tạo đơn hàng thành công",
        data={"order_id": order.id, "order_code": order.order_code, "total_amount": order.total_amount}
    )

@router.get("/{id}", response_model=StandardResponse)
def get_order_detail(id: int, db: Session = Depends(get_db)):
    order = order_service.get_order_by_id(db, id)
    if not order:
        return StandardResponse(statusCode=404, error="Not Found", message="Đơn hàng không tồn tại!", data=None)

    items_data = []
    for item in order.items:
        items_data.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name if item.product else None,
            "quantity": item.quantity,
            "unit_price": item.unit_price
        })

    order_detail = {
        "id": order.id,
        "order_code": order.order_code,
        "customer_name": order.customer_name,
        "total_amount": order.total_amount,
        "status": order.status,
        "items": items_data
    }

    return StandardResponse(
        statusCode=200,
        error=None,
        message="Lấy chi tiết đơn hàng thành công",
        data=order_detail
    )