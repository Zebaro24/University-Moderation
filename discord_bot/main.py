import config
import discord

# Возможности
import roles

bot = discord.Client()  # intents=intents_g)


@bot.event
async def on_ready():
    print(f"Bot was started: {bot.user}")
    await roles.offline_role(bot)


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
@bot.event
async def on_message(message: discord.Message):
    # Если автор совпадает с клиентом то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == bot.user:
        return
    # Не забывать await
    # await message.channel.send("sdsdsds")  # Отправить в канал
    # await message.author.send("sasasa")  # Отправить в личку

    if message.content[0:2] == "cl" and type(message.channel) != discord.channel.DMChannel:
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
        await message.channel.send('Hello!')


def start():
    bot.run(config.DISCORD_API)


if __name__ == '__main__':
    start()
