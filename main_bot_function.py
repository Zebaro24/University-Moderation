from telebot import TeleBot
from config import TELEGRAM_API

from discord.ext.commands import Bot
from discord import Intents
from dislash import InteractionClient

bot_tg = TeleBot(TELEGRAM_API)

bot_ds = Bot("!", intents=Intents.all())
slash = InteractionClient(bot_ds)
