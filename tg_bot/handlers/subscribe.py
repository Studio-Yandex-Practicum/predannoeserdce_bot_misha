import os
from http import HTTPStatus

import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import core.keyboards as kb
from core.constants import SERVER_API_CUSTOMER_URL
from core.message_config import ConversationLogMessage, SubscribeTextMessage
from core.requests_db import delete_subscriber, get_headers
from core.services import (
    format_error_messages,
    format_user_data_to_msg,
    get_data_to_send,
)
from core.settings import bot_logger


async def subscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict
) -> int:
    """Подписка на рассылку."""
    token = os.getenv(key="ADMIN_TOKEN")
    response = requests.post(
        url=SERVER_API_CUSTOMER_URL,
        json=await get_data_to_send(user_data=user_data),
        headers=get_headers(token=token),
    )
    if response.status_code == HTTPStatus.CREATED:
        bot_logger.info(
            msg=ConversationLogMessage.SUBSCRIBE_SUCCESS % user_data["user_id"]
        )
        text = (
            f"{SubscribeTextMessage.DONE}"
            f"{await format_user_data_to_msg(user_data=user_data)}"
        )
        keyboard = await kb.get_menu_button()
    else:
        error = await format_error_messages(text=response.text)
        bot_logger.error(
            msg=ConversationLogMessage.SUBSCRIBE_ERROR
            % (error, user_data["user_id"])
        )
        text = f"{SubscribeTextMessage.ERROR}{error}"
        keyboard = await kb.get_subscribe_buttons()
    await update.message.reply_text(
        text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML
    )
    context.user_data["callback"] = None
    return ConversationHandler.END


async def unsubscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отписка от подписки на рассылку."""
    id = update.message.from_user.id
    response = delete_subscriber(user_id=id)
    if response.status_code == HTTPStatus.NO_CONTENT:
        text = SubscribeTextMessage.UNSUBSCRIBE
        bot_logger.info(msg=ConversationLogMessage.UNSUSCRIBE_SUCCESS % id)
    else:
        error = await format_error_messages(text=response.text)
        text = f"{SubscribeTextMessage.ERROR}{error}"
        bot_logger.error(
            msg=ConversationLogMessage.UNSUBSCRIBE_ERROR
            % (f"status.code={response.status_code}, error={error}", id)
        )
    await update.message.reply_text(
        text=text,
        reply_markup=await kb.get_main_menu(user_id=id),
    )
