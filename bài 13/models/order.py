from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_code = Column(String(20), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default="PENDING")  # PENDING, COMPLETED, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")