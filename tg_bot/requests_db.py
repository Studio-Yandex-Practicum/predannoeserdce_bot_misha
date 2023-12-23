import json
import os
from http import HTTPStatus

import requests
from requests import Response

from constants import (
    ADMIN_LOGIN,
    ADMIN_PASSWORD,
    SERVER_API_FAQ_URL,
    SERVER_API_TOKEN_URL,
    MainCallbacks,
)
from message_config import MESSAGES, MenuLogMessage
from settings import bot_logger


def get_faq() -> list[dict[str, str | int]]:
    """Получение из БД списка частых вопросов и ответов."""
    url = SERVER_API_FAQ_URL
    results = {}
    while True:
        try:
            response: Response = requests.get(url=url)
        except Exception as error:
            bot_logger.error(msg=MenuLogMessage.UNKNOWN_ERROR % (error,))
        if response.status_code != HTTPStatus.OK:
            bot_logger.error(
                msg=MenuLogMessage.SERVER_ERROR % (response.status_code,)
            )
            return [
                {
                    "question": MESSAGES["server_error"],
                    "order": MainCallbacks.SERVER_ERROR,
                }
            ]
        data = response.json()
        results.update(data["results"])
        if not data["next"]:
            break
        url = data["next"]
    bot_logger.info(msg=MenuLogMessage.UPDATE_FAQ_DICT)
    return results


def get_token():
    token_url = SERVER_API_TOKEN_URL
    credentials = {"email": ADMIN_LOGIN, "password": ADMIN_PASSWORD}
    response = requests.post(token_url, data=credentials)
    print(response.text)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("auth_token")
        os.environ["ADMIN_TOKEN"] = token
        bot_logger.info(msg="Токен получен")
