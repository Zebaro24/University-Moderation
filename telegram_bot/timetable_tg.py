from telegram_bot.main_telegram import bot
from database_func import admins, teachers, calendar, db_run, edit_data
from timetable.additional_func import check_default, markup_all, show, check_data, day_dz, rep
from config import tg_chanel_id
from telebot import types
from datetime import timedelta


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == "private":

        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJIdhhiSG0K6iUciZOoueWASUDG1jHoAACoAEAAjDUnRGDNNeGcpfWEyIE')
        bot.send_message(message.chat.id, f'Приветствую {message.from_user.first_name} рад вас видеть здесь.')
        if message.chat.id in admins:
            bot.send_message(message.chat.id, 'Ты админ!', reply_markup=markup_all("adm"))

        else:
            bot.send_message(message.chat.id, 'Вот твои возможности!', reply_markup=markup_all())


@bot.message_handler(commands=['add_hw'])
def home_work(message):
    check_default()
    if message.chat.type == "private":

        if message.chat.id in teachers:
            bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :', reply_markup=markup_all("ans"))
            teachers[message.chat.id] = 'add_hw'
        elif message.chat.id in admins:
            bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :', reply_markup=markup_all("ans"))
            admins[message.chat.id] = 'add_hw'


@bot.message_handler(commands=['add_one_adm'])
def send_admin(message):
    if message.chat.type == "private":
        if (message.chat.id not in admins) or (message.chat.id not in teachers):
            db_run(f"INSERT INTO admin VALUES ('{message.chat.id}')")
            admins[message.chat.id] = None
            bot.send_message(message.chat.id, 'Ты теперь админ и у тебя добавились кнопки!',
                             reply_markup=markup_all("adm"))
            print(f'Добавился админ {message.from_user.first_name}!')


@bot.message_handler(commands=['i_am_teacher'])
def send_teacher(message):
    if message.chat.type == "private":
        if (message.chat.id not in admins) or (message.chat.id not in teachers):
            db_run(f"INSERT INTO teacher VALUES ('{message.chat.id}')")
            admins[message.chat.id] = None
            bot.send_message(message.chat.id, 'Ты теперь преподаватель и у тебя добавились кнопки!',
                             reply_markup=markup_all("tch"))
            print(f'Добавился преподаватель {message.from_user.first_name}!')


@bot.message_handler(commands=['edit'])
def send_edit(message):
    check_default()
    if message.chat.type == "private":
        if message.chat.id in admins:
            bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :', reply_markup=markup_all("ans"))
            admins[message.chat.id] = 'edit'


@bot.message_handler(commands=['show_next'])
def send_next(message):
    print(f'Запрос на след неделю от {message.chat.first_name}!')
    check_default()
    show(message.chat.id, 'next')


@bot.message_handler(commands=['show_day'])
def send_day(message):
    print(f'Запрос от {message.chat.first_name} на: {message.text[10:]}!')

    if message.text[10:] == 'KI_214_bot':
        bot.send_message(message.chat.id, 'Формат для show_day:\n/show_day 2020:09:28\n2020:09:28 - Дата')
    elif not message.text[10:] == '':
        check_default()
        good_data = check_data(message.text[10:], message.chat.id)
        if good_data:
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Прошлый", callback_data=f'early{good_data.strftime("%Y:%m:%d")}', )
            item2 = types.InlineKeyboardButton("Следующий", callback_data=f'next{good_data.strftime("%Y:%m:%d")}')

            markup.add(item1, item2)
            day_dz(message.chat.id, good_data, markup)

    else:
        bot.send_message(message.chat.id, 'Формат для show_day:\n/show_day 2020:09:28\n2020:09:28 - Дата')


@bot.message_handler(commands=['show_now'])
def send_now(message):
    print(f'Запрос на эту неделю от {message.chat.first_name}!')
    check_default()
    show(message.chat.id, 'now')


@bot.message_handler(commands=['show_now_day'])
def send_early(message):
    print(f'Запрос на сегодня от {message.chat.first_name}!')
    check_default()
    show(message.chat.id, 'now_day')


