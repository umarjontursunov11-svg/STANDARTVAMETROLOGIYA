"""
Ma'lumotlar bazasi so'rovlari va amallari (CRUD) moduli.
"""

from typing import List, Optional, Dict, Any
from bot.database.db import get_db


async def get_categories() -> List[Dict[str, Any]]:
    """Barcha kategoriyalarni olish."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM categories ORDER BY id ASC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def get_category_by_id(category_id: int) -> Optional[Dict[str, Any]]:
    """ID bo'yicha kategoriyani olish."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_products_by_category(
    category_id: int,
    limit: int = 5,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Kategoriya bo'yicha mahsulotlarni sahifalab olish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM products WHERE category_id = ? ORDER BY id ASC LIMIT ? OFFSET ?",
            (category_id, limit, offset)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def get_category_product_count(category_id: int) -> int:
    """Kategoriya ichidagi mahsulotlar umumiy soni."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM products WHERE category_id = ?",
            (category_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else 0
    finally:
        await db.close()


async def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    """ID bo'yicha mahsulot yoki xizmatni olish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """
            SELECT p.*, c.name as category_name, c.icon as category_icon
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?
            """,
            (product_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


def _get_search_variants(query: str) -> List[str]:
    """Qidiruv so'rovi uchun transliteratsiya, sinonimlar va punktuatsiya variantlarini hosil qilish."""
    variants = [query.strip()]
    lower_q = query.lower().strip()
    
    if "," in query:
        variants.append(query.replace(",", ".").strip())
    if "." in query:
        variants.append(query.replace(".", ",").strip())

    # Latin to Cyrillic
    lat_to_cyr_multi = {
        "shch": "щ", "yo": "ё", "yu": "ю", "ya": "я", "ch": "ч", "sh": "ш", 
        "ts": "ц", "ye": "е", "zh": "ж", "o'": "о", "g'": "г", "kh": "х"
    }
    lat_to_cyr_single = {
        "a": "а", "b": "б", "v": "в", "g": "г", "d": "д", "e": "е", "z": "з", 
        "i": "и", "y": "й", "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н", 
        "o": "о", "p": "п", "r": "р", "s": "с", "t": "т", "u": "у", "f": "ф", 
        "x": "х", "h": "х", "c": "ц", "q": "к", "w": "в"
    }

    # Cyrillic to Latin
    cyr_to_lat = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", 
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "m": "m", 
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", 
        "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", 
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o'", "ғ": "g'"
    }

    # Transliterate Latin -> Cyrillic
    trans_cyr = lower_q
    for k, v in lat_to_cyr_multi.items():
        trans_cyr = trans_cyr.replace(k, v)
    for k, v in lat_to_cyr_single.items():
        trans_cyr = trans_cyr.replace(k, v)
    
    if trans_cyr != lower_q:
        variants.append(trans_cyr)
        if trans_cyr.startswith("е"):
            variants.append("э" + trans_cyr[1:])

    # Transliterate Cyrillic -> Latin
    trans_lat = ""
    for ch in lower_q:
        trans_lat += cyr_to_lat.get(ch, ch)
    if trans_lat != lower_q:
        variants.append(trans_lat)

    # Kimyoviy va metrologik sinonimlar
    synonyms = {
        "simob": ["ртуть", "hg", "7879", "8004"],
        "ртуть": ["simob", "hg", "7879", "8004"],
        "qorgoshin": ["свинец", "pb", "7877"],
        "qo'rg'oshin": ["свинец", "pb", "7877"],
        "свинец": ["qorgoshin", "qo'rg'oshin", "pb", "7877"],
        "mis": ["медь", "cu", "7836"],
        "медь": ["mis", "cu", "7836"],
        "temir": ["железо", "fe", "7835", "8032"],
        "железо": ["temir", "fe", "7835", "8032"],
        "rux": ["цинк", "zn", "7837", "8053"],
        "цинк": ["rux", "tsink", "zn", "7837", "8053"],
        "tsink": ["цинк", "rux", "zn", "7837", "8053"],
        "kadmiy": ["кадмий", "cd", "7874"],
        "кадмий": ["kadmiy", "cd", "7874"],
        "marganes": ["марганец", "mn", "7875", "7876", "8056"],
        "марганец": ["marganes", "mn", "7875", "7876", "8056"],
        "magniy": ["магний", "mg", "7681", "7190"],
        "магний": ["magniy", "mg", "7681", "7190"],
        "mishyak": ["мышьяк", "as", "7976"],
        "мышьяк": ["mishyak", "as", "7976"],
        "nikel": ["никель", "ni", "7873"],
        "никель": ["nikel", "ni", "7873"],
        "kobalt": ["кобальт", "co", "7880"],
        "кобальт": ["kobalt", "co", "7880"],
        "alyuminiy": ["алюминий", "al", "7927", "8059", "7854"],
        "алюминий": ["alyuminiy", "al", "7927", "8059", "7854"],
        "xrom": ["хром", "cr", "7834", "8035"],
        "хром": ["xrom", "cr", "7834", "8035"],
        "ftorid": ["фторид", "фтор", "8125"],
        "фторид": ["ftorid", "8125"],
        "xlorid": ["хлорид", "хлор", "7616", "7617", "6687"],
        "хлорид": ["xlorid", "7616", "7617", "6687"],
        "fosfat": ["фосфат", "7748", "7018"],
        "фосфат": ["fosfat", "7748", "7018"],
        "fosfor": ["фосфор", "7241"],
        "фосфор": ["fosfor", "7241"],
        "ammoniy": ["аммоний", "nh4", "7747", "7015"],
        "аммоний": ["ammoniy", "nh4", "7747", "7015"],
        "fenol": ["фенол", "7101"],
        "фенол": ["fenol", "7101"],
        "loyqalik": ["мутность", "формазин", "12428", "7271"],
        "loyqa": ["мутность", "формазин", "12428", "7271"],
        "мутность": ["loyqalik", "формазин", "12428", "7271"],
        "rangdorlik": ["цветность", "11431", "7853"],
        "ranglilik": ["цветность", "11431", "7853"],
        "цветность": ["rangdorlik", "11431", "7853"],
        "qattiqlik": ["жесткость", "7680", "9284"],
        "жесткость": ["qattiqlik", "7680", "9284"],
        "kremniy": ["кремний", "sio2", "8934"],
        "кремний": ["kremniy", "sio2", "8934"],
        "rodanid": ["роданид", "тиоцианат", "7618"],
        "роданид": ["rodanid", "тиоцианат", "7618"],
        "bariy": ["барий", "ba", "7107"],
        "барий": ["bariy", "ba", "7107"],
        "selen": ["селен", "se", "7340"],
        "селен": ["selen", "se", "7340"],
        "bor": ["бор", "b", "7337"],
        "бор": ["bor", "b", "7337"],
        "kaliy": ["калий", "k", "8092", "8094"],
        "калий": ["kaliy", "k", "8092", "8094"],
        "natriy": ["натрий", "na", "8062", "8064"],
        "натрий": ["natriy", "na", "8062", "8064"],
        "strontsiy": ["стронций", "sr", "7145"],
        "стронций": ["strontsiy", "sr", "7145"],
        "surma": ["сурьма", "sb", "7204"],
        "сурьма": ["surma", "sb", "7204"],
        "formaldegid": ["формальдегид", "формалин", "9376"],
        "формальдегид": ["formaldegid", "9376"],
        "molibden": ["молибден", "mo", "8086"],
        "молибден": ["molibden", "mo", "8086"],
        "benzol": ["бензол", "7141"],
        "бензол": ["benzol", "7141"],
        "sulfat": ["сульфат", "6693", "7437"],
        "сульфат": ["sulfat", "6693", "7437"],
        "nitrat": ["нитрат", "6696"],
        "нитрат": ["nitrat", "6696"],
        "bpk": ["бпк", "8048"],
        "бпк": ["bpk", "8048"],
        "xpk": ["хпк", "7425", "8048"],
        "хпк": ["xpk", "7425", "8048"],
        "triglitserid": ["триглицерид", "9437"],
        "триглицерид": ["triglitserid", "9437"],
        "ekrosxim": ["экросхим", "экрос", "ekros"],
        "ekros": ["экросхим", "экрос"],
        "экросхим": ["ekrosxim", "ekros", "экрос"],
        "ekroskhim": ["экросхим", "ekrosxim"]
    }

    for word in lower_q.split():
        if word in synonyms:
            variants.extend(synonyms[word])

    return list(dict.fromkeys([v for v in variants if v]))


