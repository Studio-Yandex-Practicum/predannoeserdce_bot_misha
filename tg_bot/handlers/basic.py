import asyncio

from telegram import Update
from telegram.ext import ContextTypes

import core.keyboards as kb
from core.constants import (
    ADMIN_CHAT_ID,
    LINK_BUTTONS,
    MENU_SLEEP,
    OneButtonItems,
)
from handlers.admin import handle_admin_answer
from core.message_config import (
    BotLogMessage,
    ConversationLogMessage,
    ConversationTextMessage,
    MainMessage,
)
from core.settings import bot_logger


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
        text=MainMessage.MENU_BTN,
        reply_markup=await kb.get_menu_button(),
    )
    bot_logger.info(msg=BotLogMessage.SHOW_MENU_BTN)


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
        text=MainMessage.MENU,
        reply_markup=await kb.get_main_menu(user_id=update.effective_chat.id),
    )
    bot_logger.info(msg=BotLogMessage.SHOW_MAIN_MENU)


async def handle_alert_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отвечает пользователю на попытку отправить неподдерживаемый контент."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MainMessage.ALERT_MSG
    )


async def handle_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает текстовые сообщения."""
    if update.message.text.lower() == OneButtonItems.MENU.lower():
        await handle_show_main_menu(update=update, context=context)
    elif update.message.reply_to_message:
        await handle_admin_answer(update=update, context=context)
    else:
        await handle_alert_message(update=update, context=context)
        bot_logger.info(
            msg=BotLogMessage.UNKNOWN_MESSAGE % (update.message.text,)
        )


async def handle_url_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатие кнопки с переходом на сайт."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MainMessage.URL,
        reply_markup=await kb.get_url_button(
            btn_attrs=LINK_BUTTONS[update.message.text.lower()],
        ),
    )
    bot_logger.info(msg=BotLogMessage.PROCESSING_BTN % update.message.text)
    await handle_show_main_menu(
        update=update, context=context, delay=MENU_SLEEP
    )


async def handle_error_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает ошибку получения списка вопросов."""
    query = update.callback_query
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=ConversationTextMessage.SERVER_ERROR,
        reply_markup=await kb.remove_menu(),
    )
    bot_logger.info(msg=ConversationLogMessage.ERROR_TO_ADMIN)
    await query.edit_message_text(
        text=ConversationTextMessage.ERROR_THANKS,
    )
    query.answer()
    await handle_show_main_menu(
        update=update, context=context, delay=MENU_SLEEP
    )


async def handle_custom_question_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает кнопку `Задать вопрос`."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ConversationTextMessage.COMMUNICATION_WAY,
        reply_markup=await kb.get_communication_way(),
    )