def timetable_text(message):
    if message.chat.type == "private":
        if message.text == 'Сегодня!':
            print(f'Запрос на сегодня от {message.chat.first_name}!')
            check_default()
            show(message.chat.id, 'now_day')

        elif message.text == 'Эта неделя!':
            print(f'Запрос на эту неделю от {message.chat.first_name}!')
            check_default()
            show(message.chat.id, 'now')

        elif message.text == 'След неделя!':
            print(f'Запрос на след неделю от  {message.chat.first_name}!')
            check_default()
            show(message.chat.id, 'next')

        elif message.chat.id in admins:
            if admins[message.chat.id] == 'edit':
                good_check_data = check_data(message.text, message.chat.id)
                if message.text in edit_data:
                    admins[message.chat.id] = None
                    bot.send_message(message.chat.id, 'Дату уже изменяют!')

                elif good_check_data:
                    edit_data.append(good_check_data.strftime('%Y:%m:%d'))
                    db_run(
                        f"UPDATE admin SET work='edit',data='{good_check_data.strftime('%Y:%m:%d')}' WHERE id={message.chat.id}")
                    admins[message.chat.id] = {'edit': good_check_data}
                    print(f'Дата изменяется {message.chat.first_name} : {good_check_data}')
                    day_dz(message.chat.id, good_check_data)
                    bot.send_message(message.chat.id, 'Что хотите сделать?', reply_markup=markup_all("edit"))

            elif admins[message.chat.id] == 'add_hw':
                good_check_data = check_data(message.text, message.chat.id)
                if not good_check_data.strftime('%Y:%m:%d') in calendar:
                    bot.send_message(message.chat.id, 'На это число нету пар!')
                    admins[message.chat.id] = None
                elif good_check_data:
                    admins[message.chat.id] = {'add_hw': good_check_data}
                    day_dz(message.chat.id, good_check_data)
                    bot.send_message(message.chat.id,
                                     'Форма добавления,изменения дз 2:№25,26\n2 - Очередь Пары\n№25,26 - На что меняем',
                                     reply_markup=markup_all("ans"))

            elif message.text == 'Изменить день!':
                check_default()
                bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :',
                                 reply_markup=markup_all("ans"))
                admins[message.chat.id] = 'edit'

            elif message.text == 'Добавить дз!':
                check_default()
                bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :',
                                 reply_markup=markup_all("ans"))
                admins[message.chat.id] = 'add_hw'

            elif admins[message.chat.id] is None:
                return True

            elif list(admins[message.chat.id].keys())[0] == 'add_hw':
                try:
                    intg = int(message.text[0:1])
                    text = message.text[2:]
                    data = admins[message.chat.id]['add_hw']
                    calendar[data.strftime('%Y:%m:%d')][intg][1] = text
                    day_dz(message.chat.id, data)
                    admins[message.chat.id] = None
                    db_run(f"UPDATE owner SET hw='{text}' WHERE day='{data.strftime('%Y:%m:%d')}' AND int='{intg}'")
                    bot.send_message(message.chat.id, f'Дз добавлено!', reply_markup=markup_all("adm"))
                    if tg_chanel_id:
                        bot.send_message(tg_chanel_id,
                                         f'Добавлено дз: {message.from_user.first_name}\nНа {data.strftime("%A, (%Y:%m:%d)")}\n{intg} : {text}')

                except:
                    bot.send_message(message.chat.id, 'Не правильная форма попробуй еще.',
                                     reply_markup=markup_all("ans"))

            elif list(admins[message.chat.id].keys())[0] == 'edit':
                if message.text == 'Поменять очередность!':
                    try:
                        data = admins[message.chat.id]['edit']
                        if len(calendar[data.strftime('%Y:%m:%d')]) >= 1:
                            admins[message.chat.id] = {'edit_turn': admins[message.chat.id]['edit']}
                            db_run(f"UPDATE admin SET work='edit_turn'WHERE id={message.chat.id}")
                            bot.send_message(message.chat.id, 'Форма изменения 1:6\n1 - откуда 6 - куда',
                                             reply_markup=markup_all("ans"))
                        else:
                            bot.send_message(message.chat.id, 'Обмен невозможен!')
                    except:
                        bot.send_message(message.chat.id, 'Обмен невозможен!')
                elif message.text == 'Добавить пару!':
                    admins[message.chat.id] = {'edit_add': admins[message.chat.id]['edit']}
                    db_run(f"UPDATE admin SET work='edit_add'WHERE id={message.chat.id}")
                    bot.send_message(message.chat.id,
                                     'Название пары:\nПо типу: Дискретні структури (1-335)%Лекція%Казнадій С. П.',
                                     reply_markup=markup_all("ans"))
                elif message.text == 'Изменить пару!':
                    try:
                        data = admins[message.chat.id]['edit']
                        if len(calendar[data.strftime('%Y:%m:%d')]):
                            admins[message.chat.id] = {'edit_edit': admins[message.chat.id]['edit']}
                            db_run(f"UPDATE admin SET work='edit_edit'WHERE id={message.chat.id}")
                            bot.send_message(message.chat.id,
                                             'Форма изменения 2:Алгебра\n2 - Очередь пары\nДискретні структури (1-335)%Лекція%Казнадій С. П. - На что меняем',
                                             reply_markup=markup_all("ans"))
                        else:
                            assert False

                    except:
                        bot.send_message(message.chat.id, 'Изменение невозможно!')
                elif message.text == 'Удалить пару!':
                    try:
                        data = admins[message.chat.id]['edit']
                        if len(calendar[data.strftime('%Y:%m:%d')]):
                            admins[message.chat.id] = {'edit_delete': admins[message.chat.id]['edit']}
                            db_run(f"UPDATE admin SET work='edit_delete'WHERE id={message.chat.id}")
                            bot.send_message(message.chat.id, 'Цифра пары:',
                                             reply_markup=markup_all("ans"))
                        else:
                            assert False
                    except:
                        bot.send_message(message.chat.id, 'Удаление невозможно!')
                elif message.text == 'Вернутся назад!':
                    db_run(f"UPDATE admin SET work=null,data=null WHERE id={message.chat.id}")
                    edit_data.remove(admins[message.chat.id]['edit'].strftime('%Y:%m:%d'))
                    print(f'Дата свободна: {admins[message.chat.id]["edit"]}')
                    admins[message.chat.id] = None
                    bot.send_message(message.chat.id, 'Сделано.', reply_markup=markup_all("adm"))
                else:
                    bot.send_message(message.chat.id, 'Выберите кнопку.', reply_markup=markup_all("edit"))

            elif list(admins[message.chat.id].keys())[0] == 'edit_turn':
                try:
                    a = int(message.text[0:1])
                    b = int(message.text[2:3])

                    data = admins[message.chat.id]['edit_turn']
                    assert not a == 0 or b == 0
                    assert not a > 7 or b > 7
                    assert not a == b

                    if a in calendar[data.strftime('%Y:%m:%d')].keys():
                        if b in calendar[data.strftime('%Y:%m:%d')].keys():
                            pass
                        else:
                            calendar[data.strftime('%Y:%m:%d')][b] = None
                            db_run(f"INSERT INTO owner (day,int) VALUES ('{data.strftime('%Y:%m:%d')}',{b})")
                    elif b in calendar[data.strftime('%Y:%m:%d')].keys():
                        if a in calendar[data.strftime('%Y:%m:%d')].keys():
                            pass
                        else:
                            calendar[data.strftime('%Y:%m:%d')][a] = None
                            db_run(f"INSERT INTO owner (day,int) VALUES ('{data.strftime('%Y:%m:%d')}',{a})")
                    else:
                        assert False

                    calendar[data.strftime('%Y:%m:%d')][a], calendar[data.strftime('%Y:%m:%d')][b] = \
                        calendar[data.strftime('%Y:%m:%d')][b], calendar[data.strftime('%Y:%m:%d')][a]
                    for i in [a, b]:
                        if calendar[data.strftime('%Y:%m:%d')][i] is None:
                            db_run(f"DELETE FROM owner WHERE day='{data.strftime('%Y:%m:%d')}'AND int={i}")
                            del calendar[data.strftime('%Y:%m:%d')][i]
                        elif calendar[data.strftime('%Y:%m:%d')][i][1] is None:
                            db_run(
                                f"UPDATE owner SET lesson ='{rep(calendar[data.strftime('%Y:%m:%d')][i][0])}',hw=null WHERE day='{data.strftime('%Y:%m:%d')}'AND int={i}")
                        else:
                            db_run(
                                f"UPDATE owner SET lesson ='{rep(calendar[data.strftime('%Y:%m:%d')][i][0])}',hw={calendar[data.strftime('%Y:%m:%d')][i][1]} WHERE day='{data.strftime('%Y:%m:%d')}'AND int={i}")

                    day_dz(message.chat.id, data)
                    admins[message.chat.id] = {'edit': data}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")
                    bot.send_message(message.chat.id, 'Хотите продолжить?', reply_markup=markup_all("edit"))
                except:
                    bot.send_message(message.chat.id, 'Не правильная форма.',
                                     reply_markup=markup_all("edit"))
                    admins[message.chat.id] = {'edit': admins[message.chat.id]['edit_turn']}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")

            elif list(admins[message.chat.id].keys())[0] == 'edit_add':
                try:
                    data = admins[message.chat.id]['edit_add']
                    try:
                        calendar[data.strftime('%Y:%m:%d')]
                    except:
                        calendar[data.strftime('%Y:%m:%d')] = {}

                    k = 1
                    while True:
                        if k not in calendar[data.strftime('%Y:%m:%d')].keys():
                            break
                        k += 1

                    assert not k > 7

                    db_run(f"INSERT INTO owner VALUES ('{data.strftime('%Y:%m:%d')}',{k},'{rep(message.text)}',null)")

                    calendar[data.strftime('%Y:%m:%d')][k] = [message.text, None]
                    day_dz(message.chat.id, data)
                    admins[message.chat.id] = {'edit': data}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")
                    bot.send_message(message.chat.id, 'Хотите продолжить?', reply_markup=markup_all("edit"))
                except:
                    bot.send_message(message.chat.id, 'В день не может быть больше 7 пар, мозги закипают)',
                                     reply_markup=markup_all("edit"))
                    admins[message.chat.id] = {'edit': admins[message.chat.id]['edit_add']}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")

            elif list(admins[message.chat.id].keys())[0] == 'edit_edit':
                try:
                    intg = int(message.text[0:1])
                    assert not intg > 7
                    text = message.text[2:]
                    data = admins[message.chat.id]['edit_edit']
                    try:
                        db_run(
                            f"UPDATE owner SET lesson ='{rep(text)}' WHERE day='{data.strftime('%Y:%m:%d')}'AND int={intg}")
                        calendar[data.strftime('%Y:%m:%d')][intg][0] = text
                        day_dz(message.chat.id, data)
                        admins[message.chat.id] = {'edit': data}
                        db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")
                        bot.send_message(message.chat.id, f'Пара изменена!', reply_markup=markup_all("edit"))
                    except:
                        bot.send_message(message.chat.id, 'Такой пары нет!',
                                         reply_markup=markup_all("edit"))
                        admins[message.chat.id] = {'edit': admins[message.chat.id]['edit_edit']}
                        db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")
                except:
                    bot.send_message(message.chat.id, 'Не правильная форма.',
                                     reply_markup=markup_all("edit"))
                    admins[message.chat.id] = {'edit': admins[message.chat.id]['edit_edit']}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")

            elif list(admins[message.chat.id].keys())[0] == 'edit_delete':
                try:

                    integ = int(message.text[0:1])
                    data = admins[message.chat.id]['edit_delete']
                    les = calendar[data.strftime('%Y:%m:%d')][integ][0]
                    db_run(f"DELETE FROM owner WHERE day='{data.strftime('%Y:%m:%d')}'AND int={integ}")
                    calendar[data.strftime('%Y:%m:%d')].pop(integ)
                    day_dz(message.chat.id, data)
                    admins[message.chat.id] = {'edit': data}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")
                    bot.send_message(message.chat.id, f'Удалена пара: {les}', reply_markup=markup_all("edit"))

                except:
                    bot.send_message(message.chat.id, 'Не правильная форма.',
                                     reply_markup=markup_all("edit"))
                    admins[message.chat.id] = {'edit': admins[message.chat.id]['edit_delete']}
                    db_run(f"UPDATE admin SET work='edit'WHERE id={message.chat.id}")

        elif message.chat.id in teachers:
            if message.text == 'Добавить дз!':
                check_default()
                bot.send_message(message.chat.id, 'Напиши дату в формате (2020:09:22) :',
                                 reply_markup=markup_all("ans"))
                teachers[message.chat.id] = 'add_hw'

            elif teachers[message.chat.id] is None:
                bot.send_message(message.chat.id, 'Выбери кнопку!', reply_markup=markup_all("tch"))

            elif teachers[message.chat.id] == 'add_hw':
                good_check_data = check_data(message.text, message.chat.id)
                if not good_check_data.strftime('%Y:%m:%d') in calendar:
                    bot.send_message(message.chat.id, 'На єто число нету пар!')
                    teachers[message.chat.id] = None
                elif good_check_data:
                    edit_data.append(message.text)
                    teachers[message.chat.id] = {'add_hw': good_check_data}
                    day_dz(message.chat.id, good_check_data)
                    bot.send_message(message.chat.id,
                                     'Форма добавления,изменения дз 2:№25,26\n2 - Очередь пары\n№25,26 - На что меняем',
                                     reply_markup=markup_all("ans"))
            elif list(teachers[message.chat.id].keys())[0] == 'add_hw':
                try:
                    intg = int(message.text[0:1])
                    text = message.text[2:]
                    data = teachers[message.chat.id]['add_hw']
                    calendar[data.strftime('%Y:%m:%d')][intg][1] = text
                    day_dz(message.chat.id, data)
                    teachers[message.chat.id] = None
                    db_run(f"UPDATE owner SET hw='{text}' WHERE day='{data.strftime('%Y:%m:%d')}' AND int='{intg}'")
                    bot.send_message(message.chat.id, f'Дз добавлено!', reply_markup=markup_all("del"))
                    if tg_chanel_id:
                        bot.send_message(tg_chanel_id,
                                         f'Добавлено дз: {message.from_user.first_name}\nНа {data.strftime("%A, (%Y:%m:%d)")}\n{intg} : {text}')
                except:
                    bot.send_message(message.chat.id, 'Не правильная форма попробуй еще.',
                                     reply_markup=markup_all("ans"))

        else:
            return True


