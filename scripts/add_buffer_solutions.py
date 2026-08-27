"""
Bufer eritmalari (pH buferlar) va Konduktometr kalibrlash eritmalarini bazaga kiritish skripti.
"""

import asyncio
import sys

sys.path.append(r"c:/Users/User/Desktop/Metrologiya")

from bot.database import get_db

BUFFER_PRODUCTS = [
    # --- pH Standart Bufer Eritmalari (Category 2) ---
    {
        "category_id": 2,
        "name": "Буферный раствор рН=1,48",
        "code": "рН 1.48 (ГОСТ 8.135)",
        "standard": "ГОСТ 8.135-2004 / ISO 17034",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 1.48 (25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "pH-metrlar va elektrodlarni kislotali sohada kalibrlash uchun tayyor bufer eritma.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan.\n🎯 Qo'llanilishi: Laboratoriya pH-metrlari va sanoat analizatorlarini kalibrlash."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=1,68",
        "code": "рН 1.68 (ГОСТ 8.135)",
        "standard": "ГОСТ 8.135-2004 / ISO 17034",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 1.68 (25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "pH-metrlar va elektrodlarni kislotali sohada kalibrlash uchun tayyor bufer eritma (Kaliy tetraoksalat).\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=4,01",
        "code": "рН 4.01 (ГОСТ 8.135)",
        "standard": "ГОСТ 8.135-2004 / ISO 17034",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 4.01 (25 °C да), 250 / 500 мл / 1 L",
        "price": "Shartnoma asosida",
        "description": "pH-metrlar, ionomerlar va laboratoriya elektrodlarini 2 nuqtali kalibrlash uchun asosiy kislotali bufer eritma (Kaliy biftalat).\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=6,86",
        "code": "рН 6.86 (ГОСТ 8.135)",
        "standard": "ГОСТ 8.135-2004 / ISO 17034",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 6.86 (25 °C да), 250 / 500 мл / 1 L",
        "price": "Shartnoma asosida",
        "description": "pH-metrlarni neytral sohada kalibrlash uchun standart fosfat bufer eritmasi (Kaliy digidrofosfat va Natriy gidrofosfat).\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=7,01",
        "code": "рН 7.01 (NIST)",
        "standard": "NIST / ISO 17034 / ГОСТ 8.135",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 7.01 (25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Xalqaro NIST shkalasi bo'yicha neytral pH kalibrlash bufer eritmasi.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=9,18",
        "code": "рН 9.18 (ГОСТ 8.135)",
        "standard": "ГОСТ 8.135-2004 / ISO 17034",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 9.18 (25 °C да), 250 / 500 мл / 1 L",
        "price": "Shartnoma asosida",
        "description": "Ishqoriy sohadagi pH-metr va elektrodlarni kalibrlash uchun borat bufer eritmasi (Natriy tetraborat / Bura).\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=10,01",
        "code": "рН 10.01 (NIST)",
        "standard": "NIST / ISO 17034 / ГОСТ 8.135",
        "accuracy_class": "Аттестатланган аниқлик ±0.01 pH",
        "measurement_range": "pH = 10.01 (25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Xalqaro NIST shkalasi bo'yicha yuqori ishqoriy sohada pH-metrlarni kalibrlash bufer eritmasi.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Буферный раствор рН=11,00",
        "code": "рН 11.00 (ГОСТ 8.135)",
        "standard": "ГОСТ 8.135-2004 / ISO 17034",
        "accuracy_class": "Аттестатланган аниқлик ±0.02 pH",
        "measurement_range": "pH = 11.00 (25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Kuchli ishqoriy muhitda ishlovchi pH-metrlar va elektrodlarni kalibrlash bufer eritmasi.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },

    # --- Konduktometr va TDS Kalibrlash Eritmalari (Category 2) ---
    {
        "category_id": 2,
        "name": "Калибровочный раствор для кондуктометра 5 мкСм/см",
        "code": "CAL-EC-5",
        "standard": "ГОСТ 22171-90 / ISO 17034 / OIML R 56",
        "accuracy_class": "Аттестатланган хатолик ±1%",
        "measurement_range": "5.0 µS/cm (25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Ultra toza suv, deionizatsiyalangan suv va past o'tkazuvchanlikka ega suyuqliklar konduktometrlarini aniq kalibrlash standarti.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Калибровочный раствор для кондуктометра 1413 мкСм/см",
        "code": "CAL-EC-1413",
        "standard": "ГОСТ 22171-90 / ISO 17034 / OIML R 56",
        "accuracy_class": "Аттестатланган хатолик ±1%",
        "measurement_range": "1413 µS/cm (1.413 mS/cm, 25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Konduktometrlar, solinomerlar va suv sifati analizatorlarini kalibrlash uchun eng ko'p qo'llaniladigan xalqaro asosiy standart eritma (0.01 M KCl asosida).\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Калибровочный раствор для кондуктометра 5000 мкСм/см",
        "code": "CAL-EC-5000",
        "standard": "ГОСТ 22171-90 / ISO 17034 / OIML R 56",
        "accuracy_class": "Аттестатланган хатолик ±1%",
        "measurement_range": "5000 µS/cm (5.0 mS/cm, 25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "O'rta va yuqori mineralizatsiyalangan suvlar hamda sanoat oqovalari konduktometrlarini kalibrlash eritmasi.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Калибровочный раствор для кондуктометра 80000 мкСм/см",
        "code": "CAL-EC-80000",
        "standard": "ГОСТ 22171-90 / ISO 17034 / OIML R 56",
        "accuracy_class": "Аттестатланган хатолик ±1%",
        "measurement_range": "80000 µS/cm (80.0 mS/cm, 25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Yuqori tuzli sho'r suvlar, dengiz suvlari va kimyoviy eritmalar konduktometrlarini kalibrlash standarti.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Калибровочный раствор для кондуктометра 111800 мкСм/см",
        "code": "CAL-EC-111800",
        "standard": "ГОСТ 22171-90 / ISO 17034 / OIML R 56",
        "accuracy_class": "Аттестатланган хатолик ±1%",
        "measurement_range": "111800 µS/cm (111.8 mS/cm, 25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "Yuqori konsentratsiyali elektrolitlar va sanoat konduktometrik datchiklarini kalibrlash uchun birlamchi standart eritma (1.0 M KCl asosida).\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    },
    {
        "category_id": 2,
        "name": "Калибровочный раствор 1382 мг/л (TDS / Солемер)",
        "code": "CAL-TDS-1382",
        "standard": "TDS / NaCl Standard / ISO 17034",
        "accuracy_class": "Аттестатланган хатолик ±1%",
        "measurement_range": "1382 mg/L (ppm NaCl, 25 °C да), 250 / 500 мл",
        "price": "Shartnoma asosida",
        "description": "TDS-metrlar, solinomerlar va suv tozalash tizimlari analizatorlarini kalibrlash uchun standart eritma.\n\n🏭 Ishlab chiqaruvchi: «ЭКРОСХИМ» Заводи\n📜 Sifat standarti: ISO 17034 talablari asosida tayyorlangan."
    }
]

async def main():
    db = await get_db()
    try:
        added = 0
        updated = 0
        for prod in BUFFER_PRODUCTS:
            cursor = await db.execute(
                "SELECT id FROM products WHERE category_id = ? AND name = ?",
                (prod["category_id"], prod["name"])
            )
            row = await cursor.fetchone()
            if row:
                await db.execute(
                    """
                    UPDATE products SET 
                        code = ?, standard = ?, accuracy_class = ?, 
                        measurement_range = ?, price = ?, description = ?
                    WHERE id = ?
                    """,
                    (
                        prod["code"], prod["standard"], prod["accuracy_class"],
                        prod["measurement_range"], prod["price"], prod["description"],
                        row["id"]
                    )
                )
                updated += 1
            else:
                await db.execute(
                    """
                    INSERT INTO products (
                        category_id, name, code, standard, accuracy_class,
                        measurement_range, price, description, is_service
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
                    """,
                    (
                        prod["category_id"], prod["name"], prod["code"], prod["standard"],
                        prod["accuracy_class"], prod["measurement_range"],
                        prod["price"], prod["description"]
                    )
                )
                added += 1
        await db.commit()
        print(f"Bufer eritmalari bazaga yuklandi: {added} ta yangi qoshildi, {updated} ta yangilandi.")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
