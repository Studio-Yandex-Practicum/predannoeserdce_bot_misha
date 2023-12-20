import logging


from telegram import Update
from telegram.ext import (CallbackQueryHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters, CommandHandler)

from constants import (FAQLIST, IN_MENU, MENU, SELECTFAQ)
from keyboards import AnswerKeyboard, FAQKeyboard
from utils import getFaq


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

START_ROUTES, END_ROUTES = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Пользователь %s перешел в раздел FAQ.", user.first_name)
    answers = getFaq()
    context.bot_data['answers'] = answers
    await update.message.reply_text(SELECTFAQ, reply_markup=FAQKeyboard(answers))
    return START_ROUTES


async def FAQList(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    questions = context.bot_data.get('answers')
    await query.edit_message_text(text=SELECTFAQ, reply_markup=FAQKeyboard(questions))
    return START_ROUTES


async def FAQAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    questions = context.bot_data.get('answers')
    for pair in questions:
        if pair['question'] == data:
            answer = pair['answer']
    await query.edit_message_text(
        text=answer, reply_markup=AnswerKeyboard()
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=IN_MENU)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(['Частые вопросы']), start)],
    states={
        START_ROUTES: [
            CallbackQueryHandler(FAQList, pattern="^" + FAQLIST + "$"),
            CallbackQueryHandler(end, pattern="^" + MENU + "$"),
            CallbackQueryHandler(FAQAnswer),
            CommandHandler("menu", end),
        ],
        END_ROUTES: [
            CallbackQueryHandler(end, pattern="^" + MENU + "$"),
            CommandHandler("menu", end),
        ],
    },
    fallbacks=[MessageHandler(filters.Text(['Частые вопросы']), start)],
)
