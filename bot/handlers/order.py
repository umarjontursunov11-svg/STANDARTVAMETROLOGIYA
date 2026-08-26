"""
Buyurtma berish, ariza va mutaxassis maslahati olish jarayoni (FSM) handleri.
O'zbek va Rus tillarini to'liq qo'llab-quvvatlaydi.
Arizalar admin shaxsiy chatiga hamda buyurtmalar guruhiga yuboriladi.
"""

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database import get_product_by_id, create_order, get_user_language
from bot.states import OrderState
from bot.keyboards import (
    contact_keyboard,
    cancel_keyboard,
    main_menu_keyboard
)
from bot.utils import (
    format_order_admin_notification,
    format_order_user_receipt
)
from bot.config import config

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text.in_(["📝 Ariza / Maslahat olish", "📝 Заявка / Консультация"]))
async def start_general_order_message(message: Message, state: FSMContext):
    """Umumiy ariza yoki maslahat so'rashni boshlash."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.clear()
    await state.set_state(OrderState.waiting_for_name)

    item_name = "Консультация по метрологии / продукции" if lang == "ru" else "Umumiy metrologik xizmat / Mahsulot maslahati"
    item_type = "Консультация" if lang == "ru" else "Maslahat"

    await state.update_data(
        item_id=0,
        item_name=item_name,
        item_type=item_type
    )

    if lang == "ru":
        text = (
            "📝 <b>Подача Заявки / Консультация</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Пожалуйста, введите ваше полное имя (Ф.И.О.) или наименование предприятия:"
        )
    else:
        text = (
            "📝 <b>Ariza va Maslahat olish</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Iltimos, to'liq ism-familiyangizni (yoki tashkilotingiz nomini) kiriting:"
        )
    await message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")


@router.callback_query(F.data.startswith("order_"))
async def start_product_order_callback(callback: CallbackQuery, state: FSMContext):
    """Aniq bir mahsulot yoki xizmat uchun buyurtma/ariza berish."""
    parts = callback.data.split("_")
    product_id = int(parts[1])
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    product = await get_product_by_id(product_id)
    item_name = product["name"] if product else ("Неизвестный товар" if lang == "ru" else "Noma'lum mahsulot")
    item_type = ("Услуга" if lang == "ru" else "Xizmat") if product and product.get("is_service") else ("Товар" if lang == "ru" else "Mahsulot")

    await state.clear()
    await state.set_state(OrderState.waiting_for_name)
    await state.update_data(
        item_id=product_id,
        item_name=item_name,
        item_type=item_type
    )

    if lang == "ru":
        text = (
            f"📝 <b>Выбрано:</b> \"{item_name}\"\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Для оформления заявки введите ваше Ф.И.О. или название организации:"
        )
    else:
        text = (
            f"📝 <b>Tanlangan:</b> \"{item_name}\"\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Buyurtmani rasmiylashtirish uchun to'liq ism-familiyangizni (yoki korxona nomini) kiriting:"
        )
    await callback.message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")
    await callback.answer()


@router.message(OrderState.waiting_for_name)
async def process_order_name(message: Message, state: FSMContext):
    """Ismni qabul qilish va telefon raqamini so'rash."""
    name = message.text.strip()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if len(name) < 2:
        warn = "⚠️ Пожалуйста, введите имя полностью:" if lang == "ru" else "⚠️ Iltimos, ismingizni to'liqroq kiriting:"
        await message.answer(warn, reply_markup=cancel_keyboard(lang=lang))
        return

    await state.update_data(full_name=name)
    await state.set_state(OrderState.waiting_for_phone)

    if lang == "ru":
        text = (
            f"Спасибо, <b>{name}</b>!\n\n"
            f"📱 Теперь отправьте ваш <b>номер телефона</b> для обратной связи.\n"
            f"Нажмите кнопку <b>'📱 Отправить номер телефона'</b> или напишите номер вручную:"
        )
    else:
        text = (
            f"Rahmat, <b>{name}</b>!\n\n"
            f"📱 Endi siz bilan bog'lanishimiz uchun telefon raqamingizni yuboring.\n"
            f"Quyidagi <b>'📱 Telefon raqamni yuborish'</b> tugmasini bosishingiz yoki raqamingizni yozib yuborishingiz mumkin:"
        )
    await message.answer(text, reply_markup=contact_keyboard(lang=lang), parse_mode="HTML")


