from constants import MENU_ITEMS, MENU_LAYOUT
from settings import logger
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


async def show_menu_button() -> ReplyKeyboardMarkup:
    """Показывает кнопку вызова меню."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="МЕНЮ")]],
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню",
    )


async def show_main_menu() -> ReplyKeyboardMarkup:
    """Показывает основное меню."""
    keyboard = []
    btn_index = 0
    btn_list = list(MENU_ITEMS.keys())
    for layout in MENU_LAYOUT:
        row = []
        for _ in range(layout):
            row.append(KeyboardButton(text=btn_list[btn_index]))
            btn_index += 1
        keyboard.append(row)
    logger.info(msg="Создана основная клавиатура")
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню",
        one_time_keyboard=True,
    )


async def remove_menu() -> ReplyKeyboardRemove:
    """Удаляет меню."""
    logger.info(msg="Клавиатура удалена")
    return ReplyKeyboardRemove()
