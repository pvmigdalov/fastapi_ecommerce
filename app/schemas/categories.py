from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, Field


class CreateCategory(BaseModel):
    """
    Categorie's schema for POST/PUT requests
    """

    name: Annotated[
        str, Field(..., min_length=1, max_length=250, description="Category name")
    ]
    parent_id: Annotated[
        UUID4 | None, Field(None, description="Category parent UUID4 v4")
    ]
    model_config = ConfigDict(extra="forbid")


class Category(CreateCategory):
    """
    Category schema for GET requests
    """

    id: Annotated[UUID4, Field(..., description="Category uuid v4")]
    is_active: Annotated[bool, Field(..., description="Activity status")]
    slug: Annotated[str, Field(..., description="Category slug")]
    model_config = ConfigDict(from_attributes=True)
