from config import DISCORD_API, discord_guild, mafia_color, mafia_channel_id
from utils import print_ds
from discord.ui import Button, View
import discord

bot = discord.Client()

discord.sl
# Создание главного сообщения для ролей
@bot.event
async def on_ready():
    print_ds(f"Бот был запущен под именем: {bot.user}")
    print_ds("В конфиг config: mafia!")
    chanel = bot.get_guild(discord_guild).get_channel(mafia_channel_id)

    embed_send = discord.Embed(title="Голосовая мафия",
                               description="Цель мирных жытелей: выгнать мафию, \nцель мафии: убить мирных жытелей.",
                               color=mafia_color)
    embed_send.set_author(name="Мафия",
                          icon_url="https://w1.pngwing.com/pngs/252/342/png-transparent-card-mafia-android-game-board-game-card-game-red-hat-thumbnail.png")
    embed_send.add_field(name="Игроки", value="Нет игроков")

    bt_1 = Button(custom_id='button1', label='Присоедениться', style=discord.ButtonStyle.red)
    bt_2 = Button(custom_id='button2', label='Правила', style=discord.ButtonStyle.red)
    view_send = View(bt_1, bt_2)

    message = await chanel.send(embed=embed_send, view=view_send)

    print_ds(f"ID сообщения реакций: {message.id}")
    await bot.close()


bot.run(DISCORD_API)
