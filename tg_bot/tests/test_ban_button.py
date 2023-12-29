import pytest
from core.keyboards import get_to_ban_button
from telegram import InlineKeyboardMarkup

test_keyboard = {
    "text": "Заблокировать пользователя",
    "callback_data": "user_to_ban",
}


@pytest.mark.asyncio
async def test_ban_kb():
    """Проверяем, что get_to_ban_button, возвращает клавиатуру"""

    keyboards = await get_to_ban_button()
    button = keyboards.inline_keyboard[0][0]

    assert isinstance(keyboards, InlineKeyboardMarkup)
    assert button["text"] == test_keyboard["text"]
    assert button["callback_data"] == test_keyboard["callback_data"]
