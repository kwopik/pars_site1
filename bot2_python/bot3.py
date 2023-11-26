import requests
from bs4 import BeautifulSoup 
import pandas as pd
import telebot
from telebot import types

token="6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8"

bot=telebot.TeleBot(token)
user_texts = {}
target_chat_id = '6950234094'


@bot.message_handler(commands=['start'])
def handle_start(message):
 
   bot.send_message(message.chat.id, "пиши")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, f"вывод: {message.text}")
    user_texts[message] = message.text
     response = requests.get(user_texts)
     if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
       
     
      a_tags = soup.find_all('div', class_='c-price') 

     for a_tag in a_tags:
        print({url}, a_tag.text)

     else:
      print(f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')
 

bot.polling(none_stop=True)

