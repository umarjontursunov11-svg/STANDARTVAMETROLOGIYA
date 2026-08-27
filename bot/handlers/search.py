"""
Mahsulotlar, standartlar va xizmatlarni aqlli qidirish tizimi handleri.
O'zbek va Rus tillarini qo'llab-quvvatlaydi.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database import search_products, log_search, get_categories, get_user_language
from bot.states import SearchState
from bot.keyboards import (
    cancel_keyboard,
    main_menu_keyboard,
    search_results_keyboard,
    categories_keyboard
)
from bot.utils import KNOWN_MENU_BUTTONS
from bot.utils.localization import get_text
from bot.config import config

router = Router()


@router.message(Command("search"))
@router.message(F.text.in_(["🔍 Mahsulot qidirish", "🔍 Поиск продукции"]))
async def start_search_message(message: Message, state: FSMContext):
    """Qidiruv rejimini ishga tushirish (xabar orqali)."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.set_state(SearchState.waiting_for_query)
    
    text = get_text("search_prompt", lang=lang)
    await message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")


@router.callback_query(F.data == "start_search")
async def start_search_callback(callback: CallbackQuery, state: FSMContext):
    """Qidiruv rejimini ishga tushirish (inline tugma orqali)."""
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    await state.set_state(SearchState.waiting_for_query)
    
    text = get_text("search_prompt", lang=lang)
    await callback.message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")
    await callback.answer()


@router.message(SearchState.waiting_for_query, F.text.in_(["❌ Bekor qilish", "❌ Отмена", "⬅ Asosiy menyuga qaytish", "⬅ Главное меню"]))
async def cancel_search(message: Message, state: FSMContext):
    """Qidiruv rejimini bekor qilish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    is_admin = user_id in (config.admin_ids or [])
    text = get_text("back_to_main_text", lang=lang)
    await message.answer(text, reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang), parse_mode="HTML")


@router.message(SearchState.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    """Foydalanuvchi yozgan qidiruv matnini qayta ishlash."""
    query = (message.text or "").strip()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    is_admin = user_id in (config.admin_ids or [])

    # Agar menyu tugmasi bosilgan bo'lsa, qidiruv holatini tozalaymiz
    if query in KNOWN_MENU_BUTTONS or query.startswith("/"):
        await state.clear()
        return

    if len(query) < 2:
        await message.answer(
            get_text("search_short", lang=lang),
            reply_markup=cancel_keyboard(lang=lang)
        )
        return

    # Qidiruvni qayd etish
    await log_search(user_id, query)

    # Bazadan qidirish
    results = await search_products(query, limit=10)

    if results:
        count = len(results)
        await state.clear()
        text = get_text("search_found", lang=lang, query=query, count=count)
        await message.answer(
            text,
            reply_markup=search_results_keyboard(results, lang=lang),
            parse_mode="HTML"
        )
    else:
        text = get_text("search_not_found", lang=lang, query=query)
        categories = await get_categories()
        await message.answer(
            text,
            reply_markup=categories_keyboard(categories, lang=lang),
            parse_mode="HTML"
        )
