import re
import requests


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
    url = 'https://api.exchangerate-api.com/v4/latest/{}'
    if value == 'BTC':
        return requests.get(
            'https://bitbay.net/API/Public/btcusd/ticker.json').json()['average'], \
               url.format('usd')
    return 1, url.format(value)


def get_course(values):
    amount, url = if_btc(values[1])
    amount, url = if_btc(values[2])
    r = requests.get(url)
    course = r.json()
    return course['rates'][values[2]] * amount * to_digit(values[0])
