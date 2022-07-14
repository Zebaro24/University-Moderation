from telebot import TeleBot
import config

bot = TeleBot(config.TELEGRAM_API)


def start():
    bot.polling()


if __name__ == '__main__':
    start()
