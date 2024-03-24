import telebot
from os import getenv

TOKEN = getenv("IE_101_TOKEN")

bot = telebot.TeleBot(TOKEN)
