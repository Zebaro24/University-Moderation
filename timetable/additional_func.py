from config import timetable_time
from datetime import date, timedelta, datetime
from pytz import timezone
from database_func import default_l, default_p, db_run, calendar

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


def day_info(day):
    title = ""
    if int(day.strftime('%W')) % 2:
        title += "Непарный\n"
    else:
        title += "Парный\n"
    title += f"{day.strftime('%A, (%Y:%m:%d)').title()}:\n\n"
    main_text = ''
    try:
        if list(calendar[day.strftime('%Y:%m:%d')].items()):
            for p in sorted(calendar[day.strftime('%Y:%m:%d')].items()):  # p,d p[1]
                if p[1][1] is None:
                    null_object = '\n          '
                    main_text += f"👉{p[0]}) ({timetable_time[int(p[0]) - 1]}){null_object}{p[1][0].replace('%', null_object)}\n\n"
                else:
                    null_object = '\n          '
                    main_text += f"👉{p[0]}) ({timetable_time[int(p[0]) - 1]}){null_object}{p[1][0].replace('%', null_object)} : {p[1][1]}\n\n"
        else:
            main_text += 'Пусто'

    except KeyError:
        main_text += 'Пусто'

    return {"title": title, "main_text": main_text}


def check_data(data):
    try:
        year = int(data[0:4])
        month = int(data[5:7])
        day = int(data[8:10])
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
