from config import client_id, client_secret, music_channel_id, discord_guild
from config import discord_guild, music_channel_id
from discord import Embed, colour
from discord_bot.main_discord import bot
from dislash import ActionRow, Button, ButtonStyle
from asyncio import run_coroutine_threadsafe
import tekore as tk
import datetime, time
from math import ceil
from threading import Thread
from datetime import timedelta
import yt_dlp

music_message = None
playlist = []
spotify = tk.Spotify(tk.request_client_token(client_id, client_secret))
gg = 1


async def update_message():
    global music_message
    # time_now = time.perf_counter()
    if playlist:
        embed = Embed(title=f'{playlist[0]["name"]}',
                      description=f"{playlist[0]['artists']}\n\n"
                                  f"**▶   0:0{gg}  ╠═══◉─────────────────────╢  {track_time(playlist[0]['time'])}**",
                      color=colour.Color.blurple())
        embed.set_author(name="Музыка",
                         icon_url="https://toppng.com/uploads/preview/light-blue-music-note-icon-ok-icon-material-design-11553494358cjw8lo837o.png")
        embed.set_thumbnail(url=playlist[0]["img"])

        num = 1
        if len(playlist[1:]) == 0:
            field_value = "Очередь пуста"
        else:
            field_value = ""

        for track in playlist[1:26]:
            field_value += f"{num}) {track['artists']} - {track['name']} - {track_time(track['time'])}\n"
            num += 1
        if len(playlist[1:]) > 25:
            field_value += "И остальные..."
        embed.add_field(name="Следующие в очереди:", value=field_value)

        bt_1 = Button(custom_id='mafia_join', emoji="▶", style=ButtonStyle.blurple)
        bt_3 = Button(custom_id='mafia_info', label='Правила', style=ButtonStyle.green)
        bt_4 = Button(custom_id='mafia_info1', label='Правила', style=ButtonStyle.blurple)
        bt_5 = Button(custom_id='mafia_info2', label='Правила', style=ButtonStyle.danger)
        bt_6 = Button(custom_id='mafia_info3', label='Правила', style=ButtonStyle.primary)
        bt_7 = Button(custom_id='mafia_info4', label='Правила', style=ButtonStyle.secondary)
        bt_8 = Button(custom_id='mafia_info5', label='Правила', style=ButtonStyle.success)

        components = [ActionRow(bt_1, bt_3, bt_4, bt_5, bt_6)]

    else:
        components = []
        embed = Embed(title="В плейлисте нет песен", color=colour.Color.green())
    # print(f"Время обработки: {float(time.perf_counter() - time_now)}")
    if music_message is None:
        music_channel = bot.get_guild(discord_guild).get_channel(music_channel_id)
        await music_channel.purge(limit=1000)
        music_message = await music_channel.send(embed=Embed(title="Загрузка...", color=colour.Color.dark_blue()))

    await music_message.edit(embed=embed, components=components)


def read_spotify(url):
    if url[:31] == "https://open.spotify.com/track/":
        track_id = url[31:]
        spotify_playlist = [spotify.track(track_id)]
    elif url[:34] == "https://open.spotify.com/playlist/":
        playlist_id = url[34:]
        items = spotify.playlist(playlist_id).tracks.items
        spotify_playlist = [i.track for i in items]
    else:
        spotify_playlist = []

    for track in spotify_playlist:
        artists = ""
        for i in track.artists:
            artists += f"{i.name}, "
        artists = artists[:-2]

        track_for_playlist = {"name": track.name,
                              "artists": artists,
                              "time": ceil(track.duration_ms / 1000),
                              "img": track.album.images[0].url,
                              "streem": None}
        playlist.append(track_for_playlist)


def read_youtube():
    pass


def streem_youtube():
    pass


async def while_music():
    time.sleep(5)
    while True:
        good_time = time.perf_counter()
        time_now = time.perf_counter()

        await update_message()
        print(time.perf_counter() - time_now)
        time.sleep(3)
        print(f"Общее: {time.perf_counter() - good_time}")


def track_time(sec):
    minute, second = divmod(sec, 60)
    time_str = f"{minute}:{second:02d}"
    return time_str
