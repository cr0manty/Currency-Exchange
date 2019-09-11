token = '973630042:AAE3jwuO6d7H9enrFbRRmuQlQkkun9wAdD4'
course_api = 'https://api.cryptonator.com/api/ticker/{}-{}'
web_hook_url = 'https://money-exchange-currency-bot.herokuapp.com/'


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///curenncy.db'