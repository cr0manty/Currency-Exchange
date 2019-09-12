import os
TOKEN = '973630042:AAHmUwaqitpNSnm3BWs2uQCmY53byZxDOl8'


class Configuration(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///curenncy.db'