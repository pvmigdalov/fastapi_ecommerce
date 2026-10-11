from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    """
    Review's schema for POST requests
    """

    product_id: Annotated[UUID4, Field(..., description="Product's uuiid v4")]
    user_id: Annotated[UUID4, Field(..., descripption="User's uuid v4")]
    comment: Annotated[str, Field(..., gt=1, le=5000, description="Text of review")]
    grade: Annotated[int, Field(..., ge=1, le=5, description="Product's grade")]


class Review(ReviewCreate):
    """
    Review's schema for GET requests
    """

    id: Annotated[UUID4, Field(..., description="Review's uuid v4")]
    is_actve: Annotated[bool, Field(..., description="Activity status")]
    model_config = ConfigDict(from_attributes=True)


class ReviewUpdate(BaseModel):
    """
    Review's schema for PATCH/PUT requests
    """

    comment: Annotated[str, Field(..., description="Text of review")]
    grade: Annotated[int, Field(..., descriotion="Product's grade")]
    model_config = ConfigDict(extra="forbid")
