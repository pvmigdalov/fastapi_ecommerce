from decimal import Decimal
from typing import Annotated

from pydantic import UUID4, AnyHttpUrl, BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """
    Product's schema for POST requests
    """

    name: Annotated[
        str, Field(..., min_length=3, max_length=100, description="Product's name")
    ]
    description: Annotated[
        str, Field("", max_length=500, description="Product's description")
    ]
    price: Annotated[
        Decimal, Field(..., gt=0, decimal_places=2, description="Product's price")
    ]
    image_url: Annotated[AnyHttpUrl | None, Field(None, description="Image's url")]
    stock: Annotated[int, Field(0, description="Product's stock")]
    category_id: Annotated[UUID4, Field(..., description="Category uuid v4")]
    model_config = ConfigDict(extra="forbid")


class ProductUpdate(BaseModel):
    """
    Product's schema for PATCH requests
    """

    name: Annotated[
        str | None,
        Field(None, min_length=3, max_length=100, description="Product's name"),
    ]
    description: Annotated[
        str | None, Field(None, max_length=500, description="Product's description")
    ]
    price: Annotated[
        Decimal | None,
        Field(None, gt=0, decimal_places=2, description="Product's price"),
    ]
    image_url: Annotated[AnyHttpUrl | None, Field(None, description="Image's url")]
    stock: Annotated[int | None, Field(None, description="Product's stock")]
    category_id: Annotated[UUID4 | None, Field(None, description="Category uuid v4")]
    model_config = ConfigDict(extra="forbid")


class Product(ProductCreate):
    """
    Product's schema for GET requests
    """

    id: Annotated[UUID4, Field(..., description="Product's uuid v4")]
    is_active: Annotated[bool, Field(..., description="Activity status")]
    slug: Annotated[str, Field(..., description="Product's slug")]
    rating: Annotated[float, Field(0, description="Product's rating")]
    supplier_id: Annotated[UUID4, Field(..., description="Supplier's uuid v4")]
    model_config = ConfigDict(from_attributes=True)
