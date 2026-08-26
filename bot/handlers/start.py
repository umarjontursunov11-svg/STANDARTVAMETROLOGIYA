"""
/start, /help, /lang va umumiy navigatsiya handlerlari (O'zbek / Rus tillarida).
"""

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.config import config
from bot.database import add_user, get_user_language, set_user_language
from bot.keyboards import main_menu_keyboard, language_select_keyboard
from bot.utils.localization import get_text

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start buyrug'i handleri."""
    await state.clear()
    
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name or "Foydalanuvchi"

    # Foydalanuvchini bazaga qo'shish
    await add_user(user_id, username, full_name)
    lang = await get_user_language(user_id)
    is_admin = user_id in (config.admin_ids or [])

    welcome_text = get_text(
        "welcome",
        lang=lang,
        full_name=full_name,
        company_name=config.company.name
    )

    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang),
        parse_mode="HTML"
    )


@router.message(Command("lang"))
@router.message(Command("language"))
@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык", "🌐 Til / Язык"]))
async def cmd_language(message: Message):
    """Tilni o'zgartirish menyusi."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    text = get_text("choose_language", lang=lang)
    await message.answer(text, reply_markup=language_select_keyboard(), parse_mode="HTML")


@router.callback_query(F.data.in_(["set_lang_uz", "set_lang_ru"]))
async def set_language_callback(callback: CallbackQuery):
    """Til tanlanganda bazaga yozish va menyuni yangilash."""
    user_id = callback.from_user.id
    new_lang = "ru" if callback.data == "set_lang_ru" else "uz"
    await set_user_language(user_id, new_lang)
    await callback.answer()

    is_admin = user_id in (config.admin_ids or [])
    confirm_text = get_text("language_changed", lang=new_lang)

    await callback.message.answer(
        confirm_text,
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=new_lang),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam buyrug'i."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    help_text = get_text(
        "help",
        lang=lang,
        support=config.company.telegram_support
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text.in_(["❌ Bekor qilish", "❌ Отмена", "⬅ Asosiy menyuga qaytish", "⬅ Главное меню"]))
async def cancel_handler(message: Message, state: FSMContext):
    """Har qanday jarayonni bekor qilib asosiy menyuga qaytish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    is_admin = user_id in (config.admin_ids or [])
    
    text = get_text("back_to_main_text", lang=lang)
    await message.answer(
        text,
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang)
    )
