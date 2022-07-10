import discord
import main_constants
from discord.ext import commands
from discord.message import Message

client = discord.Client()


@client.event
async def on_ready():
    print(f"Bot was started: {client.user}")


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
@client.event
async def on_message(message: Message):
    # Если автор совпадает с клиентом то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == client.user:
        return

    # Не забывать await
    await message.channel.send("sdsdsds")  # Отправить в канал
    await message.author.send("sasasa")  # Отправить в личку

    channel: discord.TextChannel = client.get_channel(995704829416583200)  # Канал по id
    await channel.send("sdsds")  # Отправка в канал по id

    print(message.channel.id)  # Id канала

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


if __name__ == '__main__':
    client.run(main_constants.DISCORD_API)
