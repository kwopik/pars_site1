import telebot
import mysql.connector
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Токен бота
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

# Создаем таблицу price_history, если ее еще нет
create_table_query = """
CREATE TABLE IF NOT EXISTS price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL
);
"""
cursor.execute(create_table_query)
connection.commit()

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне название товара и его цену или ссылку для парсинга.")

# Обработчик для любого текстового сообщения
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith('http'):
        # Если сообщение начинается с http, считаем его ссылкой и выполняем парсинг
        handle_url(message)
    else:
        # Иначе обрабатываем текст как свободный текст
        # Получаем название товара и цену из сообщения
        product_name, price = parse_message(message.text)

        # Сохраняем введенные данные в базу данных
        save_to_database(product_name, price)

        # Выводим историю цен для товара
        price_history = get_price_history(product_name)
        bot.send_message(message.chat.id, price_history)

# Функция для разбора сообщения на название товара и цену
def parse_message(text):
    # Пример разбора: "Название: Цена"
    parts = text.split(':')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    else:
        return text.strip(), "Неизвестная цена"

# Функция для сохранения данных в базу данных
def save_to_database(product_name, price):
    # SQL-запрос для вставки данных в таблицу price_history
    insert_query = "INSERT INTO price_history (product_name, price, timestamp) VALUES (%s, %s, %s)"
    timestamp = datetime.now()

    # Вставляем данные в таблицу MySQL
    cursor.execute(insert_query, (product_name, price, timestamp))
    connection.commit()

# Функция для получения истории цен из базы данных
def get_price_history(product_name):
    # SQL-запрос для выбора данных из таблицы price_history
    select_query = "SELECT price, timestamp FROM price_history WHERE product_name = %s"
    
    # Выполняем запрос
    cursor.execute(select_query, (product_name,))
    result = cursor.fetchall()

    # Собираем историю цен в текстовую строку
    history_text = f"История цен для товара {product_name}:\n"
    if result:
        for row in result:
            history_text += f"Цена: {row[0]}, Дата и время: {row[1]}\n"
    else:
        history_text += f"Для товара {product_name} нет истории цен."

    return history_text

# Функция для обработки URL и сохранения данных в базе
def handle_url(message):
    url = message.text
    try:
        # Выполняем HTTP-запрос для получения содержимого страницы
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Извлекаем название товара и цену
            product_name = soup.find('a', class_='c-text').text.strip()
            price = soup.find('div', class_='c-price').text.strip()

            # Сохраняем введенные данные в базу данных
            save_to_database(product_name, price)

            # Выводим историю цен для товара
            price_history = get_price_history(product_name)
            bot.send_message(message.chat.id, price_history)
        else:
            bot.send_message(message.chat.id, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

# Запускаем бота
bot.polling(none_stop=True)

# Закрываем соединение с базой данных при выходе
cursor.close()
connection.close()
