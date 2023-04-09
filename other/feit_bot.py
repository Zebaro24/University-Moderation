from utils import print_tg
import telebot
from telebot import types
from time import sleep as sl

# <---Глобальные переменные--->
TOKEN = "<TELEGRAM_API>"
CHANNEL_ID = -1001511467262
ADMIN_ID = 605313277  # 605313277  # 771348519
connect_id = 0

# <---Выполнение действий--->
bot = telebot.TeleBot(TOKEN)


# <---Используемые функции--->
def get_text(message, nick_bool):
    if message.text:
        text = message.text + "\n\n"
    elif message.caption:
        text = message.caption + "\n\n"
    else:
        text = ""

    if (index := text.find("⚜ Ник:")) != -1 and not nick_bool:
        if not index:
            text = ""
        elif text[index - 2:index] == "\n\n":
            text = text[:index - 2]
        else:
            text = text[:index]
    elif index == -1 and nick_bool:
        text += f"⚜ Ник: [{message.chat.first_name}](tg://user?id={message.chat.id}) ⚜"
    return text


def get_markup(create_bool: bool, markup, chat_id):
    if markup:
        return markup
    elif create_bool:
        markup = types.InlineKeyboardMarkup()
        m1 = types.InlineKeyboardButton(text="Отправить", callback_data="feit_yes")
        m2 = types.InlineKeyboardButton(text="Подключится", callback_data=f"feit_{chat_id}")
        markup.add(m1)
        markup.add(m2)
    else:
        markup = None
    return markup


def send_feit_mem(content_type, chat_id, message, set_nick=True, set_markup=True, markup=None,
                  parse_mode='Markdown'):
    markup = get_markup(set_markup, markup, message.chat.id)
    text = get_text(message, set_nick)

    if content_type == "text":
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)
    elif content_type == "photo":
        bot.send_photo(chat_id, message.photo[0].file_id, caption=text, reply_markup=markup, parse_mode=parse_mode)
    elif content_type == "audio":
        bot.send_audio(chat_id, message.audio.file_id, caption=text, reply_markup=markup,
                       parse_mode=parse_mode)
    elif content_type == "voice":
        bot.send_voice(chat_id, message.voice.file_id, caption=text, reply_markup=markup,
                       parse_mode=parse_mode)
    elif content_type == "video":
        bot.send_video(chat_id, message.video.file_id, caption=text, reply_markup=markup,
                       parse_mode=parse_mode)
    elif content_type == "video_note":
        bot.send_video_note(chat_id, message.video_note.file_id, reply_markup=markup)
    elif content_type == "document":
        bot.send_document(chat_id, message.document.file_id, caption=text, reply_markup=markup,
                          parse_mode=parse_mode)
    elif content_type == "sticker":
        bot.send_sticker(chat_id, message.sticker.file_id, reply_markup=markup)
    elif content_type == "animation":
        bot.send_animation(chat_id, message.animation.file_id, caption=text, reply_markup=markup,
                           parse_mode=parse_mode)


# <---Функции тригер бота--->
@bot.message_handler(chat_types=['private'], commands=["start"])
def tg_start(message: types.Message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEMxpJivXuNEd88WZF3Ywdrb0OJJlRZ6wAC_AADYQfiCoeSvVCuDHH4KQQ")
    bot.send_message(message.chat.id, "Приветствую дорогой друг нашого универа, \n"
                                      "бот создан для отправки мемов для росматрения в канал ФЕИТ Hub")
    sl(1)
    bot.send_message(message.chat.id, "Удачи в расмотрении 😉")


@bot.message_handler(chat_types=['private'], content_types=["text"])
def tg_text(message: types.Message):
    global connect_id
    if message.chat.id == ADMIN_ID and connect_id:
        if message.text == "Отсоединится":
            bot.send_message(connect_id, "🚫 Админ отсоединился 🚫")
            connect_id = 0
            bot.send_message(ADMIN_ID, f"🚫 Вы вышли из беседы 🚫", reply_markup=telebot.types.ReplyKeyboardRemove())
            return
        bot.send_message(connect_id, "Админ: " + message.text)
    elif message.chat.id == connect_id:
        bot.send_message(ADMIN_ID, f"{message.chat.first_name}: {message.text}")
    else:
        # Текст ******
        # <---Text--->
        send_feit_mem("text", ADMIN_ID, message)
        bot.send_message(message.chat.id, "Сообщение отправлено преподавателю (шутка).")


@bot.message_handler(chat_types=['private'],
                     content_types=['photo', 'audio', 'voice', 'video', 'video_note', 'document', 'sticker',
                                    'animation'])
def tg_file(message: types.Message):
    send_feit_mem(message.content_type, ADMIN_ID, message)
    bot.send_message(message.chat.id, "Сообщение отправлено преподавателю (шутка).")


@bot.callback_query_handler(lambda call: call.data[:4] == "feit")
def tg_inline(call: types.CallbackQuery):
    global connect_id
    if call.data[5:] == "yes":
        markup = types.InlineKeyboardMarkup()
        markup.add(call.message.reply_markup.keyboard[1][0])

        send_feit_mem(call.message.content_type, CHANNEL_ID, call.message, False, False, parse_mode='HTML')
        if call.message.text:
            bot.edit_message_text(call.message.html_text + "\n✅ Сообщение было отправлено ✅", call.message.chat.id,
                                  call.message.id, reply_markup=markup, parse_mode="HTML")
        elif call.message.caption:
            bot.edit_message_caption(call.message.html_caption + "\n✅ Сообщение было отправлено ✅",
                                     call.message.chat.id,
                                     call.message.id, reply_markup=markup, parse_mode="HTML")
    else:
        if connect_id:
            bot.send_message(connect_id, "🚫 Админ отсоединился 🚫")
            bot.send_message(ADMIN_ID, f"🚫 Вы вышли из беседы 🚫", reply_markup=telebot.types.ReplyKeyboardRemove())
        connect_id = int(call.data[5:])
        bot.send_message(connect_id, "👨🏼‍💻 К вам присоединился админ 👨🏼‍💻")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Отсоединится"))
        bot.send_message(call.message.chat.id, "🌐 Вы присоединились к пользователю 🌐", reply_markup=markup,
                         reply_to_message_id=call.message.id)


@bot.message_handler(chat_types=['private'], )
def else_message(message):
    bot.send_message(message.chat.id, "К сожалению мы это не поддерживаем.")

def start_feit_bot():
    # <---Запуск--->
    print("Бот запущен!")
    while True:
        bot.polling()
        print("Бот ФЕИТ перезапустился!")
        sl(5)