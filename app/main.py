from app.config import telebot, token, keys_first
from emoji import emojize
from app.func import parse_text, get_course, format_course, to_digit

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def update_course(message):
    bot.send_message(message.chat.id, 'Приветик, ' + message.from_user.first_name +
                     '! Я бот который конверирует необходимую сумму из одной валюты в другую.' +
                     'Для начала работы выбери какую валюту тебе нужно конвертировать' + emojize(':eyes:'))


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
    bot.polling()
