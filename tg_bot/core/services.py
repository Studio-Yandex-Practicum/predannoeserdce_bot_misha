import asyncio
import json
import random
from datetime import datetime, time

import pytz
from telegram import InlineKeyboardButton, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import core.keyboards as kb
from core.constants import (
    ADMIN_CHAT_ID,
    FAQ_PER_PAGE,
    AdminWorkTime,
    BanList,
    DelayedQuestionsAttr,
    DelayedQuestionsSendDelay,
    PaginationCallback,
)
from core.message_config import (
    BotLogMessage,
    ConversationLogMessage,
    DelayedQstnsLogMessage,
    DelayedQstnsTextMessage,
    InlineButtonText,
)
from core.settings import bot_logger


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


async def get_pages_count(queryset: list) -> int:
    """Возвращает количество страниц с категориями или вопросами."""
    return (len(queryset) + FAQ_PER_PAGE - 1) // FAQ_PER_PAGE


async def get_navigation_buttons(pages_count: int, page: int) -> list:
    """Возвращает список кнопок пагинации."""
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
    return navigation_buttons


async def get_page_list(queryset: list, page: int) -> list:
    """Возвращает срез списка сущностей текущей страницы пагинации."""
    start_idx = (page - 1) * FAQ_PER_PAGE
    end_idx = start_idx + FAQ_PER_PAGE
    page_list = queryset[start_idx:end_idx]
    return page_list


async def format_user_data_to_msg(user_data: dict[str, str]) -> str:
    """Подготавливает данные к представлению пользователю."""
    text = {
        "Email": user_data["user_email"],
        "Имя": user_data["user_fullname"],
        "Телефон": user_data["user_phone"],
    }
    return "\n".join(f"{key} - {value}" for key, value in text.items())


async def format_error_messages(text) -> str:
    """Преобразует словарь ошибок в строку."""
    errors = json.loads(text)
    error_messages = []
    for value in errors.values():
        value = "".join(value)
        error_messages.append(value)
    return "\n".join(error_messages)


async def get_data_to_send(user_data: dict[str, str]) -> dict[str, str]:
    """Подготавливает данные к отправке в БД."""
    return {
        "email": user_data["user_email"],
        "name": user_data["user_fullname"],
        "phone": user_data["user_phone"],
        "tg_id": user_data["user_id"],
    }


async def check_user_at_ban(user_id: int) -> bool:
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
    if not text:
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
