from ...config import DISCORD_API
from ...config import discord_color
from ...config import role_channel_id, ROLES

from discord import Client, Embed

bot = Client()


# Создание главного сообщения для ролей
@bot.event
async def on_ready():
    print(f"Бот был запущен под именем: {bot.user}")
    print("В конфиг roles_config!")
    chanel = bot.get_channel(role_channel_id)
    text = ""
    for i in ROLES.keys():
        role_name = input(f"{i} - ")
        text += f"{i} - {role_name}\n"
    message = await chanel.send(embed=Embed(title=text, color=discord_color))

    for i in ROLES.keys():
        await message.add_reaction(i)

    print(f"ID сообщения реакций: {message.id}")
    await bot.close()


bot.run(DISCORD_API)
