"""
Metrologiya AI (Sun'iy Intellekt) Xizmati.
Gemini, OpenAI, DeepSeek va aqlli lokal metrologiya bilimlar bazasi bilan integratsiya.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from collections import defaultdict

from bot.config import config
from bot.database.models import search_products, get_categories

logger = logging.getLogger(__name__)

# Foydalanuvchilarning muloqot tarixi (oxirgi 10 ta xabar)
USER_CONVERSATIONS: Dict[int, List[Dict[str, str]]] = defaultdict(list)
MAX_HISTORY = 8


METROLOGY_SYSTEM_PROMPT = """
Siz "O'zbekiston Standartlashtirish va Metrologiya Markazi"ning professional va do'stona Sun'iy Intellekt (AI) Metrolog Maslahatchisisiz.
Ismingiz: "AI Metrolog".

Sizning vazifangiz:
1. Laboratoriyalar, korxonalar va mijozlarga metrologiya, standartlashtirish, sertifikatlashtirish, qiyoslash (poverka), kalibrlash va sinov uskunalarini attestatsiyalash bo'yicha professional maslahat berish.
2. Davlat Standart Namunalar (GSO / МСО) — «ЭКРОСХИМ» Заводи (ISO 17034 standarti), bufer eritmalari (pH 1.68, 3.56, 4.01, 6.86, 9.18, 12.45), standart titrlar (fiksanallar), kimyoviy reaktivlar (XCh, ChDA, Ch), kapillyar viskozimetrlar (ВПЖ-2, ВПЖ-4), areometrlar (АОН-1, АНТ-1, АНТ-2, АМ, АМТ), termometrlar (ТЛ-2, ТЛ-4), neft ruletkalari (Р10УЗГ), gaz hisoblagichlar (ГСБ-400) va boshqa o'lchash vositalari bo'yicha aniq ma'lumot berish.
3. Asbob yoki kimyoviy standart tanlashda yordam berish, kerakli standartlar (GOST, O'z DSt, ISO/IEC 17025, ISO 17034, SanPiN) va tahlil usullari (AAS, ICP, fotometriya, titrimetriya, xromatografiya) bo'yicha tushuntirish berish.
4. Foydalanuvchiga kerak bo'lsa korxonamizdan buyurtma berish yoki ariza qoldirish uchun "📝 Ariza / Maslahat olish" bo'limidan foydalanishni taklif qilish.

Javob berish qoidalari:
- Foydalanuvchi qaysi tilda murojaat qilsa (O'zbekcha yoki Ruscha), aynan o'sha tilda javob bering.
- Javoblarni Telegram HTML formatida chiroyli qiling: <b>, <i>, <code>, emoji va ro'yxatlardan foydalaning.
- Javoblaringiz aniq, professional, tushunarli va dalillarga asoslangan bo'lsin.
- Agar ma'lumotlar bazasidan tegishli mahsulotlar taqdim etilgan bo'lsa, ularning nomi, kodi va standartini javobingizda eslatib o'ting.
"""


class AIService:
    """Sun'iy intellekt xizmati provayderi."""

    def __init__(self):
        self.provider = config.ai.provider.lower()
        self._gemini_client = None
        self._openai_client = None
        self._deepseek_client = None
        self._init_clients()

    def _init_clients(self):
        """AI mijozlarini initsializatsiya qilish."""
        # 1. Gemini
        gemini_key = config.ai.gemini_api_key or config.ai.api_key
        if gemini_key:
            model_name = config.ai.model or "gemini-3.7-flash"
            # Try new google.genai SDK first
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=gemini_key)
                self._gemini_model_name = model_name
                logger.info(f"Google GenAI mijozi muvaffaqiyatli ulandi (model: {model_name})")
            except Exception as e1:
                try:
                    import google.generativeai as genai_legacy
                    genai_legacy.configure(api_key=gemini_key)
                    self._gemini_client = genai_legacy.GenerativeModel(
                        model_name=model_name,
                        system_instruction=METROLOGY_SYSTEM_PROMPT
                    )
                    self._gemini_model_name = model_name
                    logger.info(f"Google Gemini (legacy) muvaffaqiyatli ulandi (model: {model_name})")
                except Exception as e2:
                    logger.warning(f"Gemini AI ulanishida xatolik: {e1} / {e2}")

        # 2. OpenAI
        openai_key = config.ai.openai_api_key
        if openai_key:
            try:
                from openai import AsyncOpenAI
                self._openai_client = AsyncOpenAI(api_key=openai_key)
                logger.info("OpenAI mijozi muvaffaqiyatli ulandi")
            except Exception as e:
                logger.warning(f"OpenAI ulanishida xatolik: {e}")

        # 3. DeepSeek
        deepseek_key = config.ai.deepseek_api_key
        if deepseek_key:
            try:
                from openai import AsyncOpenAI
                self._deepseek_client = AsyncOpenAI(
                    api_key=deepseek_key,
                    base_url="https://api.deepseek.com"
                )
                logger.info("DeepSeek AI mijozi muvaffaqiyatli ulandi")
            except Exception as e:
                logger.warning(f"DeepSeek ulanishida xatolik: {e}")

    async def get_response(self, user_id: int, user_message: str) -> str:
        """
        Foydalanuvchi xabariga AI maslahatchi javobini olish.
        """
        # 1. Kontekst uchun mahsulotlar bazasidan ma'lumot qidirish (RAG)
        relevant_products = await self._search_relevant_products(user_message)
        context_text = self._build_context(relevant_products)

        # 2. Tarixni yangilash
        history = USER_CONVERSATIONS[user_id]
        history.append({"role": "user", "content": user_message})
        if len(history) > MAX_HISTORY:
            history = history[-MAX_HISTORY:]
            USER_CONVERSATIONS[user_id] = history

        # 3. Faol provayder orqali javob olish
        response_text = None

        # Auto yoki Gemini
        if (self.provider in ("auto", "gemini")) and self._gemini_client:
            response_text = await self._ask_gemini(user_message, context_text, history)

        # OpenAI
        if not response_text and (self.provider in ("auto", "openai")) and self._openai_client:
            response_text = await self._ask_openai(user_message, context_text, history)

        # DeepSeek
        if not response_text and (self.provider in ("auto", "deepseek")) and self._deepseek_client:
            response_text = await self._ask_deepseek(user_message, context_text, history)

        # 4. Agar API kalit bo'lmasa yoki tashqi xizmat ishlamasa — Smart Built-in Fallback
        if not response_text:
            response_text = self._smart_built_in_consultant(user_message, relevant_products)

        # Javobni tarixga qo'shish
        history.append({"role": "assistant", "content": response_text})
        USER_CONVERSATIONS[user_id] = history

        return response_text

    async def _search_relevant_products(self, query: str) -> List[Dict[str, Any]]:
        """Qidiruv so'ziga mos mahsulotlarni topish (RAG konteksti uchun)."""
        try:
            return await search_products(query, limit=5)
        except Exception:
            return []

    def _build_context(self, products: List[Dict[str, Any]]) -> str:
        """Mahsulotlar kontekstini shakllantirish."""
        if not products:
            return ""
        lines = ["\n[Katalogimizdagi mos keluvchi mahsulotlar va standartlar]:"]
        for p in products:
            p_name = p.get("name", "")
            p_code = p.get("code", "")
            p_std = p.get("standard", "")
            p_range = p.get("measurement_range", "")
            lines.append(f"- {p_name} (Kodi: {p_code}, Standart: {p_std}, Diapazon: {p_range})")
        return "\n".join(lines)

    async def _ask_gemini(self, message: str, context: str, history: List[Dict[str, str]]) -> Optional[str]:
        """Google Gemini API orqali javob olish."""
        gemini_key = config.ai.gemini_api_key or config.ai.api_key
        if not gemini_key:
            return None

        # Format prompt with context
        full_user_msg = message
        if context:
            full_user_msg = f"{message}\n\n{context}"

        # Build contents from history
        contents = []
        for h in history[:-1]:
            role = "user" if h["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": h["content"]}]})
        contents.append({"role": "user", "parts": [{"text": full_user_msg}]})

        payload = {
            "system_instruction": {"parts": [{"text": METROLOGY_SYSTEM_PROMPT}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }

        # Try models in order
        candidate_models = [
            config.ai.model or "gemini-3.6-flash",
            "gemini-3.6-flash",
            "gemini-3.7-flash",
            "gemini-flash-latest"
        ]
        # Remove duplicates while preserving order
        candidate_models = list(dict.fromkeys([m for m in candidate_models if m]))

        import aiohttp
        for model_name in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=25)) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            candidates = data.get("candidates", [])
                            if candidates:
                                text = candidates[0]["content"]["parts"][0]["text"]
                                return self._clean_markdown_to_html(text)
                        else:
                            err_body = await resp.text()
                            logger.warning(f"Gemini ({model_name}) status {resp.status}: {err_body[:200]}")
            except Exception as e:
                logger.warning(f"Gemini ({model_name}) so'rovida xatolik: {e}")

        return None

    async def _ask_openai(self, message: str, context: str, history: List[Dict[str, str]]) -> Optional[str]:
        """OpenAI API orqali javob olish."""
        try:
            messages = [{"role": "system", "content": METROLOGY_SYSTEM_PROMPT}]
            for h in history[:-1]:
                messages.append({"role": h["role"], "content": h["content"]})
            
            user_content = message
            if context:
                user_content = f"{message}\n\n{context}"
            messages.append({"role": "user", "content": user_content})

            model_name = config.ai.model or "gpt-4o-mini"
            resp = await self._openai_client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            raw = resp.choices[0].message.content
            return self._clean_markdown_to_html(raw)
        except Exception as e:
            logger.error(f"OpenAI chaqiruvida xatolik: {e}")
            return None

    async def _ask_deepseek(self, message: str, context: str, history: List[Dict[str, str]]) -> Optional[str]:
        """DeepSeek API orqali javob olish."""
        try:
            messages = [{"role": "system", "content": METROLOGY_SYSTEM_PROMPT}]
            for h in history[:-1]:
                messages.append({"role": h["role"], "content": h["content"]})
            
            user_content = message
            if context:
                user_content = f"{message}\n\n{context}"
            messages.append({"role": "user", "content": user_content})

            model_name = config.ai.model or "deepseek-chat"
            resp = await self._deepseek_client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            raw = resp.choices[0].message.content
            return self._clean_markdown_to_html(raw)
        except Exception as e:
            logger.error(f"DeepSeek chaqiruvida xatolik: {e}")
            return None

    def _smart_built_in_consultant(self, message: str, products: List[Dict[str, Any]]) -> str:
        """
        API kalit kiritilmagan yoki oflayn holatda ishlaydigan aqlli metrologik ekspert tizimi.
        """
        lower = message.lower()
        is_ru = any(ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for ch in lower)

        # 1. GSO va standart namunalar
        if any(w in lower for w in ["gso", "гсо", "standart namuna", "стандартный образец", "мсо", "mso"]):
            if is_ru:
                res = (
                    "🧪 <b>Государственные стандартные образцы (ГСО):</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "ГСО предназначены для калибровки и поверки спектрофотометров, хроматографов, атомно-абсорбционных (ААС) и пламенно-фотометрических приборов.\n\n"
                    "🏭 <b>Производитель:</b> Завод «ЭКРОСХИМ» (Россия).\n"
                    "📜 <b>Стандарт качества:</b> Изготовлены в строгом соответствии с требованиями международного стандарта <b>ISO 17034</b>.\n\n"
                    "🔹 В наличии образцы ионов металлов (кадмий, медь, железо, марганец, свинец, ртуть, цинк, кобальт, алюминий и др.), "
                    "анионов (нитрит, нитрат, сульфат, фосфат, хлорид, фторид), показателей воды (мутность, цветность, жесткость, БПК, ХПК) и нефтепродуктов.\n"
                )
            else:
                res = (
                    "🧪 <b>Davlat Standart Namunalar (GSO):</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "GSO namunalari laboratoriyalarda analizatorlar, spektrofotometrlar, AAS va xromatograflarni kalibrlash hamda tahlil aniqligini tekshirish uchun qo'llaniladi.\n\n"
                    "🏭 <b>Ishlab chiqaruvchi:</b> «ЭКРОСХИМ» Заводи (Россия).\n"
                    "📜 <b>Sifat standarti:</b> Xalqaro <b>ISO 17034</b> talablari asosida sertifikatlangan.\n\n"
                    "🔹 Katalogimizda og'ir metallar (kadmiy, qo'rg'oshin, simob, mis, temir, rux, marganes), anionlar (nitrit, xlorid, sulfat, fosfat, ftorid), suv ko'rsatkichlari (loyqalik, rangdorlik, qattiqlik, BPK, XPK) mavjud.\n"
                )
            if products:
                res += "\n🔍 <b>Katalogimizdagi mos namunalar:</b>\n"
                for p in products[:4]:
                    res += f"• <b>{p['name']}</b> (<code>{p.get('code','')}</code>)\n"
            return res

        # 2. Poverka (Qiyoslash) va Kalibrlash
        if any(w in lower for w in ["poverka", "поверка", "qiyoslash", "kalibrlash", "калибровка", "attestatsiya", "аттестация"]):
            if is_ru:
                return (
                    "⚙️ <b>Поверка и Калибровка средств измерений:</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "• <b>Поверка (Давлат қиёслови):</b> Обязательная процедура подтверждения соответствия прибора установленным государственным метрологическим требованиям (выдается свидетельство о поверке).\n"
                    "• <b>Калибровка:</b> Определение действительных метрологических характеристик прибора путем сличения с эталоном (выдается сертификат калибровки с указанием погрешности).\n"
                    "• <b>Аттестация:</b> Определение точности и стабильности испытательного оборудования (термошкафы, печи, автоклавы).\n\n"
                    "📝 <i>Для подачи заявки на поверку или калибровку воспользуйтесь кнопкой <b>'📝 Ariza / Maslahat olish'</b>.</i>"
                )
            else:
                return (
                    "⚙️ <b>Qiyoslash (Poverka) va Kalibrlash xizmatlari:</b>\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "• <b>Davlat Qiyoslovi (Poverka):</b> O'lchash vositalarining belgilangan qonuniy metrologik talablarga muvofiqligini tasdiqlash (Davlat qiyoslash guvohnomasi beriladi).\n"
                    "• <b>Kalibrlash:</b> O'lchash vositasining ko'rsatkichlarini yuqori aniqlikdagi etalon bilan solishtirish va aniq xatoligini belgilash (Kalibrlash sertifikati beriladi).\n"
                    "• <b>Attestatsiyalash:</b> Sinov uskunalari (termoshkaflar, pechlar, iqlim kameralari) ning harorat va parametr barqarorligini tasdiqlash.\n\n"
                    "📝 <i>Ariza qoldirish uchun <b>'📝 Ariza / Maslahat olish'</b> tugmasidan foydalaning.</i>"
                )

        # 3. pH Bufer eritmalar
        if any(w in lower for w in ["bufer", "буфер", "ph", "рн"]):
            return (
                "💧 <b>pH Standart Bufer Eritmalari (ГОСТ 8.135-2004):</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "pH-metrlar, ionomerlar va laboratoriya elektrodlarini 1- va 2-toifali aniqlikda kalibrlash uchun tayyor bufer eritmalar:\n\n"
                "• <b>pH 1.68</b> — Kislotali soha (Kaliy tetraoksalat)\n"
                "• <b>pH 3.56</b> — Kislotali ishchi etalon (Kaliy gidrotartrat)\n"
                "• <b>pH 4.01</b> — Kislotali soha (Kaliy gidroftalat)\n"
                "• <b>pH 6.86</b> — Neytral soha (Fosfat buferi)\n"
                "• <b>pH 9.18</b> — Ishqoriy soha (Natriy tetraborat / Bura)\n"
                "• <b>pH 12.45</b> — Kuchli ishqoriy soha (Kaltsiy gidroksid)\n\n"
                "📦 Tayyor eritmalar (250 ml, 500 ml, 1 L) va fiksanal ampulalari mavjud."
            )

        # 4. Fiksanallar (Standart-titrlar)
        if any(w in lower for w in ["fiksanal", "фиксанал", "titr", "титр", "0.1n", "0,1н"]):
            return (
                "⚗️ <b>Standart-titrlar (Fiksanallar):</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Titrimetrik tahlillar uchun aniq 0.1 N (0.1 mol/dm³) konsentratsiyadagi standart eritmalar tayyorlashga mo'ljallangan germetik ampulalar to'plami (10 dona/quti).\n\n"
                "• Kislotalar: <code>HCl</code>, <code>H2SO4</code>, <code>HNO3</code>, <code>H2C2O4</code>\n"
                "• Ishqorlar: <code>NaOH</code>, <code>KOH</code>, <code>Na2CO3</code>\n"
                "• Oksidlovchi/Qaytaruvchilar: <code>KMnO4</code>, <code>Na2S2O3</code>, <code>K2Cr2O7</code>, <code>I2</code>\n"
                "• Kompleksonlar va tuzlar: <code>Trilon B (EDTA)</code>, <code>NaCl</code>, <code>AgNO3</code>, <code>NH4SCN</code>\n\n"
                "🏭 Ishlab chiqaruvchi: «Уралхиминвест» va «Ленреактив»."
            )

        # 5. O'lchash vositalari (Areometr, Viskozimetr, Termometr, Ruletka)
        if any(w in lower for w in ["areometr", "ареометр", "viskozimetr", "вискозиметр", "termometr", "термометр", "ruletka", "рулетка", "manometr", "манометр"]):
            return (
                "🔬 <b>Laboratoriya va sanoat o'lchash vositalari:</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "• <b>Areometrlar:</b> Suyuqliklar zichligini o'lchash (АОН-1, АОН-2, АНТ-1, АНТ-2 neft areometrlari, АМ sut areometrlari).\n"
                "• <b>Kapillyar viskozimetrlar:</b> Kinematik qovushqoqlikni o'lchash (ВПЖ-2, ВПЖ-4).\n"
                "• <b>Termometrlar:</b> Shisha simobli va spirtli termometrlar (ТЛ-2, ТЛ-4, ТЛ-5, ТН).\n"
                "• <b>Neft ruletkalari:</b> Idishlardagi neft sathini o'lchovchi og'irlik yukli ruletkalar (Р10УЗГ, Р20УЗГ).\n"
                "• <b>Gaz hisoblagichlar:</b> Laboratoriya barabanli gaz hisoblagichlari (ГСБ-400).\n\n"
                "Barcha asboblar qiyoslangan va rasmiy Davlat Qiyoslash guvohnomasiga ega."
            )

        # 6. Umumiy javob + topilgan mahsulotlar
        if products:
            res = (
                f"🤖 <b>AI Maslahatchi javobi:</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"So'rovingiz bo'yicha bazamizdan quyidagi standartlar va mahsulotlar topildi:\n\n"
            )
            for p in products:
                res += f"🔹 <b>{p['name']}</b>\n"
                if p.get('code'):
                    res += f"   🔖 Kodi: <code>{p['code']}</code>\n"
                if p.get('standard'):
                    res += f"   📜 Standart: <i>{p['standard']}</i>\n"
                if p.get('measurement_range'):
                    res += f"   📏 Diapazon: {p['measurement_range']}\n"
                res += "\n"
            res += "<i>Batafsil ma'lumot olish yoki buyurtma berish uchun mahsulot qidirish yoki ariza bo'limidan foydalanishingiz mumkin.</i>"
            return res

        # Standart yordam
        if is_ru:
            return (
                "🤖 <b>AI Консультант по Метрологии:</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Я могу помочь вам по следующим направлениям:\n"
                "• Подбор стандартных образцов (ГСО) и буферных растворов рН\n"
                "• Подбор фиксаналов (стандарт-титров) и химических реактивов\n"
                "• Консультация по поверке, калибровке и аттестации приборов\n"
                "• Выбор ареометров (АОН, АНТ), вискозиметров (ВПЖ) и термометров\n\n"
                "<i>Задайте ваш вопрос подробно, и я предоставлю точную информацию!</i>"
            )
        else:
            return (
                "🤖 <b>AI Metrolog Maslahatchi:</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Men sizga quyidagi masalalarda yordam bera olaman:\n"
                "• Davlat Standart Namunalar (GSO) va pH bufer eritmalarini tanlash\n"
                "• Standart-titrlar (fiksanallar) va kimyoviy reaktivlar bo'yicha ma'lumot\n"
                "• Qiyoslash (poverka), kalibrlash va attestatsiyalash talablari\n"
                "• Areometrlar (AON, ANT), viskozimetrlar (VPJ) va termometrlarni tanlash\n\n"
                "<i>Savolingizni aniqroq yozing yoki kerakli standart/asbob nomini kiriting!</i>"
            )

    def _clean_markdown_to_html(self, text: str) -> str:
        """Markdown formatini Telegram HTML formatiga o'tkazish."""
        if not text:
            return ""
        
        # Soddalashtirilgan xavfsiz konvertatsiya
        t = text
        # **bold** -> <b>bold</b>
        import re
        t = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', t)
        # *italic* -> <i>italic</i>
        t = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', t)
        # `code` -> <code>code</code>
        t = re.sub(r'`(.*?)`', r'<code>\1</code>', t)
        # ```code``` -> <pre><code>code</code></pre>
        t = re.sub(r'```(?:\w+)?\n?(.*?)```', r'<pre><code>\1</code></pre>', t, flags=re.DOTALL)
        
        return t

    def clear_history(self, user_id: int):
        """Foydalanuvchi muloqot tarixini tozalash."""
        if user_id in USER_CONVERSATIONS:
            USER_CONVERSATIONS[user_id].clear()


# Yagona singleton AI servis obyekti
ai_service = AIService()
