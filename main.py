from discord_bot.main_discord import start as start_discord
from telegram_bot.main import start as start_telegram


def start_bots():
    start_discord()
    start_telegram()


if __name__ == '__main__':
    start_bots()
    print("denis crutoy perets")
