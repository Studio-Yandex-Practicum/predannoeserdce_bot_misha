import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from constants import TELEGRAM_TOKEN, TOKEN_UPDATE
from handlers.subscription import sub_handler
from message_config import MESSAGES
from utils import get_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

scheduller = AsyncIOScheduler()
scheduller.add_job(
    func=get_token,
    trigger="interval",
    hours=TOKEN_UPDATE,
)
scheduller.start()
get_token()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отвечает пользователю на команду /start."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGES['start']
    )
    await asyncio.sleep(3)
    await menu(update, context)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команды основного меню."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGES['menu']
    )


async def alert_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отвечает пользователю на попытку отправить неподдерживаемый контент."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MESSAGES['alert_message']
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    handlers = [
        CommandHandler('start', start),
        CommandHandler('menu', menu),
        MessageHandler((filters.AUDIO | filters.PHOTO), alert_message),
        sub_handler
    ]
    for handler in handlers:
        application.add_handler(handler)
    application.run_polling()
