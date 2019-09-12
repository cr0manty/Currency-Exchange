# encoding=utf-8
from telebot import types
from emoji import emojize
import os

from module import CourseList, StartBot
from config import TOKEN
from app import server

bot = StartBot(server, TOKEN)
course = CourseList()


@bot.message_handler(commands=['start'])
def update_course(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name +
                     '! Я бот который конверирует необходимую сумму из одной валюты в другую.\n' +
                     'Ты можешь использовать меня как в этом, так и в других чатах.\n' +
                     'Но тебе обязательно нужно придерживаться формата ввода 👀\n' +
                     "Формат ввода: 'число' 'валюта из' 'валюта в'")


@bot.inline_handler(func=lambda query: len(query.query) > 8)
def query_text(query):
    try:
        CourseList.parse_text(query.query)
    except AttributeError as e:
        return
    text = query.query.upper().split()
    try:
        if course.update(text):
            result = types.InlineQueryResultArticle(
                id='0', title="Конвертор",
                description=str(course.value),
                input_message_content=types.InputTextMessageContent(
                    message_text=str(course.value)))
        else:
            result = types.InlineQueryResultArticle(
                id='0', title="Не формат", description="Формат: 'число' 'валюта из' 'валюта в'",
                input_message_content=types.InputTextMessageContent(
                    message_text=''))
        bot.answer_inline_query(query.id, [result])
    except Exception as e:
        if bot.debug():
            bot.query_error(query.id, e)


@bot.inline_handler(func=lambda query: len(query.query) < 8)
def empty_query(query):
    try:
        result = types.InlineQueryResultArticle(
            id='1',
            title='Ожидается формат',
            description="Формат: 'число' 'валюта из' 'валюта в'",
            input_message_content=types.InputTextMessageContent(
                message_text=query.query))
        bot.answer_inline_query(query.id, [result])
    except Exception as e:
        if bot.debug():
            bot.query_error(query.id, e)


@bot.message_handler(commands=['know'])
def known_course(message):
    try:
        bot_message = ''
        if not course:
            bot_message = 'Прости, я еще не знаю ни одной валюты'
        else:
            for i in course:
                bot_message += str(i) + ' '
        bot.send_message(message.chat.id, bot_message)
    except Exception as e:
        if bot.debug():
            bot.msg_error(message.chat.id, e, message.text)


@bot.message_handler(commands=['add'])
def add_course(message):
    global course
    try:
        new_course = message.text.lower().split()[1]
        if 3 < len(new_course) < 6:
            bot.send_message(message.chat.id, 'Ошибка! Такой курс невозможен!\n' +
                             'Для добавления курса требуется ввести его аббревиатуру!\n' +
                             "Пример сообщения: '/add uah'")
        elif new_course in course:
            bot.send_message(message.chat.id, 'Такой курс уже у меня есть!☺')
        else:
            if course == new_course:
                course += new_course
                bot.send_message(message.chat.id, 'Ура! Теперь мне доступна {}!☺'.
                                 format(new_course.upper()))
            else:
                bot.send_message(message.chat.id, 'Ох! Я не могу найти такую валюту 😰')
    except Exception as e:
        if bot.debug():
            bot.msg_error(message.chat.id, e, message.text)
        bot.send_message(message.chat.id, 'Ой! Что-то пошло не так 😰')


@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if CourseList.parse_text(message.text):
            text = message.text.upper().split()
            if course.update(text):
                bot.send_message(message.chat.id, str(course))
            else:
                bot.send_message(message.chat.id, 'Выражение введено неправильно или одна из валют мне не известна'
                                 + emojize(':anxious_face_with_sweat:'))
        elif 'привет' in message.text.lower():
            bot.send_message(message.chat.id, 'Приветик, ' + message.from_user.first_name
                             + emojize(':winking_face:'))
        elif 'пока' in message.text.lower():
            bot.send_message(message.chat.id, 'Прощай' + emojize(':anxious_face_with_sweat:'))
        else:
            bot.send_message(message.chat.id, 'Извини, я не понимаю что ты сказал'
                             + emojize(':grinning_face_with_sweat:'))
    except Exception as e:
        if bot.debug():
            bot.msg_error(message.chat.id, e, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.update()
    return 'Message update', 200


if __name__ == '__main__':
    bot.start()
