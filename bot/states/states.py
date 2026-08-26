"""
FSM (Finite State Machine) holatlari.
"""

from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    """Qidiruv holati."""
    waiting_for_query = State()


class AIState(StatesGroup):
    """AI Metrolog Maslahatchi bilan suhbat holati."""
    chatting = State()


class OrderState(StatesGroup):
    """Bitta mahsulot yoki xizmat uchun to'g'ridan-to'g'ri ariza berish holati."""
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_notes = State()


class CartOrderState(StatesGroup):
    """Savatchadagi mahsulotlarni rasmiylashtirish holatlari."""
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_notes = State()


class AdminState(StatesGroup):
    """Admin amallari holatlari."""
    waiting_for_broadcast = State()
    waiting_for_product_category = State()
    waiting_for_product_name = State()
    waiting_for_product_code = State()
    waiting_for_product_price = State()
    waiting_for_product_desc = State()
