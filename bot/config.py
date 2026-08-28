"""
Bot konfiguratsiyasi va muhit o'zgaruvchilari (Environment variables) sozlamalari.
"""

import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()


@dataclass
class CompanyConfig:
    name: str = os.getenv("COMPANY_NAME", 'OOO "STANDART VA METROLOGIYA"')
    phone: str = os.getenv("COMPANY_PHONE", "+998 90 939-71-83, +998 98 361-71-83, +998 55 503-47-15")
    email: str = os.getenv("COMPANY_EMAIL", "standartvametrologiya@gmail.com")
    website: str = os.getenv("COMPANY_WEBSITE", "")
    address: str = os.getenv(
        "COMPANY_ADDRESS",
        "Toshkent sh., Sergeli t., Uzumzor ko'chasi, 16-tupik, 18-xonadon"
    )
    work_hours: str = os.getenv(
        "COMPANY_WORK_HOURS",
        "Dushanba - Juma: 09:00 - 18:00"
    )
    telegram_support: str = os.getenv("COMPANY_TELEGRAM_SUPPORT", "@standartgso_admin1")


@dataclass
class AIConfig:
    provider: str = os.getenv("AI_PROVIDER", "auto")  # auto, gemini, openai, deepseek
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    api_key: str = os.getenv("AI_API_KEY", "")  # Umumiy fallback kalit
    model: str = os.getenv("AI_MODEL", "")
    is_enabled: bool = os.getenv("AI_ENABLED", "True").lower() in ("true", "1", "yes")


@dataclass
class BotConfig:
    token: str = os.getenv("BOT_TOKEN", "")
    admin_ids: List[int] = field(default_factory=list)
    orders_channel_id: int = 0
    database_path: str = os.getenv("DATABASE_PATH", "metrologiya.db")
    company: CompanyConfig = field(default_factory=CompanyConfig)
    ai: AIConfig = field(default_factory=AIConfig)

    def __post_init__(self):
        # Admin ID larini yuklash
        admin_raw = os.getenv("ADMIN_IDS", "")
        ids = []
        for item in admin_raw.split(","):
            item = item.strip()
            if not item:
                continue
            try:
                ids.append(int(item))
            except ValueError:
                pass
        self.admin_ids = ids

        # Buyurtmalar guruhi/kanali ID si
        ch_raw = os.getenv("ORDERS_CHANNEL_ID", "-1003964640399").strip()
        if ch_raw and ch_raw.lstrip("-").isdigit():
            self.orders_channel_id = int(ch_raw)


config = BotConfig()
