from database_func import admins, teachers, edit_data, calendar
from timetable.additional_func import day_info, list_days_by_text, check_default, check_data, edit_day
from timetable.additional_func import admin_update, teacher_update
from config import tg_chanel_id
from telebot import types
from telegram_bot.main_telegram import bot
from utils import print_tg


def show_days_by_text_tg(message, text):
    check_default()
    command = text.replace("/", "").replace("@", " ").split()[0]
    if command == "now_day":
        command_name = "этот день"
    elif command == "next_day":
        command_name = "завтрашний день"
    elif command == "now_week":
        command_name = "эту неделю"
    elif command == "next_week":
        command_name = "след. неделю"
    else:
        return
    print_tg(f'Запрос на {command_name} от {message.chat.first_name}!')
    list_days = list_days_by_text(command)
    if len(list_days) == 1:
        day_info_tg(message.chat.id, list_days[0], True)
    else:
        for i in list_days:
            day_info_tg(message.chat.id, i)


def day_info_tg(chat_id: int, day: str, markup_bool=False, message_id=None):
    save_info = day_info(check_data(day))
    all_text = f"*{save_info['title']}*{save_info['main_text']}"
    if markup_bool:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Прошлый", callback_data=f'early{day}', )
        item2 = types.InlineKeyboardButton("Следующий", callback_data=f'next{day}')
        markup.add(item1, item2)
    else:
        markup = None
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=all_text, reply_markup=markup,
                              parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.send_message(chat_id, all_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)


def markup_all(user_id: int):
    if user_id in admins:
        if admins[user_id] is None:
            pass
        elif admins[user_id]["action"] in ["edit", "add_hw"] and admins[user_id]["date"] is None:
            return types.ForceReply()
        elif admins[user_id]["action"] in ["edit", "add_hw"]:
            if admins[user_id]["action"] == "edit":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if admins[user_id]["date"] in calendar:
                    if len(calendar[admins[user_id]["date"]]) < 7:
                        item_btn_1 = types.KeyboardButton('Добавить пару!')
                        item_btn_2 = types.KeyboardButton('Изменить пару!')
                        markup.add(item_btn_1, item_btn_2)
                    else:
                        item_btn_1 = types.KeyboardButton('Изменить пару!')
                        markup.add(item_btn_1)
                    item_btn_3 = types.KeyboardButton('Поменять очередность!')
                    item_btn_4 = types.KeyboardButton('Удалить пару!')
                    item_btn_5 = types.KeyboardButton('Вернутся назад!')

                    markup.add(item_btn_3, item_btn_4)
                    markup.add(item_btn_5)
                else:
                    item_btn_1 = types.KeyboardButton('Добавить пару!')
                    item_btn_2 = types.KeyboardButton('Вернутся назад!')
                    markup.add(item_btn_1)
                    markup.add(item_btn_2)
                return markup
            elif admins[user_id]["action"] == "add_hw":
                return types.ForceReply()
        elif admins[user_id]["action"] in ["edit_add", "edit_edit", "edit_turn", "edit_delete"]:
            return types.ForceReply()
    elif user_id in teachers:
        if teachers[user_id] is None:
            pass
        elif teachers[user_id]["action"] == "add_hw":
            return types.ForceReply()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_btn_1 = types.KeyboardButton('Сегодня!')
    item_btn_2 = types.KeyboardButton('Завтра!')
    item_btn_3 = types.KeyboardButton('Эта неделя!')
    item_btn_4 = types.KeyboardButton('След неделя!')
    markup.add(item_btn_1)
    markup.add(item_btn_2)
    markup.add(item_btn_3)
    markup.add(item_btn_4)
    if user_id in admins:
        item_btn_5 = types.KeyboardButton('Изменить день!')
        item_btn_6 = types.KeyboardButton('Добавить дз!')
        markup.add(item_btn_5, item_btn_6)
    elif user_id in teachers:
        item_btn_5 = types.KeyboardButton('Добавить дз!')
        markup.add(item_btn_5)
    return markup


