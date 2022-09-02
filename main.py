from discord_bot.main_discord import start as start_discord
from telegram_bot.main_telegram import start as start_telegram
from threading import Thread
from utils import bc
from os.path import isfile
from subprocess import Popen, PIPE
from database_func import load_all_elements
import locale
from timetable.additional_func import check_default
from timetable.notification import check_task


# Функция запуска ботов
def start_bots():
    if isfile(r"D:\Install\Lavalink\Lavalink.jar"):
        Popen(r"cd /d D:\Install\Lavalink & java -jar Lavalink.jar", stdout=PIPE, shell=True)
    else:
        print(f"{bc(31)}<---Lavalink не установлен--->{bc()}")

    load_all_elements()
    locale.setlocale(locale.LC_ALL, "ru_RU")
    check_default()
    check_task()

    Thread(target=start_discord, daemon=True).start()
    start_telegram()


# Запуск всего скрипта
if __name__ == '__main__':
    print(f"{bc(32)}<---Программа была запущена--->{bc()}")
    start_bots()
    print(f"{bc(32)}<---Программа была остановлена--->{bc()}")
    print("P.S.: Денис конечно же голова")
