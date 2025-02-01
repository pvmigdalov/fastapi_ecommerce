from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.database import Session, get_db_session
from app.crud import ProductCrudManager
from app.schemas import CreateProduct

router = APIRouter(prefix="/products", tags=["Products"])

session_dependency = Annotated[Session, Depends(get_db_session)]

@router.get("/")
async def get_all_products(session: session_dependency):
    return await ProductCrudManager.select_all_active(session)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    session: session_dependency,
    product: CreateProduct
):
    await ProductCrudManager.insert(session, product.model_dump())

    return {"transaction": "Successful"}


@router.get("/{category_slug}")
async def product_by_category(
    session: session_dependency,
    category_slug: str
):
    return await ProductCrudManager.select_products_by_category(session, category_slug)


@router.get("/detail/{product_slug}")
async def product_detail(session: session_dependency, product_slug: str):
    pass


@router.put("/{product_slug}")
async def update_product(session: session_dependency, product_slug: str):
    pass


@router.delete("/")
async def delete_product(session: session_dependency, product_id: int):
    pass