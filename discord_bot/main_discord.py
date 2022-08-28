# Основные дискорд библиотеки
import discord
from discord.ext import commands
import wavelink
from config import music_channel_id

# Для слеш команд используем dislash
from dislash import InteractionClient
from asyncio import sleep

# Конфиги и доп библиотеки
from utils import print_ds, bc
from config import DISCORD_API, ds_chanel_id, discord_guild, mafia_channel_id

# https://dislashpy.readthedocs.io/en/latest/quickstart.html#creating-a-simple-command - Slash command
# Основные классы бота
bot = commands.Bot("!", intents=discord.Intents.all())
slash = InteractionClient(bot)

# Возможности
from discord_bot.music.music_message import update_message
from discord_bot.control_version import check_version
import discord_bot.roles.roles_commands as roles
import discord_bot.create_voice as create_voice
import discord_bot.mafia.mafia_start as mafia_start
import discord_bot.music.music_commands as music_commands
import tg_ds.ds_to_tg as ds_to_tg
import discord_bot.discord_button
import discord_bot.activity
import discord_bot.mafia.mafia_menu
import discord_bot.decor_message
import discord_bot.help_command
import discord_bot.rgb_lenta


# При готовности бота
@bot.event
async def on_ready():
    print_ds(f"Бот был инициализирован под именем: {bot.user.name}")
    guild = bot.get_guild(discord_guild)

    print_ds("Проверка версии")
    await check_version(bot)

    print_ds("Подключение статуса")
    activity = discord.Activity(type=discord.ActivityType.listening, name="СЕРЕГА ПИРАТ - Where Is My Mind?")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

    print_ds("Проверка добавленных реакций")
    await roles.offline_role(bot)

    print_ds("Создание сообщения для игры в мафию")
    await mafia_start.mafia_start(guild.get_channel(mafia_channel_id))

    print_ds("Удаление созданных голосовых каналов")
    await create_voice.delete_excess(guild)

    bot.loop.create_task(start_wavelink())

    print_ds("Создание сообщения для плейлиста музыки")
    bot.loop.create_task(update_message())

    print_ds(f"Бот был {bc('01;38;05;34')}запущен{bc()}")


# Запуск музыкальной ноды
async def start_wavelink():
    await sleep(2)
    connect = False
    while not connect:
        node = await wavelink.NodePool.create_node(bot=bot, host='127.0.0.1', port=2333, password='ln6Bdu47')
        connect = node.is_connected()
        await sleep(5)


# Нода готова
@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print_ds(f"Музыкальная нода была запущена под идентификатором: {node.identifier}")


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
#
@bot.event
async def on_message(message: discord.Message):
    # Если автор совпадает с клиентом – то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == bot.user:
        return

    # Телеграм пересылка
    if message.channel.id == ds_chanel_id and str(message.author)[-5:] != "#0000":
        await ds_to_tg.discord_to_tg(message)
        return

    # Взаимодействие в муз канале
    if music_channel_id == message.channel.id:
        if music_commands.playlist:
            await music_commands.read_url(message.content)
            await message.reply("Музон был добавлен", delete_after=3)
        else:
            await music_commands.play(message, message.content)
        await message.delete()

    if "clear" == message.content:
        await message.channel.purge(5)

    if "gg" == message.content:
        pass


# Старт бота
def start():
    bot.run(DISCORD_API)


if __name__ == '__main__':
    start()
