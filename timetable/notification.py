import schedule
from time import sleep
from telegram_bot.main_telegram import bot
from config import tg_chanel_id, timetable_time
from datetime import datetime, timedelta
from pytz import timezone
from database_func import calendar
from telegram_bot.timetable.function import day_info_tg

tz = timezone("Europe/Kyiv")


def go_task():
    print("Задачи запущены!")
    while True:
        schedule.run_pending()
        sleep(1)


def start_task():
    try:
        print("Бот разбудил всех!")
        bot.send_message(tg_chanel_id, "Солнышко мое, вставай)")
        day_info_tg(tg_chanel_id, datetime.now(tz))
    except Exception as gg:
        print(gg)
        print("В боте произошла ошибка!")
    check_task()
    return schedule.CancelJob


def check_task():
    try:
        now = calendar[datetime.now(tz).strftime('%Y:%m:%d')]
        time_p = tz.localize(
            datetime.strptime(datetime.now(tz).strftime('%Y:%m:%d ') + timetable_time[min(now.keys()) - 1][:5],
                              "%Y:%m:%d %H:%M"))
        time_p -= timedelta(minutes=10)
        if datetime.now(tz) < time_p:
            print("Сейчас " + str(datetime.now(tz)))
            print(f"Бот разбудит всех в {time_p}")
            schedule.every().day.at(time_p.strftime("%H:%M")).do(start_task)
            return schedule.CancelJob
        else:
            print(f"Бот сегодня уже всех разбудил в {time_p}")
            schedule.every().day.at("03:00").do(check_task)
    except Exception as error:
        print(f"Error: {error}")
        print("Или ошибка или это выходной!")
        schedule.every().day.at("03:00").do(check_task)
