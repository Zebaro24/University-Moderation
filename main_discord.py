import discord
import config
from discord import utils
from discord.ext import commands
from discord.message import Message
import roles
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
    #await message.channel.send("sdsdsds")  # Отправить в канал
    #await message.author.send("sasasa")  # Отправить в личку

    print(message.author)
    channel: discord.TextChannel = client.get_channel(995704829416583200)  # Канал по id
    await channel.send("sdsds")  # Отправка в канал по id

    #client.get_user("Zebaro#9282")

    print(message.channel.id)  # Id канала

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# roles
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)

    print(member)
    try:
        emoji = str(payload.emoji)
        print(emoji)
        role = utils.get(message.guild.members, id=roles.ROLES[emoji])
        print(role)
        await member.add_roles(role)
    except:
        print("net roli")

if __name__ == '__main__':
    client.run(config.DISCORD_API)

