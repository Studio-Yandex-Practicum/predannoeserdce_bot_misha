import json
from typing import Dict

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import keyboards as kb
from constants import ADMIN_CHAT_ID, FAQ_PER_PAGE, MainCallbacks
from message_config import (ConversationLogMessage, InlineButtonText,
                            MenuLogMessage)
from settings import bot_logger


async def create_question_message(data: dict) -> str:
    """Создает текстовое сообщение для администратора."""
    text = (
        "<b>Вам сообщение!</b>\n\n"
        f"От кого: {data['user_fullname']}, id:{data['user_id']},\n"
        f"Email: {data['user_email']},\n"
        f"Телефон: {data['user_phone']},\n\n"
        f"Тема: <i>{data['subject']}</i>\n\n"
        f"Вопрос:\n{data['question']}"
    )
    return text


async def send_question_tg(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict
) -> None:
    """Отправка вопроса администратору в телеграм."""
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=await create_question_message(data=data),
        parse_mode=ParseMode.HTML,
        reply_markup=await kb.remove_menu(),
    )
    bot_logger.info(msg=ConversationLogMessage.SEND_QUESTION % data["user_id"])


async def send_question_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict
) -> None:
    """Отправка вопроса администратору на email."""
    await update.message.reply_text(
        text=MenuLogMessage.STUB_BTN % "`Отправка по email`",
    )
    bot_logger.info(msg=ConversationLogMessage.SEND_QUESTION % data["user_id"])


async def faq_pages_count(faq_list: list[dict]) -> int:
    return (
        len(await faq_buttons_list(faq_list=faq_list)) + FAQ_PER_PAGE - 1
    ) // FAQ_PER_PAGE


async def faq_buttons_list(faq_list) -> list[dict]:
    return faq_list + [
        {
            "question": InlineButtonText.CUSTOM_QUESTION,
            "order": MainCallbacks.CUSTOM_QUESTION,
        }
    ]


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


def format_error_messages(text):
    errors = json.loads(text)
    error_messages = []
    for values in errors.values():
        for message in values:
            error_messages.append(message)
    return '\n'.join(error_messages)


def get_data_to_send(user_data: Dict[str, str]):
    data_to_send = {
        'email': user_data['user_email'],
        'name': user_data['user_fullname'],
        'phone': user_data['user_phone'],
        'tg_id': user_data['user_id']
    }
    return data_to_send


def get_data_to_user(user_data: Dict[str, str]):
    data_to_user = {
        'Email': user_data['user_email'],
        'Имя': user_data['user_fullname'],
        'Телефон': user_data['user_phone'],
    }
    return data_to_user


def get_headers(token):
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    return headers
