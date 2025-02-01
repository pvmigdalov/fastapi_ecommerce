from app.crud.crud import CrudManager
from app.models import Category

class CategoryCrudManager(CrudManager):
    Model = Category