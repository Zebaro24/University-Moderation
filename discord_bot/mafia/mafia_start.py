import config
from config import mafia_color, mafia_players, discord_guild, mafia_channel_id
from utils import print_ds
import discord
# rom discord_components import Button, ButtonStyle
from discord_bot.main_discord import bot, slash
from dislash import has_permissions, interactions, ActionRow, Button, ButtonStyle
from asyncio import sleep
import dislash


# Создание главного сообщения для ролей
@slash.slash_command(description="Отправить главное сообщение")
@has_permissions(administrator=True)
async def mafia_start(ctx):
    embed_send = discord.Embed(title="Голосовая мафия",
                               description="Цель мирных жителей: выгнать мафию, \nцель мафии: убить мирных жителей.",
                               color=mafia_color)
    embed_send.set_author(name="Мафия",
                          icon_url="https://w1.pngwing.com/pngs/252/342/png-transparent-card-mafia-android-game-board-game-card-game-red-hat-thumbnail.png")
    embed_send.add_field(name="Игроки", value="Нет игроков")

    bt_1 = Button(custom_id='mafia_join', label='Присоединиться', style=ButtonStyle.red)
    bt_2 = Button(custom_id='mafia_play', label='Играть', style=ButtonStyle.red)
    bt_3 = Button(custom_id='mafia_info', label='Правила', style=ButtonStyle.red)

    if type(ctx) == interactions.app_command_interaction.SlashInteraction:
        await ctx.channel.purge(limit=1000)
        await ctx.reply("Сообщение создано", delete_after=5)
        await ctx.channel.send(embed=embed_send, components=[ActionRow(bt_1, bt_2, bt_3)])
    else:
        await ctx.purge(limit=1000)
        await ctx.send(embed=embed_send, components=[ActionRow(bt_1, bt_2, bt_3)])


async def update_start_message(message):
    embed = message.embeds[0]
    embed.clear_fields()

    players = ""
    num = 1
    player_want_play = 0
    for i in mafia_players:
        if i["want_play"]:
            player_want_play += 1
        players += f"{num}) {i['player'].mention}\n"
        num += 1
    embed.add_field(name="Игроки", value=players)
    embed.add_field(name="Хотят начать игру",
                    value=f"{player_want_play}/{len(mafia_players) if len(mafia_players) >= 4 else 4}")

    await message.edit(embed=embed)


async def start_game():
    print_ds("Игра в мафию началась!")
    chanel = bot.get_guild(discord_guild).get_channel(mafia_channel_id)

    await chanel.send("**3**")
    await chanel.trigger_typing()
    await sleep(1)
    await chanel.send("**2**")
    await chanel.trigger_typing()
    await sleep(1)
    await chanel.send("**1**")
    await chanel.trigger_typing()
    await sleep(1)
    await chanel.send("**Начинаем игру!**")
    await sleep(1)

@slash.slash_command(description="Тест мафа")
async def maf(ctx):
    ctx.reply("Ок")
    await start_game()

# На заметку
# @bot.event
# async def on_button_click(interaction: dislash.interactions.message_interaction.MessageInteraction):
#     print("gggh")
#     print(interaction.component.custom_id)
#     print(type(interaction))
#     print(interaction.component.)
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
#         opt1 = SelectOption(label="Максим", value="gh", emoji="👤")
#         opt2 = SelectOption(label="Денчик", value="gm", emoji="👤")
#
#         select = Select(placeholder="Кого хочешь убить?", options=[opt1, opt2])
#
#         embed = interaction.message.embeds[0]
#         embed.clear_fields()
#         embed.add_field(name="Игроки", value=players)
#         await interaction.message.edit(embed=embed, components=[[bt_1, bt_2]])
