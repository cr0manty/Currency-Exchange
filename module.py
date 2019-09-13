import os
import requests
import re

from telebot import TeleBot, types
from flask import request

from manage import Currency
from app import db


class Value:
    def __init__(self, text):
        self.amount_from = CourseList.to_digit(text[0])
        self.name_from = text[1]
        self.name_to = text[2]
        self.amount_to = 0

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

    @staticmethod
    def parse_text(text):
        value = re.search(r'\d+ \w{3} \w{3}', text)
        return value.group() if value else None

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
        return item in self.course_list

    def __len__(self):
        return len(self.course_list)

    def __iter__(self):
        return self

    def __str__(self):
        return str(self.value)

    def __next__(self):
        if self.index != 0:
            self.index -= 1
            return self.course_list[self.index]
        else:
            self.index = self.__len__()
            raise StopIteration


class StartBot(TeleBot):
    web_hook_url = 'https://exchange-currency-bot.herokuapp.com/'

    def __init__(self, server, token, debug=False):
        self.token = token
        super().__init__(token)
        self.server = server
        self.DEBUG = bool(os.environ.get('HEROKU_DEBUG') or debug)
        self.WEB = bool('HEROKU_DEBUG' in list(os.environ.keys()))
        self.remove_webhook()

    def start(self):
        if self.WEB:
            self.set_webhook(url=self.web_hook_url + self.token)
            self.server.run(host='0.0.0.0',
                            port=int(os.environ.get('PORT', 5000)),
                            debug=self.DEBUG)
        else:
            self.polling()

    def debug(self):
        return self.DEBUG

    def update(self):
        self.process_new_updates([
            types.Update.de_json(
                request.stream.read().decode('utf-8'))
        ])

    def msg_error(self, chat_id, exception, command):
        self.send_message(chat_id, "Exception called in '{}' with text: '{}'".
                          format(command, exception)
                          )

    def query_error(self, query_id, exception):
        result = types.InlineQueryResultArticle(
            id='0', title="Ошибка", description=exception,
            input_message_content='')
        self.answer_inline_query(query_id, [result])
