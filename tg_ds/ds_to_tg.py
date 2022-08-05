from telegram_bot.main_telegram import bot as bot_tg
from config import tg_chanel_id


def discord_to_tg(message):
    bot_tg.send_message(tg_chanel_id, f"{message.author.display_name} : {message.content}")
