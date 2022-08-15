from config import mafia_players, mafia_color, discord_guild, mafia_channel_id
from utils import print_ds
import config
from discord_bot.mafia.mafia_phrases import professions, random_roles
from discord_bot.mafia.mafia_menu import vote, vote_dict
from random import shuffle, choices, choice
from discord import Embed
from asyncio import gather, sleep
import time
from dislash import SelectOption, SelectMenu
from discord_bot.main_discord import bot


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

    professions_clone = professions.copy()
    for i in range(amount):
        mafia_players[i]["role"] = role[i]
        if role[i] == "sheriff":
            mafia_players[i]["text_role"] = ":police_officer: Шериф"
        elif role[i] == "doctor":
            mafia_players[i]["text_role"] = ":health_worker: Доктор"
        elif role[i] == "mafia":
            mafia_players[i]["text_role"] = ":detective: Мафия"
        elif role[i] == "whore":
            mafia_players[i]["text_role"] = ":kiss: Шлюшка"
        elif role[i] == "fucker":
            mafia_players[i]["text_role"] = ":japanese_goblin: Ебанат"
        elif role[i] == "priest":
            mafia_players[i]["text_role"] = ":man_mage: Священник"
        elif role[i] == "kitchener":
            mafia_players[i]["text_role"] = ":cook: Повар"
        elif role[i] == "DJ":
            mafia_players[i]["text_role"] = ":robot: Диджей"
        else:
            profession = choice(professions_clone)
            professions_clone.remove(profession)
            mafia_players[i]["profession"] = profession
            mafia_players[i]["text_role"] = f":adult: Мирный житель {profession}"

        print_mafia = mafia_players[i].copy()
        print_mafia["player"] = print_mafia["player"].name
        print_ds(f"{mafia_players[i]['player'].name.ljust(10, ' ')}-{mafia_players[i]['text_role'].split(':')[2]}")

    before_time = time.perf_counter()
    all_send = []
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
            embed = Embed(title="Диджей ебан...\nТун ту ту ту тун...\nВы диджей.", color=mafia_color)
        else:
            embed = Embed(title=f"Так как вы **мирный житель**!\nВы {player['profession']}!", color=mafia_color)

        all_send.append(player["player"].send(embed=embed))

    await gather(*all_send)
    print_ds(f"Время отправки ролей: {time.perf_counter() - before_time}")


count_days = 0
kill_people = []
ghosts = []


async def main_game(channel):
    await first_meet(channel)
    while True:
        if await day(channel):
            break
        await night(channel)
    await finish_game(channel)


async def first_meet(channel):
    global count_days
    count_days += 1
    embed = Embed(title="🏙 Это ваш первый день",
                  description="Во время первого дня вы знакомитесь между собой.\n"
                              "Не забывайте отыгрывать РП!\n",
                  color=mafia_color)
    await channel.send(embed=embed)
    await sleep(3)
    await sleep_5(channel, "знакомства")
    embed = Embed(title="🏙 Наступает ночь",
                  description="Во время первой ночи мафия знакомится между собой.\n"
                              "У мафии открывается чат для общения.",
                  color=mafia_color)
    embed.set_image(url="https://truemafia.ru/sunset.gif")
    await channel.send(embed=embed)
    await sleep(3)
    await channel.send(":stopwatch: На знакомство дается **20 секунд**. Время пошло...")
    await sleep(20)
    await channel.send(":stopwatch: Время вышло...")


async def day(channel):
    global count_days
    count_days += 1
    if kill_people:
        text = "К сожалению эта ночка была очень не спокойной!\nУмерли:\n"
        for i in kill_people:
            text += f"{i['text_role']} - {i['player'].mention}\n"
    else:
        text = "К счастью эта ночка была достаточно тихой, никто не умер."

    embed = Embed(title=f"🏙 **{count_days}** день", description=text, color=mafia_color)
    embed.set_image(url="https://truemafia.ru/sunrise.gif")
    await channel.send(embed=embed)
    await sleep(3)
    for i in kill_people:
        await channel.send(f"Последние слова: {i['player'].mention}.\n"
                           f":stopwatch: Дается **10 секунд**. Время пошло...")
        await sleep(10)
        await channel.send(":stopwatch: Время вышло...")
        ghosts.append(i)
    kill_people.clear()

    win = win_game()
    if win:
        return win

    await sleep_5(channel)

    vote("clear")
    await channel.send(":stopwatch: На голосование дается **20 секунд**. Время пошло...")

    await bot.get_guild(discord_guild).get_channel(mafia_channel_id).send("Кого считаешь мафией?",
                                                                          components=components_select("vote_kick",
                                                                                                       "Выбирай подозреваемого"),
                                                                          delete_after=20)
    await sleep(20)
    await channel.send(":stopwatch: Время вышло...")
    await sleep(1)
    kill_person = vote('day')
    if kill_person:
        move_to("kill", kill_person)
        await channel.send(f"Последние слова: {kill_person.mention}.\n"
                           f":stopwatch: Дается **10 секунд**. Время пошло...")
        await sleep(10)
        await channel.send(":stopwatch: Время вышло...")
        await sleep(1)
        await channel.send(f"А ведь этот человек был: {kill_people[0]['text_role']}")
        move_to("ghost")
        win = win_game()
        if win:
            return win
    else:
        await channel.send(f"На эту ночь мафию решили оставить живой")

    await sleep(2)


