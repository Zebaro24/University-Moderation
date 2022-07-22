from config import client_id, client_secret, discord_guild
from discord import FFmpegPCMAudio, utils
import discord
from discord_bot.main_discord import slash, bot
from utils import print_ds
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
    await ctx.send("Конвертация в YouTube...")

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

    await ctx.send("Загрузка с YouTube...")

    playlist = []
    message = await ctx.send(
        embed=discord.Embed(title="Плейлист музики", description="Загрузка...", color=discord.colour.Color.dark_blue()))
    num = 1
    for track in spotify_playlist:
        text = ""
        for i in track.artists:
            text += f"{i.name}, "
        text = text[:-2]
        text += f" - {track.name}"

        embed = message.embeds[0]
        if embed.description == "Загрузка...":
            embed.description = f"{num}) {text}"
        else:
            embed.description += f"\n{num}) {text}"
        await message.edit(embed=embed)
        num += 1

        text = "ytsearch:" + text

        ydl_opts = {'format': 'bestaudio/best'}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, False)
            playlist.append(str(info["entries"][0]["formats"][3]["url"]))

        if not utils.get(bot.voice_clients):
            await ctx.send("Подключение к голосовому каналу...")
            channel = ctx.author.voice.channel
            voice = utils.get(bot.voice_clients)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                await channel.connect()
            play_all_playlist()


def play_all_playlist():
    voice = utils.get(bot.voice_clients)

    op = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if playlist:
        source = FFmpegPCMAudio(playlist[0], **op)

        player = voice.play(source, after=lambda e: print_ds(f'Player error: {e}') if e else play_all_playlist())
        playlist.pop(0)


@slash.slash_command(description="Пауза")
async def pause(ctx: dislash.interactions.app_command_interaction.SlashInteraction):
    await ctx.reply("Ок")
    voice: discord.voice_client.VoiceClient = bot.voice_clients[0]
    if voice:
        voice.pause()


@slash.slash_command(description="Продолжить")
async def resume(ctx: dislash.interactions.app_command_interaction.SlashInteraction):
    await ctx.reply("Ок")
    voice: discord.voice_client.VoiceClient = bot.voice_clients[0]
    if voice:
        voice.resume()


@slash.slash_command(description="Скипнуть песню")
async def skip(ctx: dislash.interactions.app_command_interaction.SlashInteraction):
    await ctx.reply("Ок")
    voice: discord.voice_client.VoiceClient = bot.voice_clients[0]
    if voice:
        voice.stop()
        # play_all_playlist()
