import scheduler
from pytz import timezone
import pytz
from time import sleep
from datetime import datetime

tz = timezone("Europe/Kyiv")

print(min({4: 2, 5: 3}))


def check_task():
    print("hello")
    print(datetime.now(timezone("Etc/GMT-1")))


gg = scheduler.Scheduler(tzinfo=timezone("Etc/GMT-1"))
gg.once(datetime(2022, 10, 4, 20, 33, tzinfo=timezone("Etc/GMT-1")), check_task)

while True:
    gg.exec_jobs()
    sleep(1)

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
