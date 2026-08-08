from fastapi import FastAPI
from database import engine, Base
from routers import product_router, order_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Management System API",
    description="Hệ thống Quản lý Đơn hàng & Thương mại Điện tử Nâng cao",
    version="1.0.0"
)

app.include_router(product_router.router)
app.include_router(order_router.router)