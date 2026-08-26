"""
Kompaniya haqida, xizmatlar, kontaktlar va manzil bo'limlari handleri.
O'zbek va Rus tillarini to'liq qo'llab-quvvatlaydi.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.config import config
from bot.database import get_user_language
from bot.keyboards import company_links_keyboard
from bot.utils import format_company_info, format_services_info

router = Router()


@router.message(F.text.in_(["🏢 Kompaniya haqida", "🏢 О компании"]))
async def company_info_handler(message: Message, state: FSMContext):
    """Kompaniya haqida to'liq ma'lumot berish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    text = format_company_info(lang=lang)
    await message.answer(
        text,
        reply_markup=company_links_keyboard(lang=lang),
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@router.message(F.text.in_(["🔬 Metrologik xizmatlar", "🔬 Метрологические услуги"]))
async def services_info_handler(message: Message, state: FSMContext):
    """Metrologik xizmatlar haqida ma'lumot berish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    text = format_services_info(lang=lang)
    await message.answer(
        text,
        reply_markup=company_links_keyboard(lang=lang),
        parse_mode="HTML"
    )


@router.message(F.text.in_(["📞 Bog'lanish va Manzil", "📞 Контакты и Адрес"]))
async def contact_info_handler(message: Message, state: FSMContext):
    """Aloqa va manzil ma'lumotlarini taqdim etish hamda xaritada joylashuvni yuborish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    comp = config.company

    if lang == "ru":
        contact_text = (
            f"📞 <b>Контакты и Адрес:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏢 <b>Организация:</b> {comp.name}\n"
            f"📍 <b>Адрес:</b> {comp.address}\n"
            f"📞 <b>Телефоны:</b> {comp.phone}\n"
            f"✉️ <b>Email:</b> {comp.email}\n"
            f"🕒 <b>Режим работы:</b> {comp.work_hours}\n"
            f"💬 <b>Telegram оператор:</b> {comp.telegram_support}\n"
        )
    else:
        contact_text = (
            f"📞 <b>Bog'lanish va Manzil:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏢 <b>Tashkilot:</b> {comp.name}\n"
            f"📍 <b>Manzil:</b> {comp.address}\n"
            f"📞 <b>Ishonch telefoni:</b> {comp.phone}\n"
            f"✉️ <b>Elektron pochta:</b> {comp.email}\n"
            f"🕒 <b>Ish vaqti:</b> {comp.work_hours}\n"
            f"💬 <b>Telegram operator:</b> {comp.telegram_support}\n"
        )

    await message.answer(contact_text, parse_mode="HTML")
    
    # Lokatsiya yuborish
    try:
        await message.answer_location(
            latitude=comp.latitude,
            longitude=comp.longitude
        )
    except Exception:
        pass


@router.callback_query(F.data == "send_company_geo")
async def send_company_geo_callback(callback: CallbackQuery):
    """Inline tugma orqali lokatsiya yuborish."""
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    comp = config.company
    await callback.answer("Lokatsiya yuborilmoqda..." if lang == "uz" else "Отправка локации...")
    try:
        await callback.message.answer_location(
            latitude=comp.latitude,
            longitude=comp.longitude
        )
    except Exception:
        await callback.message.answer(
            f"📍 Manzil / Адрес: {comp.address}"
        )
