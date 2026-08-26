"""
Admin boshqaruv paneli handleri (Faqat adminlar uchun).
O'zbek va Rus tillarini qo'llab-quvvatlaydi.
"""

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.config import config
from bot.database import (
    get_stats,
    get_recent_orders,
    get_categories,
    add_product,
    get_db,
    get_user_language
)
from bot.states import AdminState
from bot.keyboards import (
    admin_menu_keyboard,
    main_menu_keyboard,
    cancel_keyboard,
    categories_keyboard
)

router = Router()


def is_admin_user(user_id: int) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish."""
    return user_id in (config.admin_ids or [])


@router.message(Command("admin"))
@router.message(F.text.in_(["⚙ Admin Paneli", "⚙ Панель администратора"]))
async def admin_panel_handler(message: Message, state: FSMContext):
    """Admin boshqaruv panelini ochish."""
    await state.clear()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if not is_admin_user(user_id):
        err = "⚠️ У вас нет прав администратора." if lang == "ru" else "⚠️ Kechirasiz, sizda admin huquqi mavjud emas."
        await message.answer(err)
        return

    text = (
        "⚙️ <b>Панель управления Стандарт и Метрология</b>\n━━━━━━━━━━━━━━━━━━━━\nВыберите раздел:" if lang == "ru"
        else "⚙️ <b>Standart va Metrologiya Admin Paneli</b>\n━━━━━━━━━━━━━━━━━━━━\nBoshqaruv bo'limlaridan birini tanlang:"
    )
    await message.answer(text, reply_markup=admin_menu_keyboard(lang=lang), parse_mode="HTML")


@router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
async def admin_stats_handler(message: Message):
    """Bot statistikasini chiqarish."""
    if not is_admin_user(message.from_user.id):
        return

    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    stats = await get_stats()

    if lang == "ru":
        text = (
            "📊 <b>Статистика Бота</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 <b>Пользователей:</b> {stats['users']} чел.\n"
            f"📦 <b>Продукции и услуг:</b> {stats['products']} поз.\n"
            f"📋 <b>Всего заявок/заказов:</b> {stats['orders']} шт.\n"
            f"🔍 <b>Выполнено поисков:</b> {stats['searches']} раз\n"
        )
    else:
        text = (
            "📊 <b>Bot Statistikasi</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 <b>Foydalanuvchilar soni:</b> {stats['users']} ta\n"
            f"📦 <b>Mahsulot va xizmatlar:</b> {stats['products']} ta\n"
            f"📋 <b>Jami tushgan arizalar:</b> {stats['orders']} ta\n"
            f"🔍 <b>Amalga oshirilgan qidiruvlar:</b> {stats['searches']} ta\n"
        )
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["📋 Oxirgi arizalar", "📋 Последние заявки"]))
async def admin_orders_handler(message: Message):
    """Oxirgi kelib tushgan arizalar ro'yxati."""
    if not is_admin_user(message.from_user.id):
        return

    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    orders = await get_recent_orders(limit=10)

    if not orders:
        empty = "Заявок пока нет." if lang == "ru" else "Hozircha hech qanday arizalar tushmagan."
        await message.answer(empty)
        return

    hdr = "📋 <b>Последние 10 заявок:</b>\n━━━━━━━━━━━━━━━━━━━━\n\n" if lang == "ru" else "📋 <b>Oxirgi kelib tushgan 10 ta ariza:</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    text = hdr
    for o in orders:
        text += (
            f"🆔 <b>#{o['id']}</b> | 👤 <b>{o['full_name']}</b>\n"
            f"📞 Tel: <code>{o['phone_number']}</code>\n"
            f"📦 Позиция: <i>{o.get('item_name', '-')}</i>\n"
            f"📝 Примечание: {o.get('notes', '-')}\n"
            f"⏰ Дата: {o.get('created_at', '-')}\n"
            f"────────────────────\n"
        )

    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["➕ Mahsulot qo'shish", "➕ Добавить продукцию"]))
async def admin_add_product_start(message: Message, state: FSMContext):
    """Yangi mahsulot kiritishni boshlash."""
    if not is_admin_user(message.from_user.id):
        return

    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    categories = await get_categories()
    if not categories:
        await message.answer("Bazada kategoriyalar topilmadi.")
        return

    cat_list_text = "\n".join([f"<b>{c['id']}</b> - {c['name']}" for c in categories])
    await state.set_state(AdminState.waiting_for_product_category)
    
    text = (
        f"➕ <b>Добавление продукции</b>\n━━━━━━━━━━━━━━━━━━━━\nВведите ID категории:\n\n{cat_list_text}" if lang == "ru"
        else f"➕ <b>Yangi mahsulot qo'shish</b>\n━━━━━━━━━━━━━━━━━━━━\nKategoriya ID raqamini tanlang va yozing:\n\n{cat_list_text}"
    )
    await message.answer(text, reply_markup=cancel_keyboard(lang=lang), parse_mode="HTML")


