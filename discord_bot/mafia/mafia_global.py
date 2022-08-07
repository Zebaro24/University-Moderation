from config import mafia_players, debug, mafia_color
from discord_bot.mafia.mafia_phrases import professions
from random import shuffle, choice
from discord import Embed


async def distribution_of_roles():
    role = ["mafia", "peace", "peace", "peace"]
    amount = len(mafia_players)

    if amount >= 5:
        role.append("doctor")
    if amount >= 6:
        role.append("sheriff")
    if amount >= 7:
        role.append("mafia")
    if amount >= 8:
        for i in range(amount - len(role)):
            role.append("peace")

    shuffle(role)

    for i in range(amount):
        mafia_players[i]["role"] = role[i]

    print(mafia_players)

    for player in mafia_players:
        if player["role"] == "mafia":
            embed = Embed(title="Вы являетесь опасной **мафией**!", color=mafia_color)
        elif player["role"] == "doctor":
            embed = Embed(title="Вы являетесь важной персоной!\nВы **доктор**!", color=mafia_color)
        elif player["role"] == "sheriff":
            embed = Embed(title="Вы являетесь важной персоной!\nВы **шериф**!", color=mafia_color)
        else:
            embed = Embed(title=f"Так как вы **мирный житель**!\nВы {choice(professions)}!", color=mafia_color)
        await player["player"].send(embed=embed)


async def main_game(channel):
    embed = Embed(title="🏙 Город просыпается")
    embed.set_image(url="https://truemafia.ru/sunrise.gif")
    await channel.send(embed=embed)

    embed = Embed(title="🌃 Город засыпет")
    embed.set_image(url="https://truemafia.ru/sunset.gif")
    await channel.send(embed=embed)
