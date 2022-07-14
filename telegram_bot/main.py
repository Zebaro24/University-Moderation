from telebot import TeleBot
import config

import discord_bot.main_discord

bot = TeleBot(config.TELEGRAM_API)

@bot.message_handler(content_types=["text"])
def telega_to_ds(message):
    discord_bot.main_discord.bot.get_guild(config.discord_guild).get_chanell("997248600960680058").send(message.text)

def start():
    bot.polling()


if __name__ == '__main__':
    start()
