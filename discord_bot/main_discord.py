# Основные дискорд библиотеки
from discord import Activity, ActivityType, Status, Message
from wavelink import NodePool, Node

# Конфиги и доп библиотеки
from config import music_channel_id
from config import DISCORD_API, ds_chanel_id, discord_guild, mafia_channel_id, activityText
from utils import print_ds, bc, exception, info
from asyncio import sleep

# https://dislashpy.readthedocs.io/en/latest/quickstart.html#creating-a-simple-command - Slash command
# Основные классы бота
from main_bot_function import bot_ds as bot
from main_bot_function import slash  # noqa

# Возможности
from discord_bot.music.music_message import update_message
from discord_bot.control_version import check_version
from discord_bot.roles import roles_commands as roles
from discord_bot import create_voice
from discord_bot.mafia import mafia_start
from discord_bot.music import music_commands
# from tg_ds import ds_to_tg

from discord_bot import discord_command  # noqa
from discord_bot import discord_button  # noqa
from discord_bot import discord_select  # noqa
from discord_bot.timetable import command  # noqa
# from . import activity  # noqa
from discord_bot import decor_message  # noqa
from discord_bot import help_command  # noqa
from discord_bot import rgb_lenta  # noqa
from discord_bot import voice_actions  # noqa


# При готовности бота
@bot.event
async def on_ready():
    print_ds(f"Бот был инициализирован под именем: {bot.user.name}")
    guild = bot.get_guild(discord_guild)

    print_ds("Проверка версии")
    await check_version(bot)

    print_ds("Подключение статуса")
    activity = Activity(type=ActivityType.watching, name=activityText)
    await bot.change_presence(status=Status.dnd, activity=activity)

    print_ds("Проверка добавленных реакций")
    await roles.offline_role(bot)

    print_ds("Создание сообщения для игры в мафию")
    await mafia_start.check_start_message(guild.get_channel(mafia_channel_id))

    print_ds("Удаление созданных голосовых каналов")
    await create_voice.delete_excess(guild)

    bot.loop.create_task(start_wavelink())

    print_ds("Создание сообщения для плейлиста музыки")
    bot.loop.create_task(update_message())

    print_ds(f"Бот был {bc('01;38;05;34')}запущен{bc()}")


# Запуск музыкальной ноды
async def start_wavelink():
    await sleep(10)
    connect = False
    for i in range(8):
        node = await NodePool.create_node(bot=bot, host='127.0.0.1', port=2333, password='ln6Bdu47')
        connect = node.is_connected()
        if connect:
            break
        await sleep(5)
    if not connect:
        info("Не удалось подключить Wavelink")


# Нода готова
@bot.event
async def on_wavelink_node_ready(node: Node):
    print_ds(f"Музыкальная нода была запущена под идентификатором: {node.identifier}")
    music_commands.start_bool = False


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
@bot.event
async def on_message(message: Message):
    # Если автор совпадает с клиентом – то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == bot.user:
        return

    # # Телеграм пересылка
    # if message.channel.id == ds_chanel_id and str(message.author)[-5:] != "#0000":
    #     await ds_to_tg.discord_to_tg(message)
    #     return

    # Взаимодействие в муз канале
    if music_channel_id == message.channel.id:
        if music_commands.playlist:
            await music_commands.read_url(message.content)
            await message.reply("🤘 Музон добавляется...", delete_after=6)
        else:
            await music_commands.play(message, message.content)
        await message.delete()

    if "clear" == message.content:
        await message.channel.purge(5)

    if "gg" == message.content:
        pass


@bot.event
async def on_error(event, *args, **kwargs):  # noqa
    exception("Discord")
    print_ds(f"Произошла ошибка на действии: {event}")


# Старт бота
def start():
    while True:
        try:
            bot.run(DISCORD_API)
        except RuntimeError:
            return
        except Exception as e:
            print_ds(f'Бот перезапустился из за \n{repr(e)}')
            exception("Discord")


# Запуск сугубо Discord бота
if __name__ == '__main__':
    start()
