import json
import os

import requests

from constants import ADMIN_LOGIN, ADMIN_PASSWORD

def get_token():
    
    token_url = 'http://84.201.129.17:8000/api/auth/token/login/'
    credentials = {
        'email': ADMIN_LOGIN,
        'password': ADMIN_PASSWORD
    }
    response = requests.post(token_url, data=credentials)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get('auth_token')
        os.environ['ADMIN_TOKEN'] = token


def format_error_messages(text):
    errors = json.loads(text)
    error_messages = []
    for values in errors.values():
        for message in values:
            error_messages.append(message)
    return '\n'.join(error_messages)
