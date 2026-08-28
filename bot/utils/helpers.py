"""
Matnlarni formatlash va vizual ko'rinish beruvchi yordamchi funksiyalar (HTML formatida).
O'zbek va Rus tillarini qo'llab-quvvatlaydi.
Barcha foydalanuvchi kiritgan matnlar html.escape orqali xavfsiz holatga keltiriladi.
"""

import html
from typing import Dict, Any, List
from bot.config import config
from bot.utils.localization import CATEGORY_TRANSLATIONS, get_text

KNOWN_MENU_BUTTONS = [
    # Uzbek buttons
    "🔍 Mahsulot qidirish", "📦 Mahsulotlar katalogi", "🛒 Savatcha",
    "🤖 AI Metrolog Maslahatchi", "🔬 Metrologik xizmatlar",
    "🏢 Kompaniya haqida", "📝 Ariza / Maslahat olish",
    "📞 Bog'lanish va Manzil", "🌐 Tilni o'zgartirish", "⚙ Admin Paneli",
    "📊 Statistika", "📋 Oxirgi arizalar", "➕ Mahsulot qo'shish", "📢 Xabar yuborish",
    "⬅ Asosiy menyuga qaytish", "❌ Bekor qilish", "🧹 Muloqotni tozalash",
    "📱 Telefon raqamni yuborish",

    # Russian buttons
    "🔍 Поиск продукции", "📦 Каталог продукции", "🛒 Корзина",
    "🤖 AI Консультант Метролог", "🔬 Метрологические услуги",
    "🏢 О компании", "📝 Заявка / Консультация",
    "📞 Контакты и Адрес", "🌐 Сменить язык", "⚙ Панель администратора",
    "📊 Статистика", "📋 Последние заявки", "➕ Добавить продукцию", "📢 Рассылка",
    "⬅ Главное меню", "❌ Отмена", "🧹 Очистить историю",
    "📱 Отправить номер телефона"
]


