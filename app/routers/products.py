from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import ProductCrudManager
from app.dependencies import check_product_exists, session_dependency
from app.schemas import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def get_all_products(session: session_dependency) -> Sequence[Product]:
    products = await ProductCrudManager.select_all_active(session)
    return [Product.model_validate(product) for product in products]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    session: session_dependency, product: ProductCreate
) -> ProductCreate:
    await ProductCrudManager.insert(session, **product.model_dump())
    return product


@router.get("/{product_id:uuid}")
async def get_product(session: session_dependency, product_id: UUID) -> Product:
    product = await ProductCrudManager.select_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return Product.model_validate(product)


@router.get("/{category_slug:str}")
async def get_product_by_category(
    session: session_dependency, category_slug: str
) -> Sequence[Product]:
    products = await ProductCrudManager.select_products_by_category(
        session, category_slug
    )
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No products found"
        )
    return [Product.model_validate(product) for product in products]


@router.get("/detail/{product_slug}")
async def get_product_detail(session: session_dependency, product_slug: str) -> Product:
    product = await ProductCrudManager.select_by_condition(session, slug=product_slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return Product.model_validate(product)


@router.put("/{product_id}", dependencies=[Depends(check_product_exists)])
async def update_product(
    session: session_dependency, product_id: UUID, product_update: ProductCreate
) -> ProductCreate:
    await ProductCrudManager.update(session, product_id, **product_update.model_dump())
    return product_update


@router.delete("/{product_id}", dependencies=[Depends(check_product_exists)])
async def delete_product(session: session_dependency, product_id: UUID):
    await ProductCrudManager.update(session, product_id, is_active=False)
    return {"transaction": "Product delete is successful"}
