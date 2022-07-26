# Основные дискорд библиотеки
import time

import discord
from discord.ext import commands
# Для слеш команд используем dislash
from dislash import InteractionClient
# Для кнопок и тд используем discord_components
# from discord_components import DiscordComponents - Убран

# Конфиги и доп библиотеки
from utils import print_ds
from config import DISCORD_API, ds_chanel_id, discord_guild, mafia_channel_id, music_channel_id

inst: discord.flags.Intents = discord.Intents.all()
# https://dislashpy.readthedocs.io/en/latest/quickstart.html#creating-a-simple-command - Slash command
bot = commands.Bot("!", intents=inst)
slash = InteractionClient(bot)

# Возможности
import discord_bot.roles.roles_commands as roles
import discord_bot.music.music_commands
import discord_bot.ds_to_tg as ds_to_tg
import discord_bot.mafia.mafia_start as mafia_start
from discord_bot.music.music_read import read_spotify, while_music, update_message


@bot.event
async def on_ready():
    print_ds(f"Бот был запущен под именем: {bot.user.name}")

    activity = discord.Activity(type=discord.ActivityType.listening, name="музыку Димы")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

    await roles.offline_role(bot)

    await update_message()
    read_spotify("https://open.spotify.com/playlist/37i9dQZF1E38pfYCyDWb2j?si=d31487aa9a324efd")
    await update_message()

    chanel = bot.get_guild(discord_guild).get_channel(mafia_channel_id)
    await mafia_start.mafia_start(chanel)


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
@bot.event
async def on_message(message: discord.Message):
    # Если автор совпадает с клиентом – то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == bot.user:
        return

    if message.channel.id == ds_chanel_id:
        ds_to_tg.discord_to_tg(message)
        return

    if "gg" == message.content:
        # gg_pl()
        pass

    member: discord.member.Member = message.author
    gg: discord.activity.Activity = member.activities[1]
    print(gg.to_dict())

    # Не забывать await
    # await message.channel.send("Hello")  # Отправить в канал
    # await message.author.send("It's me")  # Отправить в личку
    '''if message.content[0:2] == "cl" and type(message.channel) != discord.channel.DMChannel:
        try:
            num = int(message.content[3:])
        except ValueError:
            num = 5
        await message.channel.purge(limit=num)

    print(message.author)
    channel: discord.TextChannel = bot.get_channel(995704829416583200)  # Канал по id
    await channel.send("I am potato")  # Отправка в канал по id

    # client.get_user("Zebaro#9282")

    print(message.channel.id)  # Id канала

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')'''


def start():
    bot.run(DISCORD_API)


if __name__ == '__main__':
    start()
