import requests

from constants import SERVER_IP


def getFaq():
    answers = []
    print('get start')
    link = f'http://{SERVER_IP}/api/faq'
    while True:
        res = requests.get(link)
        data = res.json()['results']
        print(data)
        answers  += data
        if res.json()['next'] == None:
            break
        link = res.json()['next']
    return answers
