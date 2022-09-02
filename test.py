import datetime
from pytz import timezone

tz = timezone("Europe/Kyiv")
dt = datetime.datetime.now(tz)

print(dt)
print(dt.tzname())

print(datetime.date.today().strftime('%Y:%m:%d '))
print(datetime.datetime.today().strftime('%Y:%m:%d '))
# from telebot import TeleBot
#
# from config import TELEGRAM_API, tg_chanel_id
#
# bot = TeleBot(TELEGRAM_API)
# id_channel = -1001624889289
#
# while True:
#     text = input("Текст: ")
#     bot.send_message(id_channel, text)
