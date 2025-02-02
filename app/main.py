from fastapi import FastAPI
import uvicorn

from app.routers import category_router
from app.routers import products_router

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "My e-commerce app"}

app.include_router(category_router)
app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)