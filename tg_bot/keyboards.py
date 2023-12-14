from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from constants import LINK_ITEMS, MENU_ITEMS, MENU_LAYOUT
from message_config import MESSAGES
from settings import bot_logger
from utils import LinkButtonAttributes


async def get_menu_button() -> ReplyKeyboardMarkup:
    """Создает кнопку вызова меню."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="МЕНЮ")]],
        resize_keyboard=True,
        input_field_placeholder=MESSAGES["menu_btn"],
    )


async def get_main_menu() -> ReplyKeyboardMarkup:
    """Создает клавиатуру основного меню."""
    keyboard = []
    btn_list = list(MENU_ITEMS.keys()) + list(LINK_ITEMS.keys())
    btn_idx = 0
    while btn_idx < len(btn_list):
        row = []
        for _ in range(MENU_LAYOUT):
            if btn_idx == len(btn_list):
                break
            row.append(KeyboardButton(text=btn_list[btn_idx]))
            btn_idx += 1
        keyboard.append(row)
    bot_logger.info(msg="Создана основная клавиатура")
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню",
        one_time_keyboard=True,
    )


async def remove_menu() -> ReplyKeyboardRemove:
    """Удаляет клавиатуру."""
    bot_logger.info(msg="Клавиатура удалена")
    return ReplyKeyboardRemove()


async def get_url_button(
    btn_attrs: LinkButtonAttributes,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btn_attrs.text, url=btn_attrs.url)]
        ]
    )


async def get_faq_menu(faq_questions: list) -> InlineKeyboardMarkup:
    """Создает клавиатуру с частыми вопросами."""

    # TODO: Создать постраничную клавиатуру

    keyboard = [
        [
            InlineKeyboardButton(
                text=item["question"], callback_data=item["order"]
            )
        ]
        for item in faq_questions
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Задать другой вопрос администратору",
                callback_data="custom_question",
            )
        ]
    ),
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню",
                callback_data="main_menu",
            )
        ]
    )
    bot_logger.info(msg="Создана клавиатура частых вопросов")
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
