from discord_bot.main_discord import start as start_discord
from telegram_bot.main_telegram import start as start_telegram
from threading import Thread
from utils import bc


def start_bots():
    Thread(target=start_discord, daemon=True).start()
    start_telegram()


if __name__ == '__main__':
    print(f"{bc(35)}<---Програма была запущена--->{bc()}")
    start_bots()
    print("denis crutoy perets")
