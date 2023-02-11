from database_func import admins, teachers, edit_data, calendar
from additional_func import day_info, list_days_by_text, check_default, check_data, edit_day
from additional_func import admin_update, teacher_update
from telebot import types
from bot import bot


def show_days_by_text_tg(message, text):
    check_default()
    command = text.replace("/", "").replace("@", " ").split()[0]
    if command == "today":
        command_name = "Сьогодні"
    elif command == "this_week":
        command_name = "Цей тиждень!"
    elif command == "next_week":
        command_name = "Наступний тиждень!"
    else:
        return
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
        item1 = types.InlineKeyboardButton("Минулий", callback_data=f'early{day}', )
        item2 = types.InlineKeyboardButton("Наступний", callback_data=f'next{day}')
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
                        item_btn_1 = types.KeyboardButton('Додати пару!')
                        item_btn_2 = types.KeyboardButton('Виправити пару!')
                        markup.add(item_btn_1, item_btn_2)
                    else:
                        item_btn_1 = types.KeyboardButton('Виправити пару!')
                        markup.add(item_btn_1)
                    item_btn_3 = types.KeyboardButton('Виправити черговість!')
                    item_btn_4 = types.KeyboardButton('Видалити пару!')
                    item_btn_5 = types.KeyboardButton('Повернутися назад!')

                    markup.add(item_btn_3, item_btn_4)
                    markup.add(item_btn_5)
                else:
                    item_btn_1 = types.KeyboardButton('Додати пару!')
                    item_btn_2 = types.KeyboardButton('Повернутися назад!')
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
    item_btn_1 = types.KeyboardButton('Сьогодні!')
    item_btn_2 = types.KeyboardButton('Цей тиждень!')
    item_btn_3 = types.KeyboardButton('Наступний тиждень!')
    markup.add(item_btn_1)
    markup.add(item_btn_2)
    markup.add(item_btn_3)
    if user_id in admins:
        item_btn_4 = types.KeyboardButton('Виправити день!')
        item_btn_5 = types.KeyboardButton('Додати дз!')
        markup.add(item_btn_4, item_btn_5)
    elif user_id in teachers:
        item_btn_4 = types.KeyboardButton('Додати дз!')
        markup.add(item_btn_4)
    return markup


