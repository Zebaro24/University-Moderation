from timetable.additional_func import day_info, my_date
from telebot import types
from telegram_bot.main_telegram import bot


def show(chat_id, time):
    all_day = my_date(time)
    if not type(all_day) is list:
        day_info_tg(chat_id, all_day, True)
    else:
        for i in all_day:
            day_info_tg(chat_id, i)


def day_info_tg(chat_id, day, markup_bool=False, edit=False, message_id=None):
    save_info = day_info(day)
    all_text = f"*{save_info['title']}*{save_info['main_text']}"
    if markup_bool:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Прошлый", callback_data=f'early{day.strftime("%Y:%m:%d")}', )
        item2 = types.InlineKeyboardButton("Следующий", callback_data=f'next{day.strftime("%Y:%m:%d")}')
        markup.add(item1, item2)
    else:
        markup = None
    if not edit:
        bot.send_message(chat_id, all_text, reply_markup=markup, parse_mode='Markdown')
    elif edit:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=all_text, reply_markup=markup,
                              parse_mode='Markdown')


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
