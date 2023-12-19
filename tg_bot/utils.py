import json
import os

import requests


def get_token():
    
    token_url = 'http://84.201.129.17:8000/api/auth/token/login/'
    credentials = {
        'email': 'test@test.ru',
        'password': 'predannoe'
    }
    response = requests.post(token_url, data=credentials)
    if response.status_code == 200:
        # Обработка успешного запроса - получение токена
        token_data = response.json()
        token = token_data.get('auth_token')
        os.environ['ADMIN_TOKEN'] = token
    else:
        print('Ошибка при получении токена:', response.status_code)


def format_error_messages(text):
    errors = json.loads(text)
    error_messages = []
    for values in errors.values():
        for message in values:
            error_messages.append(message)
    return '\n'.join(error_messages)

