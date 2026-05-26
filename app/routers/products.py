from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..crud import ProductCrudManager
from ..schemas import Product, ProductCreate
from ..dependencies import check_product_exists, session_dependency

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def get_all_products(session: session_dependency) -> Sequence[Product]:
    products = await ProductCrudManager.select_all_active(session)
    return [Product.model_validate(product) for product in products]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(session: session_dependency, product: ProductCreate):
    await ProductCrudManager.insert(session, **product.model_dump())

    return {"transaction": "Successful"}


@router.get("/{product_id:uuid}")
async def get_product(session: session_dependency, product_id: UUID) -> Product:
    product = await ProductCrudManager.select_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return Product.model_validate(product)


@router.get("/{category_slug:str}")
async def product_by_category(session: session_dependency, category_slug: str):
    return await ProductCrudManager.select_products_by_category(session, category_slug)


@router.get("/detail/{product_slug}")
async def product_detail(session: session_dependency, product_slug: str):
    return await ProductCrudManager.select_by_condition(session, slug=product_slug)


@router.put("/{product_id}", dependencies=[Depends(check_product_exists)])
async def update_product(
    session: session_dependency, product_id: UUID, product_update: ProductCreate
):
    await ProductCrudManager.update(session, product_id, **product_update.model_dump())

    return {"transaction": "Product update is successful"}


@router.delete("/", dependencies=[Depends(check_product_exists)])
async def delete_product(session: session_dependency, id: UUID):
    await ProductCrudManager.update(session, id, is_active=False)
    return {"transaction": "Product delete is successful"}
