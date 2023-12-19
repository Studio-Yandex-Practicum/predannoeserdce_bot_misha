import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TOKEN_UPDATE = 12


API_CUSTOMER = 'http://84.201.129.17:8000/api/customer/'

class SubState(int, Enum):
    CHOOSING = 0
    TYPING_REPLY = 1
    TYPING_CHOICE = 2
