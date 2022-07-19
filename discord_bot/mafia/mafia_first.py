from config import DISCORD_API, discord_guild, mafia_color, mafia_channel_id
from utils import print_ds
import discord
from discord_components import DiscordComponents, Button, ButtonStyle

bot = discord.Client()
DiscordComponents(bot)


# Создание главного сообщения для ролей
@bot.event
async def on_ready():
    print_ds(f"Бот был запущен под именем: {bot.user}")
    print_ds("В конфиг config: mafia!")
    chanel = bot.get_guild(discord_guild).get_channel(mafia_channel_id)
    await chanel.purge(limit=200)

    embed_send = discord.Embed(title="Голосовая мафия",
                               description="Цель мирных жителей: выгнать мафию, \nцель мафии: убить мирных жителей.",
                               color=mafia_color)
    embed_send.set_author(name="Мафия",
                          icon_url="https://w1.pngwing.com/pngs/252/342/png-transparent-card-mafia-android-game-board-game-card-game-red-hat-thumbnail.png")
    embed_send.add_field(name="Игроки", value="Нет игроков")

    bt_1 = Button(custom_id='mafia_join', label='Присоединиться', style=ButtonStyle.red)
    bt_2 = Button(custom_id='mafia_info', label='Правила', style=ButtonStyle.red)

    message = await chanel.send(embed=embed_send, components=[[bt_1, bt_2]])

    print_ds(f"ID сообщения реакций: {message.id}")


# На заметку
# @bot.event
# async def on_button_click(interaction: interaction.Interaction):
#     print(type(interaction))
#     print(interaction.component.custom_id)
#     print(interaction.component.to_dict())
#     if interaction.component.custom_id == "button1":
#         await interaction.respond(content='Вы присоединились')
#
#         players = f"{interaction.user.mention}"
#
#         embed_send = discord.Embed(title="Голосовая мафия",
#                                    description="Цель мирных жителей: выгнать мафию, \nцель мафии: убить мирных жителей.",
#                                    color=mafia_color)
#         embed_send.set_author(name="Мафия",
#                               icon_url="https://w1.pngwing.com/pngs/252/342/png-transparent-card-mafia-android-game-board-game-card-game-red-hat-thumbnail.png")
#         embed_send.add_field(name="Игроки", value=players)
#
#         bt_1 = Button(custom_id='button1', label='Присоединиться', style=ButtonStyle.red)
#         bt_2 = Button(custom_id='button2', label='Правила', style=ButtonStyle.red)
#
#         embed = interaction.message.embeds[0]
#         embed.clear_fields()
#         embed.add_field(name="Игроки", value=players)
#         await interaction.message.edit(embed=embed, components=[[bt_1, bt_2]])
#
# @bot.event
# async def on_message(message: discord.Message):
#     print(message.content)


bot.run(DISCORD_API)
