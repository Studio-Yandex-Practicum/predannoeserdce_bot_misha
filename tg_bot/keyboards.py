from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from constants import (
    FAQ_PER_PAGE,
    LINK_BUTTONS,
    MENU_LAYOUT,
    MainCallbacks,
    MenuFuncButton,
    OneButtonItems,
    PaginationCallback,
)
from message_config import InlineButtonText, MenuLogMessage, PlaceholderMessage
from services import faq_buttons_list, faq_pages_count
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
    btn_list = list(item.value for item in MenuFuncButton) + list(
        LINK_BUTTONS.keys()
    )
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


async def get_faq_menu(faq_questions: list, page: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с частыми вопросами."""
    buttons = await faq_buttons_list(faq_list=faq_questions)
    pages_count = await faq_pages_count(faq_list=faq_questions)
    start_idx = (page - 1) * FAQ_PER_PAGE
    end_idx = start_idx + FAQ_PER_PAGE
    page_faq = buttons[start_idx:end_idx]
    keyboard = [
        [
            InlineKeyboardButton(
                text=item["question"], callback_data=item["order"]
            )
        ]
        for item in page_faq
    ]
    if pages_count == 1:
        bot_logger.info(msg=MenuLogMessage.CREATE_FAQ_KB % page)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    navigation_buttons = []
    if page > 2:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.FIRST_PAGE,
                callback_data=PaginationCallback.FIRST_PAGE,
            )
        )
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.PREV_PAGE,
                callback_data=PaginationCallback.PREV_PAGE,
            )
        )
    if page < pages_count:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.NEXT_PAGE,
                callback_data=PaginationCallback.NEXT_PAGE,
            )
        )
    if page < pages_count - 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=InlineButtonText.LAST_PAGE,
                callback_data=PaginationCallback.LAST_PAGE,
            )
        )
    keyboard.append(navigation_buttons)
    bot_logger.info(msg=MenuLogMessage.CREATE_FAQ_KB % page)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_communication_way() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру выбора способа общения (телеграм или email)."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=InlineButtonText.TELEGRAM_QUESTION,
                callback_data=MainCallbacks.TG_QUESTION,
            ),
            # ------КНОПКА ВЫБОРА ОБЩЕНИЯ ПО EMAIL----- #
            # InlineKeyboardButton(
            #     text=InlineButtonText.EMAIL_QUESTION,
            #     callback_data=MainCallbacks.EMAIL_QUESTION,
            # ),
        ]
    ]
    bot_logger.info(msg=MenuLogMessage.CREATE_CUSTOM_QUESTION_KB)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_back_to_faq() -> InlineKeyboardMarkup:
    """Создаёт кнопку возврата к частым вопросам."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=InlineButtonText.BACK_TO_FAQ,
                callback_data=MainCallbacks.BACK_TO_FAQ,
            ),
        ]
    ]
    bot_logger.info(msg=MenuLogMessage.CREATE_BACK_TO_FAQ_KB)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
