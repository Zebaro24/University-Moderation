import config
from config import mafia_color, mafia_players, discord_guild, mafia_channel_id, mafia_channel_webhook
from utils import print_ds
import discord
# from discord_components import Button, ButtonStyle
from discord_bot.main_discord import bot, slash
from dislash import has_permissions, interactions, ActionRow, Button, ButtonStyle
from asyncio import sleep
from discord_bot.mafia.mafia_phrases import quotes
from discord_bot.mafia.mafia_global import distribution_of_roles, main_game
import random
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
    num_want_play = 0
    value_want_play = ""
    for i in mafia_players:
        if i["want_play"]:
            num_want_play += 1
            value_want_play += ":ballot_box_with_check:\n"
        else:
            value_want_play += ":zzz:\n"
        players += f"{num}) {i['player'].mention}\n"
        num += 1
    embed.add_field(name="Игроки", value=players)
    embed.add_field(name=f"Хотят начать игру ({num_want_play}/{len(mafia_players) if len(mafia_players) >= 4 else 4})",
                    value=value_want_play)

    await message.edit(embed=embed)


async def start_game():
    print_ds("Игра в мафию началась!")
    channel: discord.channel.TextChannel = bot.get_guild(discord_guild).get_channel(mafia_channel_id)

    message = await channel.send("**3**")
    await sleep(1)
    await message.edit(content="**2**")
    await sleep(1)
    await message.edit(content="**1**")
    await sleep(1)
    await message.edit(content="**Начинаем игру!**", delete_after=1.9)
    await sleep(2)
    channel = await bot.fetch_webhook(mafia_channel_webhook)
    quote = random.choice(quotes)
    embed = discord.Embed(title=quote["text"], color=mafia_color)
    embed.set_footer(text=quote["author"],
                     icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4figuc0MHBNlnCY5B5XYo6EuHjEmOsSOFyw&usqp=CAU")
    await channel.send(embed=embed)
    await sleep(5)
    await distribution_of_roles()
    await channel.send("Роли были отправлены, проверяйте!")
    await sleep(10)
    await main_game(channel)


@slash.slash_command(description="Тест мафа, Debug - True", options=[
    dislash.Option("count", "Количество игроков", dislash.OptionType.INTEGER, True)])
async def maf(ctx, count):
    await ctx.reply(type=dislash.ResponseType.DeferredUpdateMessage)
    config.debug = True
    await ctx.reply("Ок", delete_after=0.5)
    for i in range(count):
        mafia_players.append({"player": ctx.author, "want_play": True})
    await start_game()
    mafia_players.clear()
    config.debug = False

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
