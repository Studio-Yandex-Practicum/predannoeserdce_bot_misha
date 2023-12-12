import logging
import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

LOGGING_LEVEL = logging.INFO

MENU_ITEMS = {
    "Частые вопросы": "faq",
    "Задать по email": "email_question",
    "Задать вопрос": "custom_question",
    "Посмотреть котиков": "see_cats",
    "Взять котика": "adopt_cat",
    "Попечительство": "patronage",
    "Пожертвования": "donat",
}

MENU_LAYOUT = (3, 2, 2)

START_SLEEP = 3
MENU_SLEEP = 5
