import asyncio
import os
from http import HTTPStatus

import requests
from telegram import Message, ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import keyboards as kb
from constants import (
    ADMIN_CHAT_ID,
    LINK_BUTTONS,
    MENU_SLEEP,
    SERVER_API_CUSTOMER_URL,
    START_SLEEP,
    ConvState,
    MainCallbacks,
    PaginationCallback,
)
from message_config import (
    BotLogMessage,
    ConversationLogMessage,
    ConversationTextMessage,
    InlineButtonText,
    MainMessage,
    SubscribeTextMessage,
)
from requests_db import get_faq
from services import (
    facts_to_str,
    faq_pages_count,
    format_error_messages,
    get_data_to_send,
    get_data_to_user,
    get_headers,
    send_question_email,
    send_question_tg,
)
from settings import bot_logger
from validators import email_validate, fullname_validate, phone_validate


def update_faq() -> None:
    """Обновляет список частых вопросов."""
    global faq_dict
    faq_dict = get_faq()


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
        reply_markup=await kb.get_main_menu(),
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
    if update.message.reply_to_message:
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


async def handle_faq_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Message | None:
    """Обрабатывает нажатие кнопки `Частые вопросы`."""
    query = update.callback_query
    order = query.data if query else None
    pages_count = await faq_pages_count(faq_dict=faq_dict)
    page = context.user_data.get("page", None)
    if not page or not order:
        page = 1
        context.user_data["page"] = page
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MainMessage.FAQ,
            reply_markup=await kb.get_faq_menu(
                faq_questions=faq_dict, page=page
            ),
        )
    elif order == PaginationCallback.FIRST_PAGE:
        page = 1
    elif order == PaginationCallback.LAST_PAGE:
        page = pages_count
    elif order == PaginationCallback.NEXT_PAGE:
        page += 1
    elif order == PaginationCallback.PREV_PAGE:
        page -= 1
    await update.effective_message.edit_text(
        text=MainMessage.FAQ,
        reply_markup=await kb.get_faq_menu(faq_questions=faq_dict, page=page),
    )
    context.user_data["page"] = page
    await query.answer()


async def handle_faq_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает частые вопросы. Выдаёт ответы."""
    query = update.callback_query
    order = query.data
    if order.isdigit():
        data = faq_dict[order]
        text = ConversationTextMessage.ANSWER_BY_FAQ % (
            tuple(data.values())[:2]
        )
        await query.edit_message_text(
            text=text,
            reply_markup=await kb.get_back_to_faq(),
            parse_mode=ParseMode.HTML,
        )
    elif order != MainCallbacks.CUSTOM_QUESTION:
        return await handle_faq_button(update=update, context=context)
    else:
        await query.edit_message_text(
            text=ConversationTextMessage.COMMUNICATION_WAY,
            reply_markup=await kb.get_communication_way(),
        )
    await query.answer()


# ----- НАЧАЛО ОБЩЕНИЯ ----- #
async def conv_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Начало общения, в котором пользователь подписывается на рассылку или
    задаёт свой вопрос по email.
    Запрос на получение полного имени пользователя.
    """
    if update.callback_query is not None:
        query = update.callback_query
        context.user_data["callback"] = query.data
        context.user_data[
            "entry_text"
        ] = InlineButtonText.CUSTOM_QUESTION.lower()
        await query.answer()
    else:
        query = update.message
        context.user_data["callback"] = query.text
        context.user_data["entry_text"] = query.text.lower()
    context.user_data["user_id"] = query.from_user.id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ConversationTextMessage.WRITE_FULLNAME,
        reply_markup=await kb.get_cancel_button(),
    )
    bot_logger.info(msg=ConversationLogMessage.START % query.from_user.id)
    return ConvState.EMAIL


async def conv_get_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Запрос на получение email."""
    while not await fullname_validate(update=update, context=context):
        await update.message.reply_text(
            text=ConversationTextMessage.INVALID_FULLNAME
        )
        bot_logger.info(
            msg=ConversationLogMessage.INVALID_DATA % "user_fullname"
        )
        return ConvState.EMAIL
    context.user_data["user_fullname"] = update.message.text.title()
    bot_logger.info(
        msg=ConversationLogMessage.RECEIVED_FULLNAME
        % context.user_data["user_id"]
    )
    await update.message.reply_text(
        text=ConversationTextMessage.WRITE_EMAIL,
        reply_markup=await kb.get_cancel_button(),
    )
    return ConvState.PHONE


async def conv_get_phone(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Запрос на получение номера телефона."""
    while not await email_validate(update=update, context=context):
        await update.message.reply_text(
            text=ConversationTextMessage.INVALID_EMAIL
        )
        bot_logger.info(msg=ConversationLogMessage.INVALID_DATA % "user_email")
        return ConvState.PHONE
    context.user_data["user_email"] = update.message.text
    bot_logger.info(
        msg=ConversationLogMessage.RECEIVED_EMAIL
        % context.user_data["user_id"]
    )
    await update.message.reply_text(
        text=ConversationTextMessage.WRITE_PHONE,
        reply_markup=await kb.get_cancel_button(),
    )
    return ConvState.SUBJECT


