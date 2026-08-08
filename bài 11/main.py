from fastapi import FastAPI
import models.book_model as book_model
from database import engine
from routers import book_router

book_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API System",
    description="Hệ thống RESTful API Quản lý Thư viện - Day 11 Hackathon",
    version="1.0.0"
)

app.include_router(book_router.router)