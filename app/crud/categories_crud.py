from app.crud.crud import BaseCrudManager
from app.models import Category


class CategoryCrudManager(BaseCrudManager[Category]):
    model_name = Category.__tablename__
    Model = Category
