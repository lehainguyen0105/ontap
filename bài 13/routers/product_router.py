from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import StandardResponse, ProductResponse, ProductCreate, ProductUpdate
from models.category import CategoryModel
import services.product_service as product_service
from typing import List, Optional

router = APIRouter(tags=["Products & Categories"])

@router.get("/products/", response_model=StandardResponse[List[ProductResponse]])
def get_products(category_id: Optional[int] = Query(None), search: Optional[str] = Query(None), db: Session = Depends(get_db)):
    products = product_service.get_products(db, category_id, search)
    return StandardResponse(
        statusCode=200,
        error=None,
        message="Lấy danh sách sản phẩm thành công",
        data=products
    )

@router.post("/products/", response_model=StandardResponse)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    # Check category exists
    category = db.query(CategoryModel).filter(CategoryModel.id == product_in.category_id).first()
    if not category:
        return StandardResponse(statusCode=404, error="Not Found", message="Danh mục sản phẩm không tồn tại!", data=None)

    # Check duplicate product_code
    if product_service.get_product_by_code(db, product_in.product_code):
        return StandardResponse(statusCode=400, error="Bad Request", message=f"Mã sản phẩm '{product_in.product_code}' đã tồn tại!", data=None)

    new_product = product_service.create_product(db, product_in)
    return StandardResponse(
        statusCode=201,
        error=None,
        message="Thêm mới sản phẩm thành công",
        data=ProductResponse.model_validate(new_product)
    )

@router.put("/products/{id}", response_model=StandardResponse)
def update_product(id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = product_service.update_product(db, id, product_in)
    if not updated_product:
        return StandardResponse(statusCode=404, error="Not Found", message="Sản phẩm không tồn tại!", data=None)

    return StandardResponse(
        statusCode=200,
        error=None,
        message="Cập nhật sản phẩm thành công",
        data=ProductResponse.model_validate(updated_product)
    )

@router.delete("/categories/{id}", response_model=StandardResponse)
def delete_category(id: int, db: Session = Depends(get_db)):
    result = product_service.delete_category_check(db, id)
    if result == "NOT_FOUND":
        return StandardResponse(statusCode=404, error="Not Found", message="Danh mục không tồn tại!", data=None)
    if result == "HAS_PRODUCTS":
        return StandardResponse(statusCode=400, error="Bad Request", message="Không thể xóa danh mục đang chứa sản phẩm!", data=None)

    return StandardResponse(statusCode=200, error=None, message="Xóa danh mục thành công", data=None)