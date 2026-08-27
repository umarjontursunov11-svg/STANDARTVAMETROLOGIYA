"""
AI (Sun'iy Intellekt) Metrolog Maslahatchi handleri.
Foydalanuvchilarga metrologiya, standartlar, GSO va asboblar bo'yicha 24/7 AI maslahat beradi.
O'zbek va Rus tillarini to'liq qo'llab-quvvatlaydi.
"""

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.services import ai_service
from bot.database import get_user_language
from bot.states import AIState
from bot.keyboards import (
    main_menu_keyboard,
    ai_chat_keyboard,
    ai_suggestions_keyboard
)
from bot.utils.localization import get_text
from bot.utils import KNOWN_MENU_BUTTONS
from bot.config import config

router = Router()


@router.message(Command("ai"))
@router.message(F.text.in_(["🤖 AI Metrolog Maslahatchi", "🤖 AI Консультант Метролог"]))
async def start_ai_chat_handler(message: Message, state: FSMContext):
    """AI Metrolog Maslahatchi suhbat rejimini ishga tushirish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.set_state(AIState.chatting)

    welcome_text = get_text("ai_welcome", lang=lang)
    quick_text = get_text("ai_quick_topics", lang=lang)

    await message.answer(
        welcome_text,
        reply_markup=ai_chat_keyboard(lang=lang),
        parse_mode="HTML"
    )
    await message.answer(
        quick_text,
        reply_markup=ai_suggestions_keyboard(lang=lang),
        parse_mode="HTML"
    )


@router.message(AIState.chatting, F.text.in_(["🧹 Muloqotni tozalash", "🧹 Очистить историю"]))
async def clear_ai_history_handler(message: Message, state: FSMContext):
    """AI muloqot tarixini tozalash."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    ai_service.clear_history(user_id)

    text = get_text("ai_history_cleared", lang=lang)
    await message.answer(
        text,
        reply_markup=ai_chat_keyboard(lang=lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("ai_ask_"))
async def ai_suggestion_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Tezkor savollar tugmasi bosilganda AI javobini chiqarish."""
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    await state.set_state(AIState.chatting)
    await callback.answer()

    if lang == "ru":
        topic_map = {
            "ai_ask_gso": "Расскажите подробно про ГСО (государственные стандартные образцы) завода ЭКРОСХИМ по ISO 17034 и буферные растворы",
            "ai_ask_poverka": "В чем разница между поверкой, калибровкой и аттестацией средств измерений?",
            "ai_ask_water": "Какими ГСО определяются показатели жесткости, мутности и цветности воды?",
            "ai_ask_devices": "Как правильно подобрать капиллярный вискозиметр ВПЖ и ареометры АОН/АНТ?",
            "ai_ask_fixanals": "Что такое стандарт-титры (фиксаналы) и как они применяются в анализе?"
        }
        default_q = "Расскажите об услугах поверки и калибровки"
    else:
        topic_map = {
            "ai_ask_gso": "GSO (Davlat standart namunalari) va bufer eritmalar haqida to'liq ma'lumot bering",
            "ai_ask_poverka": "Qiyoslash (poverka) va kalibrlashning farqi nimada?",
            "ai_ask_water": "Suvning umumiy qattiqligi va loyqaligini qanday GSO standartlar bilan aniqlash mumkin?",
            "ai_ask_devices": "Kapillyar viskozimetrlar (VPJ) va areometrlar (AON, ANT) qanday tanlanadi?",
            "ai_ask_fixanals": "Standart titrlar (fiksanallar) nima va qanday tahlillarda ishlatiladi?"
        }
        default_q = "Metrologik xizmatlar haqida ma'lumot bering"

    user_query = topic_map.get(callback.data, default_q)

    # Typing holatini ko'rsatish
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

    response = await ai_service.get_response(user_id, user_query)

    await callback.message.answer(
        response,
        reply_markup=ai_chat_keyboard(lang=lang),
        parse_mode="HTML"
    )


@router.message(AIState.chatting, F.text.in_(["⬅ Asosiy menyuga qaytish", "⬅ Главное меню", "❌ Bekor qilish", "❌ Отмена"]))
async def exit_ai_chat(message: Message, state: FSMContext):
    """AI suhbat rejimidan chiqish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    is_admin = user_id in (config.admin_ids or [])
    text = get_text("back_to_main_text", lang=lang)
    await message.answer(
        text,
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang)
    )


@router.message(AIState.chatting, F.text & ~F.text.startswith("/") & ~F.text.in_(KNOWN_MENU_BUTTONS))
async def process_ai_chat_message(message: Message, bot: Bot, state: FSMContext):
    """AI suhbat rejimida yozilgan xabarga javob qaytarish."""
    user_text = message.text.strip()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    # Typing animatsiyasi
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # AI dan javob olish
    response = await ai_service.get_response(user_id, user_text)

    await message.answer(
        response,
        reply_markup=ai_chat_keyboard(lang=lang),
        parse_mode="HTML"
    )


@router.message(StateFilter(None), F.text & ~F.text.startswith("/") & ~F.text.in_(KNOWN_MENU_BUTTONS))
async def fallback_smart_ai_handler(message: Message, bot: Bot, state: FSMContext):
    """
    Foydalanuvchi menyu tugmasi bo'lmagan erkin savol yozganda AI orqali aqlli maslahat berish.
    Faqatgina hech qanday FSM holat faol bo'lmaganda va matn menyu tugmasi bo'lmaganda ishlaydi.
    """
    user_text = message.text.strip()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    # Typing animatsiyasi
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # AI dan javob olish
    response = await ai_service.get_response(user_id, user_text)

    is_admin = user_id in (config.admin_ids or [])
    hint = (
        "💡 <i>Для непрерывного диалога выберите раздел <b>'🤖 AI Консультант Метролог'</b>.</i>" if lang == "ru"
        else "💡 <i>AI bilan doimiy muloqot qilish uchun <b>'🤖 AI Metrolog Maslahatchi'</b> bo'limini tanlang.</i>"
    )

    await message.answer(
        f"{response}\n\n{hint}",
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang),
        parse_mode="HTML"
    )
