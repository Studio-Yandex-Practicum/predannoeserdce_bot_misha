import pytest
from core.keyboards import get_url_button
from core.utils import LinkButtonAttributes
from telegram import InlineKeyboardMarkup

test_keyboard = LinkButtonAttributes(
    text="Нажми на меня", url="https://www.google.com/"
)


@pytest.mark.asyncio
async def test_url_button():
    """Проверяем, что get_url_button, возвращает кнопку"""

    keyboards = await get_url_button(test_keyboard)
    button = keyboards.inline_keyboard[0][0]

    assert isinstance(keyboards, InlineKeyboardMarkup)
    assert button["text"] == test_keyboard.text
    assert button["url"] == test_keyboard.url
