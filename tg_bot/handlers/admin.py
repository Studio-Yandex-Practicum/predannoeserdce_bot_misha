from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import core.keyboards as kb
from core.constants import ADMIN_CHAT_ID
from core.message_config import ConversationLogMessage, ConversationTextMessage
from core.settings import bot_logger


async def handle_admin_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обработка ответа администратора, отправка его пользователю."""
    if update.message.from_user.id != int(ADMIN_CHAT_ID):
        return None
    text = update.message.reply_to_message.text.split()
    to_chat_id = int(next(word for word in text if "id:" in word)[3:])

    await context.bot.send_message(
        chat_id=to_chat_id,
        text=ConversationTextMessage.ANSWER_FROM_ADMIN % update.message.text,
        parse_mode=ParseMode.HTML,
        reply_markup=await kb.get_main_menu(user_id=to_chat_id),
    )
    bot_logger.info(msg=ConversationLogMessage.ANSWER_FROM_ADMIN % to_chat_id)
