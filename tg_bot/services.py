from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import keyboards as kb
from constants import ADMIN_CHAT_ID
from message_config import ConversationLogMessage, MenuLogMessage
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
