from .config import debug
from .utils import bc, set_logger, info, time_start_bot

from .discord_bot.main_discord import start as start_discord
from .telegram_bot.main_telegram import start as start_telegram

from .other.IE_101.main_telegram import start as start_dima_bot
from .other.feit_bot import start_feit_bot

from .database_func import load_all_elements

from threading import Thread
from subprocess import Popen, PIPE
import locale


class Worker:
    def __init__(self):
        pass

    # Функция запуска ботов
    @staticmethod
    def start():
        set_logger()
        print(f"{bc(32)}<---Программа была запущена--->{bc()}")
        info("<---Программа была запущена--->")
        time_start_bot()

        Popen(r"java -jar Lavalink.jar -Xmx200m", stdout=PIPE, shell=True)

        load_all_elements()
        locale.setlocale(locale.LC_ALL, "uk_UA")

        Thread(target=start_telegram, daemon=True).start()
        if not debug:
            Thread(target=start_feit_bot, daemon=True).start()
            Thread(target=start_dima_bot, daemon=True).start()
        start_discord()

        print(f"{bc(32)}<---Программа была остановлена--->{bc()}")
        info("<---Программа была остановлена--->")
        print("P.S.: Денис конечно же голова")


# Запуск всего скрипта
if __name__ == '__main__':
    Worker().start()
