import uvicorn
from fastapi import FastAPI

from app.routers import auth_router, categories_router, products_router, reviews_router
from app.exception_heandlers import register_exception_handlers

app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "My e-commerce app"}


app.include_router(categories_router)
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(reviews_router)

register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
