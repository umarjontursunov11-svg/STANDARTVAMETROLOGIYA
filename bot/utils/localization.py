"""
Ko'p tillik (O'zbekcha 🇺🇿 / Русский 🇷🇺) lokalizatsiya moduli.
Barcha matnlar, xabarlar va tugmalar tarjimalari.
"""

from typing import Dict, Any, List
from bot.config import config

TEXTS = {
    # ----------------------------------------------------
    # UMUMIY VA ASOSIY MENYU TUGMALARI
    # ----------------------------------------------------
    "btn_search": {
        "uz": "🔍 Mahsulot qidirish",
        "ru": "🔍 Поиск продукции"
    },
    "btn_catalog": {
        "uz": "📦 Mahsulotlar katalogi",
        "ru": "📦 Каталог продукции"
    },
    "btn_cart": {
        "uz": "🛒 Savatcha",
        "ru": "🛒 Корзина"
    },
    "btn_ai": {
        "uz": "🤖 AI Metrolog Maslahatchi",
        "ru": "🤖 AI Консультант Метролог"
    },
    "btn_services": {
        "uz": "🔬 Metrologik xizmatlar",
        "ru": "🔬 Метрологические услуги"
    },
    "btn_company": {
        "uz": "🏢 Kompaniya haqida",
        "ru": "🏢 О компании"
    },
    "btn_order": {
        "uz": "📝 Ariza / Maslahat olish",
        "ru": "📝 Заявка / Консультация"
    },
    "btn_contact": {
        "uz": "📞 Bog'lanish va Manzil",
        "ru": "📞 Контакты и Адрес"
    },
    "btn_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык"
    },
    "btn_back_main": {
        "uz": "⬅ Asosiy menyuga qaytish",
        "ru": "⬅ Главное меню"
    },
    "btn_cancel": {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена"
    },
    "btn_send_contact": {
        "uz": "📱 Telefon raqamni yuborish",
        "ru": "📱 Отправить номер телефона"
    },
    "btn_clear_history": {
        "uz": "🧹 Muloqotni tozalash",
        "ru": "🧹 Очистить историю"
    },
    "btn_admin_panel": {
        "uz": "⚙ Admin Paneli",
        "ru": "⚙ Панель администратора"
    },

    # ----------------------------------------------------
    # START VA YORDAM MATNLARI
    # ----------------------------------------------------
    "choose_language": {
        "uz": "🇺🇿 <b>Iltimos, o'zingizga qulay tilni tanlang:</b>\n🇷🇺 <b>Пожалуйста, выберите удобный для вас язык:</b>",
        "ru": "🇷🇺 <b>Пожалуйста, выберите язык обслуживания:</b>\n🇺🇿 <b>Iltimos, xizmat ko'rsatish tilini tanlang:</b>"
    },
    "language_changed": {
        "uz": "✅ <b>Til muvaffaqiyatli o'zgartirildi:</b> O'zbekcha 🇺🇿",
        "ru": "✅ <b>Язык успешно изменен на:</b> Русский 🇷🇺"
    },
    "welcome": {
        "uz": (
            "Assalomu alaykum, <b>{full_name}</b>!\n\n"
            "🏢 <b>{company_name}</b> rasmiy Telegram botiga xush kelibsiz!\n\n"
            "Bizning bot orqali siz:\n"
            "🛒 <b>Savatcha</b> — Standart namunalar va asboblarni yig'ib umumiy buyurtma berishingiz\n"
            "🤖 <b>AI Metrolog Maslahatchi</b> — Metrologiya, standartlar va reaktivlar bo'yicha 24/7 aqlli maslahat olishingiz\n"
            "🧪 <b>Standart namunalar (GSO)</b>, <b>bufer eritmalari</b>, <b>fiksanallar</b> va <b>kimyoviy reaktivlar</b> katalogi bilan tanishishingiz\n"
            "⚙️ O'lchash vositalari va davlat standartlarini (ISO 17034, GOST, O'z DSt) qidirishingiz\n"
            "📋 Qiyoslash (poverka), kalibrlash va mahsulot buyurtmasi uchun onlayn ariza qoldirishingiz mumkin.\n\n"
            "<i>Quyidagi menyudan kerakli bo'limni tanlang:</i>"
        ),
        "ru": (
            "Здравствуйте, <b>{full_name}</b>!\n\n"
            "🏢 Добро пожаловать в официальный Telegram-бот компании <b>{company_name}</b>!\n\n"
            "С помощью нашего бота вы можете:\n"
            "🛒 <b>Корзина</b> — Добавлять образцы и приборы для оформления единого заказа\n"
            "🤖 <b>AI Консультант Метролог</b> — Получать круглосуточные экспертные консультации по ГОСТ, ГСО и метрологии\n"
            "🧪 <b>Каталог ГСО</b>, <b>буферных растворов</b>, <b>стандарт-титров (фиксаналов)</b> и <b>химреактивов</b>\n"
            "⚙️ Находить средства измерений и нормативные стандарты (ISO 17034, ГОСТ, O'z DSt)\n"
            "📋 Оставлять онлайн-заявки на поверку, калибровку, аттестацию и поставку продукции.\n\n"
            "<i>Выберите нужный раздел из меню ниже:</i>"
        )
    },
    "help": {
        "uz": (
            "ℹ️ <b>Botdan foydalanish bo'yicha qo'llanma:</b>\n\n"
            "🛒 <b>Savatcha</b> (/cart) — Yig'ilgan mahsulotlarni ko'rish, miqdorini tahrirlash (➕/➖) va umumiy buyurtma berish.\n\n"
            "🤖 <b>AI Metrolog Maslahatchi</b> (/ai) — Metrologiya, standartlar, GSO va tahlil usullari bo'yicha sun'iy intellekt maslahatchisi.\n\n"
            "🔍 <b>Mahsulot qidirish</b> (/search) — Standart namunalar, reaktivlar, titrlar yoki o'lchash vositalari nomini yozib qidiring (masalan: <code>GSO 7874</code>, <code>pH bufer</code>, <code>fiksanal</code>, <code>manometr</code>).\n\n"
            "📦 <b>Mahsulotlar katalogi</b> (/catalog) — Standart namunalar, bufer eritmalar, kimyoviy reaktivlar va o'lchash vositalarining to'liq katalogi.\n\n"
            "🔬 <b>Metrologik xizmatlar</b> — Ko'rsatiladigan metrologik xizmatlar (poverka, kalibrlash, attestatsiya) haqida ma'lumot.\n\n"
            "📝 <b>Ariza / Maslahat olish</b> — Mahsulot xarid qilish yoki xizmatlarga ariza qoldirish.\n\n"
            "🌐 <b>Tilni o'zgartirish</b> (/lang) — O'zbekcha va Ruscha interfeys.\n\n"
            "<i>Savollaringiz bo'lsa, {support} ga murojaat qilishingiz mumkin.</i>"
        ),
        "ru": (
            "ℹ️ <b>Руководство по использованию бота:</b>\n\n"
            "🛒 <b>Корзина</b> (/cart) — Просмотр добавленных товаров, изменение количества (➕/➖) и оформление заказа.\n\n"
            "🤖 <b>AI Консультант Метролог</b> (/ai) — Круглосуточный интеллектуальный помощник по метрологии, стандартам ГСО и оборудованию.\n\n"
            "🔍 <b>Поиск продукции</b> (/search) — Поиск по названию, коду ГСО, формуле или типу прибора (например: <code>ГСО 7874</code>, <code>буфер рН</code>, <code>фиксанал</code>, <code>манометр</code>).\n\n"
            "📦 <b>Каталог продукции</b> (/catalog) — Полный структурированный каталог сертифицированных ГСО (ЭКРОСХИМ ISO 17034), реактивов и приборов.\n\n"
            "🔬 <b>Метрологические услуги</b> — Информация о государственной поверке, калибровке и аттестации.\n\n"
            "📝 <b>Заявка / Консультация</b> — Быстрое оформление заявки на поверку, калибровку или покупку.\n\n"
            "🌐 <b>Сменить язык</b> (/lang) — Переключение между узбекским и русским языками.\n\n"
            "<i>По вопросам поддержки: {support}</i>"
        )
    },
    "back_to_main_text": {
        "uz": "Bosh sahifaga qaytdingiz. Kerakli bo'limni tanlang:",
        "ru": "Вы вернулись в главное меню. Выберите нужный раздел:"
    },

    # ----------------------------------------------------
    # QIDIRUV (SEARCH) MATNLARI
    # ----------------------------------------------------
    "search_prompt": {
        "uz": (
            "🔍 <b>Mahsulot yoki Standartni qidirish</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Qidirmoqchi bo'lgan mahsulot nomi, markasi, standarti yoki kalit so'zini kiriting.\n\n"
            "<i>Masalan:</i>\n"
            "• <code>GSO 7874</code> yoki <code>kadmiy</code>\n"
            "• <code>bufer 4.01</code> yoki <code>fiksanal</code>\n"
            "• <code>manometr</code> yoki <code>termometr</code>\n"
            "• <code>areometr ANT</code> yoki <code>VPJ-2</code>"
        ),
        "ru": (
            "🔍 <b>Поиск продукции и стандартов</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Введите наименование, номер ГСО, химический элемент или тип прибора.\n\n"
            "<i>Примеры:</i>\n"
            "• <code>ГСО 7874</code> или <code>кадмий</code>\n"
            "• <code>буфер 4.01</code> или <code>фиксанал</code>\n"
            "• <code>манометр</code> или <code>термометр</code>\n"
            "• <code>ареометр АНТ</code> или <code>ВПЖ-2</code>"
        )
    },
    "search_short": {
        "uz": "⚠️ Qidiruv uchun kamida 2 ta harf kiriting:",
        "ru": "⚠️ Для поиска введите не менее 2 символов:"
    },
    "search_found": {
        "uz": "🎯 <b>Qidiruv natijalari:</b> \"<i>{query}</i>\"\n━━━━━━━━━━━━━━━━━━━━\nTopildi: <b>{count} ta</b> mos keluvchi element.\nBatafsil ma'lumot olish uchun quyidagilardan birini tanlang:",
        "ru": "🎯 <b>Результаты поиска:</b> \"<i>{query}</i>\"\n━━━━━━━━━━━━━━━━━━━━\nНайдено: <b>{count} шт.</b> подходящих позиций.\nВыберите позицию для просмотра подробной информации:"
    },
    "search_not_found": {
        "uz": "❌ <b>Natija topilmadi:</b> \"<i>{query}</i>\"\n━━━━━━━━━━━━━━━━━━━━\nBoshqa so'z bilan qidirib ko'ring yoki umumiy katalog bo'limidan foydalaning.",
        "ru": "❌ <b>Ничего не найдено по запросу:</b> \"<i>{query}</i>\"\n━━━━━━━━━━━━━━━━━━━━\nПопробуйте изменить запрос или воспользуйтесь каталогом продукции."
    },

    # ----------------------------------------------------
    # KATALOG MATNLARI
    # ----------------------------------------------------
    "catalog_title": {
        "uz": "📦 <b>Mahsulotlar va Xizmatlar Katalogi</b>\n━━━━━━━━━━━━━━━━━━━━\nO'zingizga kerakli bo'limni tanlang:",
        "ru": "📦 <b>Каталог продукции и метрологических услуг</b>\n━━━━━━━━━━━━━━━━━━━━\nВыберите интересующий вас раздел:"
    },
    "category_info": {
        "uz": "{icon} <b>{name}</b>\n━━━━━━━━━━━━━━━━━━━━\n<i>{desc}</i>\n\nMavjud elementlar soni: <b>{total_count} ta</b>\nBatafsil ma'lumot olish uchun mahsulot ustiga bosing:",
        "ru": "{icon} <b>{name}</b>\n━━━━━━━━━━━━━━━━━━━━\n<i>{desc}</i>\n\nКоличество позиций: <b>{total_count} шт.</b>\nНажмите на позицию для подробностей:"
    },

    # ----------------------------------------------------
    # SAVATCHA (CART) MATNLARI
    # ----------------------------------------------------
    "cart_empty": {
        "uz": "🛒 <b>Sizning savatchangiz bo'sh</b>\n━━━━━━━━━━━━━━━━━━━━\nKatalogdan yoki qidiruv orqali kerakli standart namunalar va o'lchash vositalarini savatchaga qo'shishingiz mumkin.",
        "ru": "🛒 <b>Ваша корзина пуста</b>\n━━━━━━━━━━━━━━━━━━━━\nВы можете добавить интересующие стандартные образцы, буферные растворы и приборы из каталога или поиска."
    },
    "cart_added_alert": {
        "uz": "✅ Savatchaga qo'shildi! (Jami: {qty} ta)",
        "ru": "✅ Добавлено в корзину! (Всего: {qty} шт)"
    },
    "cart_cleared_alert": {
        "uz": "🗑 Savatcha tozalandi!",
        "ru": "🗑 Корзина очищена!"
    },
    "cart_deleted_alert": {
        "uz": "🗑 Mahsulot o'chirildi",
        "ru": "🗑 Товар удален из корзины"
    },
    "product_added_success": {
        "uz": "✅ <b>'{name}'</b> muvaffaqiyatli saqlandi va katalogga qo'shildi!",
        "ru": "✅ <b>'{name}'</b> успешно сохранена в каталоге!"
    },

    # ----------------------------------------------------
    # AI METROLOG MATNLARI
    # ----------------------------------------------------
    "ai_welcome": {
        "uz": (
            "🤖 <b>Sun'iy Intellekt (AI) Metrolog Maslahatchisi</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Assalomu alaykum! Men metrologiya, standartlar (ISO 17034, GOST, O'z DSt), "
            "Davlat Standart Namunalar (GSO), bufer eritmalar, fiksanallar va laboratoriya "
            "o'lchash vositalari bo'yicha sizga yordam beruvchi aqlli maslahatchiman.\n\n"
            "💬 <i>Menga istalgan savolingizni yozishingiz yoki quyidagi tayyor mavzulardan birini tanlashingiz mumkin:</i>"
        ),
        "ru": (
            "🤖 <b>AI Консультант по Метрологии и Стандартам</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Здравствуйте! Я интеллектуальный консультант по стандартам (ISO 17034, ГОСТ, O'z DSt), "
            "государственным стандартным образцам (ГСО завода ЭКРОСХИМ), фиксаналам, "
            "буферным растворам и средствам измерений.\n\n"
            "💬 <i>Напишите ваш вопрос или выберите одну из готовых тем ниже:</i>"
        )
    },
    "ai_quick_topics": {
        "uz": "💡 <b>Tezkor savollar:</b>",
        "ru": "💡 <b>Популярные темы:</b>"
    },
    "ai_history_cleared": {
        "uz": "🧹 <b>Muloqot xotirasi tozalandi!</b>\nYangi savolingizni yozishingiz mumkin.",
        "ru": "🧹 <b>Память диалога очищена!</b>\nВы можете задать новый вопрос."
    }
}


