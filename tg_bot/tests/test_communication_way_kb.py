import pytest
from core.keyboards import get_communication_way
from telegram import InlineKeyboardMarkup

test_keyboard = {
    "text": "Telegram",
    "callback_data": "tg_question",
}


@pytest.mark.asyncio
async def test_communication_kb():
    """Проверяем, что get_communication_way, возвращает клавиатуру"""

    keyboards = await get_communication_way()
    button = keyboards.inline_keyboard[0][0]

    assert isinstance(keyboards, InlineKeyboardMarkup)
    assert button["text"] == test_keyboard["text"]
    assert button["callback_data"] == test_keyboard["callback_data"]