async def conv_get_subject(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Запрос на получение темы сообщения."""
    while not await phone_validate(update=update, context=context):
        await update.message.reply_text(
            text=ConversationTextMessage.INVALID_PHONE
        )
        bot_logger.info(msg=ConversationLogMessage.INVALID_DATA % "user_phone")
        return ConvState.SUBJECT
    context.user_data["user_phone"] = update.message.text
    user_data = context.user_data
    bot_logger.info(
        msg=ConversationLogMessage.RECEIVED_PHONE
        % context.user_data["user_id"]
    )
    if context.user_data["callback"] == "Подписаться на рассылку":
        text, keyboard = await subscribe(user_data=user_data)
        await update.message.reply_text(text=text, reply_markup=keyboard)
        return ConversationHandler.END

    await update.message.reply_text(
        text=ConversationTextMessage.WRITE_SUBJECT,
        reply_markup=await kb.get_cancel_button(),
    )
    return ConvState.QUESTION


async def conv_get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Получение сообщения от пользователя (кастомный вопрос)."""
    context.user_data["subject"] = update.message.text
    bot_logger.info(
        msg=ConversationLogMessage.RECEIVED_SUBJECT
        % context.user_data["user_id"]
    )
    await update.message.reply_text(
        text=ConversationTextMessage.WRITE_QUESTION,
        reply_markup=await kb.get_cancel_button(),
    )

    return ConvState.SEND


async def conv_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение общения."""
    context.user_data["question"] = update.message.text
    bot_logger.info(
        msg=ConversationLogMessage.RECEIVED_QUESTION
        % context.user_data["user_id"]
    )
    if context.user_data["callback"] == MainCallbacks.TG_QUESTION:
        await send_question_tg(
            update=update, context=context, data=context.user_data
        )
        await update.message.reply_text(
            text=ConversationTextMessage.SEND_QUESTION_TG,
            reply_markup=await kb.remove_menu(),
        )
        await handle_show_main_menu(
            update=update, context=context, delay=START_SLEEP
        )
    if context.user_data["callback"] == MainCallbacks.EMAIL_QUESTION:
        await send_question_email(
            update=update, context=context, data=context.user_data
        )
        await update.message.reply_text(
            text=ConversationTextMessage.SEND_QUESTION_EMAIL,
            reply_markup=await kb.remove_menu(),
        )
        await handle_show_main_menu(
            update=update, context=context, delay=START_SLEEP
        )
    bot_logger.info(
        msg=ConversationLogMessage.END % context.user_data["user_id"]
    )
    return ConversationHandler.END


async def conv_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отмена общения пользователем."""
    bot_logger.info(
        msg=ConversationLogMessage.CANCEL % update.message.from_user.id
    )
    await update.message.reply_text(
        text=ConversationTextMessage.CANCEL
        % context.user_data.get("entry_text", "продолжить"),
        reply_markup=await kb.get_main_menu(),
    )
    return ConversationHandler.END


# ----- КОНЕЦ ОБЩЕНИЯ ----- #


async def handle_admin_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обработка ответа администратора, отправка его пользователю."""
    if update.message.from_user.id != int(ADMIN_CHAT_ID):
        return None
    text = update.message.reply_to_message.text.split(sep=",")
    to_chat_id = int([s for s in text if "id:" in s][0].split(sep=":")[-1])

    await context.bot.send_message(
        chat_id=to_chat_id,
        text=ConversationTextMessage.ANSWER_FROM_ADMIN % update.message.text,
        parse_mode=ParseMode.HTML,
        reply_markup=await kb.get_main_menu(),
    )
    bot_logger.info(msg=ConversationLogMessage.ANSWER_FROM_ADMIN % to_chat_id)


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
        # reply_markup=await kb.remove_menu(),
    )
    query.answer()
    await handle_show_main_menu(
        update=update, context=context, delay=MENU_SLEEP
    )


async def subscribe(user_data) -> tuple[str, ReplyKeyboardMarkup]:
    token = os.getenv(key="ADMIN_TOKEN")
    response = requests.post(
        url=SERVER_API_CUSTOMER_URL,
        json=get_data_to_send(user_data=user_data),
        headers=get_headers(token=token),
    )
    if response.status_code == HTTPStatus.CREATED:
        facts = get_data_to_user(user_data=user_data)
        text = f"{SubscribeTextMessage.DONE}{facts_to_str(user_data=facts)}"
        keyboard = await kb.get_menu_button()
    else:
        error = format_error_messages(text=response.text)
        text = f"{SubscribeTextMessage.ERROR}{error}"
        keyboard = await kb.get_subscribe_buttons()

    return text, keyboard
