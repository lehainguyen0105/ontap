from sqlalchemy.orm import Session
from models.product import ProductModel
from models.category import CategoryModel
from schemas.product import ProductCreate, ProductUpdate
from typing import Optional, List

def get_products(db: Session, category_id: Optional[int] = None, search: Optional[str] = None):
    query = db.query(ProductModel)
    if category_id:
        query = query.filter(ProductModel.category_id == category_id)
    if search:
        query = query.filter(ProductModel.name.ilike(f"%{search}%"))
    return query.all()

def get_product_by_code(db: Session, code: str):
    return db.query(ProductModel).filter(ProductModel.product_code == code).first()

def get_product_by_id(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def create_product(db: Session, product_in: ProductCreate):
    db_product = ProductModel(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_in: ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_category_check(db: Session, category_id: int):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        return "NOT_FOUND"

    product_count = db.query(ProductModel).filter(ProductModel.category_id == category_id).count()
    if product_count > 0:
        return "HAS_PRODUCTS"

    db.delete(category)
    db.commit()
    return "SUCCESS"