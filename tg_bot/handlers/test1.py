import requests


def get_token():
# URL для получения токена
    token_url = 'http://84.201.129.17:8000//api/auth/token/login/'

    # Данные логина и пароля
    credentials = {
        'email': 'test@test.ru',
        'password': 'predannoe'
    }

    # Отправка POST-запроса для получения токена
    response = requests.post(token_url, data=credentials)

    # Проверка статуса запроса
    if response.status_code == 200:
        # Обработка успешного запроса - получение токена
        token_data = response.json()
        access_token = token_data.get('auth_token')
        print('Токен доступа:', access_token)
    else:
        # Обработка ошибки запроса
        print('Ошибка при получении токена:', response.status_code)

get_token()