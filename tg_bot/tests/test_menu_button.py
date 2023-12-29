import pytest
from core.keyboards import get_menu_button
from telegram import ReplyKeyboardMarkup

test_keyboard = [["ГЛАВНОЕ МЕНЮ"]]


@pytest.mark.asyncio
async def test_menu_button():
    """Проверяем, что get_menu_button, возвращает кнопку"""
    text = []
    text_row = []
    keyboards = await get_menu_button()
    buttons = keyboards.keyboard
    for buttons_row in buttons:
        for button in buttons_row:
            text_row.append(button["text"])
        text.append(text_row)
        text_row = []

    assert isinstance(keyboards, ReplyKeyboardMarkup)
    assert len(buttons) == len(test_keyboard)
    assert text == test_keyboard
