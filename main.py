from fastapi import FastAPI
import uvicorn

from app.routers import category_router
from app.routers import products_router
from app.routers import auth_router

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "My e-commerce app"}

app.include_router(category_router)
app.include_router(products_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000, 
        reload=True
    )