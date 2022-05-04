from main import collect_data
import telebot
from telebot import types
import os

token = "TOKEN"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['go', 'start'])  # Обработка команды для старта
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item3 = types.KeyboardButton("Города")
    markup.add(item3)

    bot.send_message(message.chat.id,
                     "<i>Добро пожаловать, {0.first_name}!</i>\n"
                     "Бот называется - <b>{1.first_name}</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['stop'])   # обработка команды остановки
def end(message):
    kill_keyboard = types.ReplyKeyboardRemove()   #убирает клавиатуру
    bot.send_message(message.chat.id, 'Досвидания, {0.first_name}, бот останавниает свою работу'.format(message.from_user, bot.get_me()), reply_markup=kill_keyboard)
    exit()

@bot.callback_query_handler(lambda call: call.data in ['Moscow', 'Yarensk'])  # обработчик Приложений callback_data
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Moscow':
                bot.send_message(call.message.chat.id, "Подождите немного" )
                file = collect_data(city_code='2398')
                bot.send_document(call.message.chat.id, document=open(file, 'rb'))
                os.remove(file)

            elif call.data == 'Yarensk':
                bot.send_message(call.message.chat.id, "Подождите немного")
                file = collect_data(city_code='13067')
                bot.send_document(call.message.chat.id, document=open(file, 'rb'))
                os.remove(file)


    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=['text'])
def go_send_message(message):
    if message.text == 'Города':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton('Moscow', callback_data='Moscow')
        button2 = types.InlineKeyboardButton('Yarensk', callback_data='Yarensk')
        # по callback_data мы будем обрабатывать кнопки, по возращаемому значению

        keyboard.add(button2, button1)

        bot.send_message(message.chat.id, 'Смотри какие есть города', reply_markup=keyboard)

# RUN
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)
    finally:
        print("Здесь всё закончилось")

# проверяю ебат
