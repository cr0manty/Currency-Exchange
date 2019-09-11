import os
token = '973630042:AAHmUwaqitpNSnm3BWs2uQCmY53byZxDOl8'
web_hook_url = 'https://exchange-currency-bot.herokuapp.com/'
WEB_DEBUG = int(os.environ.get('HEROKU_DEBUG') or '0')


class Configuration(object):
    DEBUG = WEB_DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///curenncy.db'