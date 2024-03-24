from ...config import mafia_voice_channel_id, mafia_players
from ..main_discord import bot
from .. import voice_actions
from .mafia_global import move_to, leave_players, ghosts, kill_people

from discord import Member, VoiceState, VoiceChannel

from asyncio import gather


async def mafia_game(member: Member, before: VoiceState, after: VoiceState):
    if member in mafia_players or member in leave_players:
        if before == after:
            return
        elif after.channel:
            if member in leave_players:
                move_to("join", member)
                await member.send(
                    "Хух успел...\n"
                    "Больше так не делай!")
            if after.channel.id != mafia_voice_channel_id:
                await member.send("Нельзя менять канал во  время игры!")
                vc = bot.get_channel(mafia_voice_channel_id)
                await member.edit(voice_channel=vc)
        else:
            move_to("leave", member)
            await member.send("У вас есть время перезайти в голосовой канал до разглашения мертвых или предателей!\n"
                              "Если не успеете зайти то вы будете считаться мертвым!")
    elif after.channel == bot.get_channel(mafia_voice_channel_id):
        if before.channel != after.channel:
            await voice_actions.voice_save(member)
            await voice_change_member(member)
        else:
            return True
    elif before.channel == bot.get_channel(mafia_voice_channel_id):
        if before.channel != after.channel:
            await voice_actions.voice_return(member)


global_period = None
whore = False


def period_voice():
    global whore
    if global_period == "day":
        player = {"mute": False, "deaf": False}
        ghost = {"mute": True, "deaf": False}
    elif global_period == "night":
        if whore:
            for player, information in mafia_players.items():
                if "whore" in information:
                    del mafia_players[player]["whore"]
            whore = False
        player = {"mute": False, "deaf": True}
        ghost = {"mute": False, "deaf": False}
    elif global_period == "last":
        player = {"mute": True, "deaf": False}
        ghost = {"mute": True, "deaf": False}
    else:
        player = {"mute": False, "deaf": False}
        ghost = {"mute": False, "deaf": False}
    return {"player": player, "ghost": ghost}


async def voice_change(period=None):
    global global_period, whore
    global_period = period
    all_do = []
    who_period = period_voice()

    channel: VoiceChannel = bot.get_channel(mafia_voice_channel_id)

    for member in channel.members:
        if member in mafia_players and "whore" in mafia_players[member]:
            whore = True
            all_do.append(member.edit(mute=who_period["ghost"]["mute"], deafen=who_period["ghost"]["deaf"]))
        elif member in mafia_players | kill_people:
            all_do.append(member.edit(mute=who_period["player"]["mute"], deafen=who_period["player"]["deaf"]))
        elif member in ghosts:
            all_do.append(member.edit(mute=who_period["ghost"]["mute"], deafen=who_period["ghost"]["deaf"]))
        else:
            all_do.append(member.edit(mute=who_period["ghost"]["mute"], deafen=who_period["ghost"]["deaf"]))

    await gather(*all_do)


async def voice_change_member(member):
    global whore
    who_period = period_voice()

    if member in mafia_players and "whore" in mafia_players[member]:
        whore = True
        member.edit(mute=who_period["ghost"]["mute"], deafen=who_period["ghost"]["deaf"])
    elif member in mafia_players | kill_people:
        await member.edit(mute=who_period["player"]["mute"], deafen=who_period["player"]["deaf"])
    elif member in ghosts:
        await member.edit(mute=who_period["ghost"]["mute"], deafen=who_period["ghost"]["deaf"])
    else:
        await member.edit(mute=who_period["ghost"]["mute"], deafen=who_period["ghost"]["deaf"])
