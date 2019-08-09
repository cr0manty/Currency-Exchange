import telebot
from app.config import token
from emoji import emojize
from app.func import *
from telebot import types

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def update_course(message):
    bot.send_message(message.chat.id, 'Приветик, ' + message.from_user.first_name +
                     '! Я бот который конверирует необходимую сумму из одной валюты в другую.\n' +
                     'Ты можешь использовать меня как в этом, так и в других чатах.\n' +
                     'Но тебе обязательно нужно придерживаться формата ввода 👀\n' +
                     "Формат ввода: 'число' 'валюта из' 'валюта в'")


@bot.inline_handler(func=lambda query: len(query.query) > 8)
def query_text(query):
    try:
        parse_text(query.query)
    except AttributeError as e:
        return
    text = query.query.upper().split()
    try:
        if text[1] in course_list and text[2] in course_list and to_digit(text[0]):
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
    try:
        result = types.InlineQueryResultArticle(
            id='1',
            title='Ожидается формат',
            description="Формат: 'число' 'валюта из' 'валюта в'",
            input_message_content=types.InputTextMessageContent(
                message_text=query.query)
        )
        bot.answer_inline_query(query.id, [result])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['know'])
def known_course(message):
    bot_message = ''
    for i in course_list:
        bot_message += i + ' '
    bot.send_message(message.chat.id, bot_message)


@bot.message_handler(commands=['add'])
def add_course(message):
    try:
        new_course = message.text.upper().split()[1]
        if len(new_course) != 3:
            bot.send_message(message.chat.id, '''Ошибочка! Такой курс невозможен!
Для добавления курса требуется ввести его аббревиатуру!
Пример сообщения: \'/add uah\'''')
        elif new_course in course_list:
            bot.send_message(message.chat.id, 'Такой курс уже у меня есть!☺')
        else:
            course = check_course(new_course)
            if course:
                course_list.append(new_course)
                bot.send_message(message.chat.id, 'Ура! Теперь мне доступна новая валюта!☺')
            else:
                bot.send_message(message.chat.id, 'Ох! Я не могу найти такую валюту 😰')
    except:
        bot.send_message(message.chat.id, 'Ой! Что-то пошло не так 😰')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if parse_text(message.text):
        text = message.text.upper().split()
        if text[1] in course_list and text[2] in course_list and to_digit(text[0]):
            text.append(get_course(text))
            bot.send_message(message.chat.id, format_course(text))
        else:
            bot.send_message(message.chat.id, 'Выражение введено неправильно или одна из валют мне не известна'
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
    bot.polling()
