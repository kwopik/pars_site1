
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime


token = "6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8"
bot = telebot.TeleBot(token)

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

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Пришли мне URL для парсинга.")

# Обработчик для входящих текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Получаем текст сообщения от пользователя
    user_input_text = message.text

    # Выполняем обработку текста
    handle_free_text(user_input_text, message.chat.id)

# Обработчик свободного текста
def handle_free_text(text, chat_id):
    # Выполняем запрос с использованием введенного текста
    response = requests.get(text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a', class_='c-text')
        prices = soup.find_all('div', class_='c-price')

        # Создаем название для новой таблицы из значения name
        table_name = a_tags[0].text.strip().replace(' ', '_').lower()

        # SQL-запрос для создания новой таблицы
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            price VARCHAR(50) NOT NULL,
            time_and_date DATETIME NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Вставляем данные в новую таблицу
        insert_query = f"INSERT INTO {table_name} (price, time_and_date) VALUES (%s, %s)"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_to_insert = [(price.text.strip(), current_time) for price in prices]
        cursor.executemany(insert_query, data_to_insert)

        # Подтверждаем изменения в базе данных
        connection.commit()

        # Выводим результат в чат
        bot.send_message(chat_id, f"Данные успешно записаны в таблицу {table_name}.")

    else:
        # Сообщение об ошибке при выполнении запроса
        bot.send_message(chat_id, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')

# Запуск бота
bot.polling(none_stop=True)

# Закрываем соединение с базой данных при выходе
cursor.close()
connection.close()
