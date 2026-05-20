from .crud import BaseCrudManager
from ..models import Category


class CategoryCrudManager(BaseCrudManager[Category]):
    model_name = Category.__tablename__
    Model = Category