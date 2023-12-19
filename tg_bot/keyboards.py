from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from constants import LINK_ITEMS, MENU_ITEMS, MENU_LAYOUT, OneButtonItems
from message_config import InlineButtonText, MenuLogMessage, PlaceholderMessage
from settings import bot_logger
from utils import LinkButtonAttributes


async def get_menu_button() -> ReplyKeyboardMarkup:
    """Создает кнопку вызова меню."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=OneButtonItems.MENU.upper())]],
        resize_keyboard=True,
        input_field_placeholder=PlaceholderMessage.MENU_BTN,
    )


async def get_cancel_button() -> ReplyKeyboardMarkup:
    """Создает кнопку отмены разговора."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=OneButtonItems.CANCEL.upper())]],
        resize_keyboard=True,
        one_time_keyboard=True,
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
            row.append(KeyboardButton(text=btn_list[btn_idx].capitalize()))
            btn_idx += 1
        keyboard.append(row)
    bot_logger.info(msg=MenuLogMessage.CREATE_MAIN_KB)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=PlaceholderMessage.MAIN_MENU,
        one_time_keyboard=True,
    )


async def remove_menu() -> ReplyKeyboardRemove:
    """Удаляет клавиатуру."""
    bot_logger.info(msg=MenuLogMessage.REMOVE_KB)
    return ReplyKeyboardRemove()


async def get_url_button(
    btn_attrs: LinkButtonAttributes,
) -> InlineKeyboardMarkup:
    """Создаёт клавиатуру с кнопкой-ссылкой."""
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
                text=InlineButtonText.CUSTOM_QUESTION,
                callback_data="custom_question",
            )
        ]
    )

    bot_logger.info(msg=MenuLogMessage.CREATE_FAQ_KB)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_communication_way() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру выбора способа общения (телеграм или email)."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=InlineButtonText.TELEGRAM_QUESTION,
                callback_data="tg_question",
            ),
            InlineKeyboardButton(
                text=InlineButtonText.EMAIL_QUESTION,
                callback_data="email_question",
            ),
        ]
    ]
    bot_logger.info(msg=MenuLogMessage.CREATE_CUSTOM_QUESTION_KB)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
