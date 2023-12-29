import pytest
from core.keyboards import remove_menu
from telegram import ReplyKeyboardRemove


@pytest.mark.asyncio
async def test_remove_keyboard():
    """Проверяем, что remove_menu, удаляет клавиатуру"""

    keyboards = await remove_menu()
    assert type(keyboards) == ReplyKeyboardRemove
