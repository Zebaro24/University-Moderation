from config import DISCORD_API
from utils import print_ds
from config import discord_guild, discord_color
from config import role_channel_id, ROLES

import discord

bot = discord.Client()


# Создание главного сообщения для ролей
@bot.event
async def on_ready():
    print_ds(f"Бот был запущен под именем: {bot.user}")
    print_ds("В конфиг roles_config!")
    chanel = bot.get_guild(discord_guild).get_channel(role_channel_id)
    text = ""
    for i in ROLES.keys():
        role_name = input(f"{i} - ")
        text += f"{i} - {role_name}\n"
    message = await chanel.send(embed=discord.Embed(title=text, color=discord_color))

    for i in ROLES.keys():
        await message.add_reaction(i)

    print_ds(f"ID сообщения реакций: {message.id}")
    await bot.close()


bot.run(DISCORD_API)
