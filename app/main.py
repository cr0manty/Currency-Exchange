import telebot
import config
import requests
from datetime import datetime, timedelta
from emoji import emojize

bot = telebot.TeleBot(config.token)
course = list()
currency = {'USD': '$', 'RUB': '₽', 'EUR': '€'}


def stf(num):
    try:
        val = int(num)
    except ValueError:
        try:
            val = float(num)
        except ValueError:
            val = 1
    return val


def make_update(message, first_text='Обновление данных. Подождите...' + emojize(':eyes:')):
    bot.send_message(message.chat.id, first_text)
    get_course()
    msg = 'Данные успешно обновленны!' + emojize(':winking_face:') if \
        course else 'Ошибка, попробуйте позже. ' + emojize(':grinning_face_with_sweat:')
    bot.send_message(message.chat.id, msg + '''
Теперь я готов к работе и могу перевести любую сумму гривен в другие валюты.\n
Для этого пришли мне необходимое число и я покажу тебе кое что ''' + emojize(':new_moon_face:'))


def format_course(amount=1.0):
    message = ''
    amount = stf(amount)

    for i in course['exchangeRate']:
        if 'currency' in i and i['currency'] in currency:
            message += '*{}*₴ в {} = *{}*{}\n'.format(amount, i['currency'], i['saleRateNB'] * amount,
                                                  currency[i['currency']])
    message += 'Курс актуален на {}\nДанные взяты с {}'.format(course['date'], course['bank'])
    return message


def get_course(day=0):
    r = requests.get(
        'https://api.privatbank.ua/p24api/exchange_rates?json&date={}'.format(
            datetime.strftime(datetime.now() - timedelta(day), '%d.%m.%Y')))
    if not r.json()['exchangeRate']:
        get_course(day + 1)
    else:
        global course
        course = r.json()


@bot.message_handler(commands=['update'])
def upd(message):
    make_update(message)


@bot.message_handler(commands=['start'])
def update_course(message):
    make_update(message,
                'Привет, для начала работы мне нужно обновить данные. Подожди немного ' + emojize(':eyes:'))


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.isdigit():
        bot.send_message(message.chat.id,
                         format_course(message.text) if course else 'Данные для обмена отсутствуют, требуется обновление',
                         parse_mode= 'Markdown')
    elif 'привет' in message.text.lower():
        bot.send_message(message.chat.id, 'Приветик, ' + message.from_user.first_name + emojize(
            ':winking_face:'))
    elif 'пока' in message.text.lower():
        bot.send_message(message.chat.id, 'Прощай' + emojize(':anxious_face_with_sweat:'))
    else:
        bot.send_message(message.chat.id, 'Извини, я не понимаю что ты сказал' + emojize(':grinning_face_with_sweat:'))

if __name__ == '__main__':
    bot.polling()
