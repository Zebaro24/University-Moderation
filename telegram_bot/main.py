import telebot
import config

bot = telebot.TeleBot(config.TELEGRAM_API)


def start():
    bot.polling()


if __name__ == '__main__':
    pass
