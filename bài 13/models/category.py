from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    products = relationship("ProductModel", back_populates="category")