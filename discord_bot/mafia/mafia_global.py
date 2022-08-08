from config import mafia_players, mafia_color
from discord_bot.mafia.mafia_phrases import professions, random_roles
from random import shuffle, choices, choice
from discord import Embed


async def distribution_of_roles():
    role = ["mafia", "peace", "peace", "sheriff"]
    amount = len(mafia_players)

    if amount >= 5:
        role.append("doctor")
    if amount >= 6:
        random_roles_clone = random_roles.copy()
        for i in range(amount - len(role) if amount - len(role) <= 6 else 6):
            random_role = choices(list(random_roles_clone.keys()), random_roles_clone.values())[0]
            del random_roles_clone[random_role]
            role.append(random_role)
    if amount >= 12:
        for i in range(amount - len(role)):
            role.append("peace")

    shuffle(role)

    for i in range(amount):
        mafia_players[i]["role"] = role[i]
        print(mafia_players[i])

    professions_clone = professions.copy()
    for player in mafia_players:
        if player["role"] == "mafia":
            embed = Embed(title="Вы являетесь опасной **мафией**!", color=mafia_color)
        elif player["role"] == "doctor":
            embed = Embed(title="Вы являетесь важной персоной!\nВы **доктор**!", color=mafia_color)
        elif player["role"] == "sheriff":
            embed = Embed(title="Вы являетесь важной персоной!\nВы **шериф**!", color=mafia_color)
        elif player["role"] == "whore":
            embed = Embed(title="Откуда у тебя этот айфон.\nТы грязная шлюха(без обид, такая жизнь))",
                          color=mafia_color)
        elif player["role"] == "fucker":
            embed = Embed(title="Знаешь откуда у меня эти шрамы?\nСкорее всего ты ебанат)", color=mafia_color)
        elif player["role"] == "priest":
            embed = Embed(title="А вы верите в бога?\nВы священник.", color=mafia_color)
        elif player["role"] == "kitchener":
            embed = Embed(title="Пять лет в техническо-кулинарной шараге не прошли даром.\nВы повар)",
                          color=mafia_color)
        elif player["role"] == "DJ":
            embed = Embed(title="Диджей еблан...\nТун ту ту тун...\nВы диджей.", color=mafia_color)
        else:
            profession = choice(professions_clone)
            professions_clone.remove(profession)
            embed = Embed(title=f"Так как вы **мирный житель**!\nВы {profession}!", color=mafia_color)

        await player["player"].send(embed=embed)


async def main_game(channel):
    embed = Embed(title="🏙 Город просыпается")
    embed.set_image(url="https://truemafia.ru/sunrise.gif")
    await channel.send(embed=embed)

    embed = Embed(title="🌃 Город засыпет")
    embed.set_image(url="https://truemafia.ru/sunset.gif")
    await channel.send(embed=embed)
