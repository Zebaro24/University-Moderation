from config import mafia_players, mafia_color, mafia_channel_id, mafia_statistics, mafia_chat
from utils import print_ds
import config
from discord_bot.mafia.mafia_phrases import professions, random_roles
from discord_bot.mafia.mafia_menu import vote
import discord_bot.mafia.mafia_voice as mafia_voice
from random import shuffle, choices, choice
from discord import Embed
from asyncio import gather, sleep
import time
from dislash import SelectOption, SelectMenu, Button, ButtonStyle, ActionRow
from discord_bot.main_discord import bot
import discord_bot.mafia.mafia_start as mafia_start


async def distribution_of_roles():
    role = ["mafia", "peace", "peace", "doctor"]
    amount = len(mafia_players)

    if amount >= 5:
        role.append("sheriff")
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
    for i in mafia_players:
        player_role = choice(role)
        role.remove(player_role)
        mafia_players[i]["role"] = player_role
        if player_role == "sheriff":
            mafia_players[i]["text_role"] = ":police_officer: Шериф"
        elif player_role == "doctor":
            mafia_players[i]["text_role"] = ":health_worker: Доктор"
        elif player_role == "mafia":
            mafia_players[i]["text_role"] = ":detective: Мафия"
        elif player_role == "whore":
            mafia_players[i]["text_role"] = ":kiss: Шлюшка"
            mafia_players[i]["ability"] = False
        elif player_role == "fucker":
            mafia_players[i]["text_role"] = ":japanese_goblin: Ебанат"
        elif player_role == "priest":
            mafia_players[i]["text_role"] = ":man_mage: Священник"
            mafia_players[i]["ability"] = True
        elif player_role == "kitchener":
            mafia_players[i]["text_role"] = ":cook: Повар"
        elif player_role == "DJ":
            mafia_players[i]["text_role"] = ":robot: Диджей"
            mafia_players[i]["ability"] = False
        else:
            profession = choice(professions_clone)
            professions_clone.remove(profession)
            mafia_players[i]["profession"] = profession
            mafia_players[i]["text_role"] = f":adult: Мирный житель {profession}"

        print_ds(f"{i.name.ljust(10, ' ')}-{mafia_players[i]['text_role'].split(':')[2]}")

    before_time = time.perf_counter()
    all_send = []
    for player, information in mafia_players.items():
        if information["role"] == "mafia":
            embed = Embed(title="Вы являетесь опасной **мафией**!", color=mafia_color)
        elif information["role"] == "doctor":
            embed = Embed(title="Вы являетесь важной персоной!\nВы **доктор**!", color=mafia_color)
        elif information["role"] == "sheriff":
            embed = Embed(title="Вы являетесь важной персоной!\nВы **шериф**!", color=mafia_color)
        elif information["role"] == "whore":
            embed = Embed(title="Откуда у тебя этот айфон.\nТы грязная шлюха(без обид, такая жизнь))",
                          color=mafia_color)
        elif information["role"] == "fucker":
            embed = Embed(title="Знаешь откуда у меня эти шрамы?\nСкорее всего ты ебанат)", color=mafia_color)
        elif information["role"] == "priest":
            embed = Embed(title="А вы верите в бога?\nВы священник.", color=mafia_color)
        elif information["role"] == "kitchener":
            embed = Embed(title="Пять лет в техническо-кулинарной шараге не прошли даром.\nВы повар)",
                          color=mafia_color)
        elif information["role"] == "DJ":
            embed = Embed(title="Диджей ебан...\nТун ту ту ту тун...\nВы диджей.", color=mafia_color)
        else:
            embed = Embed(title=f"Так как вы **мирный житель**!\nВы {information['profession']}!", color=mafia_color)

        all_send.append(player.send(embed=embed))

    await gather(*all_send)
    print_ds(f"Время отправки ролей: {time.perf_counter() - before_time}")


count_days = 0
kill_people = {}
ghosts = {}

leave_players = []


async def main_game(channel):
    await first_meet(channel)
    while True:
        if return_ans := await day(channel):
            break
        await night(channel)
    await finish_game(channel, return_ans)


async def first_meet(channel):
    global count_days
    for player, information in mafia_players.items():
        if information["role"] == "priest":
            await player.send("Да будет бог с тобой.\nЯ верю в тебя, возроди одного в любую секунду...",
                              components=components_select("priest", "Выбери беднягу", skip=False))
        if information["role"] == "DJ":
            bt_1 = Button(custom_id='mafia_DJ_amogus', label='AMOGUS', style=ButtonStyle.red)
            bt_2 = Button(custom_id='mafia_DJ_dam', label='Плотину надо поднять', style=ButtonStyle.red)
            bt_3 = Button(custom_id='mafia_DJ_toilet', label='Я не умру в туалете', style=ButtonStyle.red)

            await player.send("Короче, надо тусануть днем...\nТолько один раз за день.",
                              components=[ActionRow(bt_1, bt_2, bt_3)])

    await mafia_voice.voice_change("day")
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
    await mafia_voice.voice_change("night")
    for player, information in mafia_players.items():
        if information["role"] == "mafia":
            await bot.get_channel(mafia_chat).set_permissions(player, read_messages=True)
    await bot.get_channel(mafia_chat).send("Чат был открыт!")
    await sleep(3)
    await channel.send(":stopwatch: На знакомство дается **20 секунд**. Время пошло...")
    await sleep(20)
    await channel.send(":stopwatch: Время вышло...")


