from telebot import TeleBot
from utils import print_tg
from config import TELEGRAM_API, tg_chanel_id

bot = TeleBot(TELEGRAM_API)

from telegram_bot.tg_to_ds import telegram_to_ds


@bot.message_handler(content_types=["text"])
def message_text(message):
    telegram_to_ds(message)

    bot.send_message(tg_chanel_id, "Проверка, отправлено!")
    pass


def start():
    print_tg(f"Бот был запущен под именем: {bot.user.first_name}")
    bot.polling()


if __name__ == '__main__':
    start()