def admin_message_check(message: types.Message):
    if message.chat.id in admins:
        if admins[message.chat.id] is None:
            if message.text == 'Виправити день!':
                check_default()
                admin_update(message.chat.id, "edit")
                bot.send_message(message.chat.id, 'Напиши дату в форматі (2020:09:22):',
                                 reply_markup=markup_all(message.chat.id))
                return True

            elif message.text == 'Додати дз!':
                check_default()
                admin_update(message.chat.id, "add_hw")
                bot.send_message(message.chat.id, 'Напиши дату в форматі (2020:09:22):',
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

            if admins[message.chat.id]["action"] == "edit":
                admin_update(message.chat.id, "edit", date_text)
                day_info_tg(message.chat.id, date_text)
                bot.send_message(message.chat.id, "Що хочеш зробити?", reply_markup=markup_all(message.chat.id))
            elif admins[message.chat.id]["action"] == "add_hw":
                if date_text not in calendar:
                    bot.send_message(message.chat.id, "На це число немає пар!")
                else:
                    admin_update(message.chat.id, "add_hw", date_text)
                    day_info_tg(message.chat.id, date_text)
                    bot.send_message(message.chat.id, 'Форма додавання,виправлення дз 2:№25,26\n'
                                                      '2 - Черга пари\n'
                                                      '№25,26 - На що змінюєм',
                                     reply_markup=markup_all(message.chat.id))

        # На изменении если есть дата
        elif admins[message.chat.id]["action"] in ["edit", "add_hw"]:
            date_text = admins[message.chat.id]["date"]

            if admins[message.chat.id]["action"] == "add_hw":
                if not message.text[0:1].isdecimal():
                    bot.send_message(message.chat.id, 'Неправильна форма.', reply_markup=markup_all(message.chat.id))
                    return True

                couple_number = int(message.text[0:1])
                text = message.text[2:]

                condition_check = edit_day("add_hw", date_text, num_1=couple_number, text=text)
                if not condition_check:
                    bot.send_message(message.chat.id, 'Неправильні дані!', reply_markup=markup_all(message.chat.id))
                    return True
                admin_update(message.chat.id)

                day_info_tg(message.chat.id, date_text)
                bot.send_message(message.chat.id, f"Дз додано!", reply_markup=markup_all(message.chat.id))


            elif admins[message.chat.id]["action"] == "edit":
                if message.text == 'Додати пару!':
                    if date_text in calendar:
                        if not len(calendar[date_text]) < 7:
                            bot.send_message(message.chat.id, "Не більше 7 пар!",
                                             reply_markup=markup_all(message.chat.id))
                            return True

                    admin_update(message.chat.id, "edit_add", date_text)
                    bot.send_message(message.chat.id, 'Назва пари:\n'
                                                      'По типу: Дискретні структури (1-335)%Лекція%Казнадій С. П.',
                                     reply_markup=markup_all(message.chat.id))

                elif message.text == 'Виправити пару!' and date_text in calendar:
                    admin_update(message.chat.id, "edit_edit", date_text)
                    bot.send_message(message.chat.id, 'Форма виправлення 2:Алгебра\n'
                                                      '2 - Черга пари\n'
                                                      'Дискретні структури (1-335)%Лекція%Казнадій С. П. - На что меняем',
                                     reply_markup=markup_all(message.chat.id))
                elif message.text == 'Виправити черговість!' and date_text in calendar:
                    admin_update(message.chat.id, "edit_turn", date_text)
                    bot.send_message(message.chat.id, 'Форма виправлення 1:6\n'
                                                      '1 - звідки 6 - куди',
                                     reply_markup=markup_all(message.chat.id))

                elif message.text == 'Видалити пару!' and date_text in calendar:
                    admin_update(message.chat.id, "edit_delete", date_text)
                    bot.send_message(message.chat.id, 'Цифра пари:',
                                     reply_markup=markup_all(message.chat.id))

                elif message.text == 'Повернутися назад!':
                    admin_update(message.chat.id)
                    bot.send_message(message.chat.id, 'Виправлено.', reply_markup=markup_all(message.chat.id))

                else:
                    bot.send_message(message.chat.id, 'Обери кнопку.', reply_markup=markup_all(message.chat.id))

        elif admins[message.chat.id]["action"] in ["edit_add", "edit_edit", "edit_turn", "edit_delete"]:
            date_text = admins[message.chat.id]["date"]

            if admins[message.chat.id]["action"] == "edit_turn":
                if not (message.text[0:1].isdecimal() and message.text[2:3].isdecimal()):
                    bot.send_message(message.chat.id, 'Неправильна форма ввода.',
                                     reply_markup=markup_all(message.chat.id))
                    return True

                couple_number_1 = int(message.text[0:1])
                couple_number_2 = int(message.text[2:3])

                condition_check = edit_day("turn", date_text, couple_number_1, couple_number_2)
                if not condition_check:
                    bot.send_message(message.chat.id, 'Пари не можуть бути однакові'
                                                      ,
                                     reply_markup=markup_all(message.chat.id))
                    return True

            elif admins[message.chat.id]["action"] == 'edit_add':
                edit_day("add", date_text, text=message.text)

            elif admins[message.chat.id]["action"] == 'edit_edit':
                if (not message.text[0:1].isdecimal()) or message.text[2:] == "":
                    bot.send_message(message.chat.id, 'Неправильна форма ввода.',
                                     reply_markup=markup_all(message.chat.id))
                    return True

                couple_number = int(message.text[0:1])
                text = message.text[2:]

                condition_check = edit_day("edit", date_text, couple_number, text=text)
                if not condition_check:
                    bot.send_message(message.chat.id, 'Пари під цим номером немає!',
                                     reply_markup=markup_all(message.chat.id))
                    return True

            elif admins[message.chat.id]["action"] == 'edit_delete':
                if not message.text[0:1].isdecimal():
                    bot.send_message(message.chat.id, 'Неправильна форма ввода.',
                                     reply_markup=markup_all(message.chat.id))
                    return True

                couple_number = int(message.text[0:1])

                condition_check = edit_day("delete", date_text, couple_number)
                if not condition_check:
                    bot.send_message(message.chat.id, "Пари під цим номером немає!",
                                     reply_markup=markup_all(message.chat.id))
                    return True

            admin_update(message.chat.id, "edit", date_text)

            day_info_tg(message.chat.id, date_text)
            bot.send_message(message.chat.id, 'Хочеш продовжити?', reply_markup=markup_all(message.chat.id))
        return True
    else:
        return False


def teacher_message_check(message: types.Message):
    if message.chat.id in teachers:
        if teachers[message.chat.id] is None:
            if message.text == 'Додати дз!':
                check_default()
                bot.send_message(message.chat.id, 'Напиши дату в форматі (2020:09:22):',
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


            if date_text not in calendar:
                bot.send_message(message.chat.id, "На це число немає пар!")
            else:
                teacher_update(message.chat.id, "add_hw", date_text)
                day_info_tg(message.chat.id, date_text)
                bot.send_message(message.chat.id, 'Форма додавання,редагування дз 2:№25,26\n'
                                                  '2 - Черга Пари\n'
                                                  '№25,26 - На що змінюємо', reply_markup=markup_all(message.chat.id))

        elif teachers[message.chat.id]["action"] == "add_hw":
            date_text = teachers[message.chat.id]["date"]

            if not message.text[0:1].isdecimal():
                bot.send_message(message.chat.id, 'Неправильна форма.', reply_markup=markup_all(message.chat.id))
                return

            couple_number = int(message.text[0:1])
            text = message.text[2:]

            condition_check = edit_day("add_hw", date_text, num_1=couple_number, text=text)
            if not condition_check:
                bot.send_message(message.chat.id, 'Неправильні дані!', reply_markup=markup_all(message.chat.id))
                return
            teacher_update(message.chat.id)

            day_info_tg(message.chat.id, date_text)
            bot.send_message(message.chat.id, f"Дз додано!", reply_markup=markup_all(message.chat.id))

        return True
    else:
        return False
