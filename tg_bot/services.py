import asyncio
import json
import random
from datetime import datetime, time

import pytz
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import keyboards as kb
from constants import (
    ADMIN_CHAT_ID,
    FAQ_PER_PAGE,
    AdminWorkTime,
    BanList,
    DelayedQuestionsAttr,
    DelayedQuestionsSendDelay,
    MainCallbacks,
)
from message_config import (
    BotLogMessage,
    ConversationLogMessage,
    DelayedQstnsLogMessage,
    DelayedQstnsTextMessage,
    InlineButtonText,
)
from settings import bot_logger


async def check_work_time() -> bool:
    """Проверяет рабочее время администратора с учетом часового пояса."""
    timezone = pytz.timezone(zone=AdminWorkTime.TIMEZONE)
    current_time = datetime.now(tz=timezone).time()
    start_time = time(
        hour=AdminWorkTime.START_H, minute=AdminWorkTime.START_MIN
    )
    end_time = time(hour=AdminWorkTime.END_H, minute=AdminWorkTime.END_MIN)
    return start_time <= current_time <= end_time


async def send_question_tg(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict
) -> None:
    """Отправка вопроса администратору в телеграм."""
    user = update.message.from_user
    msg = (
        "<b>Вам сообщение от пользователя</b>\n\n"
        f"Ник: {user.username if user.username else 'Не указано'}\n"
        f"Имя: {user.full_name if user.full_name else 'Не указано'}\n"
        f"id:{user.id}\n\n"
        f"<b>Вопрос:</b>\n{data['question']}"
    )
    if not await check_work_time():
        with open(
            file=DelayedQuestionsAttr.FILENAME,
            mode="a",
            encoding=DelayedQuestionsAttr.ENCODING,
        ) as file:
            file.write(msg + DelayedQuestionsAttr.MSG_SEPARATOR)
            bot_logger.info(
                msg=DelayedQstnsLogMessage.QUESTION_DELAYED % user.id
            )
            return None
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=msg,
        parse_mode=ParseMode.HTML,
        reply_markup=await kb.get_to_ban_button(),
    )
    bot_logger.info(msg=ConversationLogMessage.SEND_QUESTION % user.id)


async def send_question_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict
) -> None:
    """Отправка вопроса администратору на email."""
    await update.message.reply_text(
        text=BotLogMessage.STUB_BTN % "`Отправка по email`",
    )
    bot_logger.info(msg=ConversationLogMessage.SEND_QUESTION % data["user_id"])


async def faq_pages_count(faq_dict: dict) -> int:
    """Возвращает количество страниц с вопросами."""
    return (
        len(await faq_buttons(faq_dict=faq_dict)) + FAQ_PER_PAGE - 1
    ) // FAQ_PER_PAGE


async def faq_buttons(faq_dict) -> dict:
    """Добавляет к кнопкам с вопросами кнопку с кастомным вопросом."""
    faq_dict.update(
        {
            MainCallbacks.CUSTOM_QUESTION: {
                "question": InlineButtonText.CUSTOM_QUESTION,
            }
        }
    )
    return faq_dict


def format_user_data_to_msg(user_data: dict[str, str]) -> str:
    """Подготавливает данные к представлению пользователю."""
    text = {
        "Email": user_data["user_email"],
        "Имя": user_data["user_fullname"],
        "Телефон": user_data["user_phone"],
    }
    return "\n".join(f"{key} - {value}" for key, value in text.items())


def format_error_messages(text) -> str:
    """Преобразует словарь ошибок в строку."""
    errors = json.loads(text)
    error_messages = []
    for value in errors.values():
        value = "".join(value)
        error_messages.append(value)
    return "\n".join(error_messages)


def get_data_to_send(user_data: dict[str, str]) -> dict[str, str]:
    """Подготавливает данные к отправке в БД."""
    return {
        "email": user_data["user_email"],
        "name": user_data["user_fullname"],
        "phone": user_data["user_phone"],
        "tg_id": user_data["user_id"],
    }


def get_headers(token) -> dict[str, str]:
    """Подготавливает заголовок."""
    return {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }


def check_user_at_ban(user_id: int) -> bool:
    """Проверяет пользователя на нахождение в чёрном списке."""
    with open(
        file=BanList.FILENAME, mode="r", encoding=BanList.ENCODING
    ) as file:
        ban_list = file.readlines()
    return user_id in [int(id.strip()) for id in ban_list]


async def send_delayed_questions(bot):
    """Отсылает отложенные вопросы для администратора."""
    with open(
        file=DelayedQuestionsAttr.FILENAME,
        mode="r",
        encoding=DelayedQuestionsAttr.ENCODING,
    ) as file:
        text = file.readlines()
    if text == "":
        return None
    msg_list = "".join(text).split(sep=DelayedQuestionsAttr.MSG_SEPARATOR)
    bot_logger.info(msg=DelayedQstnsLogMessage.SEND_START)
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=DelayedQstnsTextMessage.SEND_START,
        parse_mode=ParseMode.HTML,
    )
    for msg in msg_list:
        if msg == "":
            continue
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=msg,
            parse_mode=ParseMode.HTML,
            reply_markup=await kb.get_to_ban_button(),
        )
        await asyncio.sleep(
            delay=random.randint(
                DelayedQuestionsSendDelay.MINIMUM,
                DelayedQuestionsSendDelay.MAXIMUM,
            )
        )
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=DelayedQstnsTextMessage.SEND_END,
        parse_mode=ParseMode.HTML,
    )
    with open(file=DelayedQuestionsAttr.FILENAME, mode="r+") as file:
        file.truncate(0)
    bot_logger.info(msg=DelayedQstnsLogMessage.SEND_END)
