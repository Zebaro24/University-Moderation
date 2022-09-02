from config import timetable_time
from datetime import date, timedelta, datetime
from pytz import timezone
from database_func import default_l, default_p, db_run, calendar
from telebot import types
from telegram_bot.main_telegram import bot

tz = timezone("Europe/Kyiv")


def rep(str_l):  # Замена ' на ''
    return str_l.replace("'", "''")


def check_default():
    now = datetime.now(tz)
    day_to_week = timedelta(now.weekday())
    one_day = timedelta(1)

    day_delt = now - day_to_week

    for n in range(2):
        if n:
            day_delt += one_day
            day_delt += one_day
        if int(day_delt.strftime('%W')) % 2:
            default_r = default_l
        else:
            default_r = default_p

        for i in range(5):
            try:
                calendar[day_delt.strftime('%Y:%m:%d')]
            except KeyError:
                calendar[day_delt.strftime('%Y:%m:%d')] = {}
                print(f"Добавление дня {day_delt.strftime('%Y:%m:%d')}!")
                for b, d in default_r[day_delt.weekday()].items():
                    calendar[day_delt.strftime('%Y:%m:%d')][b] = [d, None]
                    d = d.replace("'", "''")
                    db_run(f"INSERT INTO owner VALUES ('{day_delt.strftime('%Y:%m:%d')}',{b},'{d}',null)")

            day_delt += one_day


def my_date(time):
    if time == 'next':
        all_day = []
        now = datetime.now(tz)
        one_week = timedelta(weeks=1)
        day_to_week = timedelta(now.weekday())
        one_day = timedelta(1)

        day_delt = now - day_to_week + one_week

        for i in range(5):
            all_day.append(day_delt)
            day_delt += one_day

        return all_day

    elif time == 'now':
        all_day = []
        now = datetime.now(tz)
        day_to_week = timedelta(now.weekday())
        one_day = timedelta(1)

        day_delt = now - day_to_week

        for i in range(5):
            all_day.append(day_delt)
            day_delt += one_day

        return all_day

    elif time == 'now_day':
        now = datetime.now(tz)

        return now


def day_dz(chat_id, day, markup=None, edit=False, message_id=None):
    all_text = ''
    if int(day.strftime('%W')) % 2:
        all_text += "Непарный\n"
    else:
        all_text += "Парный\n"
    all_text += f"{day.strftime('%A, (%Y:%m:%d)').title()}:\n\n"
    try:
        if list(calendar[day.strftime('%Y:%m:%d')].items()):
            for p in sorted(calendar[day.strftime('%Y:%m:%d')].items()):  # p,d p[1]
                if p[1][1] is None:
                    null_object = '\n          '
                    all_text += f"👉{p[0]}) ({timetable_time[int(p[0]) - 1]}){null_object}{p[1][0].replace('%', null_object)}\n\n"
                else:
                    null_object = '\n          '
                    all_text += f"👉{p[0]}) ({timetable_time[int(p[0]) - 1]}){null_object}{p[1][0].replace('%', null_object)} : {p[1][1]}\n\n"
        else:
            all_text += 'Пусто'

    except:
        all_text += 'Пусто'
    if not edit:
        bot.send_message(chat_id, all_text, reply_markup=markup, parse_mode='Markdown')
    elif edit:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=all_text, reply_markup=markup,
                              parse_mode='Markdown')


def show(chat_id, time):
    all_day = my_date(time)
    if not type(all_day) is list:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Прошлый", callback_data=f'early{all_day.strftime("%Y:%m:%d")}', )
        item2 = types.InlineKeyboardButton("Следующий", callback_data=f'next{all_day.strftime("%Y:%m:%d")}')

        markup.add(item1, item2)
        day_dz(chat_id, all_day, markup)
    else:
        for i in all_day:
            day_dz(chat_id, i)


def check_data(data, chat_id):
    try:
        year = int(data[0:4])
        month = int(data[5:7])
        day = int(data[8:10])
        if not 2021 <= year <= 2025:
            bot.send_message(chat_id, 'Не тот год, попробуй еще!')
            return False
        if not 1 <= month <= 12:
            bot.send_message(chat_id, 'Не правильный месяц, попробуй еще!')
            return False
        if not 1 <= day <= 31:
            bot.send_message(chat_id, 'Не правильный день, попробуй еще!')
            return False
        try:
            good_data = date(year, month, day)
            return good_data
        except:
            bot.send_message(chat_id, 'Не правильный день, попробуй еще!')
            return False
    except:
        bot.send_message(chat_id, 'Не верный формат, попробуй еще!')
        return False


def markup_all(stud=None):
    if stud == "edit":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_1 = types.KeyboardButton('Поменять очередность!')
        item_btn_2 = types.KeyboardButton('Добавить пару!')
        item_btn_3 = types.KeyboardButton('Изменить пару!')
        item_btn_4 = types.KeyboardButton('Удалить пару!')
        item_btn_5 = types.KeyboardButton('Вернутся назад!')
        markup.add(item_btn_1, item_btn_2)
        markup.add(item_btn_3, item_btn_4)
        markup.add(item_btn_5)
        return markup
    elif stud == "del":
        return types.ReplyKeyboardRemove()
    elif stud == "ans":
        return types.ForceReply()
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_1 = types.KeyboardButton('Сегодня!')
        item_btn_2 = types.KeyboardButton('Эта неделя!')
        item_btn_3 = types.KeyboardButton('След неделя!')
        markup.add(item_btn_1)
        markup.add(item_btn_2)
        markup.add(item_btn_3)
        if stud == "adm":
            item_btn_4 = types.KeyboardButton('Изменить день!')
            item_btn_5 = types.KeyboardButton('Добавить дз!')
            markup.add(item_btn_4, item_btn_5)
        elif stud == "tch":
            item_btn_4 = types.KeyboardButton('Добавить дз!')
            markup.add(item_btn_4)
        return markup

# if __name__ == '__main__':
#     print(f'Админы: {admins}')
#     print(f'Преподаватели: {teachers}')
#     print(f'Даты на изменении: {edit_data}')
#     print('Бот запущен!')
#     print(datetime.now())
#
#     p = Process(target=go_task)
#     p.start()
#
#     while True:
#         try:
#             bot.polling()
#         except Exception as e:
#             print(f'Бот перезапустился из за \n{repr(e)}')
#             sl(5)
