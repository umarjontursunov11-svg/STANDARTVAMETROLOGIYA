"""
Mahsulotlar va xizmatlar katalogi, kategoriyalar va mahsulot kartochkasi handleri.
O'zbek va Rus tillarini qo'llab-quvvatlaydi.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database import (
    get_categories,
    get_category_by_id,
    get_products_by_category,
    get_category_product_count,
    get_product_by_id,
    get_cart_item,
    get_user_language
)
from bot.keyboards import (
    categories_keyboard,
    products_list_keyboard,
    product_detail_keyboard
)
from bot.utils import format_product_card
from bot.utils.localization import get_text, CATEGORY_TRANSLATIONS

router = Router()
PAGE_SIZE = 5


@router.message(Command("catalog"))
@router.message(F.text.in_(["📦 Mahsulotlar katalogi", "📦 Каталог продукции"]))
async def show_catalog_handler(message: Message, state: FSMContext):
    """Kategoriyalar ro'yxatini ko'rsatish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    categories = await get_categories()
    
    if not categories:
        empty_msg = "В каталоге пока нет позиций." if lang == "ru" else "Hozircha katalogda kategoriyalar mavjud emas."
        await message.answer(empty_msg)
        return

    text = get_text("catalog_title", lang=lang)
    await message.answer(
        text,
        reply_markup=categories_keyboard(categories, lang=lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_cats")
async def back_to_categories_callback(callback: CallbackQuery, state: FSMContext):
    """Kategoriyalar ro'yxatiga qaytish."""
    await state.clear()
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    categories = await get_categories()
    
    text = get_text("catalog_title", lang=lang)
    await callback.message.edit_text(
        text,
        reply_markup=categories_keyboard(categories, lang=lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def category_products_callback(callback: CallbackQuery):
    """Tanlangan kategoriya ichidagi mahsulotlar ro'yxatini sahifalab chiqarish."""
    parts = callback.data.split("_")
    category_id = int(parts[1])
    page = int(parts[2]) if len(parts) > 2 else 1
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    category = await get_category_by_id(category_id)
    if not category:
        await callback.answer("Kategoriya topilmadi." if lang == "uz" else "Категория не найдена.", show_alert=True)
        return

    total_count = await get_category_product_count(category_id)
    offset = (page - 1) * PAGE_SIZE
    products = await get_products_by_category(category_id, limit=PAGE_SIZE, offset=offset)

    icon = category.get("icon", "📁")
    cat_name = category["name"]
    cat_desc = category.get("description", "")
    if lang == "ru" and category_id in CATEGORY_TRANSLATIONS:
        cat_name = CATEGORY_TRANSLATIONS[category_id]["name"]
        cat_desc = CATEGORY_TRANSLATIONS[category_id]["description"]

    text = get_text(
        "category_info",
        lang=lang,
        icon=icon,
        name=cat_name,
        desc=cat_desc,
        total_count=total_count
    )

    markup = products_list_keyboard(
        products=products,
        category_id=category_id,
        page=page,
        total_count=total_count,
        page_size=PAGE_SIZE,
        lang=lang
    )

    await callback.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("prod_"))
async def product_detail_callback(callback: CallbackQuery):
    """Mahsulot yoki xizmatning to'liq ma'lumotini ko'rsatish."""
    parts = callback.data.split("_")
    product_id = int(parts[1])
    category_id = int(parts[2]) if len(parts) > 2 else 0
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    product = await get_product_by_id(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi." if lang == "uz" else "Товар не найден.", show_alert=True)
        return

    in_cart_item = await get_cart_item(user_id, product_id)
    in_cart_qty = in_cart_item["quantity"] if in_cart_item else 0

    text = format_product_card(product, lang=lang)
    markup = product_detail_keyboard(
        product_id=product_id,
        category_id=category_id,
        is_service=bool(product.get("is_service", 0)),
        in_cart_qty=in_cart_qty,
        lang=lang
    )

    await callback.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    """Hech narsa bajarmaydigan tugma (masalan, sahifa raqami)."""
    await callback.answer()
