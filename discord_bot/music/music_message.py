from config import discord_guild, music_channel_id, music_colour, music_button_colour as b_colour
from discord_bot.main_discord import bot
from discord_bot.music.music_read import playlist, details_player

from discord import Embed, PartialEmoji
from dislash import Button, ActionRow

from datetime import timedelta, datetime
from asyncio import sleep
from math import ceil

music_message = None


async def update_message():
    global music_message
    temple = 1
    while True:
        if temple == [playlist, show_detail("position"), details_player]:
            await sleep(3)
            continue
        else:
            temple = [playlist.copy(), show_detail("position"), details_player.copy()]

        if playlist:
            embed = Embed(title=f'{playlist[0]["name"]}',
                          description=f"{playlist[0]['artists']}\n\n"
                                      f"**{show_detail('status')}"
                                      f"⠀{timeline(show_detail('position'), playlist[0]['time'])}"
                                      f"⠀{show_detail('volume')}**",
                          color=music_colour)
            embed.set_author(name="Музыка",
                             icon_url="https://www.iconsdb.com/icons/download/royal-blue/music-record-512.png")
            embed.set_thumbnail(url=playlist[0]["img"])

            if len(playlist[1:]) == 0:
                field_value = "Очередь пуста"
            else:
                field_value = ""

            num = 1
            for track in playlist[1:]:
                add_value = f"{num}) {track['artists']} - {track['name']} - {time_text(track['time'])}\n"
                if len(field_value + add_value + "И остальные...") > 1024:
                    field_value += "И остальные..."
                    break
                field_value += add_value
                num += 1

            embed.add_field(name="Следующие в очереди:", value=field_value)

            if details_player["status"] == "pause":
                bt_1 = Button(custom_id='music_play', emoji=PartialEmoji(name="play", id=1001490575347962017),
                              style=b_colour)
            else:
                bt_1 = Button(custom_id='music_pause', emoji=PartialEmoji(name="pause", id=1001487958739779715),
                              style=b_colour)
            bt_2 = Button(custom_id='music_skip', emoji=PartialEmoji(name="skip", id=1001490141543682078),
                          style=b_colour)
            bt_3 = Button(custom_id='music_shuffle', emoji=PartialEmoji(name="shuffle", id=1001490912037306469),
                          style=b_colour)
            bt_4 = Button(custom_id='music_conn', emoji=PartialEmoji(name="conn", id=1001494112664551486),
                          style=b_colour)

            bt_5 = Button(custom_id='music_stop', emoji=PartialEmoji(name="stop", id=1001505894988791883),
                          style=b_colour)
            bt_6 = Button(custom_id='music_low', emoji=PartialEmoji(name="low", id=1001500402644156567), style=b_colour)
            bt_7 = Button(custom_id='music_med', emoji=PartialEmoji(name="med", id=1001507090050863154), style=b_colour)
            bt_8 = Button(custom_id='music_high', emoji=PartialEmoji(name="high", id=1001507394762838087),
                          style=b_colour)

            components = [ActionRow(bt_1, bt_2, bt_3, bt_4),
                          ActionRow(bt_5, bt_6, bt_7, bt_8)]

        else:
            components = []
            embed = Embed(title="🚫 В плейлисте нет песен", color=music_colour)

        if music_message and music_message.created_at + timedelta(hours=1) < datetime.utcnow():
            await music_message.delete()
            music_message = None

        if music_message is None:
            message_or = await check_message()
            if message_or:
                music_message = message_or
            else:
                music_channel = bot.get_guild(discord_guild).get_channel(music_channel_id)
                await music_channel.purge(limit=1000)
                music_message = await music_channel.send(embed=embed, components=components)
        else:
            await music_message.edit(embed=embed, components=components)

        await sleep(1)


async def check_message():
    message_list = await bot.get_guild(discord_guild).get_channel(music_channel_id).history(limit=1).flatten()
    if len(message_list) == 1:
        if len(message_list[0].embeds) >= 1:
            if message_list[0].embeds[0].title == "🚫 В плейлисте нет песен":
                return message_list[0]
    return None


def time_text(sec):
    minute, second = divmod(sec, 60)
    time_str = f"{minute}:{second:02d}"
    return time_str


def timeline(start, end):
    time_start = (ceil(start / end * 20) if start < end else 20) * "═"
    time_end = (20 - len(time_start)) * "─"
    return f"`{time_text(start)}` ╠{time_start}◉{time_end}╢ `{time_text(end)}`"


def show_detail(choice):
    if choice == "status":
        if details_player["status"] == "play":
            return PartialEmoji(name='play', id=1001490575347962017)
        elif details_player["status"] == "pause":
            return PartialEmoji(name="pause", id=1001487958739779715)

    elif choice == "volume":
        if details_player["volume"] == "low":
            return PartialEmoji(name="low", id=1001500402644156567)
        elif details_player["volume"] == "med":
            return PartialEmoji(name="med", id=1001507090050863154)
        elif details_player["volume"] == "high":
            return PartialEmoji(name="high", id=1001507394762838087)

    elif choice == "position":
        vc = bot.voice_clients
        if vc:
            return int(vc[0].position)
        else:
            return 0
