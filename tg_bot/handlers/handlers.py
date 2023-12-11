import requests

def FAQList():
    res = requests.get('https://scotch.io')
    print(res)

FAQList()