def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    """Belgilangan tildagi matnni formatlab qaytarish."""
    lang = lang if lang in ("uz", "ru") else "uz"
    item = TEXTS.get(key, {})
    raw_text = item.get(lang, item.get("uz", key))
    if kwargs:
        try:
            return raw_text.format(**kwargs)
        except Exception:
            return raw_text
    return raw_text


# Kategoriya nomlari va tavsiflarining ruscha tarjimalari
CATEGORY_TRANSLATIONS = {
    1: {
        "name": "Стандартные образцы (ГСО)",
        "description": "Государственные стандартные образцы (ГСО) завода «ЭКРОСХИМ» (ISO 17034) — ионы металлов, анионы, показатели воды и нефтепродукты."
    },
    2: {
        "name": "Буферные растворы (рН буферы)",
        "description": "Готовые стандартные буферные растворы (рН 1.68 - 12.45) для калибровки и поверки рН-метров и иономеров по ГОСТ 8.135-2004."
    },
    3: {
        "name": "Стандарт-титры (Фиксаналы)",
        "description": "Ампулы с точной концентрацией 0.1 N для титриметрического анализа (кислоты, щелочи, окислители, соли) производства «Уралхиминвест» и «Ленреактив»."
    },
    4: {
        "name": "Химические реактивы",
        "description": "Высокочистые химические реактивы (ХЧ, ЧДА, Ч) для аналитических лабораторий и промышленного контроля."
    },
    5: {
        "name": "Капиллярные вискозиметры (ВПЖ)",
        "description": "Стеклянные вискозиметры ВПЖ-2 и ВПЖ-4 для определения кинематической вязкости прозрачных жидкостей и масел."
    },
    6: {
        "name": "Ареометры (Измерение плотности)",
        "description": "Стеклянные ареометры общего назначения (АОН-1, АОН-2), нефтеденсиметры (АНТ-1, АНТ-2) и ареометры для молока (АМ, АМТ)."
    },
    7: {
        "name": "Термометры и термогигрометры",
        "description": "Лабораторные стеклянные термометры (ТЛ-2, ТЛ-4, ТЛ-5, ТН) и электронные термогигрометры с поверкой."
    },
    8: {
        "name": "Линейные и геометрические СИ",
        "description": "Рулетки с грузом для нефтепродуктов (Р10УЗГ, Р20УЗГ), металлические линейки, штангенциркули, щупы и толщиномеры."
    },
    9: {
        "name": "Приборы давления и расхода",
        "description": "Лабораторные барабанные счетчики газа (ГСБ-400), технические и образцовые манометры."
    },
    10: {
        "name": "Лабораторные приборы и оборудование",
        "description": "Магнитные мешалки, аналитические весы, сушильные шкафы и испытательное оборудование."
    },
    11: {
        "name": "Стандарты и нормативы",
        "description": "Официальные стандарты, методики поверки и нормативно-техническая документация."
    },
    12: {
        "name": "Метрологические услуги",
        "description": "Государственная поверка, калибровка средств измерений и аттестация испытательного оборудования."
    }
}