async def night(channel):
    embed = Embed(title="🌃 Город засыпает", description="Продается гараж.\nТут должна быть ваша реклама.",
                  color=mafia_color)
    embed.set_image(url="https://truemafia.ru/sunset.gif")
    await channel.send(embed=embed)
    await sleep(2)
    vote("clean")
    await channel.send("Нечисть выходит на охоту...\nШериф и доктор чувствуют что-то не ладное...")
    await channel.send(":stopwatch: Время на все про все дается **30 секунд**. Время пошло...")

    for plyer in mafia_players:
        if plyer["role"] == "mafia":
            await plyer["player"].send("Кого хочешь убить?",
                                       components=components_select("mafia", "Выбирай кого не жалко", "mafia",
                                                                    False), delete_after=30)
        elif plyer["role"] == "doctor":
            await plyer["player"].send("Мне кажется, кого-то хотят убить.\nЗа кем будешь дежурить?",
                                       components=components_select("doctor", "Выбирай гражданина", skip=False),
                                       delete_after=30)
        elif plyer["role"] == "sheriff":
            await plyer["player"].send("Среди нас есть предатель.\nДавай за кем-то проследим.",
                                       components=components_select("sheriff", "Выбирай гражданина", "sheriff",
                                                                    False), delete_after=30)
        elif plyer["role"] == "whore":
            await plyer["player"].send("Кому хочешь сделать приятно?",
                                       components=components_select("whore", "Выбирай сладость", "whore",
                                                                    False), delete_after=30)
        elif plyer["role"] == "fucker":
            await plyer["player"].send("Кого хочешь йобнуть?",
                                       components=components_select("fucker", "Выбирай стерву", "fucker",
                                                                    False), delete_after=30)
        elif plyer["role"] == "kitchener":
            await plyer["player"].send("Кого хочешь накормить своими булочками)?",
                                       components=components_select("kitchener", "Выбирай сыночка", "kitchener",
                                                                    False), delete_after=30)

    await sleep(30)
    await channel.send(":stopwatch: Время вышло...")

    print(vote_dict)
    vote_sherif = vote("sheriff")
    if vote_sherif:
        sheriff = None
        check_player_role = None
        for i in mafia_players:
            if i["role"] == "sheriff":
                sheriff = i["player"]
            elif i["player"] == vote_sherif:
                check_player_role = i["text_role"]
        await sheriff.send(f"{vote_sherif.mention} - является: {check_player_role}")
    move_to("kill", vote("mafia"))
    move_to("kill", vote("fucker"))
    move_to("treat", vote("doctor"))
    # whore - Не забыть сделать!!!
    # kitchener - Не забыть сделать!!!
    vote("clear")

    await sleep(2)


async def finish_game(channel):
    await channel.send("Вы победили")


def components_select(custom_id, description, skip_role=None, skip=True):
    options = []
    num = 0
    for player in mafia_players:
        if player["role"] != skip_role:
            if config.debug:
                options.append(SelectOption(label=player['player'].name, value=f"player_{num}", emoji="👤"))
                num += 1
            else:
                options.append(SelectOption(label=player['player'].name, value=str(player['player'].id), emoji="👤"))

    if skip:
        options.append(SelectOption(label="Скипнуть...", value="skip", emoji="🚫"))

    return [SelectMenu(custom_id=custom_id, placeholder=description, options=options)]


async def sleep_5(channel, text="обсуждения"):
    if not True:
        await channel.send(f":stopwatch: Вам дается **5 минут** на {text}. Время пошло...")
        await sleep(240)
        await channel.send(":stopwatch: Осталась **1 минута**...")
        await sleep(50)
        await channel.send(":stopwatch: Осталась **10 секунд**...")
        await sleep(10)
        await channel.send(":stopwatch: Время вышло...")
        await sleep(1)
    else:
        await channel.send(":stopwatch: Скипаем 5 мин...")


def move_to(where, who=None):
    if where == "kill" and who:
        for i in mafia_players:
            if who == i["player"]:
                kill_people.append(i)
                mafia_players.remove(i)
    elif where == "treat" and who:
        for i in kill_people:
            if who == i["player"]:
                kill_people.remove(i)
                mafia_players.append(i)
    elif where == "ghost":
        for i in kill_people:
            ghosts.append(i)
            kill_people.remove(i)


def win_game():
    mafia = 0
    fucker = 0
    peace = 0

    for i in mafia_players:
        if i["role"] == "mafia":
            mafia += 1
        elif i["role"] == "fucker":
            fucker += 1
        else:
            peace += 1

    if mafia >= peace + fucker:  # Мафия выиграла
        return "Мафия победила в честном бою"
    elif fucker == 1 and peace == 1:  # Тот самый выиграл
        return "Ебанат победил"
    elif fucker == 1 and mafia == 1 and peace == 0:  # Ничья между злыми силами
        return "Ничья между ебанатом и мафией"
    elif mafia == 0 and fucker == 0:  # Выиграли мирные
        return "Выиграли мирные жители"
