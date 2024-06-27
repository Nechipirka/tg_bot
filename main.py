import telebot
from telebot import types
import datetime
import re
from math import floor

import base

bot = telebot.TeleBot('7204281465:AAGEzB_3uu9_KJmLBOTkn-QL44P9zLDcvl8', parse_mode=None)


# Обработка команды 'start'
@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, Здравствуйте!\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_options = types.KeyboardButton("Что ты умеешь делать?")
    btn_authentication = types.KeyboardButton("Войти или зарегистрироваться")
    markup.add(btn_options, btn_authentication)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text in ('Войти', 'Попробовать снова'):
        markup = types.ReplyKeyboardRemove(selective=False)
        mesg = bot.send_message(message.chat.id, text="Введите логин и пароль для входа", reply_markup=markup)
        bot.register_next_step_handler(mesg, login)

    elif message.text in ('Регистрация', 'Пройти регистрацию заново',):
        markup = types.ReplyKeyboardRemove(selective=False)
        mesg = bot.send_message(message.chat.id, text="Введите логин и пароль для регистрации", reply_markup=markup)
        bot.register_next_step_handler(mesg, registration)

    elif message.text in ('Войти или зарегистрироваться', 'Авторизация'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_login = types.KeyboardButton("Войти")
        btn_registration = types.KeyboardButton("Регистрация")
        markup.add(btn_login, btn_registration)
        bot.send_message(message.chat.id, text='Авторизация', parse_mode='html', reply_markup=markup)

    elif message.text in ('Что ты умеешь делать?', 'Что ты умеешь делать'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_time = types.KeyboardButton("Время")
        btn_me = types.KeyboardButton("Кто ты?")
        btn_why = types.KeyboardButton("Зачем тебя создали?")
        btn_match = types.KeyboardButton("Решать пример")
        btn_authentication = types.KeyboardButton("Авторизация")
        markup.add(btn_time, btn_me, btn_why, btn_match, btn_authentication)
        bot.send_message(message.chat.id,
                         text='Я умею выполнять простые математические задачи, подсказывать который час и регистрировать вас в базе данных',
                         parse_mode='html', reply_markup=markup)

    elif message.text in ('Какое сейчас время?', 'Сколько времени?', 'Который час?',
                          'Какое сейчас время', 'Сколько времени', 'Который час', 'Время'):
        # Проверка есть ли id пользователя в базе
        if base.check_id(message.chat.id):
            current_datetime = datetime.datetime.now()
            bot.send_message(message.chat.id,
                             text=f'Сейчас {current_datetime.hour} часов {current_datetime.minute} минут',
                             parse_mode='html')

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_authentication = types.KeyboardButton("Войти или зарегистрироваться")
            markup.add(btn_authentication)
            bot.send_message(message.chat.id, text='Доступ к функционалу ограничен, пройдите авторизацию',
                             parse_mode='html', reply_markup=markup)

    elif message.text in ('Реши пример', 'Решить ещё', 'Решать пример'):
        # Проверка есть ли id пользователя в базе
        if base.check_id(message.chat.id):
            markup = types.ReplyKeyboardRemove(selective=False)
            mesg = bot.send_message(message.chat.id, text="Введите пример", reply_markup=markup)
            bot.register_next_step_handler(mesg, math)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_authentication = types.KeyboardButton("Войти или зарегистрироваться")
            markup.add(btn_authentication)
            bot.send_message(message.chat.id, text='Доступ к функционалу ограничен, пройдите авторизацию',
                             parse_mode='html', reply_markup=markup)

    elif message.text in ('Кто ты?', 'Кто ты'):
        bot.send_message(message.chat.id, text='Я телеграм бот, созданых для выполнения простых задач)',
                         parse_mode='html')

    elif message.text in ('Зачем тебя создали?', 'Зачем тебя создали'):
        bot.send_message(message.chat.id, text='Меня создали для демонстрации умений хозяина', parse_mode='html')

    elif message.text.lower() in ('пока', 'до свидания'):
        bot.send_message(message.chat.id, text='До скорой встречи)', parse_mode='html')

    elif message.text.lower() in ('спасибо', 'спасибо за помощь'):
        bot.send_message(message.chat.id, text='Обращайтесь снова)', parse_mode='html')


# Функция входа пользователя
def login(message):
    data = str(message.text).split()
    if len(data) != 2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_login = types.KeyboardButton("Попробовать снова")
        markup.add(btn_login)
        bot.send_message(message.chat.id, text="Данные введены неверно", parse_mode='html', reply_markup=markup)

    else:
        if base.login_db(data[0], data[1], message.chat.id):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_options = types.KeyboardButton("Что ты умеешь делать?")
            markup.add(btn_options)
            bot.send_message(message.chat.id, text="Вы успешно вошли)))", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_login = types.KeyboardButton("Попробовать снова")
            markup.add(btn_login)
            bot.send_message(message.chat.id, text="Введён неверный логин или пароль", parse_mode='html',
                             reply_markup=markup)


# Функция регистрации пользователя
def registration(message):
    data = str(message.text).split()
    if len(data) != 2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_registration = types.KeyboardButton("Пройти регистрацию заново")
        markup.add(btn_registration)
        bot.send_message(message.chat.id, text="Данные введены неверно", parse_mode='html', reply_markup=markup)

    else:
        if base.registration_db(data[0], data[1], message.chat.id):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_registration = types.KeyboardButton("Войти")
            markup.add(btn_registration)
            bot.send_message(message.chat.id, text="Вы успешно зарегистрировались, попробуйте войти", parse_mode='html',
                             reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_registration = types.KeyboardButton("Пройти регистрацию заново")
            markup.add(btn_registration)
            bot.send_message(message.chat.id, text="Данный логин уже используется", parse_mode='html',
                             reply_markup=markup)


# Функция решающая математические задачи
def math(message):
    words = ['сложи', 'вычти', 'умножить', 'разделить']
    # Если использовали слова 'сложи', 'вычти', 'умножить', 'разделить'
    if any(s in str(message.text).lower() for s in words):
        data = str(message.text).split()
        if data[-1].isdigit() and data[-3].isdigit():
            if 'сложи' in str(message.text).lower():
                res = int(data[-1]) + int(data[-3])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_more = types.KeyboardButton("Решить ещё")
                markup.add(btn_more)
                bot.send_message(message.chat.id, text=f'Результат вычисления {res}',
                                 parse_mode='html', reply_markup=markup)

            elif 'вычти' in str(message.text).lower():
                res = int(data[-1]) - int(data[-3])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_more = types.KeyboardButton("Решить ещё")
                markup.add(btn_more)
                bot.send_message(message.chat.id, text=f'Результат вычисления {res}',
                                 parse_mode='html', reply_markup=markup)

            elif 'умножить' in str(message.text).lower():
                res = int(data[-1]) * int(data[-3])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_more = types.KeyboardButton("Решить ещё")
                markup.add(btn_more)
                bot.send_message(message.chat.id, text=f'Результат вычисления {res}',
                                 parse_mode='html', reply_markup=markup)

            elif 'разделить' in str(message.text).lower():
                res = int(data[-3]) / int(data[-1])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_more = types.KeyboardButton("Решить ещё")
                markup.add(btn_more)
                bot.send_message(message.chat.id, text=f'Результат вычисления {res}',
                                 parse_mode='html', reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_options = types.KeyboardButton("Что ты умеешь делать?")
            btn_more = types.KeyboardButton("Решить ещё")
            markup.add(btn_options, btn_more)
            bot.send_message(message.chat.id,
                             text='Введены некоректные данные, попробуйте ещё раз. Пример"Сложи 5 и 10"',
                             parse_mode='html', reply_markup=markup)

    # Если написали пример вида 10 * 10
    else:
        expression = re.search(r"\d+ ([+*\-/]) \d+", str(message.text))
        if expression:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_options = types.KeyboardButton("Что ты умеешь делать?")
            btn_more = types.KeyboardButton("Решить ещё")
            markup.add(btn_options, btn_more)
            bot.send_message(message.chat.id, text=f'Результат вычисления {floor(eval(expression.group()))}',
                             parse_mode='html', reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_options = types.KeyboardButton("Что ты умеешь делать?")
            btn_more = types.KeyboardButton("Решить ещё")
            markup.add(btn_options, btn_more)
            bot.send_message(message.chat.id,
                             text='Введены некоректные данные, попробуйте добавить пробелы между числами и знаками',
                             parse_mode='html', reply_markup=markup)


bot.infinity_polling()
