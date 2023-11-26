import requests
from bs4 import BeautifulSoup 
import telebot
from telebot import types

token="6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8"

bot=telebot.TeleBot(token)

# Словарь для хранения введенных текстов по chat_id
user_texts = {}
all_data = []

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Пиши мне что-нибудь.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Сохраняем введенный текст в словаре по chat_id
    user_texts[message.chat.id] = message.text

    # Выводим сообщение об успешном сохранении
    bot.send_message(message.chat.id, f"Ты сказал: {message.text}")

    # Передаем введенный текст в функцию для обработки
    process_user_text(message.chat.id, message.text)

def process_user_text(chat_id, text):
    # Выполняем запрос с использованием введенного текста
    response = requests.get(text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a', class_='c-text') 
        prices = soup.find_all('div', class_='c-price')
        page_data = {'Текст': [], 'Цена': []}

        for a_tag, price in zip(a_tags, prices):
            # Добавляем данные о товаре в словарь
            page_data['Текст'].append(a_tag.text)
            page_data['Цена'].append(price.text.strip())

            # Выводим результат в чат
            bot.send_message(chat_id, f" NAME: {a_tag.text}, PRICE: {price.text.strip()}")

        # Добавляем данные о товарах в общий список
        all_data.append(page_data)
    else:
        bot.send_message(chat_id, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')

# Запуск бота
bot.polling(none_stop=True)