@router.message(AdminState.waiting_for_product_category)
async def admin_product_category_input(message: Message, state: FSMContext):
    """Kategoriya ID sini olish."""
    text = message.text.strip()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if not text.isdigit():
        warn = "⚠️ Введите числовой номер категории:" if lang == "ru" else "⚠️ Iltimos, faqat kategoriya raqamini kiriting:"
        await message.answer(warn)
        return

    await state.update_data(category_id=int(text))
    await state.set_state(AdminState.waiting_for_product_name)
    prompt = "Введите наименование продукции:" if lang == "ru" else "Mahsulot nomini kiriting:"
    await message.answer(prompt, parse_mode="HTML")


@router.message(AdminState.waiting_for_product_name)
async def admin_product_name_input(message: Message, state: FSMContext):
    """Mahsulot nomini qabul qilish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.update_data(name=message.text.strip())
    await state.set_state(AdminState.waiting_for_product_code)
    prompt = "Введите код или норматив (например: ГОСТ 2405-88 или ГСО 7874):" if lang == "ru" else "Mahsulot kodi yoki standartini kiriting:"
    await message.answer(prompt, parse_mode="HTML")


@router.message(AdminState.waiting_for_product_code)
async def admin_product_code_input(message: Message, state: FSMContext):
    """Mahsulot kodi/standartini qabul qilish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.update_data(code=message.text.strip())
    await state.set_state(AdminState.waiting_for_product_price)
    prompt = "Введите цену (например: 250 000 сум или По запросу):" if lang == "ru" else "Mahsulot narxini kiriting:"
    await message.answer(prompt, parse_mode="HTML")


@router.message(AdminState.waiting_for_product_price)
async def admin_product_price_input(message: Message, state: FSMContext):
    """Mahsulot narxini qabul qilish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.update_data(price=message.text.strip())
    await state.set_state(AdminState.waiting_for_product_desc)
    prompt = "Введите описание продукции:" if lang == "ru" else "Mahsulot tavsifi va xususiyatlarini kiriting:"
    await message.answer(prompt, parse_mode="HTML")


@router.message(AdminState.waiting_for_product_desc)
async def admin_product_desc_input(message: Message, state: FSMContext):
    """Tavsifni qabul qilib bazaga saqlash."""
    desc = message.text.strip()
    data = await state.get_data()
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    await add_product(
        category_id=data["category_id"],
        name=data["name"],
        code=data["code"],
        standard=data["code"],
        accuracy_class="Standart",
        measurement_range="По паспорту / Texnik pasport bo'yicha",
        price=data["price"],
        description=desc,
        is_service=0
    )

    await state.clear()
    success = (
        f"✅ <b>'{data['name']}'</b> успешно сохранена в каталоге!" if lang == "ru"
        else f"✅ <b>'{data['name']}'</b> muvaffaqiyatli saqlandi va katalogga qo'shildi!"
    )
    await message.answer(
        success,
        reply_markup=admin_menu_keyboard(lang=lang),
        parse_mode="HTML"
    )


@router.message(F.text.in_(["📢 Xabar yuborish", "📢 Рассылка"]))
async def admin_broadcast_start(message: Message, state: FSMContext):
    """Barcha foydalanuvchilarga xabar yuborishni boshlash."""
    if not is_admin_user(message.from_user.id):
        return

    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.set_state(AdminState.waiting_for_broadcast)
    prompt = "📢 Введите текст сообщения для всех пользователей:" if lang == "ru" else "📢 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringiz matnini kiriting:"
    await message.answer(
        prompt,
        reply_markup=cancel_keyboard(lang=lang)
    )


@router.message(AdminState.waiting_for_broadcast)
async def admin_broadcast_process(message: Message, state: FSMContext, bot: Bot):
    """Xabarni barcha ro'yxatdan o'tgan foydalanuvchilarga tarqatish."""
    broadcast_text = message.text
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await state.clear()

    db = await get_db()
    try:
        cursor = await db.execute("SELECT user_id FROM users")
        users = await cursor.fetchall()
    finally:
        await db.close()

    sent_count = 0
    fail_count = 0

    await message.answer(f"⏳ Отправка {len(users)} пользователям..." if lang == "ru" else f"⏳ Xabar {len(users)} ta foydalanuvchiga yuborilmoqda...")

    for row in users:
        u_id = row[0]
        try:
            await bot.send_message(
                chat_id=u_id,
                text=f"📢 <b>Информация / Yangilik:</b>\n\n{broadcast_text}",
                parse_mode="HTML"
            )
            sent_count += 1
        except Exception:
            fail_count += 1

    done = (
        f"✅ Рассылка завершена!\n\n• Доставлено: {sent_count}\n• Не доставлено: {fail_count}" if lang == "ru"
        else f"✅ Xabar yuborish yakunlandi!\n\n• Muvaffaqiyatli: {sent_count} ta\n• Yuborilmadi: {fail_count} ta"
    )
    await message.answer(
        done,
        reply_markup=admin_menu_keyboard(lang=lang)
    )
