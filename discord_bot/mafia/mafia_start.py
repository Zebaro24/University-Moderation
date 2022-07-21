import config
from config import mafia_color, mafia_players
from utils import print_ds
import discord
# rom discord_components import Button, ButtonStyle
from discord_bot.main_discord import bot, slash
from dislash import has_permissions, interactions, ActionRow, Button, ButtonStyle
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


# На заметку
@bot.event
async def on_button_click(interaction: dislash.interactions.message_interaction.MessageInteraction):
    if interaction.component.custom_id == "mafia_info":
        await interaction.reply("Правила", ephemeral=True)
    elif interaction.component.custom_id == "mafia_join":
        if interaction.author in [i["player"] for i in mafia_players]:
            await interaction.reply("Вы уже присоединились", ephemeral=True)
            return
        player = {"player": interaction.author, "role": None, "want_play": False}
        mafia_players.append(player)
        embed = interaction.message.embeds[0]
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

        await interaction.message.edit(embed=embed)
        await interaction.reply("Вы присоединились", ephemeral=True)
    elif interaction.component.custom_id == "mafia_play":
        if interaction.author in [i["player"] for i in mafia_players]:
            for i in range(len(mafia_players)):
                if interaction.author == mafia_players[i]["player"]:
                    mafia_players[i]["want_play"] = True
                    embed = interaction.message.embeds[0]
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

                    await interaction.message.edit(embed=embed)
                    await interaction.reply("Ждем остальных игроков", ephemeral=True)
        else:
            await interaction.reply("Вы еще не присоединились", ephemeral=True)
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
#
