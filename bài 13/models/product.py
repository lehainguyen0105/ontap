from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("CategoryModel", back_populates="products")
    order_items = relationship("OrderItemModel", back_populates="product")