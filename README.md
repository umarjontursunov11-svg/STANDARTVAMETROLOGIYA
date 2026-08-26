# 🏛 Standart va Metrologiya Telegram Boti (Python / aiogram 3 / Multi-language / AI)

Standartlashtirish, metrologik xizmatlar (qiyoslash, kalibrlash, attestatsiya), Davlat Standart Namunalar (GSO — EKROSXIM ISO 17034), bufer eritmalar, fiksanallar, kimyoviy reaktivlar va o'lchash vositalari haqida ma'lumot beruvchi, mahsulotlarni qidirish, **Savatcha (Корзина)** orqali buyurtma berish hamda **Sun'iy Intellekt (AI) Metrolog Maslahatchi** bilan jihozlangan ko'p tilli (O'zbekcha 🇺🇿 / Русский 🇷🇺) zamonaviy Telegram boti.

---

## 🌟 Asosiy Imkoniyatlar

1. **🌐 Ikki tilli (Ko'p tilli) tizim:**
   - **O'zbekcha 🇺🇿** va **Русский 🇷🇺** tillarida to'liq interfeys.
   - `/lang` buyrug'i yoki `🌐 Tilni o'zgartirish` tugmasi orqali istalgan paytda tilni almashtirish.
   - Har bir foydalanuvchining tanlagan tili ma'lumotlar bazasida doimiy saqlanadi.

2. **🛒 Savatcha (Корзина / Shopping Cart) Tizimi:**
   - Katalogdan yoki qidiruvdan kerakli standart namunalarni bittalab savatchaga yig'ish.
   - Mahsulotlar sonini o'zgartirish (`➕` / `➖`) va o'chirish (`🗑`).
   - Yig'ilgan barcha mahsulotlarga bir vaqtning o'zida yagona buyurtma (Checkout) rasmiylashtirish.

3. **🤖 Sun'iy Intellekt (AI) Metrolog Maslahatchi:**
   - 24/7 rejimida foydalanuvchilarning barcha metrologik, kimyoviy va texnik savollariga ikki tilda jonli javob beradi.
   - Google Gemini, OpenAI (ChatGPT) va DeepSeek modellari integratsiyasi + mustaqil aqlli ichki ekspert tizimi.

4. **🧪 Davlat Standart Namunalar (GSO) va Mahsulotlar Katalogi:**
   - «ЭКРОСХИМ» Заводи (Rossiya) tomonidan **ISO 17034** xalqaro talablari asosida ishlab chiqarilgan 67+ xil GSO namunalari.
   - pH bufer eritmalar (pH 1.68 – 12.45), standart titrlar (fiksanallar 0.1 N), kimyoviy reaktivlar (XCh, ChDA, Ch).
   - Kapillyar viskozimetrlar (ВПЖ-2, ВПЖ-4), areometrlar (АОН-1, АНТ-1, АМ), termometrlar, neft ruletkalari va gaz hisoblagichlar.

5. **🔍 Mahsulot va Standartlarni Aqlli Qidirish:**
   - Ko'p tilli (o'zbekcha lotin/kirill, ruscha), GSO kodlari, kimyoviy formulalar va sinonimlar bo'yicha tezkor qidiruv.

6. **⚙️ Boshqaruv (Admin) Paneli:**
   - `/admin` buyrug'i (faqat `.env` da ko'rsatilgan adminlar uchun).
   - Bot statistikasi, oxirgi arizalarni ko'rish, mahsulot qo'shish va ommaviy xabar yuborish (Broadcast).

---

## 📁 Loyiha Strukturasi

```
Metrologiya/
├── bot/
│   ├── config.py                 # Sozlamalar va .env o'qish
│   ├── database/
│   │   ├── db.py                 # SQLite asinxron ulanishi va jadvallar
│   │   ├── models.py             # CRUD amallari, tillar va aqlli qidiruv
│   │   └── seed_data.py          # Boshlang'ich metrologiya ma'lumotlari (185+ ta)
│   ├── handlers/
│   │   ├── start.py              # /start, /help, /lang navigatsiya
│   │   ├── ai.py                 # 🤖 AI Metrolog Maslahatchi handleri
│   │   ├── cart.py               # 🛒 Savatcha va buyurtma rasmiylashtirish
│   │   ├── company.py            # Kompaniya, xizmatlar, kontaktlar, lokatsiya
│   │   ├── catalog.py            # Katalog, kategoriyalar va mahsulot kartochkasi
│   │   ├── search.py             # Aqlli qidiruv tizimi
│   │   ├── order.py              # FSM buyurtma va arizalar jarayoni
│   │   └── admin.py              # Admin boshqaruv paneli
│   ├── keyboards/
│   │   ├── reply.py              # Reply klaviatura tugmalari (UZ / RU)
│   │   └── inline.py             # Inline interaktiv tugmalar (UZ / RU)
│   ├── services/
│   │   └── ai.py                 # Sun'iy intellekt xizmati
│   ├── states/
│   │   └── states.py             # FSM holatlari
│   └── utils/
│       ├── helpers.py            # Matn formatlash (HTML, UZ / RU)
│       └── localization.py       # Ko'p tillik lug'ati va tarjimalar
├── .env.example                  # Misol konfiguratsiya fayli
├── .env                          # Konfiguratsiya fayli
├── requirements.txt              # Kerakli Python kutubxonalari
├── README.md                     # Qo'llanma
└── main.py                       # Botni ishga tushirish nuqtasi
```

---

## 🚀 O'rnatish va Ishga Tushirish

```bash
# 1. Virtual muhitni yaratish va faollashtirish
python -m venv venv
.\venv\Scripts\activate

# 2. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 3. .env fayliga bot tokenini kiritish
# BOT_TOKEN=...

# 4. Botni ishga tushirish
python main.py
```
