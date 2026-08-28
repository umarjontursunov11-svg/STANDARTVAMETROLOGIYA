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

    name = comp.name if comp.name and "STANDART VA METROLOGIYA" in comp.name else 'OOO "STANDART VA METROLOGIYA"'
    phones = comp.phone if comp.phone and "939-71-83" in comp.phone else '+998 90 939-71-83, +998 98 361-71-83, +998 55 503-47-15'
    email = comp.email if comp.email and "standartvametrologiya" in comp.email else 'standartvametrologiya@gmail.com'
    tg_support = comp.telegram_support if comp.telegram_support and "standartgso" in comp.telegram_support else '@standartgso_admin1'

    if lang == "ru":
        addr_ru = "г. Ташкент, Сергелийский р-н, ул. Узумзор, 16-тупик, дом 18"
        work_ru = "Понедельник - Пятница: 09:00 - 18:00"
        contact_text = (
            f"📞 <b>Контакты и Адрес:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏢 <b>Организация:</b> {name}\n"
            f"📍 <b>Адрес:</b> {addr_ru}\n"
            f"📞 <b>Телефоны:</b> {phones}\n"
            f"✉️ <b>Email:</b> {email}\n"
            f"🕒 <b>Режим работы:</b> {work_ru}\n"
            f"💬 <b>Telegram оператор:</b> {tg_support}\n"
        )
    else:
        addr_uz = "Toshkent sh., Sergeli t., Uzumzor ko'chasi, 16-tupik, 18-xonadon"
        work_uz = "Dushanba - Juma: 09:00 - 18:00"
        contact_text = (
            f"📞 <b>Bog'lanish va Manzil:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏢 <b>Tashkilot:</b> {name}\n"
            f"📍 <b>Manzil:</b> {addr_uz}\n"
            f"📞 <b>Ishonch telefoni:</b> {phones}\n"
            f"✉️ <b>Elektron pochta:</b> {email}\n"
            f"🕒 <b>Ish vaqti:</b> {work_uz}\n"
            f"💬 <b>Telegram operator:</b> {tg_support}\n"
        )

    await message.answer(
        contact_text,
        reply_markup=company_links_keyboard(lang=lang),
        parse_mode="HTML"
    )
