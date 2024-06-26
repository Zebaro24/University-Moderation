from config import tg_chanel_id, timetable_time
from utils import print_tg
from telegram_bot.timetable.function import day_info_tg
from database_func import calendar
from main_bot_function import bot_tg as bot
from timetable.birthdays import birth, birthdays_phrases
from timetable.notification_phrases import phrases

from pyowm.weatherapi25.weather import Weather
from pyowm import OWM
from datetime import datetime, timedelta, time, date
from scheduler import Scheduler
from pytz import timezone
from time import sleep
from random import choice
import xmltodict
import requests

horo = {
    "aries": "♈ Овен",
    "taurus": "♉ Телец",
    "gemini": "♊ Близнецы",
    "cancer": "♋ Рак",
    "leo": "♌ Лев",
    "virgo": "♍ Дева",
    "libra": "♎ Весы",
    "scorpio": "♏ Скорпион",
    "sagittarius": "♐ Стрелец",
    "capricorn": "♑ Козерог",
    "aquarius": "♒ Водолей",
    "pisces": "♓ Рыбы"
}

api_weather = OWM("542abfd3fa5280d48120c9b9df384872")  # noqa
api_weather.config["language"] = "ru"
tz = timezone("Europe/Kyiv")
schedule = Scheduler(tzinfo=tz)


def check_birthdays():
    for date_bd, name in birth.items():
        if datetime.now().day == date_bd.day and datetime.now().month == date_bd.month:
            age = date.today().year - date_bd.year
            print_tg(f"Бот поздравил {name}")
            text = choice(birthdays_phrases) % {"name": name.split()[1], "fullname": name, "age": age}
            bot.send_message(tg_chanel_id, text, parse_mode='Markdown')


def horoscope_text():
    response = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml')
    dict_data = xmltodict.parse(response.content)["horo"]
    dict_data.pop("date")
    slv = list(horo.keys())[int(datetime.now(tz).timestamp() // 86400 % 12)]
    text_slv = f"*Знак зодиака: {horo[slv]}*\n"
    text_slv += dict_data[slv]["today"]
    return text_slv


def find_weather():
    weather: Weather = api_weather.weather_manager().weather_at_place(
        "Chernihiv,Ukraine").weather
    temp = weather.temperature('celsius')

    sticker = requests.get(weather.weather_icon_url('4x'), stream=True).raw
    text = f"*{weather.detailed_status.capitalize()}*\n"
    text += f"🌡 Температура: {temp['temp']}°C\n"
    text += f"😏 Чувствуется: {temp['feels_like']}°C\n"
    text += f"🌬 Скорость ветра: {weather.wind()['speed']}м/c\n"
    text += f"💦 Влажность: {weather.humidity}%\n"
    text += f"🫥 Давление: {weather.barometric_pressure()['press']}гПа\n"
    text += f"🌅 Восход: {datetime.fromtimestamp(weather.sunrise_time('unix'), tz).strftime('%H:%M')} "
    text += f"🌇 Закат: {datetime.fromtimestamp(weather.sunset_time('unix'), tz).strftime('%H:%M')}\n"
    return {"sticker": sticker, "text": text}


def go_task():
    print_tg("Задачи запущены!")
    while True:
        schedule.exec_jobs()
        sleep(1)


def start_task(pars=True):
    try:
        # check_birthdays()
        print_tg("Бот разбудил всех!")
        # weather = find_weather()
        # bot.send_sticker(tg_chanel_id, weather["sticker"])
        # dt = datetime.now(tz)
        # month = dt.month
        # season = ["🎄", "❄", "💦", "🌸", "🌱", "☀️", "🔥", "🌴", "🍃", "🍁", "🍂", "☃️"]
        # bot.send_message(tg_chanel_id, f"{season[month - 1]} *{dt.strftime('%d %B')}*", parse_mode='Markdown')
        # bot.send_message(tg_chanel_id, choice(phrases))
        # bot.send_message(tg_chanel_id, weather["text"], parse_mode='Markdown')
        # bot.send_message(tg_chanel_id, horoscope_text(), parse_mode='Markdown')
        if pars:
            day_info_tg(tg_chanel_id, datetime.now(tz).strftime('%Y:%m:%d'))
    except Exception as error:
        print_tg(f"Error: {error}")
        print_tg("В боте произошла ошибка!")
    sleep(1)
    check_task()


def check_task():
    try:
        now_str = datetime.now(tz).strftime('%Y:%m:%d')

        if not (now_str in calendar and calendar[now_str]):
            print_tg(f"Сегодня выходной: {now_str}!")
            schedule.once(time(9, tzinfo=tz), check_birthdays)
            schedule.once(time(3, tzinfo=tz), check_task)
            return

        time_p = tz.localize(
            datetime.strptime(now_str + " " + timetable_time[min(calendar[now_str]) - 1][:5], "%Y:%m:%d %H:%M"))
        time_p -= timedelta(minutes=10)
        if datetime.now(tz) < time_p:
            print_tg("Сейчас " + str(datetime.now(tz)))
            print_tg(f"Бот разбудит всех в {time_p}")
            schedule.once(time_p, start_task)
        else:
            print_tg(f"Бот сегодня уже всех разбудил в {time_p}")
            schedule.once(time(3, tzinfo=tz), check_task)
    except Exception as error:
        print_tg(f"Error: {error}")
        print_tg("Ошибка в notification!")
        schedule.once(time(3, tzinfo=tz), check_task)


if __name__ == '__main__':
    import locale
    from database_func import load_all_elements

    load_all_elements()
    locale.setlocale(locale.LC_ALL, "ru_RU")

    tg_chanel_id = 771348519

    # check_task()
    # go_task()

    # print(schedule)

    start_task()
