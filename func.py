import re
import requests

from manage import Currency
from app import db


class Value:
    def __init__(self, text):
        try:
            self.amount_from = CourseList.to_digit(text[0])
            self.name_from = text[1]
            self.name_to = text[2]
            self.amount_to = 0
        except:
            raise ValueError('Not enough information')

    def __str__(self):
        return '{} {} = {} {}'.format(self.amount_from,
                                      self.name_from,
                                      self.amount_to,
                                      self.name_to)

    def __bool__(self):
        return self.name_to and self.amount_from

    def get(self):
        course = requests.get(CourseList.API.format(
            self.name_from, self.name_to)).json()['ticker']['price']
        self.amount_to = round(CourseList.to_digit(course) * self.amount_from, 4)


class CourseList:
    course_list = []
    value = None
    API = 'https://api.cryptonator.com/api/ticker/{}-{}'

    def __init__(self):
        self.course_list = Currency.query.all()
        self.index = len(self.course_list)

    @staticmethod
    def to_digit(num):
        try:
            return int(num)
        except ValueError:
            try:
                return float(num)
            except ValueError:
                return 0

    def in_list(self, text):
        return text[1] in self.course_list and text[2] in \
               self.course_list and self.to_digit(text[0])

    def __eq__(self, other):
        if other == 'usd':
            return True
        r = requests.get(self.API.format('usd', other)).json()
        return False if r['error'] else True

    def __iadd__(self, other):
        cor = Currency(name=other)
        self.course_list.append(cor)
        db.session.add(cor)
        db.session.commit()
        return self

    def update(self, values):
        self.value = Value(values)
        self.value.get()
        return self.value is not None

    def __bool__(self):
        return len(self.course_list) != 0

    def __getitem__(self, index):
        return self.course_list[index]

    def __contains__(self, item):
        return item in self

    def __len__(self):
        return len(self.course_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index != 0:
            self.index -= 1
            return self.course_list[self.index]
        else:
            self.index = self.__len__()
            raise StopIteration


def parse_text(text):
    value = re.search(r'\d+ \w{3} \w{3}', text)
    return value.group() if value else None
