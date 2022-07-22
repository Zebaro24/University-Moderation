from config import client_id, client_secret, discord_guild
from discord import FFmpegPCMAudio, utils
import discord
from discord_bot.main_discord import slash, bot
import dislash

import tekore as tk
import yt_dlp

playlist = []


@slash.slash_command(description="Воспроизвести песню",
                     options=[dislash.Option("url", "Введите ссылку на песню", dislash.OptionType.STRING, True)])
async def play(ctx: dislash.interactions.app_command_interaction.SlashInteraction, url):
    global playlist
    if discord_guild != ctx.guild_id:
        await ctx.reply("Здесь нельзя запускать музыку", ephemeral=True)
        return
    await ctx.send("Загрузка...")

    spotify = tk.Spotify(tk.request_client_token(client_id, client_secret))

    if url[:31] == "https://open.spotify.com/track/":
        track_id = url[31:]
        spotify_playlist = [spotify.track(track_id)]
    elif url[:34] == "https://open.spotify.com/playlist/":
        playlist_id = url[34:]
        items = spotify.playlist(playlist_id).tracks.items
        spotify_playlist = [i.track for i in items]
    else:
        spotify_playlist = []

    playlist = []
    for track in spotify_playlist:
        text = "ytsearch:"
        for i in track.artists:
            text += f"{i.name}, "
        text = text[:-2]
        text += f" - {track.name}"

        ydl_opts = {'format': 'bestaudio/best'}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, False)
            playlist.append(str(info["entries"][0]["formats"][3]["url"]))
        if len(playlist) == 1:
            print(playlist)
            channel = ctx.author.voice.channel
            voice = utils.get(bot.voice_clients)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            op = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            # options -http_persistent 0
            # D:\ffmpeg\bin
            print(playlist)
            source = FFmpegPCMAudio(playlist[0], **op)
            player = voice.play(source, after=lambda: next(ctx))


@slash.slash_command(description="Следующая песня")
async def next(ctx: dislash.interactions.app_command_interaction.SlashInteraction):
    voice_client = ctx.guild.voice_client
    playlist.pop(0)
    op = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if not playlist:
        source = FFmpegPCMAudio(playlist[0], **op)
        player = voice_client.play(source)
