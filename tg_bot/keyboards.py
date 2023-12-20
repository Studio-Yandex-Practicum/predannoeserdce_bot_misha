from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants import (BACK_TO_FAQ, BACK_TO_MENU, FAQLIST, MENU,)


def FAQKeyboard(answers):
    keyboard = []
    for i in answers:
        keyboard.append([InlineKeyboardButton(i['question'], callback_data=i['question'])])
    keyboard.append([InlineKeyboardButton(BACK_TO_MENU, callback_data=MENU)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def AnswerKeyboard():
    keyboard = [
        [InlineKeyboardButton(BACK_TO_FAQ, callback_data=FAQLIST)],
        [InlineKeyboardButton(BACK_TO_MENU, callback_data=MENU)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
