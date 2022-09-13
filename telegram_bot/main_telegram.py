from telebot import TeleBot, types
from utils import print_tg, bc
from config import TELEGRAM_API, tg_chanel_id
from threading import Thread
from timetable.additional_func import check_default

bot = TeleBot(TELEGRAM_API)

from timetable.notification import check_task, go_task
from tg_ds.tg_to_ds import coroutine_send
from telegram_bot.timetable.function import markup_all
from telegram_bot.timetable.command import timetable_text


@bot.message_handler(commands=['id'])
def send_now(message: types.Message):
    bot.send_message(message.chat.id, f"Id группы: {message.chat.id}")
    print(f"Id группы: {message.chat.id}")


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


def start():
    print_tg(f"Бот был {bc('01;38;05;34')}запущен{bc()} под именем: {bot.user.first_name}")

    check_default()
    check_task()
    Thread(target=go_task, daemon=True).start()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    start()
