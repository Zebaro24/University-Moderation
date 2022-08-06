import time

import wavelink

from config import music_channel_id, discord_guild
from discord import utils
import discord
from discord_bot.main_discord import slash, bot
from utils import print_ds
import dislash
from discord_bot.music.music_read import read_url, playlist


@slash.slash_command(description="Воспроизвести плейлист или трек",
                     options=[
                         dislash.Option("url", "Введите ссылку на плейлист или трек", dislash.OptionType.STRING, True)])
async def play(ctx: dislash.interactions.app_command_interaction.SlashInteraction, url):
    if discord_guild != ctx.guild_id:
        print_ds("Использование функции музыки в личных сообщениях!")
        return
    if music_channel_id != ctx.channel_id:
        await ctx.reply("Здесь нельзя запускать музыку", ephemeral=True)
        return
    if not ctx.author.voice:
        await ctx.reply("Вы не зашли в голосовой канал", ephemeral=True)
        return

    await ctx.channel.trigger_typing()

    before_time = time.perf_counter()
    playlist.clear()
    await read_url(url)

    track_name = f"{playlist[0]['artists']} - {playlist[0]['name']}"
    track = await wavelink.YouTubeTrack.search(track_name, return_first=True)

    vc: wavelink.player.Player
    if not bot.voice_clients:
        await ctx.send("Подключение к голосовому каналу...", delete_after=3)
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await vc.set_filter(wavelink.Filter(vc.filter, volume=0.015))

    elif bot.voice_clients[0].channel != ctx.author.voice.channel:
        await ctx.send("Подключение к голосовому каналу...", delete_after=3)
        await bot.voice_clients[0].move_to(ctx.author.voice.channel)
        vc = bot.voice_clients[0]

    else:
        vc = bot.voice_clients[0]

    await ctx.send("Запускаю музон...", delete_after=3)
    await vc.play(track)
    print_ds(f"Загрузка музыки за: {time.perf_counter() - before_time} сек")
    print_ds(f"Играет музыка: {track}")


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track, reason):
    # print(f"Трек закончился причина: {reason}")
    if len(player.channel.members) >= 2:
        if bot.user not in player.channel.members:
            playlist.clear()
            await player.disconnect()
    else:
        playlist.clear()
        await player.disconnect()

    if reason == "REPLACED":
        return
    elif reason == "LOAD_FAILED":
        await bot.get_guild(discord_guild).get_channel(music_channel_id).send(
            "Во время загрузки трека произошла ошибка", delete_after=5)

    if playlist:
        playlist.pop(0)
    if playlist:
        track_name = f"{playlist[0]['artists']} - {playlist[0]['name']}"
        track = await wavelink.YouTubeTrack.search(track_name, return_first=True)
        print_ds(f"Играет музыка: {track}")
        await player.play(track)


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
