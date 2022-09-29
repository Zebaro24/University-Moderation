import schedule
from time import sleep
from telegram_bot.main_telegram import bot
from timetable.notification_phrases import phrases
from config import tg_chanel_id, timetable_time
from datetime import datetime, timedelta
from pytz import timezone
from database_func import calendar
from telegram_bot.timetable.function import day_info_tg
from utils import print_tg
import pyowm
from pyowm.weatherapi25.weather import Weather
import requests
import xmltodict
import random

horo = {"aries": "♈ Овен",
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
        "pisces": "♓ Рыбы"}

api_weather = pyowm.OWM("542abfd3fa5280d48120c9b9df384872") # noqa
api_weather.config["language"] = "ru"
tz = timezone("Europe/Kyiv")


def horoscope_text():
    response = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml')
    dict_data = xmltodict.parse(response.content)["horo"]
    dict_data.pop("date")
    slv = random.choice(list(dict_data.keys()))
    text_slv = f"*Знак зодиака: {horo[slv]}*\n"
    text_slv += dict_data[slv]["today"]
    return text_slv


def find_weather():
    weather: pyowm.weatherapi25.weather.Weather = api_weather.weather_manager().weather_at_place(
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
        schedule.run_pending()
        sleep(1)


def start_task():
    try:
        print_tg("Бот разбудил всех!")
        weather = find_weather()
        bot.send_sticker(tg_chanel_id, weather["sticker"])
        dt = datetime.now(tz)
        month = dt.month
        season = ["💦", "🌈", "🌱", "☀️", "🔥", "🌴", "🍃", "🍁", "🍂", "☃️", "🎄", "❄"]
        bot.send_message(tg_chanel_id, f"{season[month - 1]} *{dt.strftime('%d %B')}*", parse_mode='Markdown')
        bot.send_message(tg_chanel_id, random.choice(phrases))
        bot.send_message(tg_chanel_id, weather["text"], parse_mode='Markdown')
        bot.send_message(tg_chanel_id, horoscope_text(), parse_mode='Markdown')
        day_info_tg(tg_chanel_id, datetime.now(tz).strftime('%Y:%m:%d'))
    except Exception as gg:
        print_tg(gg)
        print_tg("В боте произошла ошибка!")
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
            print_tg("Сейчас " + str(datetime.now(tz)))
            print_tg(f"Бот разбудит всех в {time_p}")
            schedule.every().day.at(time_p.strftime("%H:%M")).do(start_task)
            return schedule.CancelJob
        else:
            print_tg(f"Бот сегодня уже всех разбудил в {time_p}")
            schedule.every().day.at("03:00").do(check_task)
    except Exception as error:
        print_tg(f"Error: {error}")
        print_tg("Или ошибка или это выходной!")
        schedule.every().day.at("03:00").do(check_task)


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, "ru_RU")
    start_task()
