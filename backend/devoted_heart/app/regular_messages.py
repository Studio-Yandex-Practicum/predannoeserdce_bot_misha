import asyncio
import logging
import json
import os
import random
import requests
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from requests.exceptions import RequestException

from app.models import Customer, Messages

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
URLD = 'https://api.thedogapi.com/v1/images/search'
URLC = 'https://api.thecatapi.com/v1/images/search'
URLTEXT = 'https://api.forismatic.com/api/1.0/?method=getQuote&format=jsonp&jsonp=parseQuote'  # noqa

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start_scheduler():
    """
    Рассылка сообщений по расписанию 1 раз в три дня
    """
    asyncio.sleep(1)
    if not scheduler.running:
        scheduler.add_job(
            send_messages, 'interval',
            seconds=72 * 60 * 60, id='send_messages_job'
        )
        scheduler.start()


def stop_scheduler():
    """
    Остановка регулярной рассылки сообщений
    """
    if scheduler.running:
        scheduler.remove_job('send_messages_job')


def get_random_text():
    messages = [
        "Привет! Как дела?",
        "Замечательный день для общения!",
        "С вами всегда приятно общаться."
    ]
    return random.choice(messages)


def get_random_positive_thought():
    try:
        response = requests.get(URLTEXT)
        response.raise_for_status()  # Raises HTTPError if any
        jsonp_content = response.text
        start_pos = jsonp_content.find('(') + 1
        end_pos = jsonp_content.rfind(')')
        json_content = jsonp_content[start_pos:end_pos]
        quote_data = json.loads(json_content)
        quote = quote_data.get('quoteText', '')
        author = quote_data.get('quoteAuthor', '')
        return quote + '  ' + author
    except RequestException as e:
        logger.error(f"Ошибка получить positive thought: {e}")
        return None


def get_random_cat_image():
    try:
        response = requests.get(URLC)
        response.raise_for_status()
        cat_data = response.json()
        if cat_data:
            return cat_data[0].get('url')
    except RequestException as e:
        logger.error(f"Ошибка получить cat image: {e}")
    return None


def get_random_dog_image():
    try:
        response = requests.get(URLD)
        response.raise_for_status()
        dog_data = response.json()
        if dog_data:
            return dog_data[0].get('url')
    except RequestException as e:
        logger.error(f"Ошибка получить dog image: {e}")
    return None


def send_regular_message(chat_id, message_content=None):
    try:
        if message_content:
            bot.send_message(chat_id, message_content)
        text = get_random_text()
        cat_photo = get_random_cat_image()
        dog_photo = get_random_dog_image()
        phrase = get_random_positive_thought()
        choices = [1, 2, 3, 4]
        _choice = random.choice(choices)
        if _choice == 1:
            bot.send_message(chat_id, text)
        elif _choice == 2:
            bot.send_photo(chat_id, cat_photo)
        elif _choice == 3:
            bot.send_photo(chat_id, dog_photo)
        elif _choice == 4:
            bot.send_message(chat_id, phrase)
    except telebot.apihelper.ApiException as e:
        logger.error(f"Telegram API error: {e}")


def get_chat_ids():
    try:
        chat_ids = Customer.objects.values_list(
            'tg_id', flat=True
        )      # нет subscribed в модели .filter(subscribed=True)??
        return chat_ids
    except Exception as e:
        logger.error(f"Ошибка с получением chat IDs: {e}")
        return []


def send_messages(selected_messages=None):
    chat_ids = get_chat_ids()
    for chat_id in chat_ids:
        try:
            if selected_messages:
                for message in selected_messages:
                    send_regular_message(chat_id, message.text)
            else:
                for message in Messages.objects.all():
                    send_regular_message(chat_id, message.text)
        except Exception as e:
            logger.error(
                f"Ошибка с отправкой сообщений на chat ID {chat_id}: {e}"
            )
