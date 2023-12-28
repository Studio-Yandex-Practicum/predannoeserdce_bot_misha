import re

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import core.keyboards as kb
from core.constants import (
    START_SLEEP,
    ConvState,
    MainCallbacks,
    MenuFuncButton,
    OneButtonItems,
)
from handlers.ban import handle_user_at_ban
from handlers.basic import handle_show_main_menu
from handlers.subscribe import subscribe
from core.message_config import (
    ConversationLogMessage,
    ConversationTextMessage,
    InlineButtonText,
)
from core.services import (
    check_user_at_ban,
    send_question_email,
    send_question_tg,
)
from core.settings import bot_logger
from core.validators import email_validate, fullname_validate, phone_validate


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
    if (
        context.user_data["callback"].lower()
        == MenuFuncButton.SUBSCRIBE.value.lower()
        or context.user_data["callback"].lower()
        == OneButtonItems.RETURN.lower()
    ):
        return await subscribe(
            update=update, context=context, user_data=user_data
        )

    await update.message.reply_text(
        text=ConversationTextMessage.WRITE_SUBJECT,
        reply_markup=await kb.get_cancel_button(),
    )
    return ConvState.QUESTION


async def conv_get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Получение сообщения от пользователя (кастомный вопрос)."""
    callback = context.user_data.get("callback", None)
    text = ConversationTextMessage.WRITE_QUESTION
    reply_markup = await kb.get_cancel_button()
    if callback and callback != MainCallbacks.TG_QUESTION:
        context.user_data["subject"] = update.message.text
        bot_logger.info(
            msg=ConversationLogMessage.RECEIVED_SUBJECT
            % context.user_data["user_id"]
        )
        await update.message.reply_text(text=text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        context.user_data["callback"] = query.data
        context.user_data["user_id"] = query.from_user.id
        context.user_data[
            "entry_text"
        ] = InlineButtonText.CUSTOM_QUESTION.lower()
        if await check_user_at_ban(user_id=query.from_user.id):
            return await handle_user_at_ban(update=update, context=context)
        await context.bot.send_message(
            chat_id=query.from_user.id, text=text, reply_markup=reply_markup
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
    context.user_data["callback"] = None
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
        reply_markup=await kb.get_main_menu(update.message.from_user.id),
    )
    context.user_data["callback"] = None
    return ConversationHandler.END


cancel_pattern = re.compile(
    pattern=rf"^{OneButtonItems.CANCEL}$", flags=re.IGNORECASE
)
subscribe_pattern = re.compile(
    pattern=rf"^(?:{MenuFuncButton.SUBSCRIBE.value}|"
    f"{OneButtonItems.RETURN})$",
    flags=re.IGNORECASE,
)
conv_filters = (
    ~filters.Regex(pattern=cancel_pattern) & filters.TEXT & ~filters.COMMAND
)


data_collect_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=conv_start,
            pattern=MainCallbacks.EMAIL_QUESTION,
        ),
        MessageHandler(
            filters=filters.Regex(pattern=subscribe_pattern),
            callback=conv_start,
        ),
    ],
    states={
        ConvState.EMAIL: [
            MessageHandler(
                filters=conv_filters,
                callback=conv_get_email,
            ),
        ],
        ConvState.PHONE: [
            MessageHandler(
                filters=conv_filters,
                callback=conv_get_phone,
            ),
        ],
        ConvState.SUBJECT: [
            MessageHandler(
                filters=conv_filters,
                callback=conv_get_subject,
            )
        ],
        ConvState.QUESTION: [
            MessageHandler(
                filters=conv_filters,
                callback=conv_get_question,
            )
        ],
        ConvState.SEND: [
            MessageHandler(
                filters=conv_filters,
                callback=conv_end,
            )
        ],
    },
    fallbacks=[
        MessageHandler(
            filters=(filters.Regex(pattern=cancel_pattern) | filters.COMMAND),
            callback=conv_cancel,
        ),
    ],
)


tg_question_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=conv_get_question,
            pattern=MainCallbacks.TG_QUESTION,
        ),
    ],
    states={
        ConvState.SEND: [
            MessageHandler(
                filters=conv_filters,
                callback=conv_end,
            )
        ],
    },
    fallbacks=[
        MessageHandler(
            filters=(filters.Regex(pattern=cancel_pattern) | filters.COMMAND),
            callback=conv_cancel,
        ),
    ],
)