def format_product_card(product: Dict[str, Any], lang: str = "uz") -> str:
    """Mahsulot yoki xizmat haqidagi to'liq kartochka matni (O'zbek / Rus)."""
    is_service = bool(product.get("is_service", 0))
    header_icon = "🔬" if is_service else "📦"
    
    cat_id = product.get("category_id", 0)
    cat_name = product.get("category_name", "")
    if lang == "ru" and cat_id in CATEGORY_TRANSLATIONS:
        cat_name = CATEGORY_TRANSLATIONS[cat_id]["name"]

    lbl_cat = "Категория" if lang == "ru" else "Kategoriya"
    lbl_code = "Код / Обозначение" if lang == "ru" else "Belgisi / Kodi"
    lbl_std = "Стандарт / Норматив" if lang == "ru" else "Standart / Normativ"
    lbl_acc = "Класс / Погрешность" if lang == "ru" else "Aniqlik darajasi / sinfi"
    lbl_rng = "Диапазон измерений" if lang == "ru" else "O'lchash diapazoni"
    lbl_prc = "Цена / Тариф" if lang == "ru" else "Narxi / Tarif"
    lbl_dsc = "Описание и применение" if lang == "ru" else "Tavsif va qo'llanishi"

    name_safe = html.escape(str(product.get("name", "")))
    text = (
        f"{header_icon} <b>{name_safe}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )

    if cat_name:
        icon = product.get("category_icon", "📁")
        text += f"📂 <b>{lbl_cat}:</b> {icon} {html.escape(cat_name)}\n"

    if product.get("code"):
        text += f"🔖 <b>{lbl_code}:</b> <code>{html.escape(str(product['code']))}</code>\n"

    if product.get("standard"):
        text += f"📜 <b>{lbl_std}:</b> <i>{html.escape(str(product['standard']))}</i>\n"

    if product.get("accuracy_class"):
        text += f"🎯 <b>{lbl_acc}:</b> {html.escape(str(product['accuracy_class']))}\n"

    if product.get("measurement_range"):
        text += f"📏 <b>{lbl_rng}:</b> {html.escape(str(product['measurement_range']))}\n"

    if product.get("price"):
        text += f"💰 <b>{lbl_prc}:</b> <b>{html.escape(str(product['price']))}</b>\n"

    text += f"━━━━━━━━━━━━━━━━━━━━\n"
    
    if product.get("description"):
        text += f"📝 <b>{lbl_dsc}:</b>\n{html.escape(str(product['description']))}\n"

    return text


def format_cart_view(cart_items: List[Dict[str, Any]], lang: str = "uz") -> str:
    """Savatcha tarkibini chiroyli ko'rsatish matni."""
    if not cart_items:
        return get_text("cart_empty", lang)

    total_qty = sum(item.get("quantity", 1) for item in cart_items)
    distinct_count = len(cart_items)

    if lang == "ru":
        text = (
            f"🛒 <b>Ваша Корзина:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Всего наименований: <b>{distinct_count} вид(ов)</b>\n"
            f"Общее количество: <b>{total_qty} шт.</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for idx, item in enumerate(cart_items, 1):
            name = html.escape(str(item.get("product_name", "Товар")))
            code = item.get("product_code", "")
            code_str = f" [<code>{html.escape(str(code))}</code>]" if code else ""
            qty = item.get("quantity", 1)
            price = html.escape(str(item.get("product_price", "По запросу / договорная")))
            text += (
                f"<b>{idx}. {name}</b>{code_str}\n"
                f"   🔢 Количество: <b>{qty} шт</b> | 💰 Цена: <i>{price}</i>\n\n"
            )
        text += (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Для изменения количества или оформления заказа воспользуйтесь кнопками ниже:</i>"
        )
    else:
        text = (
            f"🛒 <b>Sizning Savatchangiz:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Jami turdagi mahsulotlar: <b>{distinct_count} xil</b>\n"
            f"Jami soni: <b>{total_qty} ta</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for idx, item in enumerate(cart_items, 1):
            name = html.escape(str(item.get("product_name", "Mahsulot")))
            code = item.get("product_code", "")
            code_str = f" [<code>{html.escape(str(code))}</code>]" if code else ""
            qty = item.get("quantity", 1)
            price = html.escape(str(item.get("product_price", "Shartnoma asosida")))
            text += (
                f"<b>{idx}. {name}</b>{code_str}\n"
                f"   🔢 Miqdori: <b>{qty} ta</b> | 💰 Narxi: <i>{price}</i>\n\n"
            )
        text += (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Mahsulotlar sonini o'zgartirish yoki buyurtmani rasmiylashtirish uchun quyidagi tugmalardan foydalaning:</i>"
        )
    return text


def format_cart_order_user_receipt(order_data: Dict[str, Any], lang: str = "uz") -> str:
    """Savatcha orqali rasmiylashtirilgan buyurtmaning mijoz kvitansiyasi."""
    order_id = order_data.get("order_id", "-")
    full_name = html.escape(str(order_data.get("full_name", "-")))
    phone_number = html.escape(str(order_data.get("phone_number", "-")))
    total_items = order_data.get("total_items", 0)
    items_summary = html.escape(str(order_data.get("items_summary", "")))

    if lang == "ru":
        return (
            f"✅ <b>Ваш заказ успешно принят!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Номер заказа:</b> #{order_id}\n"
            f"👤 <b>Заказчик:</b> {full_name}\n"
            f"📞 <b>Телефон:</b> {phone_number}\n"
            f"📦 <b>Количество позиций:</b> {total_items} шт.\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Состав заказа:</b>\n"
            f"{items_summary}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Наши специалисты свяжутся с вами в ближайшее время для согласования условий поставки.\n\n"
            f"<i>Спасибо за доверие к нашей компании!</i>"
        )
    return (
        f"✅ <b>Savatchangizdagi buyurtma muvaffaqiyatli qabul qilindi!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Buyurtma raqami:</b> #{order_id}\n"
        f"👤 <b>Buyurtmachi:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> {phone_number}\n"
        f"📦 <b>Jami mahsulotlar soni:</b> {total_items} ta\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Tanlangan mahsulotlar:</b>\n"
        f"{items_summary}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Mutaxassislarimiz qisqa vaqt ichida siz bilan bog'lanib, shartnoma va yetkazib berish shartlarini muvofiqlashtirishadi.\n\n"
        f"<i>Ishonchingiz uchun rahmat!</i>"
    )


def format_cart_order_admin_notification(order_data: Dict[str, Any]) -> str:
    """Savatcha buyurtmasi kelganda adminga yuboriladigan to'liq bildirishnoma."""
    order_id = order_data.get("order_id", "-")
    full_name = html.escape(str(order_data.get("full_name", "-")))
    phone_number = html.escape(str(order_data.get("phone_number", "-")))
    total_items = order_data.get("total_items", 0)
    notes = html.escape(str(order_data.get("notes") or "Mavjud emas / Нет"))
    items_summary = html.escape(str(order_data.get("items_summary", "")))

    return (
        f"🛒 <b>YANGI SAVATCHA BUYURTMASI KELIB TUSHDI!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>Buyurtma ID:</b> #{order_id}\n"
        f"👤 <b>Mijoz:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> <code>{phone_number}</code>\n"
        f"📦 <b>Jami elementlar:</b> {total_items} ta\n"
        f"📝 <b>Qo'shimcha izoh:</b> {notes}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Buyurtma tarkibi:</b>\n"
        f"{items_summary}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Iltimos, buyurtmachi bilan imkon qadar tezroq bog'laning!</i>"
    )


def format_company_info(lang: str = "uz") -> str:
    """Kompaniya haqida to'liq ma'lumot (O'zbek / Rus)."""
    comp = config.company
    if lang == "ru":
        addr_ru = "г. Ташкент, Сергелийский р-н, ул. Узумзор, 16-тупик, дом 18"
        work_ru = "Понедельник - Пятница: 09:00 - 18:00"
        text = (
            f"🏢 <b>{comp.name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Наша компания специализируется на поставке высококачественных <b>Государственных Стандартных Образцов (ГСО)</b>, "
            f"<b>буферных растворов</b>, <b>стандарт-титров (фиксаналов)</b>, <b>химических реактивов</b> "
            f"и оказании комплексных <b>метрологических услуг</b> (поверка, калибровка, аттестация) для лабораторий и предприятий по всему Узбекистану.\n\n"
            f"🏆 <b>Наши ключевые преимущества:</b>\n"
            f"• Сертифицированные ГСО завода «ЭКРОСХИМ» (Россия) по международному стандарту <b>ISO 17034</b>\n"
            f"• Высокоточные буферные растворы (рН 1.68 - 12.45) по ГОСТ 8.135-2004\n"
            f"• Стандарт-титры (фиксаналы 0.1 N) для точного аналитического титрования\n"
            f"• Реактивы высокой степени чистоты (ХЧ, ЧДА, Ч)\n"
            f"• Официальные свидетельства о поверке и сертификаты калибровки\n"
            f"• Профессиональные консультации экспертов и оперативная доставка\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Адрес:</b> {addr_ru}\n"
            f"📞 <b>Телефоны:</b> {comp.phone}\n"
            f"✉️ <b>Email:</b> {comp.email}\n"
        )
        if comp.website and comp.website.strip():
            text += f"🌐 <b>Веб-сайт:</b> {comp.website}\n"
        text += f"🕒 <b>Режим работы:</b> {work_ru}\n"
        return text

    text = (
        f"🏢 <b>{comp.name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Bizning korxona O'zbekiston Respublikasi bo'ylab laboratoriyalar, ishlab chiqarish "
        f"korxonalari va tahlil markazlari uchun yuqori sifatli <b>Davlat Standart Namunalar (GSO)</b>, "
        f"<b>bufer eritmalari</b>, <b>standart titrlar (fiksanallar)</b>, <b>kimyoviy reaktivlar</b> yetkazib berish "
        f"hamda professional <b>metrologik xizmatlar</b> (qiyoslash, kalibrlash, attestatsiya) ko'rsatishga ixtisoslashgan.\n\n"
        f"🏆 <b>Bizning afzalliklarimiz:</b>\n"
        f"• Davlat reestriga kiritilgan sertifikatlangan Standart Namunalar (GSO)\n"
        f"• «ЭКРОСХИМ» Заводи томонидан <b>ISO 17034</b> талаблари асосида ишлаб чиқарилган ГСО намуналари\n"
        f"• Yuqori aniqlikdagi bufer eritmalar va standart titrlar (fiksanallar)\n"
        f"• Sifatli va tozalik darajasi yuqori kimyoviy reaktivlar (XCh, ChDA, Ch)\n"
        f"• Rasmiy davlat qiyoslovi (poverka) va kalibrlash guvohnomalari\n"
        f"• Malakali mutaxassislar maslahati va tezkor yetkazib berish\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 <b>Manzil:</b> {comp.address}\n"
        f"📞 <b>Telefonlar:</b> {comp.phone}\n"
        f"✉️ <b>Email:</b> {comp.email}\n"
    )
    if comp.website and comp.website.strip():
        text += f"🌐 <b>Veb-sayt:</b> {comp.website}\n"
    text += f"🕒 <b>Ish vaqti:</b> {comp.work_hours}\n"
    return text


def format_services_info(lang: str = "uz") -> str:
    """Metrologik xizmatlar va mahsulotlar haqida ma'lumot (O'zbek / Rus)."""
    if lang == "ru":
        return (
            f"🔬 <b>Продукция и Метрологические Услуги:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🧪 <b>1. Стандартные образцы (ГСО)</b>\n"
            f"Сертифицированные ГСО завода «ЭКРОСХИМ» (ISO 17034) для градуировки спектрофотометров, хроматографов, ААС и контроля точности измерений.\n\n"
            f"💧 <b>2. Буферные растворы (рН буферы)</b>\n"
            f"Стандартные буферные растворы по ГОСТ 8.135-2004 для калибровки и поверки рН-метров и иономеров.\n\n"
            f"⚗️ <b>3. Стандарт-титры (Фиксаналы)</b>\n"
            f"Ампулы точной концентрации (0.1 N) для количественного титриметрического анализа.\n\n"
            f"🧪 <b>4. Химические реактивы</b>\n"
            f"Органические и неорганические реактивы квалификаций ХЧ, ЧДА, Ч для лабораторных исследований.\n\n"
            f"⚙️ <b>5. Государственная поверка</b>\n"
            f"Определение соответствия средств измерений установленным метрологическим требованиям с выдачей государственного свидетельства.\n\n"
            f"📊 <b>6. Калибровка средств измерений</b>\n"
            f"Сличение показаний СИ с эталонами высокой точности с выдачей сертификата калибровки.\n\n"
            f"🌡 <b>7. Аттестация испытательного оборудования</b>\n"
            f"Первичная и периодическая аттестация сушильных шкафов, муфельных печей, термостатов и климатических камер.\n\n"
            f"📜 <b>8. Стандартизация и консалтинг</b>\n"
            f"Разработка методик измерений, стандартов предприятий и технической документации.\n\n"
            f"<i>Для заказа продукции или подачи заявки на услуги воспользуйтесь кнопкой <b>'📝 Заявка / Консультация'</b> или <b>'🛒 Корзина'</b>.</i>"
        )
    return (
        f"🔬 <b>Mahsulotlar va Metrologik Xizmatlar:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🧪 <b>1. Standart namunalar (GSO)</b>\n"
        f"Laboratoriya sinovlari, asboblarni kalibrlash va tahlillar aniqligini ta'minlash uchun sertifikatlangan Davlat Standart Namunalar (ISO 17034).\n\n"
        f"💧 <b>2. Bufer eritmalari (pH buferlar)</b>\n"
        f"pH-metrlar, ionomerlar va tahlil asboblarini aniq sozlash hamda kalibrlash uchun sifatli bufer eritmalar.\n\n"
        f"⚗️ <b>3. Standart titrlar (Fiksanallar)</b>\n"
        f"Titrimetrik va miqdoriy kimyoviy tahlillar uchun aniq konsentratsiyali ampula eritmalari to'plami.\n\n"
        f"🧪 <b>4. Kimyoviy reaktivlar</b>\n"
        f"Laboratoriya va sanoat tahlillari uchun yuqori tozalikdagi kimyoviy moddalar (XCh, ChDA, Ch).\n\n"
        f"⚙️ <b>5. Davlat Qiyoslovi (Poverka)</b>\n"
        f"O'lchash vositalarining belgilangan talablarga muvofiqligini tasdiqlash va rasmiy Davlat Qiyoslash guvohnomasini berish.\n\n"
        f"📊 <b>6. Kalibrlash (Calibration)</b>\n"
        f"O'lchash vositalarining metrologik parametrlarini etalonlar bilan solishtirish va kalibrlash sertifikatini taqdim etish.\n\n"
        f"🌡 <b>7. Sinov uskunalarini attestatsiyalash</b>\n"
        f"Termokameralar, quritish shkaflari, pechlar va sinov stendlarini birlamchi va davriy attestatsiyadan o'tkazish.\n\n"
        f"📜 <b>8. Standartlashtirish va Sertifikatlashtirish</b>\n"
        f"Texnik hujjatlar, standartlar ishlab chiqish va sertifikatlashtirish xizmatlari.\n\n"
        f"<i>Mahsulot buyurtma qilish yoki xizmatlarga ariza qoldirish uchun <b>'📝 Ariza / Maslahat olish'</b> yoki <b>'🛒 Savatcha'</b> bo'limidan foydalaning.</i>"
    )


def format_order_admin_notification(order: Dict[str, Any]) -> str:
    """Yangi buyurtma kelganda adminga yuboriladigan xabar."""
    order_id = order.get("id", "-")
    full_name = html.escape(str(order.get("full_name", "-")))
    phone_number = html.escape(str(order.get("phone_number", "-")))
    item_name = html.escape(str(order.get("item_name", "Umumiy maslahat")))
    notes = html.escape(str(order.get("notes", "Mavjud emas / Нет")))
    created_at = html.escape(str(order.get("created_at", "Hozir")))

    return (
        f"🔔 <b>YANGI ARIZA / BUYURTMA KELIB TUSHDI!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>Ariza raqami:</b> #{order_id}\n"
        f"👤 <b>Mijoz:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> <code>{phone_number}</code>\n"
        f"📦 <b>Mahsulot / Xizmat:</b> {item_name}\n"
        f"📝 <b>Izoh / Talablar:</b> {notes}\n"
        f"⏰ <b>Vaqti:</b> {created_at}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Iltimos, mijoz bilan imkon qadar tezroq bog'laning!</i>"
    )


def format_order_user_receipt(
    order_id: int,
    full_name: str,
    phone_number: str,
    item_name: str,
    lang: str = "uz"
) -> str:
    """Foydalanuvchiga arizasi qabul qilinganligi haqida xabar."""
    full_name_safe = html.escape(str(full_name))
    phone_safe = html.escape(str(phone_number))
    item_safe = html.escape(str(item_name))

    if lang == "ru":
        return (
            f"✅ <b>Ваша заявка успешно принята!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 <b>Номер заявки:</b> #{order_id}\n"
            f"👤 <b>Заказчик:</b> {full_name_safe}\n"
            f"📞 <b>Телефон:</b> {phone_safe}\n"
            f"📦 <b>Тема / Позиция:</b> {item_safe}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Наши специалисты свяжутся с вами в кратчайшие сроки.\n"
            f"Благодарим за обращение в OOO \"STANDART VA METROLOGIYA\"!"
        )
    return (
        f"✅ <b>Arizangiz muvaffaqiyatli qabul qilindi!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Ariza raqami:</b> #{order_id}\n"
        f"👤 <b>Qabul qiluvchi:</b> {full_name_safe}\n"
        f"📞 <b>Telefon:</b> {phone_safe}\n"
        f"📦 <b>Mavzu:</b> {item_safe}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Mutaxassislarimiz qisqa vaqt ichida siz bilan bog'lanishadi.\n"
        f"OOO \"STANDART VA METROLOGIYA\" ga ishonch bildirganingiz uchun rahmat!"
    )
