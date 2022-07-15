from utils import print_ds
from config import DISCORD_API, ds_chanel_id
from dislash import InteractionClient
import discord
from discord.ext import commands

bot = commands.Bot("!")  # intents=intents_g)
# https://dislashpy.readthedocs.io/en/latest/quickstart.html#creating-a-simple-command
splash = InteractionClient(bot)


# Возможности
import discord_bot.roles.roles_commands as roles
import discord_bot.music.music_commands
import discord_bot.ds_to_tg as ds_to_tg


@bot.event
async def on_ready():
    print_ds(f"Бот был запущен под именем: {bot.user.name}")
    await roles.offline_role(bot)


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
@bot.event
async def on_message(message: discord.Message):
    # Если автор совпадает с клиентом то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == bot.user:
        return

    if message.channel.id == ds_chanel_id:
        ds_to_tg.discord_to_tg(message)
        return


    # Не забывать await
    # await message.channel.send("sdsdsds")  # Отправить в канал
    # await message.author.send("sasasa")  # Отправить в личку
    '''if message.content[0:2] == "cl" and type(message.channel) != discord.channel.DMChannel:
        try:
            num = int(message.content[3:])
        except ValueError:
            num = 5
        await message.channel.purge(limit=num)

    print(message.author)
    channel: discord.TextChannel = bot.get_channel(995704829416583200)  # Канал по id
    await channel.send("sdsds")  # Отправка в канал по id

    # client.get_user("Zebaro#9282")

    print(message.channel.id)  # Id канала

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')'''


def start():
    bot.run(DISCORD_API)


if __name__ == '__main__':
    start()
