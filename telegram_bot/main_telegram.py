import os

from telebot import types
from utils import print_tg, bc, exception, from_bytes
import utils
from speedtest import Speedtest
from config import tg_chanel_id
from threading import Thread
from timetable.additional_func import check_default

from main_bot_function import bot_tg as bot

from timetable.notification import check_task, go_task
from tg_ds.tg_to_ds import coroutine_send
from telegram_bot.timetable.function import markup_all
from telegram_bot.timetable.command import timetable_text
from time import sleep
from database_func import admins


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    if message.chat.type == "private":

        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJIdhhiSG0K6iUciZOoueWASUDG1jHoAACoAEAAjDUnRGDNNeGcpfWEyIE')
        bot.send_message(message.chat.id, f'Приветствую {message.from_user.first_name} рад вас видеть здесь.')
        if message.chat.id in admins:
            commands = "/id - ID группы\n" \
                       "/logs_file - Логи бота\n" \
                       "/del_logs - Удалить логи\n" \
                       "/status_all_bot - Статус обеих ботов"
            bot.send_message(message.chat.id, f'Ты админ!\nВот твои команды:\n{commands}',
                             reply_markup=markup_all(message.chat.id))

        else:
            bot.send_message(message.chat.id, 'Вот твои возможности!', reply_markup=markup_all(message.chat.id))


@bot.message_handler(commands=['id'])
def send_id(message: types.Message):
    bot.send_message(message.chat.id, f"Id группы: {message.chat.id}")
    print_tg(f"Id группы: {message.chat.id}")


@bot.message_handler(commands=['logs_file'])
def send_logs(message: types.Message):
    bot.send_message(message.chat.id, "Запрос логов...")
    if os.path.getsize("info.log"):
        info = open("info.log", "rb")
        bot.send_document(message.chat.id, info)
    else:
        bot.send_message(message.chat.id, "Логи INFO небыли найдены!")

    if os.path.getsize("error.log"):
        error = open("error.log", "rb")
        bot.send_document(message.chat.id, error)
    else:
        bot.send_message(message.chat.id, "Логи ERROR небыли найдены!")


@bot.message_handler(commands=['del_logs'])
def del_logs(message: types.Message):
    open("info.log", "w").close()
    open("error.log", "w").close()
    bot.send_message(message.chat.id, "Логи очищены!")


@bot.message_handler(commands=['status_all_bot'])
def status(message: types.Message):
    text = "*Статус бота:*\n"
    text += f"Бот был запущен: *{utils.start_time}*\n"
    if utils.telegram_error:
        text += f"Telegram бот имел: *{utils.telegram_error} ошибок*\n"
    else:
        text += f"Telegram бот не имел ошибок!\n"

    if utils.discord_error:
        text += f"Discord бот имел: *{utils.discord_error} ошибок*\n"
    else:
        text += f"Discord бот не имел ошибок!\n"

    text += "\n"
    text += f"INFO весит: *{from_bytes(os.path.getsize('info.log'))}*\n"
    text += f"ERROR весит: *{from_bytes(os.path.getsize('error.log'))}*\n"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

    st = Speedtest()
    st.get_best_server()
    text = "*Скорость интернета:*\n"
    text += f"Пинг: *{st.results.ping}*\n"
    bot.send_message(message.chat.id, "Проверка скорости скачивания...")
    text += f"Скорость скачивания: *{from_bytes(st.download())}*\n"
    bot.send_message(message.chat.id, "Проверка скорости загрузки...")
    text += f"Скорость загрузки: *{from_bytes(st.upload())}*\n"

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def message_text(message: types.Message):
    timetable_ret = timetable_text(message)  # Сделать если использовалось то возвращать тру
    if timetable_ret:
        bot.forward_message(tg_chanel_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Ваше сообщение было отправлено в общий чат!',
                         reply_markup=markup_all(message.chat.id))

    if message.chat.id == tg_chanel_id or timetable_ret:
        coroutine_send(message)


@bot.message_handler(
    content_types=['audio', 'photo', 'voice', 'video_note', 'video', 'document', 'location', 'contact', 'sticker',
                   'animation'])
def telegram_ds(message):
    coroutine_send(message)

    if message.chat.type == "private":
        bot.forward_message(tg_chanel_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Ваше сообщение было отправлено в общий чат!',
                         reply_markup=markup_all(message.chat.id))


class MyExcept:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def handle(self, exceptions):
        exception("Telegram")
        print_tg(f"Произошла ошибка: {exceptions}")
        return True


def start():
    bot.exception_handler = MyExcept()
    print_tg(f"Бот был {bc('01;38;05;34')}запущен{bc()} под именем: {bot.user.first_name}")

    check_default()
    check_task()
    Thread(target=go_task, daemon=True).start()

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            exception("Telegram")
            print_tg(f'Бот перезапустился из за \n{repr(e)}')
        else:
            return
        sleep(3)


if __name__ == '__main__':
    start()
