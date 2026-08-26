"""
ReplyKeyboardMarkup (Oddiy klaviatura tugmalari) moduli.
Ko'p tillik (O'zbekcha / Ruscha) formatda.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.utils.localization import get_text


def main_menu_keyboard(is_admin: bool = False, lang: str = "uz") -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari (O'zbekcha / Ruscha)."""
    keyboard = [
        [
            KeyboardButton(text=get_text("btn_search", lang)),
            KeyboardButton(text=get_text("btn_catalog", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_cart", lang)),
            KeyboardButton(text=get_text("btn_ai", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_services", lang)),
            KeyboardButton(text=get_text("btn_company", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_order", lang)),
            KeyboardButton(text=get_text("btn_contact", lang))
        ],
        [
            KeyboardButton(text=get_text("btn_lang", lang))
        ]
    ]

    if is_admin:
        keyboard.append([KeyboardButton(text=get_text("btn_admin_panel", lang))])

    placeholder = (
        "Выберите нужный раздел..." if lang == "ru"
        else "Quyidagi bo'limlardan birini tanlang..."
    )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        persistent=True,
        input_field_placeholder=placeholder
    )


def ai_chat_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """AI Metrolog bilan muloqot klaviaturasi."""
    placeholder = (
        "Задайте вопрос AI Метрологу..." if lang == "ru"
        else "AI ga savolingizni yozing..."
    )
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("btn_clear_history", lang))],
            [KeyboardButton(text=get_text("btn_back_main", lang))]
        ],
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )


def contact_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Telefon raqamni yuborish tugmasi."""
    placeholder = (
        "Нажмите кнопку или введите номер..." if lang == "ru"
        else "Tugmani bosing yoki raqamingizni yozing..."
    )
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("btn_send_contact", lang), request_contact=True)],
            [KeyboardButton(text=get_text("btn_cancel", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=placeholder
    )


def cancel_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi."""
    placeholder = (
        "Нажмите для отмены..." if lang == "ru"
        else "Bekor qilish uchun tugmani bosing..."
    )
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("btn_cancel", lang))]
        ],
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )


def admin_menu_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Admin boshqaruv menyusi."""
    if lang == "ru":
        keyboard = [
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="📋 Последние заявки")
            ],
            [
                KeyboardButton(text="➕ Добавить продукцию"),
                KeyboardButton(text="📢 Рассылка")
            ],
            [
                KeyboardButton(text="⬅ Главное меню")
            ]
        ]
    else:
        keyboard = [
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="📋 Oxirgi arizalar")
            ],
            [
                KeyboardButton(text="➕ Mahsulot qo'shish"),
                KeyboardButton(text="📢 Xabar yuborish")
            ],
            [
                KeyboardButton(text="⬅ Asosiy menyuga qaytish")
            ]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Admin amallaridan birini tanlang..."
    )
