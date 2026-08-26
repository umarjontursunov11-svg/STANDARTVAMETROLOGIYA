"""
Savatcha (Shopping Cart) va Savatcha buyurtmalarini boshqarish handleri.
O'zbek va Rus tillarini to'liq qo'llab-quvvatlaydi.
Savatcha buyurtmalari admin shaxsiy chatiga hamda buyurtmalar guruhiga yuboriladi.
"""

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database import (
    get_cart,
    get_cart_item,
    add_to_cart,
    update_cart_quantity,
    remove_from_cart,
    clear_cart,
    create_order_from_cart,
    get_product_by_id,
    get_user_language
)
from bot.states import CartOrderState
from bot.keyboards import (
    main_menu_keyboard,
    contact_keyboard,
    cancel_keyboard,
    cart_view_keyboard,
    empty_cart_keyboard,
    product_detail_keyboard
)
from bot.utils import (
    format_cart_view,
    format_cart_order_user_receipt,
    format_cart_order_admin_notification
)
from bot.utils.localization import get_text
from bot.config import config

logger = logging.getLogger(__name__)
router = Router()


# ==========================================
# SAVATCHANI KO'RISH HANDLERLARI
# ==========================================

@router.message(Command("cart"))
@router.message(F.text.in_(["🛒 Savatcha", "🛒 Корзина"]))
async def show_cart_message_handler(message: Message, state: FSMContext):
    """Savatchani xabar orqali ochish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    cart_items = await get_cart(user_id)

    if not cart_items:
        text = get_text("cart_empty", lang=lang)
        await message.answer(text, reply_markup=empty_cart_keyboard(lang=lang), parse_mode="HTML")
        return

    text = format_cart_view(cart_items, lang=lang)
    await message.answer(text, reply_markup=cart_view_keyboard(cart_items, lang=lang), parse_mode="HTML")


@router.callback_query(F.data == "view_cart")
async def show_cart_callback_handler(callback: CallbackQuery, state: FSMContext):
    """Savatchani inline tugma orqali ochish."""
    await state.clear()
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    cart_items = await get_cart(user_id)

    if not cart_items:
        text = get_text("cart_empty", lang=lang)
        await callback.message.edit_text(text, reply_markup=empty_cart_keyboard(lang=lang), parse_mode="HTML")
        await callback.answer()
        return

    text = format_cart_view(cart_items, lang=lang)
    await callback.message.edit_text(text, reply_markup=cart_view_keyboard(cart_items, lang=lang), parse_mode="HTML")
    await callback.answer()


# ==========================================
# SAVATCHAGA QO'SHISH VA MIQDORNI O'ZGARTIRISH
# ==========================================

@router.callback_query(F.data.startswith("add_cart_"))
async def add_to_cart_callback(callback: CallbackQuery):
    """Mahsulotni savatchaga qo'shish."""
    parts = callback.data.split("_")
    product_id = int(parts[2])
    category_id = int(parts[3]) if len(parts) > 3 else 0
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    product = await get_product_by_id(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi." if lang == "uz" else "Товар не найден.", show_alert=True)
        return

    new_qty = await add_to_cart(user_id=user_id, product_id=product_id, quantity=1)
    await callback.answer(get_text("cart_added_alert", lang=lang, qty=new_qty), show_alert=False)

    # Mahsulot kartochkasi ostidagi tugmani yangilash
    markup = product_detail_keyboard(
        product_id=product_id,
        category_id=category_id,
        is_service=bool(product.get("is_service", 0)),
        in_cart_qty=new_qty,
        lang=lang
    )
    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except Exception:
        pass


@router.callback_query(F.data.startswith("cart_inc_"))
async def cart_inc_callback(callback: CallbackQuery):
    """Savatchadagi mahsulot sonini 1 taga oshirish."""
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    await update_cart_quantity(user_id=user_id, product_id=product_id, delta=+1)
    cart_items = await get_cart(user_id)

    if not cart_items:
        text = get_text("cart_empty", lang=lang)
        await callback.message.edit_text(text, reply_markup=empty_cart_keyboard(lang=lang), parse_mode="HTML")
    else:
        text = format_cart_view(cart_items, lang=lang)
        await callback.message.edit_text(text, reply_markup=cart_view_keyboard(cart_items, lang=lang), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("cart_dec_"))
async def cart_dec_callback(callback: CallbackQuery):
    """Savatchadagi mahsulot sonini 1 taga kamaytirish."""
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    await update_cart_quantity(user_id=user_id, product_id=product_id, delta=-1)
    cart_items = await get_cart(user_id)

    if not cart_items:
        text = get_text("cart_empty", lang=lang)
        await callback.message.edit_text(text, reply_markup=empty_cart_keyboard(lang=lang), parse_mode="HTML")
    else:
        text = format_cart_view(cart_items, lang=lang)
        await callback.message.edit_text(text, reply_markup=cart_view_keyboard(cart_items, lang=lang), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("cart_del_"))
async def cart_del_callback(callback: CallbackQuery):
    """Mahsulotni savatchadan butunlay o'chirish."""
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)

    await remove_from_cart(user_id=user_id, product_id=product_id)
    cart_items = await get_cart(user_id)

    await callback.answer(get_text("cart_deleted_alert", lang=lang), show_alert=False)

    if not cart_items:
        text = get_text("cart_empty", lang=lang)
        await callback.message.edit_text(text, reply_markup=empty_cart_keyboard(lang=lang), parse_mode="HTML")
    else:
        text = format_cart_view(cart_items, lang=lang)
        await callback.message.edit_text(text, reply_markup=cart_view_keyboard(cart_items, lang=lang), parse_mode="HTML")