async def day(channel):
    global count_days
    count_days += 1
    if kill_people:
        leave_players.clear()
        text = "К сожалению эта ночка была очень не спокойной!\nУмерли:\n"
        for player, information in kill_people.items():
            text += f"{player.mention}\n"  # text += f"{information['text_role']} - {player.mention}\n"
    else:
        text = "К счастью эта ночка была достаточно тихой, никто не умер."

    embed = Embed(title=f"🏙 **{count_days}** день", description=text, color=mafia_color)
    embed.set_image(url="https://truemafia.ru/sunrise.gif")
    await channel.send(embed=embed)
    await sleep(3)
    for player, information in kill_people.items():
        await mafia_voice.voice_change("last")
        if player.voice:
            await player.edit(mute=False)
        await channel.send(f"Последние слова: {player.mention}.\n"
                           f":stopwatch: Дается **10 секунд**. Время пошло...")
        await sleep(10)
        await channel.send(":stopwatch: Время вышло...")
    move_to("ghost")
    await mafia_voice.voice_change("day")

    win = win_game()
    if win:
        return win

    for player, information in mafia_players.items():
        if "DJ" in information["role"]:
            mafia_players[player]["ability"] = True

    await sleep_5(channel)

    for player, information in mafia_players.items():
        if "DJ" in information["role"]:
            mafia_players[player]["ability"] = False

    await mafia_voice.voice_change("night")
    vote("clear")
    await channel.send(":stopwatch: На голосование дается **20 секунд**. Время пошло...")

    await bot.get_channel(mafia_channel_id).send("Кого считаешь мафией?",
                                                 components=components_select("vote_kick", "Выбирай подозреваемого"),
                                                 delete_after=20)
    await sleep(20)
    await channel.send(":stopwatch: Время вышло...")
    await sleep(1)
    kill_person = vote('day')
    if kill_person and type(kill_person) != str:
        move_to("kill", kill_person)
        await mafia_voice.voice_change("last")
        if kill_person.voice:
            await kill_person.edit(mute=False)
        await channel.send(f"Последние слова: {kill_person.mention}.\n"
                           f":stopwatch: Дается **10 секунд**. Время пошло...")
        await sleep(10)
        await channel.send(":stopwatch: Время вышло...")
        await sleep(1)
        # await channel.send(f"А ведь этот человек был: {kill_people[kill_person]['text_role']}")
        move_to("ghost")
        win = win_game()
        if win:
            return win
    else:
        await channel.send(f"На эту ночь мафию решили оставить живой")

    await sleep(2)