def admin_message_check(message: types.Message):
    if message.chat.id in admins:
        if admins[message.chat.id] is None:
            if message.text == 'Изменить день!':
                check_default()
                admin_update(message.chat.id, "edit")
                bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22):',
                                 reply_markup=markup_all(message.chat.id))
                return True

            elif message.text == 'Добавить дз!':
                check_default()
                admin_update(message.chat.id, "add_hw")
                bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22):',
                                 reply_markup=markup_all(message.chat.id))
                return True
            else:
                return False

        # На изменении если нет даты
        elif admins[message.chat.id]["action"] in ["edit", "add_hw"] and admins[message.chat.id]["date"] is None:
            date_text = message.text
            good_check_data = check_data(date_text)

            if type(good_check_data) == str:
                bot.send_message(message.chat.id, good_check_data, reply_markup=markup_all(message.chat.id))
                return True
            elif date_text in edit_data:
                bot.send_message(message.chat.id, "В данный момент над этой датой ведутся изменения!")
                return True

            print_tg(f'Дата изменяется {message.chat.first_name} : {date_text}')
            if admins[message.chat.id]["action"] == "edit":
                admin_update(message.chat.id, "edit", date_text)
                day_info_tg(message.chat.id, date_text)
                bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=markup_all(message.chat.id))
            elif admins[message.chat.id]["action"] == "add_hw":
                if date_text not in calendar:
                    bot.send_message(message.chat.id, "На это число нету пар!")
                else:
                    admin_update(message.chat.id, "add_hw", date_text)
                    day_info_tg(message.chat.id, date_text)
                    bot.send_message(message.chat.id, 'Форма добавления,изменения дз 2:№25,26\n'
                                                      '2 - Очередь Пары\n'
                                                      '№25,26 - На что меняем',
                                     reply_markup=markup_all(message.chat.id))

        # На изменении если есть дата
        elif admins[message.chat.id]["action"] in ["edit", "add_hw"]:
            date_text = admins[message.chat.id]["date"]

            if admins[message.chat.id]["action"] == "add_hw":
                if not message.text[0:1].isdecimal():
                    bot.send_message(message.chat.id, 'Не правильная форма.', reply_markup=markup_all(message.chat.id))
                    return True

                couple_number = int(message.text[0:1])
                text = message.text[2:]

                condition_check = edit_day("add_hw", date_text, num_1=couple_number, text=text)
                if not condition_check:
                    bot.send_message(message.chat.id, 'Не верные данные!', reply_markup=markup_all(message.chat.id))
                    return True
                admin_update(message.chat.id)

                day_info_tg(message.chat.id, date_text)
                bot.send_message(message.chat.id, f"Дз добавлено!", reply_markup=markup_all(message.chat.id))

                if tg_chanel_id:
                    bot.send_message(tg_chanel_id, f"Добавлено дз: {message.from_user.first_name}\n")
                    day_info_tg(tg_chanel_id, date_text)

            elif admins[message.chat.id]["action"] == "edit":
                if message.text == 'Добавить пару!':
                    if date_text in calendar:
                        if not len(calendar[date_text]) < 7:
                            bot.send_message(message.chat.id, "Ты издеваешься, не может быть больше 7 пар в день. "
                                                              "Мозги вылезут!",
                                             reply_markup=markup_all(message.chat.id))
                            return True

                    admin_update(message.chat.id, "edit_add", date_text)
                    bot.send_message(message.chat.id, 'Название пары:\n'
                                                      'По типу: Дискретні структури (1-335)%Лекція%Казнадій С. П.',
                                     reply_markup=markup_all(message.chat.id))

                elif message.text == 'Изменить пару!' and date_text in calendar:
                    admin_update(message.chat.id, "edit_edit", date_text)
                    bot.send_message(message.chat.id, 'Форма изменения 2:Алгебра\n'
                                                      '2 - Очередь пары\n'
                                                      'Дискретні структури (1-335)%Лекція%Казнадій С. П. - На что меняем',
                                     reply_markup=markup_all(message.chat.id))
                elif message.text == 'Поменять очередность!' and date_text in calendar:
                    admin_update(message.chat.id, "edit_turn", date_text)
                    bot.send_message(message.chat.id, 'Форма изменения 1:6\n'
                                                      '1 - откуда 6 - куда',
                                     reply_markup=markup_all(message.chat.id))

                elif message.text == 'Удалить пару!' and date_text in calendar:
                    admin_update(message.chat.id, "edit_delete", date_text)
                    bot.send_message(message.chat.id, 'Цифра пары:',
                                     reply_markup=markup_all(message.chat.id))

                elif message.text == 'Вернутся назад!':
                    print_tg(f'Дата свободна: {admins[message.chat.id]["date"]}')
                    admin_update(message.chat.id)
                    bot.send_message(message.chat.id, 'Сделано.', reply_markup=markup_all(message.chat.id))

                else:
                    bot.send_message(message.chat.id, 'Выберите кнопку.', reply_markup=markup_all(message.chat.id))

        elif admins[message.chat.id]["action"] in ["edit_add", "edit_edit", "edit_turn", "edit_delete"]:
            date_text = admins[message.chat.id]["date"]

            if admins[message.chat.id]["action"] == "edit_turn":
                if not (message.text[0:1].isdecimal() and message.text[2:3].isdecimal()):
                    bot.send_message(message.chat.id, 'Не правильная форма ввода.',
                                     reply_markup=markup_all(message.chat.id))
                    return True

                couple_number_1 = int(message.text[0:1])
                couple_number_2 = int(message.text[2:3])

                condition_check = edit_day("turn", date_text, couple_number_1, couple_number_2)
                if not condition_check:
                    bot.send_message(message.chat.id, 'Пары не могут совпадать'
                                                      'и должны быть в пределах от 1 до 7!',
                                     reply_markup=markup_all(message.chat.id))
                    return True

            elif admins[message.chat.id]["action"] == 'edit_add':
                edit_day("add", date_text, text=message.text)

            elif admins[message.chat.id]["action"] == 'edit_edit':
                if (not message.text[0:1].isdecimal()) or message.text[2:] == "":
                    bot.send_message(message.chat.id, 'Не правильная форма ввода.',
                                     reply_markup=markup_all(message.chat.id))
                    return True

                couple_number = int(message.text[0:1])
                text = message.text[2:]

                condition_check = edit_day("edit", date_text, couple_number, text=text)
                if not condition_check:
                    bot.send_message(message.chat.id, 'Пары под этим номером нет!',
                                     reply_markup=markup_all(message.chat.id))
                    return True

            elif admins[message.chat.id]["action"] == 'edit_delete':
                if not message.text[0:1].isdecimal():
                    bot.send_message(message.chat.id, 'Не правильная форма ввода.',
                                     reply_markup=markup_all(message.chat.id))
                    return True

                couple_number = int(message.text[0:1])

                condition_check = edit_day("delete", date_text, couple_number)
                if not condition_check:
                    bot.send_message(message.chat.id, "Пары под этим номером нет!",
                                     reply_markup=markup_all(message.chat.id))
                    return True

            admin_update(message.chat.id, "edit", date_text)

            day_info_tg(message.chat.id, date_text)
            bot.send_message(message.chat.id, 'Хотите продолжить?', reply_markup=markup_all(message.chat.id))
        return True
    else:
        return False


