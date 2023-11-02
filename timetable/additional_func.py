from config import timetable_time
from datetime import date, timedelta, datetime
from pytz import timezone
from database_func import default_l, default_p, db_run, calendar, admins, teachers, edit_data
from utils import print_tg

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

        # Проверка на каникулы
        if not day_delt > datetime(2023, 2, 5, tzinfo=tz):
            for i in range(5):
                day_delt += one_day
            print_tg(f"Сейчас каникулы: {day_delt}")
            continue

        if int(day_delt.strftime('%W')) % 2:
            default_r = default_l
        else:
            default_r = default_p

        for i in range(5):
            try:
                calendar[day_delt.strftime('%Y:%m:%d')]
            except KeyError:
                calendar[day_delt.strftime('%Y:%m:%d')] = {}
                print_tg(f"Добавление дня {day_delt.strftime('%Y:%m:%d')}!")
                for b, d in default_r[day_delt.weekday()].items():
                    calendar[day_delt.strftime('%Y:%m:%d')][b] = [d, None]
                    d = d.replace("'", "''")
                    db_run(f"INSERT INTO owner VALUES ('{day_delt.strftime('%Y:%m:%d')}',{b},'{d}',null)")

            day_delt += one_day


def list_days_by_text(time):
    all_day = []
    if time == 'next_week':
        now = datetime.now(tz)
        one_week = timedelta(weeks=1)
        day_to_week = timedelta(now.weekday())
        one_day = timedelta(1)

        day_delt = now - day_to_week + one_week

        for i in range(5):
            all_day.append(day_delt.strftime('%Y:%m:%d'))
            day_delt += one_day

    elif time == 'now_week':
        now = datetime.now(tz)
        day_to_week = timedelta(now.weekday())
        one_day = timedelta(1)

        day_delt = now - day_to_week

        for i in range(5):
            all_day.append(day_delt.strftime('%Y:%m:%d'))
            day_delt += one_day

    elif time == 'now_day':
        all_day.append(datetime.now(tz).strftime('%Y:%m:%d'))

    elif time == 'next_day':
        all_day.append((datetime.now(tz) + timedelta(1)).strftime('%Y:%m:%d'))

    return all_day


def day_info(day: date, space=None):
    title = ""
    if int(day.strftime('%W')) % 2:
        title += "Парний\n"
    else:
        title += "Непарний\n"
    title += f"{day.strftime('%A, (%Y:%m:%d)').title()}:\n\n".replace("'Я", "'я")
    main_text = ''
    try:
        if list(calendar[day.strftime('%Y:%m:%d')].items()):
            if space == "ds":
                null_object = '\n   '
            else:
                null_object = '\n            '
            enter = "\n"
            for p in sorted(calendar[day.strftime('%Y:%m:%d')].items()):  # p,d p[1]
                pair = f"👉{p[0]}) ({timetable_time[int(p[0]) - 1]})\n" \
                       f"{p[1][0]}"
                if p[1][1]:
                    pair += f"\n_Дз:_\n{p[1][1]}"
                main_text += pair.replace(enter, null_object) + "\n\n"
        else:
            main_text += 'Пусто'

    except KeyError:
        main_text += 'Пусто'

    return {"title": title, "main_text": main_text}


def check_data(date_text: str):
    try:
        year = int(date_text[0:4])
        month = int(date_text[5:7])
        day = int(date_text[8:10])
        if not 2021 <= year <= 2025:
            return 'Не тот год, попробуй еще!'
        if not 1 <= month <= 12:
            return 'Не правильный месяц, попробуй еще!'
        if not 1 <= day <= 31:
            return 'Не правильный день, попробуй еще!'
        try:
            good_data = date(year, month, day)
            return good_data
        except ValueError:
            return 'Не правильный день, попробуй еще!'
    except ValueError:
        return 'Не верный формат, попробуй еще!'


def edit_day(action: str, date_text: str, num_1: int = None, num_2: int = None, text: str = None):
    if action == "add_hw":
        calendar[date_text][num_1][1] = text
        db_run(f"UPDATE owner SET hw='{text}' WHERE day='{date_text}' AND int='{num_1}'")
        return True

    elif action == "turn":
        couples_number = calendar[date_text]

        if num_1 not in couples_number and num_2 not in couples_number:
            return False
        elif (not 1 <= num_1 <= 7) or (not 1 <= num_2 <= 7):
            return False
        elif num_1 == num_2:
            return False
        # Чтобы поменять их местами и если надо выполнить следующий if
        if num_1 not in couples_number:
            num_1, num_2 = num_2, num_1

        if num_2 not in couples_number:
            calendar[date_text][num_2] = calendar[date_text][num_1]
            del calendar[date_text][num_1]
            hw = f"'{rep(calendar[date_text][num_2][1])}'" if calendar[date_text][num_2][1] else "null"
            db_run(f"INSERT INTO owner (day,int,lesson,hw) "
                   f"VALUES ('{date_text}',{num_2},'{rep(calendar[date_text][num_2][0])}',{hw})")
            db_run(f"DELETE FROM owner WHERE day='{date_text}'AND int={num_1}")
        else:
            calendar[date_text][num_1], calendar[date_text][num_2] = \
                calendar[date_text][num_2], calendar[date_text][num_1]
            hw_1 = f"'{rep(calendar[date_text][num_1][1])}'" if calendar[date_text][num_1][1] else "null"
            hw_2 = f"'{rep(calendar[date_text][num_2][1])}'" if calendar[date_text][num_2][1] else "null"
            db_run(f"UPDATE owner SET lesson ='{rep(calendar[date_text][num_1][0])}',hw={hw_1} "
                   f"WHERE day='{date_text}'AND int={num_1}")
            db_run(f"UPDATE owner SET lesson ='{rep(calendar[date_text][num_2][0])}',hw={hw_2} "
                   f"WHERE day='{date_text}'AND int={num_2}")
        return True

    elif action == "add":
        if date_text not in calendar:
            calendar[date_text] = {}

        number = 1
        while True:
            if number not in calendar[date_text]:
                break
            number += 1

        if not number <= 7:
            return False

        calendar[date_text][number] = [text, None]
        db_run(f"INSERT INTO owner VALUES ('{date_text}',{number},'{rep(text)}',null)")
        return True

    elif action == "edit":
        if num_1 not in calendar[date_text]:
            return False

        calendar[date_text][num_1][0] = text
        db_run(f"UPDATE owner SET lesson ='{rep(text)}' WHERE day='{date_text}'AND int={num_1}")
        return True

    elif action == "delete":
        if num_1 not in calendar[date_text]:
            return False

        del calendar[date_text][num_1]
        if not calendar[date_text]:
            del calendar[date_text]

        db_run(f"DELETE FROM owner WHERE day='{date_text}'AND int={num_1}")
        return True


def moderator_update(moderators_dict: dict, moderator_id: int, action: str = None, date_text: str = None):
    if date_text not in edit_data:
        edit_data.append(date_text)
    elif action is None:
        edit_data.remove(moderators_dict[moderator_id]["date"])
    action_db = f"'{action}'" if action else "null"
    date_text_db = f"'{date_text}'" if date_text else "null"
    db_run(f"UPDATE admin SET work={action_db},data={date_text_db} WHERE id={moderator_id}")
    moderators_dict[moderator_id] = {"action": action, "date": date_text} if action else None


def admin_update(admin_id: int, action: str = None, date_text: str = None):
    moderator_update(admins, admin_id, action, date_text)


def teacher_update(teacher_id: int, action: str = None, date_text: str = None):
    moderator_update(teachers, teacher_id, action, date_text)
