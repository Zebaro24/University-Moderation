from discord_bot.music.music_read import playlist
from discord import Embed, PartialEmoji
from dislash import Button, ActionRow
from discord_bot.main_discord import bot
from config import discord_guild, music_channel_id, music_colour
from config import music_button_colour as b_colour
from math import ceil
from asyncio import sleep

music_message = None


async def update_message():
    global music_message
    temple = 1
    while True:
        if bot.voice_clients:
            if temple == [playlist, bot.voice_clients[0].position]:
                await sleep(3)
                continue
            else:
                if bot.voice_clients:
                    temple = [playlist.copy(), bot.voice_clients[0].position]
        else:
            if temple == [playlist]:
                await sleep(3)
                continue
            else:
                temple = [playlist.copy()]

        if playlist:
            if bot.voice_clients:
                position = bot.voice_clients[0].position
            else:
                position = 0
            embed = Embed(title=f'{playlist[0]["name"]}',
                          description=f"{playlist[0]['artists']}\n\n"
                                      f"**{PartialEmoji(name='play', id=1001490575347962017)}"
                                      f"⠀{timeline(int(position), playlist[0]['time'])}"
                                      f"⠀{PartialEmoji(name='low', id=1001500402644156567)}**",
                          color=music_colour)
            embed.set_author(name="Музыка",
                             icon_url="https://www.iconsdb.com/icons/download/royal-blue/music-record-512.png")
            embed.set_thumbnail(url=playlist[0]["img"])

            num = 1
            if len(playlist[1:]) == 0:
                field_value = "Очередь пуста"
            else:
                field_value = ""

            for track in playlist[1:26]:
                field_value += f"{num}) {track['artists']} - {track['name']} - {time_text(track['time'])}\n"
                num += 1
            if len(playlist[1:]) > 25:
                field_value += "И остальные..."
            embed.add_field(name="Следующие в очереди:", value=field_value)

            bt_1 = Button(custom_id='music_play', emoji=PartialEmoji(name="play", id=1001490575347962017),
                          style=b_colour)
            bt_2 = Button(custom_id='music_pause', emoji=PartialEmoji(name="pause", id=1001487958739779715),
                          style=b_colour)
            bt_3 = Button(custom_id='music_skip', emoji=PartialEmoji(name="skip", id=1001490141543682078),
                          style=b_colour)
            bt_4 = Button(custom_id='music_mix', emoji=PartialEmoji(name="mix", id=1001490912037306469), style=b_colour)
            bt_5 = Button(custom_id='music_conn', emoji=PartialEmoji(name="conn", id=1001494112664551486),
                          style=b_colour)

            bt_6 = Button(custom_id='music_stop', emoji=PartialEmoji(name="stop", id=1001505894988791883),
                          style=b_colour)
            bt_7 = Button(custom_id='music_low', emoji=PartialEmoji(name="low", id=1001500402644156567), style=b_colour)
            bt_8 = Button(custom_id='music_med', emoji=PartialEmoji(name="med", id=1001507090050863154), style=b_colour)
            bt_9 = Button(custom_id='music_high', emoji=PartialEmoji(name="high", id=1001507394762838087),
                          style=b_colour)

            components = [ActionRow(bt_1, bt_2, bt_3, bt_4, bt_5),
                          ActionRow(bt_6, bt_7, bt_8, bt_9)]

        else:
            components = []
            embed = Embed(title="В плейлисте нет песен", color=music_colour)

        if music_message is None:
            music_channel = bot.get_guild(discord_guild).get_channel(music_channel_id)
            await music_channel.purge(limit=1000)
            music_message = await music_channel.send(embed=embed, components=components)
        else:
            await music_message.edit(embed=embed, components=components)

        await sleep(2)


def time_text(sec):
    minute, second = divmod(sec, 60)
    time_str = f"{minute}:{second:02d}"
    return time_str


def timeline(start, end):
    time_start = (ceil(start / end * 20) if start < end else 20) * "═"
    time_end = (20 - len(time_start)) * "─"
    return f"{time_text(start)} ╠{time_start}◉{time_end}╢ {time_text(end)}"
