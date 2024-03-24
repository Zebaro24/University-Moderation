from ...config import mafia_players
from ...utils import print_ds
from . import mafia_global
from . import mafia_voice

from dislash import MessageInteraction

vote_dict = {}


async def mafia_select(inter: MessageInteraction):
    # print(custom_id)
    # print(inter.select_menu.selected_options[0].value)
    # print(inter.author)
    custom_id = inter.select_menu.custom_id.split("_")[1]
    if inter.author not in mafia_players:
        print_ds(f"Проголосовал человек который не участвует в игре: {inter.author}")
        return

    if custom_id == "priest":
        if inter.author in mafia_players and mafia_players[inter.author]["role"] == "priest" and \
                mafia_players[inter.author]["ability"]:
            await inter.send("Так, посмотрим кого на кого выбор пал...")
        elif inter.author in mafia_global.kill_people and mafia_global.kill_people[inter.author]["role"] == "priest" and \
                mafia_global.kill_people[inter.author]["ability"]:
            await inter.send("Ану ка глянем, а ты на волоске от смерти оказывается...")
        elif inter.author in mafia_global.ghosts and mafia_global.ghosts[inter.author]["role"] == "priest" and \
                mafia_global.ghosts[inter.author]["ability"]:
            await inter.send("Выбор твой, надеюсь ты выбрал себя, посмотрим...")
        else:
            await inter.send("Возможность давалась лишь на одну жизнь!")
            return

        choice_player = None
        if int(inter.select_menu.selected_options[0].value) in [i.id for i in mafia_players]:
            await inter.send("Ты выбрал живую особь.\n"
                             "Не спеши, выбери розумно!")
            return

        elif int(inter.select_menu.selected_options[0].value) in [i.id for i in mafia_global.kill_people]:
            await inter.send("Откуда ты узнал, да будет исполнено.")
            for player in mafia_global.kill_people:
                if player.id == int(inter.select_menu.selected_options[0].value):
                    choice_player = player
                    break

        elif int(inter.select_menu.selected_options[0].value) in [i.id for i in mafia_global.ghosts]:
            await inter.send("Да будет исполнено, выбор только за тобой.")
            for player in mafia_global.ghosts:
                if player.id == int(inter.select_menu.selected_options[0].value):
                    choice_player = player
                    break

        else:
            await inter.send("Он находится за гранью, это не возможного.")
            return

        if inter.author in mafia_players:
            mafia_players[inter.author]["ability"] = False
        elif inter.author in mafia_global.kill_people:
            mafia_global.kill_people[inter.author]["ability"] = False
        elif inter.author in mafia_global.ghosts:
            mafia_global.ghosts[inter.author]["ability"] = False

        if choice_player in mafia_global.kill_people:
            mafia_global.move_to("treat", choice_player)
        elif choice_player in mafia_global.ghosts:
            mafia_players[choice_player] = mafia_global.ghosts[choice_player]
            del mafia_global.ghosts[choice_player]
        await mafia_voice.voice_change_member(choice_player)
        await inter.message.delete()

        return

    try:
        if inter.select_menu.selected_options[0].value == "skip":
            index = "skip"
        else:
            index = "skip"
            for player in mafia_players:
                if player.id == int(inter.select_menu.selected_options[0].value):
                    index = player
    except ValueError:
        print_ds("Скорее всего ошибка, или нажато не в том меню")
        return

    author_role = mafia_players[inter.author]["role"]

    if custom_id == "vote_kick":
        if index == "skip":
            await inter.reply(f"{inter.author.mention} - решил скипнуть голосование")
        else:
            await inter.reply(f"{inter.author.mention} - проголосовал за: {index.mention}")
        vote("day", inter.author, index)
    elif custom_id == "mafia":
        await inter.reply(f"{inter.author.mention} - проголосовал за: {index.mention}")
        vote("mafia", inter.author, index)
    elif author_role == custom_id:
        await inter.reply(f"Вы выбрали: {index.mention}")
        vote(author_role, inter.author, index)


def vote(custom_id, author=None, vote_to=None):
    if custom_id == "clear":
        vote_dict.clear()
    elif author and vote_to:
        if custom_id not in vote_dict.keys():
            vote_dict[custom_id] = {}

        vote_dict[custom_id][author] = vote_to
    elif custom_id in vote_dict:  # Finish vote
        all_vote = {}
        for i in vote_dict[custom_id].values():
            if i in all_vote.keys():
                all_vote[i] += 1
            else:
                all_vote[i] = 1

        del vote_dict[custom_id]

        max_value = max(all_vote.values())

        if list(all_vote.values()).count(max_value) == 1:
            return list(all_vote.keys())[list(all_vote.values()).index(max_value)]