def teacher_message_check(message: types.Message):
    if message.chat.id in teachers:
        if teachers[message.chat.id] is None:
            if message.text == 'Добавить дз!':
                check_default()
                bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22):',
                                 reply_markup=markup_all(message.chat.id))
                teacher_update(message.chat.id, "add_hw")
                return True
            else:
                return False

        elif teachers[message.chat.id]["action"] == "add_hw" and teachers[message.chat.id]["date"] is None:
            date_text = message.text
            good_check_data = check_data(date_text)

            if type(good_check_data) == str:
                bot.send_message(message.chat.id, good_check_data, reply_markup=markup_all(message.chat.id))
                return
            elif date_text in edit_data:
                bot.send_message(message.chat.id, "В данный момент над этой датой ведутся изменения!")
                return

            print_tg(f'Дата изменяется {message.chat.first_name} : {date_text}')

            if date_text not in calendar:
                bot.send_message(message.chat.id, "На это число нету пар!")
            else:
                teacher_update(message.chat.id, "add_hw", date_text)
                day_info_tg(message.chat.id, date_text)
                bot.send_message(message.chat.id, 'Форма добавления,изменения дз 2:№25,26\n'
                                                  '2 - Очередь Пары\n'
                                                  '№25,26 - На что меняем', reply_markup=markup_all(message.chat.id))

        elif teachers[message.chat.id]["action"] == "add_hw":
            date_text = teachers[message.chat.id]["date"]

            if not message.text[0:1].isdecimal():
                bot.send_message(message.chat.id, 'Не правильная форма.', reply_markup=markup_all(message.chat.id))
                return

            couple_number = int(message.text[0:1])
            text = message.text[2:]

            condition_check = edit_day("add_hw", date_text, num_1=couple_number, text=text)
            if not condition_check:
                bot.send_message(message.chat.id, 'Не верные данные!', reply_markup=markup_all(message.chat.id))
                return
            teacher_update(message.chat.id)

            day_info_tg(message.chat.id, date_text)
            bot.send_message(message.chat.id, f"Дз добавлено!", reply_markup=markup_all(message.chat.id))

            if tg_chanel_id:
                bot.send_message(tg_chanel_id,
                                 f"Добавлено дз: {message.from_user.first_name}\n"
                                 f"На {check_data(date_text).strftime('%A, (%Y:%m:%d)')}\n"
                                 f"{couple_number} : {text}")
        return True
    else:
        return False
