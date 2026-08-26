"""
Tugmalar (Keyboards) paketi.
"""
from .reply import (
    main_menu_keyboard,
    ai_chat_keyboard,
    contact_keyboard,
    cancel_keyboard,
    admin_menu_keyboard
)
from .inline import (
    categories_keyboard,
    products_list_keyboard,
    product_detail_keyboard,
    search_results_keyboard,
    company_links_keyboard,
    ai_suggestions_keyboard,
    cart_view_keyboard,
    empty_cart_keyboard,
    language_select_keyboard
)

__all__ = [
    "main_menu_keyboard",
    "ai_chat_keyboard",
    "contact_keyboard",
    "cancel_keyboard",
    "admin_menu_keyboard",
    "categories_keyboard",
    "products_list_keyboard",
    "product_detail_keyboard",
    "search_results_keyboard",
    "company_links_keyboard",
    "ai_suggestions_keyboard",
    "cart_view_keyboard",
    "empty_cart_keyboard",
    "language_select_keyboard"
]
