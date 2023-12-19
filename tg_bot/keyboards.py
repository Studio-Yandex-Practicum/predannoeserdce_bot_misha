from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from message_config import CUSTOMER, SUB


async def get_customer_menu():

    keyboard = []
    for values, item in CUSTOMER.items():
        keyboard.append([InlineKeyboardButton(item, callback_data=values)])
        
    return InlineKeyboardMarkup(keyboard)

async def get_sub_menu():

    keyboard = []
    for values, item in CUSTOMER.items():
        keyboard.append([InlineKeyboardButton(item, callback_data=values)])
    for values, item in SUB.items():
        keyboard.append([InlineKeyboardButton(item, callback_data=values)])
    
    return InlineKeyboardMarkup(keyboard)
