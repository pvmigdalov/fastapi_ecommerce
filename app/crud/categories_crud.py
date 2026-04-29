from .crud import CrudManager
from ..models import Category


class CategoryCrudManager(CrudManager):
    model_name = "categories"
    Model = Category