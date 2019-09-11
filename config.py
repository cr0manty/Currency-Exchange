import os
token = '973630042:AAE3jwuO6d7H9enrFbRRmuQlQkkun9wAdD4'
course_api = 'https://api.cryptonator.com/api/ticker/{}-{}'
web_hook_url = 'https://exchange-currency-bot.herokuapp.com/'


class Configuration(object):
    if "HEROKU" not in list(os.environ.keys()):
        DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///curenncy.db'