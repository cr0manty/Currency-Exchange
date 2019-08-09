import re
import requests
from app.config import course_list, course_api, btc_api


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
        return requests.get(btc_api).json()['average'], \
               course_api.format('usd')
    return 1, course_api.format(value)


def get_course(values):
    amount, url = if_btc(values[1])
    # TODO добавить еще крипты
    course = requests.get(url).json()
    try:
        result = round(course['rates'][values[2]] * amount * to_digit(values[0]), 4)
        return result
    except KeyError:
        try:
            amount, url = if_btc(values[2])
            result = round(course['rates']['USD'] / amount * to_digit(values[0]), 4)
            return result
        except:
            return


def read_from_file():
    # TODO исправить /add
    global course_list
    with open('course.txt', 'r', encoding='utf-8') as f:
        from_file = f.read()
        course_list = from_file.split()


def write_to_file(data):
    with open('course.txt', 'a', encoding='utf-8') as f:
        f.write(data + ' ')


def check_course(to_check):
    return requests.get(course_api.format(to_check)).json()['rates'][to_check]
