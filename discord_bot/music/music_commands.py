from discord_bot.music.spotify_config import *
from discord import FFmpegPCMAudio

import tekore as tk
import yt_dlp


async def play_music(bot, message):
    track_url = "https://open.spotify.com/track/1AuvZZkmzlsArfACRNk97B?si=39a7cdf6d1d74c1a"
    if track_url[:31] == "https://open.spotify.com/track/":
        track_id = track_url[31:]
    else:
        track_id = ""

    spotify = tk.Spotify(tk.request_client_token(client_id, client_secret))
    track = spotify.track(track_id)

    text = "ytsearch:"

    for i in track.artists:
        text += f"{i.name}, "
    text = text[:-2]
    text += f" - {track.name}"

    ydl_opts = {'format': 'bestaudio/best'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(text, False)
        url_track = info["entries"][0]["formats"][3]["url"]

        channel = message.author.voice.channel
        # voice = get(bot.voice_clients, guild=message.guild)
        # if voice and voice.is_connected():
        #     await voice.move_to(channel)
        # else:
        #     voice = await channel.connect()
        voice = await channel.connect()
        op = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        # options -http_persistent 0
        # D:\ffmpeg\bin
        source = FFmpegPCMAudio(url_track, **op)
        player = voice.play(source)
