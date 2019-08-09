import re
import requests
from app.config import course_api, course_list


def parse_text(_text):
    pattern = r'\d+ \w{3} \w{3}'
    value = re.search(pattern, _text)
    return value.group() if value else None


def to_digit(num):
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            return 0


def format_course(_text):
    message = '{} {} = {} {}'.format(_text[0], _text[1], _text[3], _text[2])
    return message


def get_course(values):
    try:
        course = requests.get(course_api.format(values[1], values[2])).json()['ticker']['price']
        return round(to_digit(course) * float(values[0]), 4)
    except:
        return


def check_course(to_check):
    r = requests.get(course_api.format('usd',to_check.lower())).json()
    return False if r['error'] else True
