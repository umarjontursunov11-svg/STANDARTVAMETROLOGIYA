import asyncio
import sys

# Ensure the project root is in the Python path
sys.path.append(r"c:/Users/User/Desktop/Metrologiya")

from bot.database import add_product

# List of GSO products to be added. Only name and code are provided; other fields are left empty.
PRODUCTS = [
    {"name": "ГСО ХЛОРИД-ИОНОВ (9.5-10.5)", "code": "ГСО 7478-98"},
    {"name": "Ионов железа (III)", "code": "ГСО 7476-98"},
    {"name": "Сульфат- ионов", "code": "ГСО 7253-96"},
    {"name": "ГСО ИОНОВ КАДМИЯ (0.95-1.05)", "code": "ГСО 7472-98"},
    {"name": "ГСО ионов меди", "code": "ГСО 7255-96"},
    {"name": "ГСО хлорид ионов", "code": "ГСО 7262-96"},
    {"name": "ГСО ионов хрома", "code": "ГСО 7257-96"},
    {"name": "ГСО общей жесткости воды", "code": "ГСО 8206-2002"},
    {"name": "ГСО фенола", "code": "ГСО 7270-96"},
    {"name": "ГСО ионов цинка", "code": "ГСО 7256-96"},
    {"name": "ГСО ионов цинка", "code": "ГСО 7470-98"},
    {"name": "ГСО ионов цинка", "code": "ГСО 7471-98"},
    {"name": "ГСО ионов меди", "code": "ГСО 8205-2002"},
    {"name": "ГСО сульфат ионов", "code": "ГСО 7480-98"},
    {"name": "ГСО ионов аммония", "code": "ГСО 7259-96"},
    {"name": "ГСО ионов мышьяка", "code": "ГСО 7264-96"},
    {"name": "ГСО нитрат ионов", "code": "ГСО 7258-96"},
    {"name": "Ионов никеля", "code": "ГСО 7265-96"},
    {"name": "Ионов висмута", "code": "ГСО 7477-98"},
    {"name": "Ионов марганца", "code": "ГСО 7266-96"},
    {"name": "Ионов свинца", "code": "ГСО 7252-96"},
    {"name": "Ионов ртути", "code": "ГСО 7263-96"},
]

CATEGORY_ID = 1  # "Standart Namunalar (GSO)"

async def main():
    added = 0
    for prod in PRODUCTS:
        await add_product(
            category_id=CATEGORY_ID,
            name=prod["name"],
            code=prod["code"],
            standard="",
            accuracy_class="",
            measurement_range="",
            price="",
            description="",
            is_service=0,
        )
        added += 1
    print(f"✅ Added {added} GSO products to category {CATEGORY_ID}.")

if __name__ == "__main__":
    asyncio.run(main())
