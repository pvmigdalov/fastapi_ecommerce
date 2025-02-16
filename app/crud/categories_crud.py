from app.crud.crud import CrudManager
from app.models import Category

class CategoryCrudManager(CrudManager):
    model_name = "categories"
    Model = Category