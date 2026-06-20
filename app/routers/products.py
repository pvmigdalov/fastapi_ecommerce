from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import ProductCrudManager
from app.dependencies import (
    check_category_exists,
    check_product_exists,
    session_dependency,
)
from app.schemas import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=Sequence[Product])
async def get_all_products(session: session_dependency):
    return await ProductCrudManager.select_all_active(session)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductCreate)
async def create_product(session: session_dependency, product: ProductCreate):
    await check_category_exists(session, product.category_id)
    return await ProductCrudManager.insert(session, **product.model_dump())


@router.get("/{product_id:uuid}", response_model=Product)
async def get_product(session: session_dependency, product_id: UUID):
    product = await ProductCrudManager.select_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.get("/{category_slug:str}", response_model=Sequence[Product])
async def get_product_by_category(session: session_dependency, category_slug: str):
    products = await ProductCrudManager.select_products_by_category(
        session, category_slug
    )
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No products found"
        )
    return products


@router.get("/detail/{product_slug}", response_model=Product)
async def get_product_detail(session: session_dependency, product_slug: str):
    product = await ProductCrudManager.select_by_condition(session, slug=product_slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.put("/{product_id:uuid}", response_model=Product)
async def update_product(
    session: session_dependency, product_id: UUID, product_update: ProductCreate
):
    product = await check_product_exists(session, product_id)
    await ProductCrudManager.update(session, product_id, **product_update.model_dump())
    await session.refresh(product)
    return product


@router.delete("/{product_id: uuid}", dependencies=[Depends(check_product_exists)])
async def delete_product(session: session_dependency, product_id: UUID):
    await ProductCrudManager.update(session, product_id, is_active=False)
    return {"transaction": "Product delete is successful"}