@bot.message_handler(
    content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                   "animation"])
def sticker(message):
    if message.chat.type == "private":
        bot.forward_message(tg_chanel_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Ваше сообщение было отправлено в общий чат!', reply_markup=markup_all())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data[0:5] == 'early':
                good_data = check_data(call.data[5:], 0)
                good_data -= timedelta(1)
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Прошлый", callback_data=f'early{good_data.strftime("%Y:%m:%d")}')
                item2 = types.InlineKeyboardButton("Следующий", callback_data=f'next{good_data.strftime("%Y:%m:%d")}')
                markup.add(item1, item2)
                print(f'Запрос от {call.message.chat.first_name} на {good_data.strftime("%Y:%m:%d")}!')

                day_dz(call.message.chat.id, good_data, markup, True, call.message.message_id)

            elif call.data[0:4] == 'next':
                good_data = check_data(call.data[4:], 0)
                good_data += timedelta(1)
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Прошлый", callback_data=f'early{good_data.strftime("%Y:%m:%d")}')
                item2 = types.InlineKeyboardButton("Следующий", callback_data=f'next{good_data.strftime("%Y:%m:%d")}')
                markup.add(item1, item2)
                print(f'Запрос от {call.message.chat.first_name} на {good_data.strftime("%Y:%m:%d")}!')

                day_dz(call.message.chat.id, good_data, markup, True, call.message.message_id)

            # remove inline buttons

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
            #                          text="Уведомление!!!")

    except Exception as e:
        print(repr(e))