@router.message(OrderState.waiting_for_phone, F.contact)
@router.message(OrderState.waiting_for_phone, F.text)
async def process_order_phone(message: Message, state: FSMContext):
    """Telefon raqamni qabul qilish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if message.contact:
        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = f"+{phone}"
    else:
        phone = message.text.strip()
        digits = [c for c in phone if c.isdigit() or c == "+"]
        clean_phone = "".join(digits)
        if len(clean_phone) < 7:
            warn = (
                "⚠️ Пожалуйста, введите корректный номер телефона (например: +998901234567):" if lang == "ru"
                else "⚠️ Iltimos, to'g'ri telefon raqam kiriting (masalan: +998901234567):"
            )
            await message.answer(warn, reply_markup=contact_keyboard(lang=lang))
            return
        phone = clean_phone

    await state.update_data(phone_number=phone)
    await state.set_state(OrderState.waiting_for_notes)

    if lang == "ru":
        text = (
            f"📱 Номер телефона принят: <b>{phone}</b>\n\n"
            f"📝 Есть ли у вас дополнительные требования или примечания? (Если нет, напишите <b>'Нет'</b>):"
        )
    else:
        text = (
            f"📱 Telefon raqamingiz qabul qilindi: <b>{phone}</b>\n\n"
            f"📝 Qo'shimcha talab yoki izohingiz bormi? (Bo'lsa yozing, bo'lmasa <b>'Yo'q'</b> deb yuboring):"
        )
    await message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")


@router.message(OrderState.waiting_for_notes)
async def process_order_notes_and_finish(message: Message, state: FSMContext, bot: Bot):
    """Izohni qabul qilib arizani saqlash va adminga hamda guruhga yuborish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    notes = message.text.strip()
    if notes.lower() in ["yo'q", "yoq", "yo`q", "yo’q", "no", "none", "-", "йўқ", "нет", "net"]:
        notes = "Qo'shimcha izoh yo'q" if lang == "uz" else "Без дополнительных примечаний"

    data = await state.get_data()
    full_name = data.get("full_name", message.from_user.full_name)
    phone_number = data.get("phone_number", "")
    item_name = data.get("item_name", "Umumiy ariza")
    item_type = data.get("item_type", "Ariza")

    # Bazaga yozish
    order_id = await create_order(
        user_id=user_id,
        full_name=full_name,
        phone_number=phone_number,
        item_name=item_name,
        item_type=item_type,
        notes=notes
    )

    await state.clear()
    is_admin = user_id in (config.admin_ids or [])

    # Foydalanuvchiga tasdiq xabari
    receipt_text = format_order_user_receipt(
        order_id=order_id,
        full_name=full_name,
        phone_number=phone_number,
        item_name=item_name,
        lang=lang
    )
    await message.answer(
        receipt_text,
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang),
        parse_mode="HTML"
    )

    # Adminlarga va Guruhga xabar yuborish
    admin_order_data = {
        "id": order_id,
        "full_name": full_name,
        "phone_number": phone_number,
        "item_name": item_name,
        "notes": notes,
        "created_at": "Hozirgina"
    }
    admin_text = format_order_admin_notification(admin_order_data)

    recipients = set(config.admin_ids)
    if config.orders_channel_id:
        recipients.add(config.orders_channel_id)

    for chat_id in recipients:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=admin_text,
                parse_mode="HTML"
            )
            logger.info(f"Yangi ariza #{order_id} qabul qiluvchi #{chat_id} ga yuborildi.")
        except Exception as e:
            logger.error(f"Xabar yuborishda xatolik #{chat_id}: {e}")
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"Yangi ariza #{order_id}:\nMijoz: {full_name}\nTel: {phone_number}\nMavzu: {item_name}\nIzoh: {notes}"
                )
            except Exception as e2:
                logger.error(f"Fallback xabari ham bormadi #{chat_id}: {e2}")