async def search_products(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Mahsulot, standart, standart-titr yoki xizmatlarni aqlli qidirish.
    Titr nomi, kimyoviy formula, kod, standart yoki tavsif bo'yicha qidiradi.
    Lotincha va kirillcha transliteratsiyani qo'llab-quvvatlaydi.
    """
    db = await get_db()
    try:
        variants = _get_search_variants(query)
        primary_query = variants[0]
        
        # Barcha mahsulotlarni toifasi bilan olamiz va aqlli ball (score) bo'yicha saralaymiz
        cursor = await db.execute(
            """
            SELECT p.*, c.name as category_name, c.icon as category_icon
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            """
        )
        rows = await cursor.fetchall()
        all_products = [dict(row) for row in rows]
        
        scored_results = []
        for p in all_products:
            p_name = (p.get("name") or "").lower()
            p_code = (p.get("code") or "").lower()
            p_standard = (p.get("standard") or "").lower()
            p_desc = (p.get("description") or "").lower()
            full_text = f"{p_name} {p_code} {p_standard} {p_desc}"
            
            score = 0
            
            for v in variants:
                v_lower = v.lower()
                words = [w for w in v_lower.split() if len(w) > 1]
                
                # To'liq moslik yoki boshlanish
                if v_lower in p_name:
                    score = max(score, 100 + (20 if p_name.startswith(v_lower) else 10))
                if v_lower in p_code:
                    score = max(score, 90)
                if v_lower in p_standard:
                    score = max(score, 70)
                if v_lower in p_desc:
                    score = max(score, 50)
                    
                # Har bir so'z bo'yicha tekshirish (multi-word match)
                if words:
                    all_words_in_name = all(w in p_name for w in words)
                    all_words_in_full = all(w in full_text for w in words)
                    
                    if all_words_in_name:
                        score = max(score, 85)
                    elif all_words_in_full:
                        score = max(score, 60)
            
            if score > 0:
                scored_results.append((score, p))
        
        # Ball bo'yicha kamayish tartibida saralash
        scored_results.sort(key=lambda x: (-x[0], x[1]["id"]))
        return [item[1] for item in scored_results[:limit]]
    finally:
        await db.close()


async def log_search(user_id: int, query: str):
    """Qidiruv so'rovini tarixga saqlash."""
    db = await get_db()
    try:
        await db.execute(
            "INSERT INTO search_logs (user_id, query) VALUES (?, ?)",
            (user_id, query)
        )
        await db.commit()
    finally:
        await db.close()


async def add_user(user_id: int, username: Optional[str], full_name: str, language: str = "uz"):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish yoki ma'lumotlarini yangilash."""
    db = await get_db()
    try:
        await db.execute(
            """
            INSERT INTO users (user_id, username, full_name, language)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
            """,
            (user_id, username, full_name, language)
        )
        await db.commit()
    finally:
        await db.close()


async def get_user_language(user_id: int) -> str:
    """Foydalanuvchi tanlagan tilni olish ('uz' yoki 'ru')."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row and row[0]:
            return row[0]
        return "uz"
    finally:
        await db.close()


async def set_user_language(user_id: int, language: str):
    """Foydalanuvchi tilini yangilash."""
    lang = "ru" if language.lower().startswith("ru") else "uz"
    db = await get_db()
    try:
        await db.execute(
            """
            INSERT INTO users (user_id, language)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET language = excluded.language
            """,
            (user_id, lang)
        )
        await db.commit()
    finally:
        await db.close()


# ==========================================
# SAVATCHA (SHOPPING CART) FUNKSIYALARI
# ==========================================

async def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> int:
    """Mahsulotni savatchaga qo'shish yoki miqdorini oshirish."""
    db = await get_db()
    try:
        await db.execute(
            """
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, product_id) DO UPDATE SET
                quantity = cart.quantity + excluded.quantity
            """,
            (user_id, product_id, quantity)
        )
        await db.commit()
        
        # Yangi miqdorni qaytarish
        cursor = await db.execute(
            "SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        row = await cursor.fetchone()
        return row[0] if row else quantity
    finally:
        await db.close()


async def get_cart(user_id: int) -> List[Dict[str, Any]]:
    """Foydalanuvchining savatchasidagi barcha mahsulotlarni olish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """
            SELECT 
                c.id as cart_item_id,
                c.user_id,
                c.product_id,
                c.quantity,
                p.name as product_name,
                p.code as product_code,
                p.standard as product_standard,
                p.accuracy_class,
                p.measurement_range,
                p.price as product_price,
                p.is_service,
                cat.name as category_name,
                cat.icon as category_icon
            FROM cart c
            JOIN products p ON c.product_id = p.id
            LEFT JOIN categories cat ON p.category_id = cat.id
            WHERE c.user_id = ?
            ORDER BY c.id ASC
            """,
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def get_cart_item_count(user_id: int) -> int:
    """Savatchadagi jami mahsulotlar soni."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return int(row[0]) if row else 0
    finally:
        await db.close()


async def get_cart_item(user_id: int, product_id: int) -> Optional[Dict[str, Any]]:
    """Savatchadagi aniq bitta mahsulot holatini olish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def update_cart_quantity(user_id: int, product_id: int, delta: int) -> int:
    """Savatchadagi mahsulot sonini o'zgartirish (+1 yoki -1). Agar <=0 bo'lsa o'chiriladi."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        row = await cursor.fetchone()
        if not row:
            if delta > 0:
                await db.execute(
                    "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                    (user_id, product_id, delta)
                )
                await db.commit()
                return delta
            return 0
        
        current_q = row[0]
        new_q = current_q + delta
        if new_q <= 0:
            await db.execute(
                "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )
            await db.commit()
            return 0
        else:
            await db.execute(
                "UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?",
                (new_q, user_id, product_id)
            )
            await db.commit()
            return new_q
    finally:
        await db.close()


async def remove_from_cart(user_id: int, product_id: int) -> bool:
    """Mahsulotni savatchadan butunlay o'chirish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def clear_cart(user_id: int) -> bool:
    """Foydalanuvchi savatchasini butunlay tozalash."""
    db = await get_db()
    try:
        cursor = await db.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        await db.commit()
        return cursor.rowcount > 0
    finally:
        await db.close()


async def create_order_from_cart(
    user_id: int,
    full_name: str,
    phone_number: str,
    notes: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Savatchadagi barcha mahsulotlardan umumiy buyurtma shakllantirish va savatni tozalash."""
    cart_items = await get_cart(user_id)
    if not cart_items:
        return None

    # Buyurtma matnini shakllantirish
    item_lines = []
    total_qty = 0
    for idx, item in enumerate(cart_items, 1):
        name = item.get("product_name", "")
        code = item.get("product_code", "")
        code_str = f" ({code})" if code else ""
        qty = item.get("quantity", 1)
        total_qty += qty
        item_lines.append(f"{idx}. {name}{code_str} — {qty} ta/шт")

    items_summary = "\n".join(item_lines)

    db = await get_db()
    try:
        cursor = await db.execute(
            """
            INSERT INTO orders (user_id, full_name, phone_number, item_name, item_type, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                full_name,
                phone_number,
                f"Savatcha buyurtmasi ({total_qty} ta element)",
                "Savatcha",
                f"Tanlangan mahsulotlar:\n{items_summary}\n\nQo'shimcha izoh:\n{notes or 'Mavjud emas'}"
            )
        )
        order_id = cursor.lastrowid
        
        # Savatni tozalash
        await db.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        await db.commit()

        return {
            "order_id": order_id,
            "total_items": total_qty,
            "items_summary": items_summary,
            "full_name": full_name,
            "phone_number": phone_number,
            "notes": notes
        }
    finally:
        await db.close()


# ==========================================
# ARIZALAR VA ADMIN FUNKSIYALARI
# ==========================================

async def create_order(
    user_id: int,
    full_name: str,
    phone_number: str,
    item_name: Optional[str] = None,
    item_type: Optional[str] = None,
    notes: Optional[str] = None
) -> int:
    """Yangi buyurtma yoki maslahat arizasini yaratish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """
            INSERT INTO orders (user_id, full_name, phone_number, item_name, item_type, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, full_name, phone_number, item_name, item_type, notes)
        )
        await db.commit()
        return cursor.lastrowid
    finally:
        await db.close()


async def get_recent_orders(limit: int = 10) -> List[Dict[str, Any]]:
    """Oxirgi arizalarni olish (Admin uchun)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


async def get_stats() -> Dict[str, int]:
    """Bot statistikasi (Admin uchun)."""
    db = await get_db()
    try:
        users_c = await db.execute("SELECT COUNT(*) FROM users")
        total_users = (await users_c.fetchone())[0]

        products_c = await db.execute("SELECT COUNT(*) FROM products")
        total_products = (await products_c.fetchone())[0]

        orders_c = await db.execute("SELECT COUNT(*) FROM orders")
        total_orders = (await orders_c.fetchone())[0]

        searches_c = await db.execute("SELECT COUNT(*) FROM search_logs")
        total_searches = (await searches_c.fetchone())[0]

        return {
            "users": total_users,
            "products": total_products,
            "orders": total_orders,
            "searches": total_searches
        }
    finally:
        await db.close()


async def add_product(
    category_id: int,
    name: str,
    code: str,
    standard: str,
    accuracy_class: str,
    measurement_range: str,
    price: str,
    description: str,
    is_service: int = 0
) -> int:
    """Yangi mahsulot kiritish."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """
            INSERT INTO products (
                category_id, name, code, standard, accuracy_class,
                measurement_range, price, description, is_service
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                category_id, name, code, standard, accuracy_class,
                measurement_range, price, description, is_service
            )
        )
        await db.commit()
        return cursor.lastrowid
    finally:
        await db.close()


async def get_all_products_count() -> int:
    """Barcha mahsulotlar soni."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT COUNT(*) FROM products")
        return (await cursor.fetchone())[0]
    finally:
        await db.close()
