from telebot import TeleBot

from config import TELEGRAM_API, tg_chanel_id

bot = TeleBot(TELEGRAM_API)
id_channel = -1001624889289

while True:
    text = input("Текст: ")
    bot.send_message(id_channel, text)
