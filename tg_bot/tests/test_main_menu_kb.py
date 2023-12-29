import pytest
from core.keyboards import get_main_menu
from telegram import ReplyKeyboardMarkup

test_keyboard = [
    ["Частые вопросы", "Задать вопрос", "Подписаться на рассылку"],
    ["Сделать пожертвование", "Список животных", "Попечительская программа"],
]

test_user_id = "123"


@pytest.mark.asyncio
async def test_main_menu_keyboard():
    """Проверяем, что get_main_menu, возвращает клавиатуру"""
    text = []
    text_row = []
    keyboards = await get_main_menu(test_user_id)
    buttons = keyboards.keyboard
    for buttons_row in buttons:
        for button in buttons_row:
            text_row.append(button["text"])
        text.append(text_row)
        text_row = []

    assert isinstance(keyboards, ReplyKeyboardMarkup)
    assert len(buttons) == len(test_keyboard)

    for i in range(len(test_keyboard) - 1):
        assert len(buttons[i]) == len(test_keyboard[i])

    assert text == test_keyboard
