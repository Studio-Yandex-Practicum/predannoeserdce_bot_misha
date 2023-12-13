import logging

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackQueryHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

from constants import (BACK_TO_FAQ, BACK_TO_MENU, FAQLIST, IN_MENU, MENU,
                       SELECTFAQ, SERVER_IP)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

START_ROUTES, END_ROUTES = range(2)

async def getFaq():
    answers = []
    while True:
        link = f'http://{SERVER_IP}/api/faq'
        res = requests.get(link)
        data = res.json()['results']
        answers  += data
        if res.json()['next'] == None:
            break
        link = res.json()['next']
    return answers


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    keyboard = []
    logger.info("Пользователь %s перешел в раздел FAQ.", user.first_name)
    answers = getFaq()
    context.bot_data['answers'] = answers
    for i in answers:
        keyboard.append([InlineKeyboardButton(i['question'], callback_data=i['question'])])
    keyboard.append([InlineKeyboardButton(BACK_TO_MENU, callback_data=MENU)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(SELECTFAQ, reply_markup=reply_markup)
    return START_ROUTES


async def FAQList(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = []
    questions = context.bot_data.get('answers')
    for i in questions:
        keyboard.append([InlineKeyboardButton(i['question'], callback_data=i['question'])])
    keyboard.append([InlineKeyboardButton(BACK_TO_MENU, callback_data=MENU)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=SELECTFAQ, reply_markup=reply_markup)
    return START_ROUTES


async def FAQAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    questions = context.bot_data.get('answers')
    for pair in questions:
        if pair['question'] == data:
            answer = pair['answer']
    keyboard = [
        [InlineKeyboardButton(BACK_TO_FAQ, callback_data=FAQLIST)],
        [InlineKeyboardButton(BACK_TO_MENU, callback_data=MENU)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
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
        ],
        END_ROUTES: [
            CallbackQueryHandler(end, pattern="^" + MENU + "$"),
        ],
    },
    fallbacks=[MessageHandler(filters.Text(['Частые вопросы']), start)],
)
