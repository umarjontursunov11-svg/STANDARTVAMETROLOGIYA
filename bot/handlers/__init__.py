"""
Bot handlerlari paketi.
Tartib: start -> katalog -> qidiruv -> savatcha -> kompaniya -> buyurtma -> admin -> AI
"""
from .start import router as start_router
from .catalog import router as catalog_router
from .search import router as search_router
from .cart import router as cart_router
from .company import router as company_router
from .order import router as order_router
from .admin import router as admin_router
from .ai import router as ai_router

all_routers = [
    start_router,
    catalog_router,
    search_router,
    cart_router,
    company_router,
    order_router,
    admin_router,
    ai_router
]

__all__ = ["all_routers"]
