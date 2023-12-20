import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TOKEN_UPDATE = 12

ADMIN_LOGIN = os.getenv('ADMIN_LOGIN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

API_CUSTOMER = 'http://84.201.129.17:8000/api/customer/'

class SubState(int, Enum):
    CHOOSING = 0
    TYPING_REPLY = 1
    TYPING_CHOICE = 2
