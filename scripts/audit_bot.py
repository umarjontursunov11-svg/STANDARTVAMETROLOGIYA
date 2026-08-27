"""
Botning to'liq diagnostika va test skripti (UTF-8 xavfsiz).
"""

import os
import sys
import re
import asyncio

sys.path.append(r"c:/Users/User/Desktop/Metrologiya")

from bot.config import config
from bot.database import init_db, get_db, get_categories, get_stats
from bot.utils.localization import TEXTS, CATEGORY_TRANSLATIONS
from bot.handlers import all_routers

def audit_localization():
    sys.stdout.buffer.write(b"\n--- 1. LOKALIZATSIYA KALITLARINI TEKSHIRISH ---\n")
    get_text_pattern = re.compile(r'get_text\(\s*[\"\']([a-zA-Z0-9_]+)[\"\']')
    missing = []
    
    for root, dirs, files in os.walk(r"c:/Users/User/Desktop/Metrologiya/bot"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = get_text_pattern.findall(content)
                    for key in matches:
                        if key not in TEXTS:
                            missing.append((file, key))
    
    if missing:
        msg = f"[XATO] Topilgan yetishmayotgan kalitlar: {missing}\n"
    else:
        msg = "[OK] Barcha get_text() kalitlari TEXTS lug'atida mavjud!\n"
    sys.stdout.buffer.write(msg.encode("utf-8"))

    # Check uz and ru translations in each text
    lang_issues = []
    for k, v in TEXTS.items():
        if isinstance(v, dict):
            if "uz" not in v or "ru" not in v:
                lang_issues.append(k)
    if lang_issues:
        msg2 = f"[XATO] uz/ru to'liq bo'lmagan kalitlar: {lang_issues}\n"
    else:
        msg2 = "[OK] Barcha matnlarda 'uz' va 'ru' tarjimalari to'liq!\n"
    sys.stdout.buffer.write(msg2.encode("utf-8"))

def audit_routers():
    sys.stdout.buffer.write(b"\n--- 2. ROUTERLAR VA HANDLERLAR TARTIBI ---\n")
    msg = f"Ulangan routerlar soni: {len(all_routers)}\n"
    sys.stdout.buffer.write(msg.encode("utf-8"))
    for idx, r in enumerate(all_routers, 1):
        m = f"  {idx}. Router: {r.name or 'Router'}\n"
        sys.stdout.buffer.write(m.encode("utf-8"))

async def audit_database():
    sys.stdout.buffer.write(b"\n--- 3. MA'LUMOTLAR BAZASI VA INTEGRATSIYA ---\n")
    await init_db()
    cats = await get_categories()
    m1 = f"[OK] Jami kategoriyalar: {len(cats)}\n"
    sys.stdout.buffer.write(m1.encode("utf-8"))
    stats = await get_stats()
    m2 = f"[OK] Statistika: {stats}\n"
    sys.stdout.buffer.write(m2.encode("utf-8"))

    # Check all category translations
    for cat in cats:
        cid = cat["id"]
        if cid not in CATEGORY_TRANSLATIONS:
            m3 = f"[OGOHLANTIRISH] Kategoriya ID {cid} ('{cat['name']}') uchun CATEGORY_TRANSLATIONS mavjud emas!\n"
            sys.stdout.buffer.write(m3.encode("utf-8"))

async def main():
    audit_localization()
    audit_routers()
    await audit_database()
    sys.stdout.buffer.write(b"\nAudit muvaffaqiyatli yakunlandi!\n")

if __name__ == "__main__":
    asyncio.run(main())
