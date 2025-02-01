from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import categories_crud
from app.database import get_db_session


async def check_category_exists(
        session: Annotated[Session, Depends(get_db_session)], 
        category_id: int
):
    category = await categories_crud.select_category_by_id(session, category_id)
    if category is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no category found")