from .crud import BaseCrudManager
from ..models import Category


class CategoryCrudManager(BaseCrudManager):
    model_name = "categories"
    Model = Category