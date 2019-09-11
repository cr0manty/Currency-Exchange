import os
token = '973630042:AAHmUwaqitpNSnm3BWs2uQCmY53byZxDOl8'
course_api = 'https://api.cryptonator.com/api/ticker/{}-{}'
web_hook_url = 'https://exchange-currency-bot.herokuapp.com/'
WEB_DEBUG = int(os.environ.get('HEROKU_DEBUG'))


class Configuration(object):
    DEBUG = WEB_DEBUG if "HEROKU" in list(os.environ.keys()) else True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///curenncy.db'