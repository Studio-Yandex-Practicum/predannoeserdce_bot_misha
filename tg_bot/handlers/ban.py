from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from core.constants import START_SLEEP, BanList
from handlers.basic import handle_show_main_menu
from core.message_config import BotLogMessage, ConversationTextMessage
from core.settings import bot_logger


async def handle_to_ban(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Добавление пользователя в чёрный список."""
    query = update.callback_query
    context.user_data["callback"] = query.data
    text = query.message.text.split()
    user_id = next(word for word in text if "id:" in word)[3:]
    with open(
        file=BanList.FILENAME, mode="a", encoding=BanList.ENCODING
    ) as file:
        file.write(user_id + "\n")
    bot_logger.info(msg=BotLogMessage.USER_ADD_TO_BAN % user_id)
    await query.answer()
    await query.edit_message_text(
        text=ConversationTextMessage.USER_ADD_TO_BAN % user_id
    )


async def handle_user_at_ban(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заканчивает общение, т.к. пользователь в чёрном списке."""
    await update.effective_message.edit_text(
        text=ConversationTextMessage.USER_EXIST_AT_BAN,
    )
    await handle_show_main_menu(
        update=update, context=context, delay=START_SLEEP
    )
    bot_logger.info(
        msg=BotLogMessage.USER_EXIST_AT_BAN % context.user_data["user_id"]
    )
    context.user_data["callback"] = None
    return ConversationHandler.END
