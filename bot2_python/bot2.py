import telebot
from telebot import types

token="6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8"

bot=telebot.TeleBot(token)

target_chat_id = '6950234094'

@bot.message_handler(commands=['start'])
def handle_start(message):
 
   bot.send_message(message.chat.id, "пиши")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, f"вывод: {message.text}")

bot.polling(none_stop=True)