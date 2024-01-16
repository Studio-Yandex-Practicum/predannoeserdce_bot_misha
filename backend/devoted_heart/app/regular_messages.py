import logging
import json
import os
import random
import requests
import sys
import telebot
# import time
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from telegram.error import InvalidToken

from app.models import Customer, Messages, SchedulerSettings


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
try:
    pass
except InvalidToken:
    logging.error("Invalid TELEGRAM_TOKEN.")
    sys.exit(1)

URLD = 'https://api.thedogapi.com/v1/images/search'
URLC = 'https://api.thecatapi.com/v1/images/search'
URLTEXT = 'https://api.forismatic.com/api/1.0/?method=getQuote&format=jsonp&jsonp=parseQuote'  # noqa
SLEEP_BETWEEN = 0.4
CHOICES = [1, 2, 3, 4]


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start_scheduler():
    """
    Запуск планировщика.
    Перепопределяем голбальную пременную,
    иначе возникает ошибка при ошибочной
    повторной отмене планировщика администратором
    """
    global scheduler
    try:
        if scheduler.running:
            scheduler.shutdown(wait=False)
    except Exception as e:
        logger.error(f"Ошибка при остановке планировщика: {e}")

    scheduler = BackgroundScheduler()
    scheduler_timing = SchedulerSettings.objects.first().scheduler_period
    scheduler.add_job(
        send_schedular_messages,
        'interval',
        seconds=scheduler_timing,
        id='send_messages_job'
    )
    scheduler.start()


def stop_scheduler():
    """
    Остановка планировщика рассылки сообщений
    """
    try:
        if scheduler.running:
            scheduler.remove_job('send_messages_job')
    except Exception as e:
        logger.error(f"Ошибка при остановке планировщика: {e}")


def get_random_text():
    """Случайный привет"""
    messages = [
        "Привет! Как дела?",
        "Замечательный день для общения!",
        "Привет от Фуражкина!",
        "С вами всегда приятно общаться."
    ]
    return random.choice(messages)


def get_random_positive_thought():
    """Умные мысли"""
    try:
        response = requests.get(URLTEXT)
        response.raise_for_status()
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
    """Фото кошки"""
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
    """Фото собаки"""
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
    """Сборка и рассылка регулярных сообщений"""
    try:
        if message_content:
            bot.send_message(chat_id, message_content)
        text = get_random_text()
        cat_photo = get_random_cat_image()
        dog_photo = get_random_dog_image()
        phrase = get_random_positive_thought()
        choices = CHOICES
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
    """Получение телеграм id клиентов"""
    try:
        chat_ids = Customer.objects.all().values_list(
            'tg_id', flat=True
        )
        return chat_ids
    except Exception as e:
        logger.error(f"Ошибка с получением chat IDs: {e}")
        return []


def send_message(chat_id, text):
    """Отправка текстового сообщения."""
    try:
        bot.send_message(chat_id, text)
    except Exception as e:
        logger.error(f'Ошибка с отправкой текста на chat ID {chat_id}: {e}')


def send_photo(chat_id, image_path):
    """Отправка фото."""
    try:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id, photo)
    except Exception as e:
        logger.error(
            f'Ошибка с отправкой изображения на {chat_id}: {e}'
        )


def send_messages(selected_messages=None):
    """Отправка разовых сообщений клиентам."""
    chat_ids = get_chat_ids()
    executor = ThreadPoolExecutor(max_workers=len(chat_ids))

    try:
        if selected_messages is None:
            logger.info('Не выбрано сообщение')
            return None

        futures = []

        for message_text in selected_messages:
            text = message_text.text
            image_path = message_text.image.path if message_text.image else None  # noqa

            for chat_id in chat_ids:
                if text:
                    futures.append(
                        executor.submit(send_message, chat_id, text)
                    )

                if image_path and os.path.exists(image_path):
                    futures.append(
                        executor.submit(send_photo, chat_id, image_path)
                    )

        for future in futures:
            future.result()
    except Exception as e:
        logger.error(f'Ошибка с отправкой сообщений: {e}')
    finally:
        executor.shutdown()


def send_schedular_messages(selected_messages=None):
    """Отправка случайных сообщений по расписанию."""
    chat_ids = get_chat_ids()
    selected_messages = Messages.objects.filter(selected=True)
    executor = ThreadPoolExecutor(max_workers=len(chat_ids))

    try:
        futures = []

        for chat_id in chat_ids:
            if selected_messages:
                for message in selected_messages:
                    futures.append(
                        executor.submit(
                            send_regular_message, chat_id, message.text
                        )
                    )
            else:
                futures.append(executor.submit(send_regular_message, chat_id))

        for future in futures:
            future.result()
    except Exception as e:
        logger.error(f'Ошибка с отправкой сообщений: {e}')
    finally:
        executor.shutdown()
