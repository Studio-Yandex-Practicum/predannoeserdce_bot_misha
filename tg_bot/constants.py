﻿import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

BACK_TO_MENU = 'Вернуться в меню'
SERVER_IP = os.getenv('SERVER_IP')
MENU = 'MENU'
BACK_TO_FAQ = 'Вернуться к вопросам'
FAQLIST = 'FAQLIST'
IN_MENU = 'Вы в главном меню'
SELECTFAQ = 'Выберите вопрос ниже ⬇️'