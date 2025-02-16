from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import ProductCrudManager
from app.schemas import CreateProduct
from app.dependencies import check_product_exists

router = APIRouter(prefix="/products", tags=["Products"])

session_dependency = Annotated[AsyncSession, Depends(get_db_session)]

@router.get("/")
async def get_all_products(session: session_dependency):
    return await ProductCrudManager.select_all_active(session)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    session: session_dependency,
    product: CreateProduct
):
    await ProductCrudManager.insert(session, **product.model_dump())

    return {"transaction": "Successful"}


@router.get("/{category_slug}")
async def product_by_category(
    session: session_dependency,
    category_slug: str
):
    return await ProductCrudManager.select_products_by_category(session, category_slug)


@router.get("/detail/{product_slug}")
async def product_detail(session: session_dependency, product_slug: str):
    return await ProductCrudManager.select_by_condition(session, slug=product_slug)


@router.put("/{product_id}", dependencies=[Depends(check_product_exists)])
async def update_product(
    session: session_dependency, 
    product_id: int,
    product_update: CreateProduct
):
    await ProductCrudManager.update(session, product_id, **product_update.model_dump())

    return {
        "transaction": "Product update is successful"
    }


@router.delete("/", dependencies=[Depends(check_product_exists)])
async def delete_product(session: session_dependency, product_id: int):
    await ProductCrudManager.update(session, product_id, is_active=False)
    return {"transaction": "Product delete is successful"}