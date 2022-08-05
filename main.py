from discord_bot.main_discord import start as start_discord
from telegram_bot.main_telegram import start as start_telegram
from threading import Thread
from utils import bc
from os.path import isfile
from subprocess import Popen, PIPE


def start_bots():
    if isfile(r"D:\Install\Lavalink\Lavalink.jar"):
        Popen(r"cd /d D:\Install\Lavalink & java -jar Lavalink.jar", stdout=PIPE, shell=True)
    else:
        print(f"{bc(31)}<---Lavalink не установлен--->{bc()}")
    Thread(target=start_discord, daemon=True).start()
    start_telegram()


if __name__ == '__main__':
    print(f"{bc(32)}<---Программа была запущена--->{bc()}")
    start_bots()
    print(f"{bc(32)}<---Программа была остановлена--->{bc()}")
    print("P.S.: Денис конечно же голова")
