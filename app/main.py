from fastapi import FastAPI

from app.routers import category_router

app = FastAPI()
app.include_router(category_router)
