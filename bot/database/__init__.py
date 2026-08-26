"""
Ma'lumotlar bazasi bilan ishlash paketi.
"""
from .db import init_db, get_db
from .models import (
    get_categories,
    get_category_by_id,
    get_products_by_category,
    get_category_product_count,
    get_product_by_id,
    search_products,
    log_search,
    add_user,
    get_user_language,
    set_user_language,
    add_to_cart,
    get_cart,
    get_cart_item_count,
    get_cart_item,
    update_cart_quantity,
    remove_from_cart,
    clear_cart,
    create_order_from_cart,
    create_order,
    get_recent_orders,
    get_stats,
    add_product,
    get_all_products_count
)

__all__ = [
    "init_db",
    "get_db",
    "get_categories",
    "get_category_by_id",
    "get_products_by_category",
    "get_category_product_count",
    "get_product_by_id",
    "search_products",
    "log_search",
    "add_user",
    "get_user_language",
    "set_user_language",
    "add_to_cart",
    "get_cart",
    "get_cart_item_count",
    "get_cart_item",
    "update_cart_quantity",
    "remove_from_cart",
    "clear_cart",
    "create_order_from_cart",
    "create_order",
    "get_recent_orders",
    "get_stats",
    "add_product",
    "get_all_products_count"
]
