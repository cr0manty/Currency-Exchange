from os import environ
token = '973630042:AAE3jwuO6d7H9enrFbRRmuQlQkkun9wAdD4'
db_file = 'course.db'
course_api = 'https://api.cryptonator.com/api/ticker/{}-{}'


def check_heroku():
    return "HEROKU" in list(environ.keys())
