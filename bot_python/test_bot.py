import telebot
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time

# Токен бота
token = "6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8"
bot = telebot.TeleBot(token)


# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на товар для парсинга.")

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
          products_name = soup.find_all('a', class_='c-text')
          prices = soup.find_all('div', class_='c-price')

          page_data = {'Текст': [], 'Цена': []}

          for  product_name, price in zip( products_name, prices):
            # Добавляем данные о товаре в словарь
            page_data['Текст'].append(product_name.text.strip())
            page_data['Цена'].append(price.text.strip())

            # Выводим результат в чат
            bot.send_message(message.chat.id, f" NAME: {product_name.text.strip()}, PRICE: {price.text.strip()}, ")
            bot.send_message(message.chat.id, f" url: {url}")
        else:
            bot.send_message(message.chat.id, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')



# Бесконечный цикл для регулярной отправки уникальных URL раз в час
#   while True:
 #   send_unique_urls()
  #  time.sleep(3600)
    
# Запускаем бота
bot.polling(none_stop=True)

# Закрываем соединение с базой данных при выходе