@router.callback_query(F.data == "clear_cart_all")
async def clear_cart_callback(callback: CallbackQuery):
    """Savatchani to'liq tozalash."""
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    await clear_cart(user_id)
    await callback.answer(get_text("cart_cleared_alert", lang=lang), show_alert=False)

    text = get_text("cart_empty", lang=lang)
    await callback.message.edit_text(text, reply_markup=empty_cart_keyboard(lang=lang), parse_mode="HTML")


# ==========================================
# SAVATCHANI RASMIYLASHTIRISH (CHECKOUT) FLOW
# ==========================================

@router.callback_query(F.data == "checkout_cart")
async def start_cart_checkout(callback: CallbackQuery, state: FSMContext):
    """Savatchadagi mahsulotlarni rasmiylashtirishni boshlash."""
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    cart_items = await get_cart(user_id)

    if not cart_items:
        await callback.answer("Savatchangiz bo'sh!" if lang == "uz" else "Ваша корзина пуста!", show_alert=True)
        return

    await state.set_state(CartOrderState.waiting_for_name)
    user_fullname = callback.from_user.full_name or ""

    if lang == "ru":
        text = (
            "📝 <b>Оформление Заказа</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Пожалуйста, введите ваше Ф.И.О. или наименование организации:\n\n"
            f"<i>(Например: {user_fullname if user_fullname else 'Иванов Иван'} или 'ООО Лаборатория')</i>"
        )
    else:
        text = (
            "📝 <b>Buyurtmani Rasmiylashtirish</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Iltimos, to'liq ism-familiyangizni yoki tashkilotingiz nomini kiriting:\n\n"
            f"<i>(Masalan: {user_fullname if user_fullname else 'Eshmatov Toshmat'} yoki 'Oltin Kon MCHJ')</i>"
        )
    await callback.message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")
    await callback.answer()


@router.message(CartOrderState.waiting_for_name)
async def process_cart_name(message: Message, state: FSMContext):
    """Buyurtmachining ismini qabul qilish."""
    full_name = message.text.strip()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if len(full_name) < 2:
        warn = "⚠️ Пожалуйста, введите имя полностью:" if lang == "ru" else "⚠️ Iltimos, ismingizni to'liqroq kiriting:"
        await message.answer(warn)
        return

    await state.update_data(full_name=full_name)
    await state.set_state(CartOrderState.waiting_for_phone)

    if lang == "ru":
        text = (
            f"Спасибо, <b>{full_name}</b>!\n\n"
            f"📞 Для связи отправьте ваш <b>номер телефона</b>:\n"
            f"<i>(Нажмите кнопку ниже или напишите в формате +998901234567)</i>"
        )
    else:
        text = (
            f"Rahmat, <b>{full_name}</b>!\n\n"
            f"📞 Mutaxassislarimiz bog'lanishi uchun <b>telefon raqamingizni</b> yuboring:\n"
            f"<i>(Quyidagi tugmani bosing yoki raqamingizni +998901234567 formatida yozing)</i>"
        )
    await message.answer(text, reply_markup=contact_keyboard(lang=lang), parse_mode="HTML")


