# Импорт настроек
from ..config import TELEGRAM_API, ds_chanel_webhook
from ..utils import print_ds, print_tg

# Импорт Discord функций
from ..discord_bot.main_discord import bot as bot_ds
from discord import File, Webhook, Embed

# Импорт Telegram функций
from ..telegram_bot.main_telegram import bot as bot_tg
from telebot.types import Message

# Импорт доп функций
from asyncio import run_coroutine_threadsafe
from time import perf_counter
import aiohttp
import io


# Запуск coroutine функций
def coroutine_send(message: Message):
    run_coroutine_threadsafe(telegram_to_ds(message), bot_ds.loop)


# Получение файла с file_id Telegram
def get_file_url(file_id):
    get_file_path = bot_tg.get_file(file_id).file_path
    file_path = f"https://api.telegram.org/file/bot{TELEGRAM_API}/{get_file_path}"
    return file_path


# Добавление оформления текста с Telegram
def text_read(text, entities):
    if not entities:
        return text
    add_symbol = 0
    for i in entities:
        if i.type == "bold":
            text = text[:add_symbol + i.offset] + \
                   "**" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   "**" + text[add_symbol + i.offset + i.length:]
            add_symbol += 4
        elif i.type == "italic":
            text = text[:add_symbol + i.offset] + \
                   "_" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   "_" + text[add_symbol + i.offset + i.length:]
            add_symbol += 2
        elif i.type == "underline":
            text = text[:add_symbol + i.offset] + \
                   "__" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   "__" + text[add_symbol + i.offset + i.length:]
            add_symbol += 4
        elif i.type == "strikethrough":
            text = text[:add_symbol + i.offset] + \
                   "~~" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   "~~" + text[add_symbol + i.offset + i.length:]
            add_symbol += 4
        elif i.type == "code":
            text = text[:add_symbol + i.offset] + \
                   "`" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   "`" + text[add_symbol + i.offset + i.length:]
            add_symbol += 2
        elif i.type == "spoiler":
            text = text[:add_symbol + i.offset] + \
                   "||" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   "||" + text[add_symbol + i.offset + i.length:]
            add_symbol += 4
        elif i.type == "text_link":
            text = text[:add_symbol + i.offset] + \
                   "[" + text[add_symbol + i.offset:add_symbol + i.offset + i.length] + \
                   f"]({i.url})" + text[add_symbol + i.offset + i.length:]
            add_symbol += 4 + len(i.url)
    return text


# Перевод файла со ссылки в Discord File
async def file_reed(url, format_file):
    before = perf_counter()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                print_tg("Файл не был найден")
                return
            if resp.content_length > 8388608:
                print_tg("Файл больше 8мб (Не должно отправится)")
                return

            data = io.BytesIO(await resp.read())
            time_load = perf_counter() - before
            print_ds(f"Файл был отправлен за: {round(time_load, 2)} сек")
            return File(data, format_file)


# Отправка сообщения с Telegram в Discord
async def telegram_to_ds(message: Message):
    channel: Webhook = await bot_ds.fetch_webhook(ds_chanel_webhook)
    file_id = bot_tg.get_user_profile_photos(message.from_user.id).photos[0][-1].file_id
    path = bot_tg.get_file(file_id).file_path
    username = f"{message.from_user.first_name} TG"
    avatar_url = f"https://api.telegram.org/file/bot{TELEGRAM_API}/{path}"

    if message.forward_from:
        forward_embed = Embed(title=f"Переслано от **{message.forward_from.first_name}**")
        await channel.send(embed=forward_embed, username=username, avatar_url=avatar_url)
    elif message.forward_from_chat:
        forward_embed = Embed(title=f"Переслано от **{message.forward_from_chat.title}**")
        await channel.send(embed=forward_embed, username=username, avatar_url=avatar_url)
    elif message.forward_sender_name:
        forward_embed = Embed(title=f"Переслано от **{message.forward_sender_name}**")
        await channel.send(embed=forward_embed, username=username, avatar_url=avatar_url)

    if message.content_type == "text":
        text = text_read(message.text, message.entities)
        await channel.send(text, username=username, avatar_url=avatar_url)
        print_ds(f"Отправлено с TG: текст")
    elif message.content_type == "location":
        text = f"[Отправил геолакацию](https://www.google.com/maps/place/{message.location.latitude}+{message.location.longitude})"

        if message.location.live_period == 900:
            text += "\nДействует 15 мин"
        elif message.location.live_period == 3600:
            text += "\nДействует 1 час"
        elif message.location.live_period == 28800:
            text += "\nДействует 8 часов"
        elif message.location.live_period:
            text += f"\nДействует {message.location.live_period} секунд"

        await channel.send(text, username=username, avatar_url=avatar_url)
        print_ds(f"Отправлено с TG: локация")

    elif message.content_type == "contact":
        embed = Embed(title=f"Контакт: {message.contact.first_name}",
                      description=f"Номер: {message.contact.phone_number}")
        await channel.send(embed=embed, username=username, avatar_url=avatar_url)
        print_ds(f"Отправлено с TG: контакт")

    elif message.content_type in ["photo", "video", "video_note", "animation", "sticker", "voice", "audio", "document"]:
        if message.content_type == "photo":
            if message.photo[-1].file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.photo[-1].file_id)
            file = "photo.jpg"
            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: фото")

        elif message.content_type == "video":
            if message.video.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.video.file_id)

            if message.video.file_name:
                file = message.video.file_name
            else:
                file = "video.mp4"

            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: видео")

        elif message.content_type == "video_note":
            if message.video_note.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.video_note.file_id)
            file = "video_note.mp4"
            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: видео кружочек")

        elif message.content_type == "animation":
            if message.animation.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.animation.file_id)

            if message.animation.file_name:
                file = message.animation.file_name
            else:
                file = "gif.mp4"

            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: анимация")

        elif message.content_type == "sticker":
            if message.sticker.thumb.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.sticker.thumb.file_id)
            file = "photo.jpg"
            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: стикер")

        elif message.content_type == "voice":
            if message.voice.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.voice.file_id)
            file = "voice.ogg"
            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: голос")

        elif message.content_type == "audio":
            if message.audio.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.audio.file_id)
            file = message.audio.file_name
            text = text_read(message.caption, message.caption_entities)

            embed = Embed(title=message.audio.title, description=message.audio.performer)
            if message.audio.thumb:
                embed.set_thumbnail(url=get_file_url(message.audio.thumb.file_id))
            await channel.send(embed=embed, username=username, avatar_url=avatar_url)
            print_ds(f"Отправлено с TG: audio")

        elif message.content_type == "document":
            if message.document.file_size > 8388608:
                url = ""
            else:
                url = get_file_url(message.document.file_id)
            file = message.document.file_name
            text = text_read(message.caption, message.caption_entities)
            print_ds(f"Отправлено с TG: файл")

        else:
            url = ""
            file = ""
            text = ""

        if text:
            embed = Embed(description=text)
        else:
            embed = None

        if url:
            await channel.send(embed=embed, file=await file_reed(url, file), username=username, avatar_url=avatar_url)
        else:
            if embed:
                embed.title = f"Файл: {file} больше 8мб и не может быть отправлен."
            else:
                embed = Embed(title=f"Файл: {file} больше 8мб и не может быть отправлен.")
            await channel.send(embed=embed, username=username, avatar_url=avatar_url)
