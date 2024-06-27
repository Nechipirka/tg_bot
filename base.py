import sqlite3
import datetime


# Функция регистрации пользователя
def registration_db(login_user, password_user, id_user):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    # Отпраляем запрос
    request = f"SELECT login FROM users WHERE login = '{login_user}'"
    cursor.execute(request)
    results = cursor.fetchall()

    # Запись sql запроса
    record(request, id_user)

    # Проверка пользователя
    if not results:
        # Добавляем нового пользователя
        request = f"INSERT INTO users (login, password, id) VALUES ('{login_user}', '{password_user}', '{id_user}')"
        cursor.execute(request)

        # Запись sql запроса
        record(request, id_user)

        # Сохраняем данные и закрываем соединение
        connection.commit()
        connection.close()
        return True
    else:
        # Закрываем соединение
        connection.close()
        return False


# Функция авторизации
def login_db(login_user, password_user, id_user):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    # Отпраляем запрос
    request = f"SELECT password FROM users WHERE login = '{login_user}'"
    cursor.execute(request)
    results = cursor.fetchall()

    # Запись sql запроса
    record(request, id_user)

    # Закрываем соединение
    connection.close()

    # Проверка пользователя
    if not results:
        return False
    elif ''.join(results[0]) == password_user:
        return True
    else:
        return False


# проверка id
def check_id(id_user):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()

    # Отпраляем запрос
    request = f"SELECT id FROM users WHERE id = '{id_user}'"
    cursor.execute(request)
    results = cursor.fetchall()

    # Запись sql запроса
    record(request, id_user)

    # Закрываем соединение
    connection.close()

    # Проверка пользователя
    if not results:
        return False
    elif ''.join(results[0]) == str(id_user):
        return True
    else:
        return False


# Функция записи sql запроса в файл
def record(request, id_user):
    current_datetime = datetime.datetime.now()
    file = open("query_database.txt", "a")
    file.write(f'{current_datetime.hour}, {current_datetime.minute} {id_user} {request}' + '\n')
    file.close()
