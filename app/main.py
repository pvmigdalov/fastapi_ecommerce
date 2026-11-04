from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database import async_get_redis_rate_limiter
from app.exception_handlers import register_exception_handlers
from app.routers import auth_router, categories_router, products_router, reviews_router
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rate_limiter = await async_get_redis_rate_limiter(
        settings.redis_settings.redis_rate_limiter_url
    )
    yield
    await app.state.rate_limiter.close()


app = FastAPI(lifespan=lifespan)


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
