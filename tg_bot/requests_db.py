import os
from http import HTTPStatus

import requests
from requests import Response

from constants import (
    ADMIN_LOGIN,
    ADMIN_PASSWORD,
    SERVER_API_FAQ_URL,
    SERVER_API_TOKEN_URL,
    SERVER_API_SUBS_URL,
    SERVER_API_CUSTOMER_URL,
    MainCallbacks,
)
from message_config import MainMessage, BotLogMessage
from services import get_headers
from settings import bot_logger


def get_faq() -> dict[str | int, str]:
    """Получение из БД списка частых вопросов и ответов."""
    url = SERVER_API_FAQ_URL
    results = {}
    while True:
        try:
            response: Response = requests.get(url=url)
        except Exception as error:
            bot_logger.error(msg=BotLogMessage.UNKNOWN_ERROR % (error,))
        if response.status_code != HTTPStatus.OK:
            bot_logger.error(
                msg=BotLogMessage.SERVER_ERROR % (response.status_code,)
            )
            results.update(
                {
                    MainCallbacks.SERVER_ERROR: {
                        "question": MainMessage.SERVER_ERROR,
                    }
                }
            )
            return results
        data = response.json()
        results.update(data["results"])
        if not data["next"]:
            break
        url = data["next"]
    bot_logger.info(msg=BotLogMessage.UPDATE_FAQ_DICT)
    return results


def get_token() -> None:
    token_url = SERVER_API_TOKEN_URL
    credentials = {"email": ADMIN_LOGIN, "password": ADMIN_PASSWORD}
    response = requests.post(url=token_url, data=credentials)
    if response.status_code != 200:
        return None
    token_data = response.json()
    token = token_data.get("auth_token")
    os.environ["ADMIN_TOKEN"] = token
    bot_logger.info(msg=BotLogMessage.TOKEN_RECEIVED)


def check_subscribe(user_id):
    subscribe_url = f'{SERVER_API_SUBS_URL}{user_id}'
    token = os.getenv(key="ADMIN_TOKEN")
    response = requests.get(
        url=subscribe_url,
        headers=get_headers(token=token),
    )
    return response


def delete_subscribe(user_id):
    subscribe_url = f'{SERVER_API_SUBS_URL}{user_id}'
    token = os.getenv(key="ADMIN_TOKEN")
    response = requests.delete(
        url=subscribe_url,
        headers=get_headers(token=token),
    )
    return response
