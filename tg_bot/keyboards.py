from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from constants import FAQ_PER_PAGE, LINK_ITEMS, MENU_ITEMS, MENU_LAYOUT
from message_config import InlineButtonText, LogMessage, PlaceholderMessage
from settings import bot_logger
from utils import LinkButtonAttributes


async def get_menu_button() -> ReplyKeyboardMarkup:
    """Создает кнопку вызова меню."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="МЕНЮ")]],
        resize_keyboard=True,
        input_field_placeholder=PlaceholderMessage.MENU_BTN,
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
    bot_logger.info(msg=LogMessage.CREATE_MAIN_KB)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=PlaceholderMessage.MAIN_MENU,
        one_time_keyboard=True,
    )


async def remove_menu() -> ReplyKeyboardRemove:
    """Удаляет клавиатуру."""
    bot_logger.info(msg=LogMessage.REMOVE_KB)
    return ReplyKeyboardRemove()


async def get_url_button(
    btn_attrs: LinkButtonAttributes,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btn_attrs.text, url=btn_attrs.url)]
        ]
    )


async def get_faq_menu(faq_questions: list, page: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с частыми вопросами."""
    items_list = faq_questions + [
        {
            "question": InlineButtonText.CUSTOM_QUESTION,
            "order": "custom_question",
        }
    ]
    pages_count = (len(items_list) + FAQ_PER_PAGE - 1) // FAQ_PER_PAGE
    if page == -1:
        page = pages_count
    start_idx = (page - 1) * FAQ_PER_PAGE
    end_idx = start_idx + FAQ_PER_PAGE
    page_faq = items_list[start_idx:end_idx]
    keyboard = [
        [
            InlineKeyboardButton(
                text=item["question"], callback_data=item["order"]
            )
        ]
        for item in page_faq
    ]
    if pages_count == 1:
        bot_logger.info(msg=LogMessage.CREATE_FAQ_KB % page)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    navigation_buttons = []
    if page > 2:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.FIRST_PAGE, callback_data="first_page"
            )
        )
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.PREV_PAGE, callback_data="prev_page"
            )
        )
    if page < pages_count:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.NEXT_PAGE, callback_data="next_page"
            )
        )
    if page < pages_count - 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.LAST_PAGE,
                callback_data="last_page",
            )
        )
    keyboard.append(navigation_buttons)
    bot_logger.info(msg=LogMessage.CREATE_FAQ_KB % page)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
