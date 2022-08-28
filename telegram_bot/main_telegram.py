from telebot import TeleBot, types
from utils import print_tg, bc
from config import TELEGRAM_API, tg_chanel_id

bot = TeleBot(TELEGRAM_API)

from tg_ds.tg_to_ds import coroutine_send


@bot.message_handler(
    content_types=['text', 'audio', 'photo', 'voice', 'video_note', 'video', 'document', 'location', 'contact', 'sticker',
                   'animation'])
def message_text(message):
    coroutine_send(message)


@bot.message_handler(commands=['net'])
def send_now(message: types.Message):
    bot.send_message(message.chat.id, str(message.chat.id))


def start():
    print_tg(f"Бот был {bc('01;38;05;34')}запущен{bc()} под именем: {bot.user.first_name}")
    bot.polling()


if __name__ == '__main__':
    start()
