from typing import Sequence

from fastapi import APIRouter, Depends, status

from ..crud import ProductCrudManager
from ..schemas import Product, ProductCreate
from ..dependencies import check_product_exists, session_dependency

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def get_all_products(session: session_dependency) -> Sequence[Product]:
    products = await ProductCrudManager.select_all_active(session)
    return [Product.model_validate(product) for product in products]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    session: session_dependency,
    product: ProductCreate
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
async def product_detail(
    session: session_dependency, 
    product_slug: str
):
    return await ProductCrudManager.select_by_condition(session, slug=product_slug)


@router.put("/{product_id}", dependencies=[Depends(check_product_exists)])
async def update_product(
    session: session_dependency, 
    id: int,
    product_update: ProductCreate
):
    await ProductCrudManager.update(session, id, **product_update.model_dump())

    return {
        "transaction": "Product update is successful"
    }


@router.delete("/", dependencies=[Depends(check_product_exists)])
async def delete_product(
    session: session_dependency, 
    id: int
):
    await ProductCrudManager.update(session, id, is_active=False)
    return {"transaction": "Product delete is successful"}