import time

import wavelink

from config import client_id, client_secret, music_channel_id, discord_guild
from discord import FFmpegPCMAudio, utils
import discord
from discord_bot.main_discord import slash, bot
from utils import print_ds
import dislash
from discord_bot.music.music_read import read_url,playlist

import tekore as tk
import yt_dlp




@slash.slash_command(description="Воспроизвести плейлист или трек",
                     options=[
                         dislash.Option("url", "Введите ссылку на плейлист или трек", dislash.OptionType.STRING, True)])
async def play(ctx: dislash.interactions.app_command_interaction.SlashInteraction, url):
    if discord_guild != ctx.guild_id:
        return
    if music_channel_id != ctx.channel_id:
        await ctx.reply("Здесь нельзя запускать музыку", ephemeral=True)
        return
    before_time = time.perf_counter()

    read_url(url)

    print("hhhh")
    if not utils.get(bot.voice_clients):
        await ctx.send("Подключение к голосовому каналу...")
        channel = ctx.author.voice.channel
        voice = utils.get(bot.voice_clients)
        print("do")
        if voice and voice.is_connected():
            print("перед")
            await voice.move_to(channel)
        else:
            print("gg")
            vc = await channel.connect(cls=wavelink.Player)
            track_name = f"{playlist[0]['artists']} - {playlist[0]['name']}"
            track = await wavelink.YouTubeTrack.search(query=track_name, return_first=True)
            await vc.play(track)
            print(time.perf_counter()-before_time)
    else:
        track_name = f"{playlist[0]['artists']} - {playlist[0]['name']}"
        track = await wavelink.YouTubeTrack.search(query=track_name, return_first=True)
        await utils.get(bot.voice_clients).play(track)


def spotify_reed():
    pass


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