async def night(channel):
    await mafia_voice.voice_change("night")
    embed = Embed(title="🌃 Город засыпает", description="Продается гараж.\nТут должна быть ваша реклама.",
                  color=mafia_color)
    embed.set_image(url="https://truemafia.ru/sunset.gif")
    await channel.send(embed=embed)
    await sleep(2)
    vote("clear")
    await channel.send("Нечисть выходит на охоту...\nШериф и доктор чувствуют что-то не ладное...")
    await channel.send(":stopwatch: Время на все про все дается **30 секунд**. Время пошло...")

    await bot.get_channel(mafia_chat).send("Кого хочешь убить?",
                                           components=components_select("mafia", "Выбирай кого не жалко", "mafia",
                                                                        False), delete_after=30)
    for player, information in mafia_players.items():
        if information["role"] == "doctor":
            await player.send("Мне кажется, кого-то хотят убить.\nЗа кем будешь дежурить?",
                              components=components_select("doctor", "Выбирай гражданина", skip=False),
                              delete_after=30)
        elif information["role"] == "sheriff":
            await player.send("Среди нас есть предатель.\nДавай за кем-то проследим.",
                              components=components_select("sheriff", "Выбирай гражданина", "sheriff", False),
                              delete_after=30)
        elif information["role"] == "whore" and not count_days % 2:
            mafia_players[player]["ability"] = True
            await player.send("Кому хочешь сделать приятно?",
                              components=components_select("whore", "Выбирай сладость", "whore", False),
                              delete_after=30)
        elif information["role"] == "fucker":
            await player.send("Кого хочешь йобнуть?",
                              components=components_select("fucker", "Выбирай стерву", "fucker", False),
                              delete_after=30)
        elif information["role"] == "kitchener":
            await player.send("Кого хочешь накормить своими булочками)?",
                              components=components_select("kitchener", "Выбирай сыночка", "kitchener", False),
                              delete_after=30)

    await sleep(30)
    await channel.send(":stopwatch: Время вышло...")

    vote_sherif = vote("sheriff")
    if vote_sherif:
        sheriff = None
        check_player_role = None
        for player, information in mafia_players.items():
            if information["role"] == "sheriff":
                sheriff = player
            elif player == vote_sherif:
                check_player_role = information["text_role"]
        await sheriff.send(f"{vote_sherif.mention} - является: {check_player_role}")

    if (player := vote("mafia")) in mafia_players:
        move_to("kill", player)
    if (player := vote("fucker")) in mafia_players:
        move_to("kill", player)
    if (player := vote("kitchener")) in mafia_players | kill_people:
        await channel.send("Похоже, этой ночью, кого-то хорошо накормили!")
        if choices(["good", "bed"], [2, 1])[0] == "good":
            if player in kill_people:
                move_to("threat", player)
        else:
            if player in mafia_players:
                move_to("kill", player)
    if (player := vote("doctor")) in kill_people:
        move_to("treat", player)
    if (player := vote("whore")) in mafia_players and True in [i["ability"] for i in mafia_players.values() if
                                                               i["role"] == "whore"]:
        mafia_players[player]["whore"] = True
        for player, information in mafia_players.items():
            if information["role"] == "whore":
                mafia_players[player]["ability"] = False

    vote("clear")

    await sleep(2)


async def finish_game(channel, ans):
    global count_days
    print_ds(ans)
    await mafia_voice.voice_change()
    channel_statistics = bot.get_channel(mafia_statistics)
    try:
        number = int((await channel_statistics.history(limit=1).flatten())[0].embeds[0].title.split("**")[1])
    except IndexError:
        number = 0

    description = "**Остались в живих:**\n"
    if not mafia_players:
        description += "Живих не осталось!\n"
    for player, information in mafia_players.items():
        description += f"{player.mention} - {information['text_role']}\n"

    description += "\n**Умерли:**\n"
    for player, information in ghosts.items():
        description += f"{player.mention} - {information['text_role']}\n"

    embed_statistics = Embed(title=f"Игра номер: **{number + 1}**\n{ans}\nКоличество дней: {count_days}",
                             description=description, color=mafia_color)

    for player, information in (mafia_players | kill_people | ghosts).items():
        if information["role"] == "mafia":
            await bot.get_channel(mafia_chat).set_permissions(player, overwrite=None)
    await bot.get_channel(mafia_chat).purge(limit=10000)

    count_days = 0
    mafia_players.clear()
    kill_people.clear()
    ghosts.clear()
    leave_players.clear()
    await channel_statistics.send(embed=embed_statistics)
    await channel.send(ans)
    await channel.send("Следующая игра будет доступна через 30 секунд...")
    await sleep(30)
    await mafia_start.mafia_start(bot.get_channel(mafia_channel_id))


def components_select(custom_id, description, skip_role=None, skip=True):
    options = []
    for player, information in mafia_players.items():
        if information["role"] != skip_role:
            options.append(SelectOption(label=player.name, value=player.id, emoji="👤"))

    if skip:
        options.append(SelectOption(label="Скипнуть...", value="skip", emoji="🚫"))

    return [SelectMenu(custom_id=custom_id, placeholder=description, options=options)]


async def sleep_5(channel, text="обсуждения"):
    if not config.debug:
        await channel.send(f":stopwatch: Вам дается **30 секунд** на {text}. Время пошло...")
        await sleep(20)
        await channel.send(":stopwatch: Осталась **10 секунд**...")
        await sleep(10)
        await channel.send(":stopwatch: Время вышло...")
        await sleep(1)
    else:
        await channel.send(":stopwatch: Debug 30 сек...")
        await sleep(30)
        await channel.send(":stopwatch: Время вышло...")
        await sleep(1)


def move_to(where, who=None):
    if where == "kill" and who:
        kill_people[who] = mafia_players[who]
        del mafia_players[who]
    elif where == "treat" and who:
        mafia_players[who] = kill_people[who]
        del kill_people[who]
    elif where == "ghost":
        for player, information in kill_people.items():
            ghosts[player] = information
        kill_people.clear()

    elif where == "leave" and who:
        leave_players.append(who)
        kill_people[who] = mafia_players[who]
        del mafia_players[who]
    elif where == "join" and who:
        leave_players.remove(who)
        mafia_players[who] = kill_people[who]
        del leave_players[who]


def win_game():
    mafia = 0
    fucker = 0
    peace = 0

    for i in mafia_players.values():
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
