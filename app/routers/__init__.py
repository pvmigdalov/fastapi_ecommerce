from .categories import router as categories_router
from .products import router as products_router
from .auth import router as auth_router


__all__ = (
    "categories_router",
    "products_router",
    "auth_router",
)
