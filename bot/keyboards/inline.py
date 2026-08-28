"""
InlineKeyboardMarkup (Xabar ostidagi tugmalar) moduli.
O'zbek va Rus tillarini to'liq qo'llab-quvvatlaydi.
"""

import math
from typing import List, Dict, Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import config
from bot.utils.localization import CATEGORY_TRANSLATIONS, get_text


def language_select_keyboard() -> InlineKeyboardMarkup:
    """Tilni tanlash tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")
            ]
        ]
    )


def categories_keyboard(categories: List[Dict[str, Any]], lang: str = "uz") -> InlineKeyboardMarkup:
    """Kategoriyalar ro'yxati tugmalari."""
    keyboard = []
    for cat in categories:
        cat_id = cat["id"]
        if lang == "ru" and cat_id in CATEGORY_TRANSLATIONS:
            cat_name = CATEGORY_TRANSLATIONS[cat_id]["name"]
        else:
            cat_name = cat["name"]

        name = f"{cat.get('icon', '📁')} {cat_name}"
        keyboard.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"cat_{cat_id}_1"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def products_list_keyboard(
    products: List[Dict[str, Any]],
    category_id: int,
    page: int,
    total_count: int,
    page_size: int = 5,
    lang: str = "uz"
) -> InlineKeyboardMarkup:
    """Kategoriya ichidagi mahsulotlar ro'yxati va paginatsiya."""
    keyboard = []
    total_pages = max(1, math.ceil(total_count / page_size))

    # Mahsulotlar tugmalari
    for prod in products:
        item_icon = "🔬" if prod.get("is_service") else "🔹"
        text = f"{item_icon} {prod['name']}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"prod_{prod['id']}_{category_id}"
            )
        ])

    # Paginatsiya qatori
    nav_row = []
    prev_txt = "⬅ Назад" if lang == "ru" else "⬅ Oldingi"
    next_txt = "Вперед ➡" if lang == "ru" else "Keyingi ➡"
    back_cats_txt = "🔙 К списку категорий" if lang == "ru" else "🔙 Kategoriyalar ro'yxatiga"
    cart_txt = "🛒 Корзина" if lang == "ru" else "🛒 Savatcha"

    if page > 1:
        nav_row.append(
            InlineKeyboardButton(
                text=prev_txt,
                callback_data=f"cat_{category_id}_{page - 1}"
            )
        )

    nav_row.append(
        InlineKeyboardButton(
            text=f"📄 {page}/{total_pages}",
            callback_data="noop"
        )
    )

    if page < total_pages:
        nav_row.append(
            InlineKeyboardButton(
                text=next_txt,
                callback_data=f"cat_{category_id}_{page + 1}"
            )
        )

    if len(nav_row) > 1:
        keyboard.append(nav_row)

    # Orqaga qaytish va savatcha tugmalari
    keyboard.append([
        InlineKeyboardButton(
            text=back_cats_txt,
            callback_data="back_to_cats"
        ),
        InlineKeyboardButton(
            text=cart_txt,
            callback_data="view_cart"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_detail_keyboard(
    product_id: int,
    category_id: int = 0,
    is_service: bool = False,
    in_cart_qty: int = 0,
    lang: str = "uz"
) -> InlineKeyboardMarkup:
    """Mahsulot tafsilotlari ostidagi amallar tugmasi."""
    keyboard = []

    if is_service:
        order_txt = "📝 Заявка на услугу" if lang == "ru" else "📝 Xizmatga yozilish / Ariza"
        keyboard.append([
            InlineKeyboardButton(
                text=order_txt,
                callback_data=f"order_{product_id}"
            )
        ])
    else:
        # Savatchaga qo'shish tugmasi
        if in_cart_qty > 0:
            cart_text = f"🛒 В корзине: {in_cart_qty} шт (➕ Еще)" if lang == "ru" else f"🛒 Savatchada: {in_cart_qty} ta (➕ Yana qo'shish)"
        else:
            cart_text = "🛒 В корзину" if lang == "ru" else "🛒 Savatchaga qo'shish"

        keyboard.append([
            InlineKeyboardButton(
                text=cart_text,
                callback_data=f"add_cart_{product_id}_{category_id}"
            )
        ])

        # To'g'ridan-to'g'ri tezkor buyurtma yoki savatchani ko'rish
        quick_txt = "⚡ Быстрый заказ" if lang == "ru" else "⚡ Tezkor buyurtma"
        view_cart_txt = "🛒 В корзину" if lang == "ru" else "🛒 Savatchani ko'rish"

        action_row = [
            InlineKeyboardButton(
                text=quick_txt,
                callback_data=f"order_{product_id}"
            )
        ]
        if in_cart_qty > 0:
            action_row.append(
                InlineKeyboardButton(
                    text=view_cart_txt,
                    callback_data="view_cart"
                )
            )
        keyboard.append(action_row)

    back_row = []
    back_list_txt = "🔙 К списку" if lang == "ru" else "🔙 Ro'yxatga qaytish"
    search_txt = "🔍 Поиск" if lang == "ru" else "🔍 Qidiruv"

    if category_id > 0:
        back_row.append(
            InlineKeyboardButton(
                text=back_list_txt,
                callback_data=f"cat_{category_id}_1"
            )
        )
    
    back_row.append(
        InlineKeyboardButton(
            text=search_txt,
            callback_data="start_search"
        )
    )

    keyboard.append(back_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cart_view_keyboard(cart_items: List[Dict[str, Any]], lang: str = "uz") -> InlineKeyboardMarkup:
    """Savatcha ko'rinishi va mahsulotlar sonini boshqarish tugmalari."""
    keyboard = []

    del_txt = "🗑 Удалить" if lang == "ru" else "🗑 O'chirish"
    checkout_txt = "✅ Оформить заказ" if lang == "ru" else "✅ Buyurtmani rasmiylashtirish"
    clear_all_txt = "🗑 Очистить корзину" if lang == "ru" else "🗑 Savatchani tozalash"
    back_cats_txt = "📦 В каталог" if lang == "ru" else "📦 Katalogga qaytish"
    unit_txt = "шт" if lang == "ru" else "ta"

    for idx, item in enumerate(cart_items, 1):
        pid = item["product_id"]
        qty = item["quantity"]
        pname = item.get("product_name", f"Mahsulot #{idx}")
        short_name = (pname[:22] + "...") if len(pname) > 25 else pname

        keyboard.append([
            InlineKeyboardButton(
                text=f"{idx}. {short_name}",
                callback_data=f"prod_{pid}_0"
            )
        ])

        keyboard.append([
            InlineKeyboardButton(text="➖", callback_data=f"cart_dec_{pid}"),
            InlineKeyboardButton(text=f"{qty} {unit_txt}", callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_inc_{pid}"),
            InlineKeyboardButton(text=del_txt, callback_data=f"cart_del_{pid}")
        ])

    keyboard.append([
        InlineKeyboardButton(
            text=checkout_txt,
            callback_data="checkout_cart"
        )
    ])

    keyboard.append([
        InlineKeyboardButton(
            text=clear_all_txt,
            callback_data="clear_cart_all"
        ),
        InlineKeyboardButton(
            text=back_cats_txt,
            callback_data="back_to_cats"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def empty_cart_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Bo'sh savatcha tugmalari."""
    cat_txt = "📦 Каталог продукции" if lang == "ru" else "📦 Mahsulotlar katalogiga o'tish"
    search_txt = "🔍 Поиск продукции" if lang == "ru" else "🔍 Mahsulot qidirish"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=cat_txt,
                    callback_data="back_to_cats"
                )
            ],
            [
                InlineKeyboardButton(
                    text=search_txt,
                    callback_data="start_search"
                )
            ]
        ]
    )


def search_results_keyboard(products: List[Dict[str, Any]], lang: str = "uz") -> InlineKeyboardMarkup:
    """Qidiruv natijalari ro'yxati tugmalari."""
    keyboard = []
    for prod in products:
        icon = "🔬" if prod.get("is_service") else "🔹"
        text = f"{icon} {prod['name']} ({prod.get('code', '')})"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"prod_{prod['id']}_0"
            )
        ])

    research_txt = "🔍 Повторить поиск" if lang == "ru" else "🔍 Qayta qidirish"
    cart_txt = "🛒 Корзина" if lang == "ru" else "🛒 Savatcha"
    full_cat_txt = "📦 Полный каталог" if lang == "ru" else "📦 To'liq katalog"

    keyboard.append([
        InlineKeyboardButton(
            text=research_txt,
            callback_data="start_search"
        ),
        InlineKeyboardButton(
            text=cart_txt,
            callback_data="view_cart"
        )
    ])
    keyboard.append([
        InlineKeyboardButton(
            text=full_cat_txt,
            callback_data="back_to_cats"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def company_links_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Kompaniya haqida bo'limi uchun havolalar va amallar."""
    keyboard = []

    web_txt = "🌐 Официальный сайт" if lang == "ru" else "🌐 Rasmiy veb-sayt"
    tg_txt = "💬 Связаться в Telegram" if lang == "ru" else "💬 Telegram orqali bog'lanish"

    if config.company.website and (config.company.website.startswith("http://") or config.company.website.startswith("https://")):
        keyboard.append([
            InlineKeyboardButton(
                text=web_txt,
                url=config.company.website
            )
        ])

    if config.company.telegram_support and (config.company.telegram_support.startswith("@") or config.company.telegram_support.startswith("http")):
        support_url = (
            f"https://t.me/{config.company.telegram_support.lstrip('@')}"
            if config.company.telegram_support.startswith("@")
            else config.company.telegram_support
        )
        keyboard.append([
            InlineKeyboardButton(
                text=tg_txt,
                url=support_url
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def ai_suggestions_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """AI Metrolog Maslahatchi uchun tezkor savollar tugmalari (O'zbek / Rus)."""
    if lang == "ru":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🧪 Что такое ГСО и буферные растворы?",
                        callback_data="ai_ask_gso"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⚙️ В чем разница поверки и калибровки?",
                        callback_data="ai_ask_poverka"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="💧 ГСО жесткости и мутности воды",
                        callback_data="ai_ask_water"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔬 Подбор вискозиметров и ареометров",
                        callback_data="ai_ask_devices"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⚗️ Стандарт-титры (Фиксаналы)",
                        callback_data="ai_ask_fixanals"
                    )
                ]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧪 GSO va Bufer eritmalar nima?",
                    callback_data="ai_ask_gso"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Poverka va Kalibrlash farqi?",
                    callback_data="ai_ask_poverka"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💧 Suv qattiqligi va loyqaligi",
                    callback_data="ai_ask_water"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔬 Viskozimetr va Areometr tanlash",
                    callback_data="ai_ask_devices"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚗️ Fiksanallar (Standart-titrlar)",
                    callback_data="ai_ask_fixanals"
                )
            ]
        ]
    )
