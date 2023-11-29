import requests
from bs4 import BeautifulSoup
import mysql.connector
import telebot
from telebot import types

# Токен бота
token = "6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8"
bot = telebot.TeleBot(token)

# Словарь для хранения введенных текстов по chat_id
user_texts = {}
all_data = []

# Параметры подключения к MySQL
db_config = {
    'host': '192.168.99.241',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'mydatabase'
}

# Подключение к MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Создаем таблицу osnova, если ее еще не существует
create_table_query = """
CREATE TABLE IF NOT EXISTS osnova (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL
);
"""
cursor.execute(create_table_query)

# Создаем таблицу osnova_new, если ее еще не существует
create_table_query_new = """
CREATE TABLE IF NOT EXISTS osnova_new (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL
);
"""
cursor.execute(create_table_query_new)

# Обработчик свободного текста
@bot.message_handler(func=lambda message: True)
def handle_free_text(message):
    # Проверяем, начинается ли текст с команды /caps
    if message.text.startswith('/caps'):
        # Если да, вызываем обработчик команды /caps
        handle_caps_command(message)
    else:
        # Иначе обрабатываем текст как свободный текст
        # Сохраняем введенный текст в словаре по chat_id
        user_texts[message.chat.id] = message.text

        # Выводим сообщение об успешном сохранении
        bot.send_message(message.chat.id, f"Ты сказал: {message.text}")

        # Выполняем запись данных в таблицу osnova
        process_user_text(message.chat.id, message.text)

# Обработчик команды /caps
@bot.message_handler(commands=['caps'])
def handle_caps_command(message):
    # Выводим сообщение о начале выполнения команды
    bot.send_message(message.chat.id, "Начинаю выполнение команды /caps...")

    # Выполняем сравнение данных
    compare_data(message.chat.id)

# Функция для записи данных в таблицу osnova
def process_user_text(chat_id, text):
    # Выполняем запрос с использованием введенного текста
    response = requests.get(text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a', class_='c-text')
        prices = soup.find_all('div', class_='c-price')

        # Создаем список кортежей с данными для вставки в таблицу osnova
        data_to_insert = [(a_tag.text, price.text.strip()) for a_tag, price in zip(a_tags, prices)]

        # SQL-запрос для вставки данных в таблицу osnova
        insert_query = "INSERT INTO osnova (name, price) VALUES (%s, %s)"

        # Вставляем данные в таблицу MySQL
        cursor.executemany(insert_query, data_to_insert)

        # Подтверждаем изменения в базе данных
        connection.commit()

        # Выводим результат в чат
        bot.send_message(chat_id, "Данные успешно записаны в таблицу osnova.")

        # После успешной записи выполняем сравнение данных
        compare_data(chat_id)

    else:
        # Сообщение об ошибке при выполнении запроса
        bot.send_message(chat_id, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')

# Функция для сравнения данных в таблицах osnova и osnova_new
def compare_data(chat_id):
    # SQL-запрос для сравнения данных в таблицах osnova и osnova_new
    compare_query = """
    SELECT o.name, o.price AS old_price, n.price AS new_price
    FROM osnova o
    JOIN osnova_new n ON o.name = n.name AND o.price <> n.price
    UNION
    SELECT o.name, o.price AS old_price, NULL AS new_price
    FROM osnova o
    LEFT JOIN osnova_new n ON o.name = n.name
    WHERE n.name IS NULL;
    """

    # Выполнение запроса на сравнение данных
    cursor.execute(compare_query)
    result = cursor.fetchall()

    # Проверка наличия различий
    if not result:
        bot.send_message(chat_id, "Данные в таблицах osnova и osnova_new идентичны.")
    else:
        bot.send_message(chat_id, "Обнаружены изменения в данных между таблицами osnova и osnova_new:")
        for row in result:
            if row[2] is not None:
                bot.send_message(chat_id, f"Товар: {row[0]}, Было: {row[1]}, Стало: {row[2]}")
            else:
                bot.send_message(chat_id, f"Товар: {row[0]}, Было: {row[1]}, Стало: NULL (удалено)")

# Запускаем бота
bot.polling(none_stop=True)

# Закрываем соединение с базой данных при выходе
cursor.close()
connection.close()
