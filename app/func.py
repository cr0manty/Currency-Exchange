import re
import requests
from app.config import keys_first, course_api


def parse_text(_text):
    pattern = r'\d+ \w{3} \w{3}'
    value = re.search(pattern, _text)
    return value.group() if value else None


def to_digit(num):
    try:
        return int(num)
    except ValueError:
        try:
            return round(float(num), 5)
        except ValueError:
            return 0


def format_course(_text):
    message = '{} {} = {} {}'.format(_text[0], _text[1], _text[3], _text[2])
    return message


def if_btc(value):
    if value == 'BTC':
        return requests.get(
            'https://bitbay.net/API/Public/btcusd/ticker.json').json()['average'], \
               course_api.format('usd')
    return 1, course_api.format(value)


def get_course(values):
    amount, url = if_btc(values[1])
    # TODO добавить из валюты в Биток
    # amount, url = if_btc(values[2])
    #TODO добавить еще крипты
    r = requests.get(url)
    course = r.json()
    return course['rates'][values[2]] * amount * to_digit(values[0])


def read_from_file():
    try:
        with open('couses.txt', 'r', encoding='utf-8') as f:
            keys_first = f.read().split()
    except:
        return


def write_to_file(data):
    try:
        with open('couses.txt', 'a', encoding='utf-8') as f:
            f.write(data + '')
    except:
        return


def check_course(to_check):
    return requests.get(course_api.format(to_check)).json()[to_check]
