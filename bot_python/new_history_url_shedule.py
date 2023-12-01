import telebot
import mysql.connector
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time

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
    url VARCHAR(255) NOT NULL,
    timestamp DATETIME NOT NULL
);
"""
cursor.execute(create_table_query)
connection.commit()

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на товар для парсинга.")

# Функция для отправки уникальных URL в чат
#@bot.message_handler(commands=['stop'])
   
def send_unique_urls(message):
    
    # SQL-запрос для выбора всех уникальных URL из таблицы price_history
    select_urls_query = "SELECT DISTINCT url FROM price_history"

    # Выполняем запрос
    cursor.execute(select_urls_query)
    unique_urls = cursor.fetchall()

    # Формируем текст с уникальными URL
    unique_urls_text = "Уникальные URL в базе данных:\n"
    for url in unique_urls:
        unique_urls_text += f"{url[0]}\n"
        bot.send_message(message.chat.id, f"тест таймера: {url}")
    
        # Отправляем текст с уникальными URL в чат
    
  #  bot.send_message(chat.id, unique_urls_text)

# Обработчик для любого текстового сообщения
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith('http'):
        # Если сообщение начинается с http, считаем его ссылкой и выполняем парсинг
        handle_url(message)
    else:
        # Иначе выводим сообщение о необходимости ввода ссылки
        bot.send_message(message.chat.id, "Введите ссылку на товар для парсинга.")

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
            save_to_database(product_name, price, url)

            # Выводим всю историю цен для товара
            price_history = get_price_history(product_name)
            bot.send_message(message.chat.id, price_history)
        else:
            bot.send_message(message.chat.id, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

# Функция для сохранения данных в базе данных
def save_to_database(product_name, price, url):
    # SQL-запрос для вставки данных в таблицу price_history
    insert_query = "INSERT INTO price_history (product_name, price, url, timestamp) VALUES (%s, %s, %s, %s)"
    timestamp = datetime.now()

    # Вставляем данные в таблицу MySQL
    cursor.execute(insert_query, (product_name, price, url, timestamp))
    connection.commit()

# Функция для получения истории цен из базы данных
def get_price_history(product_name):
    # SQL-запрос для выбора данных из таблицы price_history
    select_query = "SELECT price, timestamp FROM price_history WHERE product_name = %s ORDER BY timestamp DESC"
    
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



# Бесконечный цикл для регулярной отправки уникальных URL раз в час
while True:
    send_unique_urls(message)
    time.sleep(60)

# Запускаем бота
bot.polling(none_stop=True)

# Закрываем соединение с базой данных при выходе
cursor.close()
connection.close()
