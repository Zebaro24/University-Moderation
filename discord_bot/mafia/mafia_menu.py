from discord_bot.main_discord import bot
from dislash import MessageInteraction
from config import mafia_players

vote_dict = {}


@bot.event
async def on_dropdown(inter: MessageInteraction):
    # print(inter.select_menu.custom_id)
    # print(inter.select_menu.selected_options[0].value)
    # print(inter.author)

    try:
        if inter.select_menu.selected_options[0].value == "skip":
            index = "skip"
        else:
            index = [i["player"].id for i in mafia_players].index(int(inter.select_menu.selected_options[0].value))
    except ValueError:
        print("Скорее всего ошибка, или нажато после игры")
        return

    if inter.select_menu.custom_id == "vote_kick":
        await inter.reply(f"{inter.author.mention} - проголосовал за: {mafia_players[index]['player'].mention}")
        vote("day", inter.author, mafia_players[index]["player"])
    elif inter.select_menu.custom_id == "mafia":
        pass
    elif inter.select_menu.custom_id == "doctor":
        pass
    elif inter.select_menu.custom_id == "sheriff":
        pass
    elif inter.select_menu.custom_id == "whore":
        pass
    elif inter.select_menu.custom_id == "fucker":
        pass
    elif inter.select_menu.custom_id == "kitchener":
        pass


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
