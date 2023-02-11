from other.IE_101.bot import bot
from other.IE_101.database_func import admins, teachers, db_run
from other.IE_101.additional_func import check_default, check_data
from other.IE_101.function import day_info_tg, show_days_by_text_tg, markup_all
from other.IE_101.function import admin_message_check, teacher_message_check
from telebot import types
from datetime import timedelta


@bot.message_handler(commands=['add_hw'])
def home_work(message: types.Message):
    check_default()
    if message.chat.type == "private":
        if message.chat.id in teachers or message.chat.id in admins:
            bot.send_message(message.chat.id, 'Напиши дату в форматі (2020:09:22) :',
                             reply_markup=markup_all(message.chat.id))
            teachers[message.chat.id] = 'add_hw'


@bot.message_handler(commands=['add_one_adm'])
def send_admin(message: types.Message):
    if message.chat.type == "private":
        if (message.chat.id not in admins) or (message.chat.id not in teachers):
            db_run(f"INSERT INTO admin VALUES ('{message.chat.id}')")
            admins[message.chat.id] = None
            bot.send_message(message.chat.id, 'Ти тепер адмін і в тебе додалися кнопки!',
                             reply_markup=markup_all(message.chat.id))


@bot.message_handler(commands=['i_am_teacher'])
def send_teacher(message: types.Message):
    if message.chat.type == "private":
        if (message.chat.id not in admins) or (message.chat.id not in teachers):
            db_run(f"INSERT INTO teacher VALUES ('{message.chat.id}')")
            admins[message.chat.id] = None
            bot.send_message(message.chat.id, 'У тебе теперь є можливість дадавати домашнє завдання!',
                             reply_markup=markup_all(message.chat.id))


@bot.message_handler(commands=['edit'])
def send_edit(message: types.Message):
    check_default()
    if message.chat.type == "private":
        if message.chat.id in admins:
            bot.send_message(message.chat.id, 'Напиши дату у форматі (2020:09:22) :',
                             reply_markup=markup_all(message.chat.id))
            admins[message.chat.id] = 'edit'


@bot.message_handler(commands=['show_day'])
def send_day(message: types.Message):

    if message.text[10:] == 'IE_101_bot':
        bot.send_message(message.chat.id, 'Формат для show_day:\n/show_day 2020:09:28\n2020:09:28 - Дата')
    elif not message.text[10:] == '':
        check_default()
        good_data = check_data(message.text[10:])
        if type(good_data) == str:
            bot.send_message(message.chat.id, good_data)
        else:
            day_info_tg(message.chat.id, good_data, True)

    else:
        bot.send_message(message.chat.id, 'Формат для show_day:\n/show_day 2020:09:28\n2020:09:28 - Дата')


@bot.message_handler(commands=['next_week', 'now_week', 'now_day'])
def send_next(message: types.Message):
    show_days_by_text_tg(message, message.text)


def timetable_text(message: types.Message):
    if message.chat.type == "private":
        admin_message_check_bool = admin_message_check(message)
        teacher_message_check_bool = teacher_message_check(message)
        # <---Админ условие--->
        if admin_message_check_bool:
            pass

        # <---Преподаватель условие--->
        elif teacher_message_check_bool:
            pass

        elif message.text == 'Сьогодні!':
            show_days_by_text_tg(message, 'today')

        elif message.text == 'Цей тиждень!':
            show_days_by_text_tg(message, 'this_week')

        elif message.text == 'Наступний тиждень!':
            show_days_by_text_tg(message, 'next_week')

        else:
            return True


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data[0:5] == 'early':
                good_data = check_data(call.data[5:])
                good_data -= timedelta(1)
                date_text = good_data.strftime("%Y:%m:%d")

                day_info_tg(call.message.chat.id, date_text, True, call.message.message_id)

            elif call.data[0:4] == 'next':
                good_data = check_data(call.data[4:])
                good_data += timedelta(1)
                date_text = good_data.strftime("%Y:%m:%d")

                day_info_tg(call.message.chat.id, date_text, True, call.message.message_id)

    except Exception as e:
        pass