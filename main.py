from discord_bot.main_discord import start as start_discord
from telegram_bot.main_telegram import start as start_telegram
from other.feit_bot import start_feit_bot
from other.IE_101.main_telegram import start as start_dima_bot
from threading import Thread
from utils import bc, set_logger, info, time_start_bot
from subprocess import Popen, PIPE
from database_func import load_all_elements
from config import debug
import locale


# Функция запуска ботов
def start_bots():
    Popen(r"java -jar Lavalink.jar -Xmx200m", stdout=PIPE, shell=True)

    load_all_elements()
    locale.setlocale(locale.LC_ALL, "uk_UA")

    Thread(target=start_telegram, daemon=True).start()
    if not debug:
        Thread(target=start_feit_bot, daemon=True).start()
        Thread(target=start_dima_bot, daemon=True).start()
    start_discord()


# Запуск всего скрипта
if __name__ == '__main__':
    set_logger()
    print(f"{bc(32)}<---Программа была запущена--->{bc()}")
    info("<---Программа была запущена--->")
    time_start_bot()
    start_bots()
    print(f"{bc(32)}<---Программа была остановлена--->{bc()}")
    info("<---Программа была остановлена--->")
    print("P.S.: Денис конечно же голова")
