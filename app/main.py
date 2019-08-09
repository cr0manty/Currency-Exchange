import telebot
from app.config import token
from emoji import emojize
from app.func import *
from telebot import types

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def update_course(message):
    bot.send_message(message.chat.id, 'Приветик, ' + message.from_user.first_name +
                     '! Я бот который конверирует необходимую сумму из одной валюты в другую.' +
                     "Формат ввода: 'число' 'валюта из' 'валюта в'" + emojize(':eyes:'))


@bot.inline_handler(func=lambda query: len(query.query) > 8)
def query_text(query):
    try:
        parse_text(query.query)
    except AttributeError as e:
        return
    text = query.query.upper().split()
    try:
        if text[1] in keys_first and text[2] in keys_first and to_digit(text[0]):
            text.append(get_course(text))
            result = types.InlineQueryResultArticle(
                id='0', title="Конвертор",
                description=format_course(text),
                input_message_content=types.InputTextMessageContent(
                    message_text=format_course(text)))
        else:
            result = types.InlineQueryResultArticle(
                id='0', title="Не формат", description="Формат: 'число' 'валюта из' 'валюта в'",
                input_message_content=types.InputTextMessageContent(
                    message_text=''))
        bot.answer_inline_query(query.id, [result])

    except Exception as e:
        return


@bot.inline_handler(func=lambda query: len(query.query) < 8)
def empty_query(query):
    hint = "Введите ровно 2 числа и получите результат!"
    try:
        r = types.InlineQueryResultArticle(
            id='1',
            title='Ожидается формат',
            description="Формат: 'число' 'валюта из' 'валюта в'",
            input_message_content=types.InputTextMessageContent(
                message_text=query.query)
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['know'])
def known_course(message):
    known = ''
    for i in keys_first:
        known += i + ' '
    bot.send_message(message.chat.id, known)


@bot.message_handler(commands=['add'])
def add_course(message):
    new_course = message.text.upper().split()[1]
    if len(new_course) != 3:
        bot.send_message(message.chat.id, 'Ошибочка! Такой курс невозможен!\
                                          Для добавления курса требуется ввести его аббревиатуру!\n\
                                          Пример сообщения: \'/add uah\'')
    elif new_course in keys_first:
        bot.send_message(message.chat.id, 'Такой курс уже у меня есть!☺')
    else:
        course = check_course(message.text)
        #TODO исправить
        if course:
            keys_first.append(new_course)
            write_to_file(new_course)
        else:
            bot.send_message(message.chat.id, 'Ох! Я не могу найти такую валюту 😰')



@bot.message_handler(content_types=['text'])
def send_text(message):
    if parse_text(message.text):
        text = message.text.upper().split()
        if text[1] in keys_first and text[2] in keys_first and to_digit(text[0]):
            text.append(get_course(text))
            bot.send_message(message.chat.id, format_course(text))
        else:
            bot.send_message(message.chat.id, 'Выражение введено неправильно '
                             + emojize(':anxious_face_with_sweat:'))

    elif 'привет' in message.text.lower():
        bot.send_message(message.chat.id, 'Приветик, ' + message.from_user.first_name + emojize(
            ':winking_face:'))

    elif 'пока' in message.text.lower():
        bot.send_message(message.chat.id, 'Прощай' + emojize(':anxious_face_with_sweat:'))
    else:
        bot.send_message(message.chat.id, 'Извини, я не понимаю что ты сказал'
                         + emojize(':grinning_face_with_sweat:'))


if __name__ == '__main__':
    read_from_file()
    bot.polling()
