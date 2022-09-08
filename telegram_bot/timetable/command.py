from telegram_bot.main_telegram import bot
from database_func import admins, teachers, db_run, calendar
from timetable.additional_func import check_default, check_data
from telegram_bot.timetable.function import day_info_tg, show_days_by_text_tg, markup_all
from telegram_bot.timetable.function import admin_message_check, teacher_message_check
from telebot import types
from datetime import timedelta
from utils import print_tg


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    if message.chat.type == "private":

        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJIdhhiSG0K6iUciZOoueWASUDG1jHoAACoAEAAjDUnRGDNNeGcpfWEyIE')
        bot.send_message(message.chat.id, f'Приветствую {message.from_user.first_name} рад вас видеть здесь.')
        if message.chat.id in admins:
            bot.send_message(message.chat.id, 'Ты админ!', reply_markup=markup_all(message.chat.id))

        else:
            bot.send_message(message.chat.id, 'Вот твои возможности!', reply_markup=markup_all(message.chat.id))


@bot.message_handler(commands=['show_moder'])
def home_work(message: types.Message):
    bot.send_message(message.chat.id, "Модераторы были отправлены в консоль")
    print(admins)
    print(teachers)


@bot.message_handler(commands=['show_calendar'])
def home_work(message: types.Message):
    bot.send_message(message.chat.id, "Модераторы были отправлены в консоль")
    print(calendar)


@bot.message_handler(commands=['add_hw'])
def home_work(message: types.Message):
    check_default()
    if message.chat.type == "private":
        if message.chat.id in teachers or message.chat.id in admins:
            bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :',
                             reply_markup=markup_all(message.chat.id))
            teachers[message.chat.id] = 'add_hw'


@bot.message_handler(commands=['add_one_adm'])
def send_admin(message: types.Message):
    if message.chat.type == "private":
        if (message.chat.id not in admins) or (message.chat.id not in teachers):
            db_run(f"INSERT INTO admin VALUES ('{message.chat.id}')")
            admins[message.chat.id] = None
            bot.send_message(message.chat.id, 'Ты теперь админ и у тебя добавились кнопки!',
                             reply_markup=markup_all(message.chat.id))
            print_tg(f'Добавился админ {message.from_user.first_name}!')


@bot.message_handler(commands=['i_am_teacher'])
def send_teacher(message: types.Message):
    if message.chat.type == "private":
        if (message.chat.id not in admins) or (message.chat.id not in teachers):
            db_run(f"INSERT INTO teacher VALUES ('{message.chat.id}')")
            admins[message.chat.id] = None
            bot.send_message(message.chat.id, 'У Вас теперь есть возможность добавлять домашнее задание!',
                             reply_markup=markup_all(message.chat.id))
            print_tg(f'Добавился преподаватель {message.from_user.first_name}!')


@bot.message_handler(commands=['edit'])
def send_edit(message: types.Message):
    check_default()
    if message.chat.type == "private":
        if message.chat.id in admins:
            bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :',
                             reply_markup=markup_all(message.chat.id))
            admins[message.chat.id] = 'edit'


@bot.message_handler(commands=['show_day'])
def send_day(message: types.Message):
    print_tg(f'Запрос от {message.chat.first_name} на: {message.text[10:]}!')

    if message.text[10:] == 'KI_214_bot':
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

        elif message.text == 'Сегодня!':
            show_days_by_text_tg(message, 'now_day')

        elif message.text == 'Эта неделя!':
            show_days_by_text_tg(message, 'now_week')

        elif message.text == 'След неделя!':
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
                print_tg(f'Запрос от {call.message.chat.first_name} на {date_text}!')

                day_info_tg(call.message.chat.id, date_text, True, call.message.message_id)

            elif call.data[0:4] == 'next':
                good_data = check_data(call.data[4:])
                good_data += timedelta(1)
                date_text = good_data.strftime("%Y:%m:%d")
                print_tg(f'Запрос от {call.message.chat.first_name} на {date_text}!')

                day_info_tg(call.message.chat.id, date_text, True, call.message.message_id)

            # remove inline buttons

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
            #                          text="Уведомление!!!")

    except Exception as e:
        print_tg(repr(e))
