import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    Updater
)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


START_ROUTES, END_ROUTES = range(2)

ONE, TWO, THREE, FOUR = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = []
    questions = context.bot_data.get('answers')
    for i in questions.keys():
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    keyboard.append([InlineKeyboardButton('Вернуться в меню', callback_data='MENU')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите вопрос ниже ⬇️", reply_markup=reply_markup)
    return START_ROUTES


async def FAQList(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = []
    questions = context.bot_data.get('answers')
    for i in questions.keys():
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    keyboard.append([InlineKeyboardButton('Вернуться в меню', callback_data='MENU')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите вопрос ниже ⬇️", reply_markup=reply_markup)
    return START_ROUTES


async def FAQAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    questions = context.bot_data.get('answers')
    keyboard = [
        [InlineKeyboardButton("Вернуться к вопросам", callback_data='FAQLIST')],
        [InlineKeyboardButton("Вернуться в меню", callback_data='MENU')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=questions.get(data), reply_markup=reply_markup
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Вы в главном меню")
    return ConversationHandler.END


def main() -> None:

    answers = {

        'Первый вопрос':'Ответ на первый вопрос',
        'Второй вопрос':'Ответ на второй вопрос',
        'Третий вопрос':'Ответ на третий вопрос',
        'Четвертый вопрос':'Ответ на четвертый вопрос',

    }

    application = Application.builder().token("").build()
    application.bot_data['answers'] = answers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(FAQList, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(FAQList, pattern="^" + 'FAQLIST' + "$"),
                CallbackQueryHandler(end, pattern="^" + 'MENU' + "$"),
                CallbackQueryHandler(FAQAnswer),
            ],
            END_ROUTES: [
                CallbackQueryHandler(end, pattern="^" + 'MENU' + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
