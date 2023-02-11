import locale
from logging import exception
from telebot import types

from other.IE_101.additional_func import check_default
from other.IE_101.function import markup_all
from other.IE_101.command import timetable_text
from time import sleep
from other.IE_101.database_func import admins, load_all_elements
from other.IE_101.bot import bot


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    if message.chat.type == "private":

        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJIdhhiSG0K6iUciZOoueWASUDG1jHoAACoAEAAjDUnRGDNNeGcpfWEyIE')
        bot.send_message(message.chat.id, f'Приветствую {message.from_user.first_name} рад вас видеть здесь.')
        if message.chat.id in admins:
            bot.send_message(message.chat.id, f'Ты админ!\n',
                             reply_markup=markup_all(message.chat.id))

        else:
            bot.send_message(message.chat.id, 'Ось твої можливості!', reply_markup=markup_all(message.chat.id))


@bot.message_handler(content_types=['text'])
def message_text(message: types.Message):
    timetable_text(message)  # Сделать если использовалось то возвращать тру


class MyExcept:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def handle(self, exceptions):
        exception("Telegram")
        return True


def start():
    locale.setlocale(locale.LC_ALL, "ukr")
    load_all_elements()
    bot.exception_handler = MyExcept()
    check_default()

    while True:
        try:

            bot.polling(none_stop=True)
        except Exception as e:
            exception("Telegram")
        else:
            return
        sleep(3)


if __name__ == '__main__':
    start()
