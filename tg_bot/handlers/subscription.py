import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

keyboard = [
    [InlineKeyboardButton('Email', callback_data='email'), InlineKeyboardButton('ФИО', callback_data='name')],
    [InlineKeyboardButton('Телефон', callback_data='phone')],
]
markup = InlineKeyboardMarkup(keyboard)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Чтобы подписаться на рассылку, немного расскажи о себе.",
        reply_markup=markup,
    )
    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.callback_query.data
    context.user_data["choice"] = text
    print(context.user_data)
    await update.callback_query.message.edit_text(f"Напишите ваш {text.lower()}")

    return TYPING_REPLY


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    if all(key in user_data for key in ['Email', 'name', 'telephone']):
        # Показываем кнопку "Подписаться"
        keyboard.append([InlineKeyboardButton('Подписаться', callback_data='sub')])
        markup = InlineKeyboardMarkup(keyboard)
    else:
        markup = InlineKeyboardMarkup(keyboard)
    del user_data["choice"]

    await update.message.reply_text(
        "Ваши данные:"
        f"{facts_to_str(user_data)}",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    print(user_data)
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"Вы подписаны на рассылку!{facts_to_str(user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END



# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(['Подписаться на рассылку']), start)],
    states={
        CHOOSING: [
            CallbackQueryHandler(regular_choice, pattern="^(email|name|phone)$"),
        ],
        TYPING_CHOICE: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Подписаться$")), regular_choice
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Подписаться$")),
                received_information,
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Подписаться$"), done)],
)


