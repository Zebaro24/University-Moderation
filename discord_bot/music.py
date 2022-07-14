import discord
from discord.utils import get
import tekore as tk
import yt_dlp

client_id = "<SPOTIFY_CLIENT_ID>"
client_secret = "<SPOTIFY_CLIENT_SECRET>"


async def play_music(bot: discord.Client, message: discord.Message):
    track_url = "https://open.spotify.com/track/4ZOjdqmXLuwHDQUn9WWoFR?si=1c74a00c69734a06"
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
    print(text)
    print(track.album.images[0].url)

    ydl_opts = {'format': 'bestaudio/best'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(text, False)
        print(info)
        url_track = info["entries"][0]["formats"][3]["url"]
        print(url_track)

        channel = message.author.voice.channel
        voice = get(bot.voice_clients, guild=message.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        op = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        player = voice.play(discord.FFmpegPCMAudio(url_track, **op))
