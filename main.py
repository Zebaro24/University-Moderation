from discord_bot.main import start as start_discord
from telegram_bot.main import start as start_telegram


async def start_bots():
    await start_discord()
    await start_telegram()


if __name__ == '__main__':
    start_bots()
    print("denis crutoy perets")
