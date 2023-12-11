import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BACKEND_IP = os.getenv('BACKEND_IP')
