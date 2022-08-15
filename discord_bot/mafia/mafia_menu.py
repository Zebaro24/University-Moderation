from discord_bot.main_discord import bot
from dislash import MessageInteraction
from config import mafia_players

vote_dict = {}


@bot.event
async def on_dropdown(inter: MessageInteraction):
    # print(inter.select_menu.custom_id)
    # print(inter.select_menu.selected_options[0].value)
    # print(inter.author)
    if inter.author not in [i["player"] for i in mafia_players]:
        print(f"Проголосовал человек который не участвует в игре: {inter.author}")
        return
    try:
        if inter.select_menu.selected_options[0].value == "skip":
            index = "skip"
        else:
            index = [i["player"].id for i in mafia_players].index(int(inter.select_menu.selected_options[0].value))
    except ValueError:
        print("Скорее всего ошибка, или нажато не в том меню")
        return

    author_role = None
    for i in mafia_players:
        if i["player"] == inter.author:
            author_role = i["role"]

    if index == "skip":
        await inter.reply(f"{inter.author.mention} - решил скипнуть голосование")
    elif inter.select_menu.custom_id == "vote_kick":
        await inter.reply(f"{inter.author.mention} - проголосовал за: {mafia_players[index]['player'].mention}")
        vote("day", inter.author, mafia_players[index]["player"])
    elif inter.select_menu.custom_id == "mafia":
        await inter.reply(f"{inter.author.mention} - проголосовал за: {mafia_players[index]['player'].mention}")
        vote("mafia", inter.author, mafia_players[index]["player"])
    elif author_role == inter.select_menu.custom_id:
        await inter.reply(f"Вы выбрали: {mafia_players[index]['player'].mention}")
        vote(author_role, inter.author, mafia_players[index]["player"])


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
