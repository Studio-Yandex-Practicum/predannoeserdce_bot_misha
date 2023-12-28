from http import HTTPStatus

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from core.constants import (
    LINK_BUTTONS,
    MENU_LAYOUT,
    MainCallbacks,
    MenuFuncButton,
    OneButtonItems,
)
from core.message_config import (
    BotLogMessage,
    InlineButtonText,
    MainMessage,
    PlaceholderMessage,
)
from core.requests_db import check_subscribe
from core.services import (
    get_navigation_buttons,
    get_page_list,
    get_pages_count,
)
from core.settings import bot_logger
from core.utils import LinkButtonAttributes


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


async def get_main_menu(user_id) -> ReplyKeyboardMarkup:
    """Создает клавиатуру основного меню."""
    keyboard = []
    main_btn_list = list(MenuFuncButton)
    if check_subscribe(user_id=user_id).status_code != HTTPStatus.OK:
        main_btn_list.remove(MenuFuncButton.UNSUBSCRIBE)
    else:
        main_btn_list.remove(MenuFuncButton.SUBSCRIBE)
    btn_list = main_btn_list + list(LINK_BUTTONS.keys())
    btn_idx = 0
    while btn_idx < len(btn_list):
        row = []
        for _ in range(MENU_LAYOUT):
            if btn_idx == len(btn_list):
                break
            row.append(KeyboardButton(text=btn_list[btn_idx].capitalize()))
            btn_idx += 1
        keyboard.append(row)
    bot_logger.info(msg=BotLogMessage.CREATE_MAIN_KB)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=PlaceholderMessage.MAIN_MENU,
        one_time_keyboard=True,
    )


async def remove_menu() -> ReplyKeyboardRemove:
    """Удаляет клавиатуру."""
    bot_logger.info(msg=BotLogMessage.REMOVE_KB)
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


async def get_categories_menu(
    categories: list, page: int
) -> InlineKeyboardMarkup:
    """Создает клавиатуру с категориями вопросов."""
    pages_count = await get_pages_count(queryset=categories)
    page_list = await get_page_list(queryset=categories, page=page)
    if page_list[0] == MainMessage.SERVER_ERROR:
        keyboard = [
            [
                InlineKeyboardButton(
                    text=MainMessage.SERVER_ERROR,
                    callback_data=MainCallbacks.SERVER_ERROR,
                )
            ]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text=item, callback_data=item)]
            for item in page_list
        ]
    bot_logger.info(msg=BotLogMessage.CREATE_CATEGORY_KB % page)
    if pages_count != 1:
        navigation_buttons = await get_navigation_buttons(
            pages_count=pages_count, page=page
        )
        keyboard.append(navigation_buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_faq_menu(faq_questions: list, page: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с частыми вопросами в текущей категории."""
    pages_count = await get_pages_count(queryset=faq_questions)
    page_list = await get_page_list(queryset=faq_questions, page=page)
    keyboard = []
    for item in page_list:
        item_key = list(item.keys())[0]
        item_value = list(item.values())[0]
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=item_value["question"],
                    callback_data=item_key,
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=InlineButtonText.BACK_TO_CATEGORIES,
                callback_data=MainCallbacks.BACK_TO_CATEGORIES,
            )
        ]
    )
    bot_logger.info(msg=BotLogMessage.CREATE_FAQ_KB % page)
    if pages_count != 1:
        navigation_buttons = await get_navigation_buttons(
            pages_count=pages_count, page=page
        )
        keyboard.append(navigation_buttons)
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
    bot_logger.info(msg=BotLogMessage.CREATE_CUSTOM_QUESTION_KB)
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
    bot_logger.info(msg=BotLogMessage.CREATE_BACK_TO_FAQ_KB)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_subscribe_buttons() -> ReplyKeyboardMarkup:
    """Создаёт кнопки для возврата в меню и новой попытки подписки."""
    keyboard = [
        [KeyboardButton(text=OneButtonItems.RETURN.capitalize())],
        [KeyboardButton(text=OneButtonItems.MENU.upper())],
    ]
    bot_logger.info(msg=BotLogMessage.CREATE_SUBSCRIBE_KB)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def get_to_ban_button() -> InlineKeyboardMarkup:
    """Создаёт кнопку добавления пользователя в чёрный список."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=InlineButtonText.USER_TO_BAN,
                callback_data=MainCallbacks.USER_TO_BAN,
            )
        ]
    ]
    bot_logger.info(msg=BotLogMessage.CREATE_TO_BAN_KB)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
