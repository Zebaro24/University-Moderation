from discord_bot.main_discord import start as start_discord
from telegram_bot.main_telegram import start as start_telegram
from threading import Thread
from utils import bc, set_logger, info, time_start_bot
from os.path import isfile
from subprocess import Popen, PIPE
from database_func import load_all_elements
import locale


# Функция запуска ботов
def start_bots():
    time_start_bot()
    Popen(r"java -jar Lavalink.jar", stdout=PIPE, shell=True)

    load_all_elements()
    locale.setlocale(locale.LC_ALL, "ru_RU")

    Thread(target=start_telegram, daemon=True).start()
    start_discord()


# Запуск всего скрипта
if __name__ == '__main__':
    set_logger()
    print(f"{bc(32)}<---Программа была запущена--->{bc()}")
    info("<---Программа была запущена--->")
    start_bots()
    print(f"{bc(32)}<---Программа была остановлена--->{bc()}")
    info("<---Программа была остановлена--->")
    print("P.S.: Денис конечно же голова")