@router.message(CartOrderState.waiting_for_phone, F.contact)
@router.message(CartOrderState.waiting_for_phone, F.text)
async def process_cart_phone(message: Message, state: FSMContext):
    """Telefon raqamni qabul qilish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if message.contact:
        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = f"+{phone}"
    else:
        phone = message.text.strip()
        clean_phone = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
        if len(clean_phone) < 7:
            warn = (
                "⚠️ Некорректный номер телефона. Пожалуйста, проверьте и введите заново:" if lang == "ru"
                else "⚠️ Telefon raqami noto'g'ri kiritildi. Iltimos, qaytadan tekshirib yozing:"
            )
            await message.answer(warn, reply_markup=contact_keyboard(lang=lang))
            return
        phone = clean_phone

    await state.update_data(phone_number=phone)
    await state.set_state(CartOrderState.waiting_for_notes)

    if lang == "ru":
        text = (
            "📝 <b>Дополнительные примечания или реквизиты:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Укажите адрес доставки, реквизиты для договора или особые требования.\n\n"
            "<i>Если примечаний нет, напишите 'Нет' или нажмите кнопку отмены.</i>"
        )
    else:
        text = (
            "📝 <b>Qo'shimcha izoh yoki talablar:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Yetkazib berish manzili, hisob-faktura (shartnoma) rekvizitlari yoki qo'shimcha talablaringiz bo'lsa yozing.\n\n"
            "<i>Agar qo'shimcha izoh bo'lmasa, 'Yo'q' deb yozing yoki pastdagi tugmani bosing.</i>"
        )
    await message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")


@router.message(CartOrderState.waiting_for_notes)
async def process_cart_notes(message: Message, bot: Bot, state: FSMContext):
    """Qo'shimcha izohni qabul qilib buyurtmani yakunlash va adminga hamda guruhga yuborish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    notes = message.text.strip()
    if notes.lower() in ("yo'q", "yoq", "none", "-", "нет", "net", "yo`q", "yo’q"):
        notes = None

    data = await state.get_data()
    full_name = data.get("full_name", message.from_user.full_name)
    phone_number = data.get("phone_number", "")

    # Savatdan buyurtma yaratish
    order_result = await create_order_from_cart(
        user_id=user_id,
        full_name=full_name,
        phone_number=phone_number,
        notes=notes
    )
    await state.clear()

    is_admin = user_id in (config.admin_ids or [])

    if not order_result:
        err = "⚠️ В корзине нет товаров." if lang == "ru" else "⚠️ Savatchangizda mahsulot topilmadi."
        await message.answer(err, reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang))
        return

    # 1. Foydalanuvchiga tasdiq xabari
    user_receipt = format_cart_order_user_receipt(order_result, lang=lang)
    await message.answer(
        user_receipt,
        reply_markup=main_menu_keyboard(is_admin=is_admin, lang=lang),
        parse_mode="HTML"
    )

    # 2. Adminlarga va Guruhga bildirishnoma yuborish
    admin_text = format_cart_order_admin_notification(order_result)
    recipients = set(config.admin_ids)
    if config.orders_channel_id:
        recipients.add(config.orders_channel_id)

    for chat_id in recipients:
        try:
            await bot.send_message(chat_id, admin_text, parse_mode="HTML")
            logger.info(f"Savatcha buyurtmasi #{order_result.get('order_id')} qabul qiluvchi #{chat_id} ga yuborildi.")
        except Exception as e:
            logger.error(f"Savatcha xabarini yuborishda xatolik #{chat_id}: {e}")
            try:
                await bot.send_message(
                    chat_id,
                    f"Yangi savatcha buyurtmasi #{order_result.get('order_id')}:\nMijoz: {full_name}\nTel: {phone_number}\nTarkibi:\n{order_result.get('items_summary')}\nIzoh: {notes or 'Mavjud emas'}"
                )
            except Exception as e2:
                logger.error(f"Savatcha fallback xabari ham bormadi #{chat_id}: {e2}")
