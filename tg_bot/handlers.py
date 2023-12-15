import asyncio

from telegram import Update
from telegram.ext import ContextTypes

import keyboards as kb
from constants import LINK_ITEMS, MENU_ITEMS, MENU_SLEEP
from message_config import MESSAGES, LogMessage
from requests_db import get_faq
from settings import bot_logger


def update_faq() -> None:
    """Обновляет список частых вопросов."""
    global faq_dict
    faq_dict = get_faq()
    bot_logger.info(msg=LogMessage.UPDATE_FAQ_LIST)


async def handle_show_menu_btn(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    delay: int | None = None,
) -> None:
    """Показывает кнопку вызова основного меню."""
    if delay:
        await asyncio.sleep(delay=delay)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES["menu_btn"],
        reply_markup=await kb.get_menu_button(),
    )
    bot_logger.info(msg=LogMessage.SHOW_MENU_BTN)


async def handle_show_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    delay: int | None = None,
) -> None:
    """Показывает основное меню."""
    if delay:
        await asyncio.sleep(delay=delay)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES["menu"],
        reply_markup=await kb.get_main_menu(),
    )
    bot_logger.info(msg=LogMessage.SHOW_MAIN_MENU)


async def handle_alert_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отвечает пользователю на попытку отправить неподдерживаемый контент."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGES["alert_message"]
    )


async def handle_menu_buttons(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопок меню."""
    menu_keys = list(key.lower() for key in MENU_ITEMS.keys())
    link_keys = list(key.lower() for key in LINK_ITEMS.keys())
    if update.message.text.lower() in menu_keys:
        await globals()[MENU_ITEMS[update.message.text.lower()]](
            update, context
        )
    elif update.message.text.lower() in link_keys:
        await handle_url_button(update=update, context=context)
    elif update.message.text.lower() == "меню":
        await handle_show_main_menu(update=update, context=context)
    else:
        await handle_alert_message(update=update, context=context)
        bot_logger.info(
            msg=LogMessage.UNKNOWN_MESSAGE % (update.message.text,)
        )


async def handle_url_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопки с переходом на сайт."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Нажмите на кнопку, чтобы перейди на сайт.",
        reply_markup=await kb.get_url_button(
            btn_attrs=LINK_ITEMS[update.message.text.lower()],
        ),
    )
    bot_logger.info(msg=LogMessage.PROCESSING_BTN % (update.message.text,))
    await handle_show_main_menu(
        update=update, context=context, delay=MENU_SLEEP
    )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие кнопки `Частые вопросы`."""
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="Что вы хотите узнать?",
    #     reply_markup=await kb.remove_menu(),
    # )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите вопрос, который вас интересует:",
        reply_markup=await kb.get_faq_menu(faq_questions=faq_dict),
    )
    bot_logger.info(msg=LogMessage.PROCESSING_BTN % (update.message.text,))
    await handle_show_menu_btn(update=update, context=context)


async def subscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=LogMessage.STUB_BTN % (update.message.text,),
    )
    await handle_show_main_menu(update=update, context=context, delay=1),


async def handle_faq_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    order = query.data
    if order == "main_menu":
        await handle_show_main_menu(update=update, context=context)
    if order == "custom_question":
        pass
    await query.answer()
