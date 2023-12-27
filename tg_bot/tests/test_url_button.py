import pytest

from keyboards import get_url_button
from telegram import InlineKeyboardMarkup
from utils import LinkButtonAttributes

test_keyboard = LinkButtonAttributes(
    text='Нажми на меня',
    url= 'https://www.google.com/'
    )


@pytest.mark.asyncio
async def test_url_button():
    """Проверяем, что get_url_button, возвращает кнопку"""

    keyboards = await get_url_button(test_keyboard)
    button = keyboards.inline_keyboard[0][0]

    assert type(keyboards) == InlineKeyboardMarkup
    assert button['text'] == test_keyboard.text
    assert button['url'] == test_keyboard.url
