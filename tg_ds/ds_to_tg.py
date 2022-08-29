# Импорт настроек
from config import tg_chanel_id
from utils import print_tg

# Импорт Telegram бота
from telegram_bot.main_telegram import bot as bot_tg

# Импорт времени
from time import perf_counter


async def discord_to_tg(message):
    if message.attachments:
        before = perf_counter()
        for i in message.attachments:
            if i.filename[-3:] in ["png", "jpg"]:
                bot_tg.send_photo(tg_chanel_id, await i.read(use_cached=True),
                                  f"*{message.author.display_name} DS*: {message.content}", parse_mode="Markdown")
                print_tg("Оправлено с DS: фото")
            else:
                bot_tg.send_document(tg_chanel_id, await i.read(use_cached=True), visible_file_name=i.filename,
                                     caption=f"*{message.author.display_name} DS*: {message.content}",
                                     parse_mode="Markdown")
                print_tg("Оправлено с DS: файл")
        time_load = perf_counter() - before
        print_tg(f"Файл был отправлен за: {round(time_load, 2)} сек")

    else:
        bot_tg.send_message(tg_chanel_id, f"*{message.author.display_name} DS*: {message.content}",
                            parse_mode="Markdown")
        print_tg("Оправлено с DS: текст")
