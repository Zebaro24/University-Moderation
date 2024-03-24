from ...config import music_channel_id, discord_guild, mafia_voice_channel_id, mafia_players
from ...utils import print_ds
from ..main_discord import slash, bot
from .music_read import read_url, playlist, read_youtube, details_player

from discord import VoiceClient, VoiceChannel, VoiceState, Message
from dislash import Option, SlashInteraction, OptionType, has_permissions
from wavelink import Player, Filter

from time import perf_counter
from asyncio import sleep

start_bool = True


@slash.slash_command(description="Воспроизвести плейлист или трек",
                     options=[
                         Option("url", "Введите ссылку на плейлист или трек", OptionType.STRING, True)])
async def play(ctx: SlashInteraction, url, mafia=None):
    global start_bool
    if mafia:
        class Ctx:
            guild = ctx.guild
            channel = ctx
            reply = ctx.send
            author = mafia

        ctx = Ctx

    if discord_guild != ctx.guild.id:
        return
    if music_channel_id != ctx.channel.id:
        await ctx.reply("💢 Здесь нельзя запускать музыку", ephemeral=True)
        return
    if not ctx.author.voice:
        if mafia or type(ctx) == Message:
            await ctx.reply("⚠️ Вы не зашли в голосовой канал", delete_after=3)
        else:
            await ctx.reply("⚠️ Вы не зашли в голосовой канал", ephemeral=True)
        return
    if ctx.author.voice.channel.id == mafia_voice_channel_id:
        if ctx.author in mafia_players and \
                "role" in mafia_players[ctx.author] and \
                "DJ" == mafia_players[ctx.author]["role"]:
            pass
        else:
            await ctx.author.reply("💢 В этом голосовом канале нельзя запускать музыку!", ephemeral=True)
            return
    if start_bool:
        await ctx.reply("⏱ Пождите несколько секунд, выполняется команда", delete_after=3)
        return
    if playlist:
        await ctx.reply("⚠️ Сначала очистите плейлист потом выполняйте эту команду", delete_after=3)
        return
    start_bool = True

    await ctx.channel.trigger_typing()

    before_time = perf_counter()

    playlist.clear()  # По сути ненужно, но метод предосторожности
    await read_url(url)

    if not playlist:
        start_bool = False
        return
    # ----------------------------------------Нужен фикс (возможно исправил)----------------------------------------
    while True:
        if "track" in playlist[0]:
            track = playlist[0]["track"]
            break
        else:
            track_name = f"{playlist[0]['artists']} - {playlist[0]['name']}"
            track = await read_youtube(track_name, True)
            if track:
                break
            playlist.pop(0)
            if not playlist:
                start_bool = False
                return
    # ------------------------------------------------------------------------------------------
    vc: Player
    if not bot.voice_clients:
        await ctx.reply("🌐 Подключение к голосовому каналу...", delete_after=3)
        vc = await ctx.author.voice.channel.connect(cls=Player)
        if ctx.author in mafia_players:
            details_player["volume"] = "high"
            await vc.set_filter(Filter(vc.filter, volume=0.6))
        else:
            details_player["volume"] = "low"
            await vc.set_filter(Filter(vc.filter, volume=0.015))

    elif bot.voice_clients[0].channel != ctx.author.voice.channel:
        await ctx.reply("🌐 Подключение к голосовому каналу...", delete_after=3)
        await bot.voice_clients[0].move_to(ctx.author.voice.channel)
        vc = bot.voice_clients[0]

    else:
        vc = bot.voice_clients[0]

    details_player["status"] = "play"
    await ctx.reply("🎶 Запускаю музон...", delete_after=3)
    await vc.play(track)
    print_ds(f"Загрузка музыки за: {round(perf_counter() - before_time, 2)} сек")
    print_ds(f"Играет музыка: {track}")
    start_bool = False


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track, reason):  # noqa
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
            "❗️ Во время загрузки трека произошла ошибка", delete_after=5)

    if playlist:
        playlist.pop(0)
    if playlist:
        # ----------------------------------------Нужен фикс----------------------------------------
        while True:
            if "track" in playlist[0]:
                track = playlist[0]["track"]
                break
            else:
                track_name = f"{playlist[0]['artists']} - {playlist[0]['name']}"
                track = await read_youtube(track_name, True)
                if track:
                    break
                playlist.pop(0)
                if not playlist:
                    return
        # ------------------------------------------------------------------------------------------

        print_ds(f"Играет музыка: {track}")
        await player.play(track)
    else:
        await sleep(120)
        if not playlist:
            await player.disconnect()


@slash.slash_command(description="Пауза")
async def pause(ctx: SlashInteraction):
    if music_channel_id != ctx.channel.id:
        await ctx.reply("💢 Здесь нельзя использовать эту команду...", ephemeral=True)
        return
    if ctx.author.voice and ctx.author.voice.channel.id == mafia_voice_channel_id:
        await ctx.reply("💢 В данный момент нельзя использовать эту команду...", ephemeral=True)
        return
    await ctx.reply("👍 Есть пауза, сделано бос...", delete_after=6)
    voice: VoiceClient = bot.voice_clients[0]
    if voice:
        details_player["status"] = "pause"
        voice.pause()


@slash.slash_command(description="Продолжить")
async def resume(ctx: SlashInteraction):
    if music_channel_id != ctx.channel.id:
        await ctx.reply("💢 Здесь нельзя использовать эту команду...", ephemeral=True)
        return
    await ctx.reply("🥣 Уже воспроизводится, готов служить за миску риса...", delete_after=6)
    voice: VoiceClient = bot.voice_clients[0]
    if voice:
        details_player["status"] = "play"
        voice.resume()


@slash.slash_command(description="Скипнуть песню")
async def skip(ctx: SlashInteraction):
    if music_channel_id != ctx.channel.id:
        await ctx.reply("💢 Здесь нельзя использовать эту команду...", ephemeral=True)
        return
    if ctx.author.voice and ctx.author.voice.channel.id == mafia_voice_channel_id:
        await ctx.reply("💢 В данный момент нельзя использовать эту команду...", ephemeral=True)
        return
    await ctx.reply(f"😔 Зачем ты так, это был самый клевый трек...", delete_after=6)
    voice: VoiceClient = bot.voice_clients[0]
    if voice:
        voice.stop()


@slash.slash_command(description="Добавить песню",
                     options=[
                         Option("url", "Введите ссылку на плейлист или трек", OptionType.STRING, True)])
async def add(ctx: SlashInteraction, url):
    if music_channel_id != ctx.channel.id:
        await ctx.reply("💢 Здесь нельзя добавлять музыку", ephemeral=True)
        return
    if ctx.author.voice and ctx.author.voice.channel.id == mafia_voice_channel_id:
        await ctx.reply("💢 В данный момент нельзя использовать эту команду...", ephemeral=True)
        return
    if playlist:
        await ctx.reply("🤘 Музон добавляется...", delete_after=6)
        await read_url(url)
    else:
        await ctx.reply("🤷‍♂️ Плейлист бота не играет!", delete_after=2)


@slash.slash_command(description="Громкость на полную")
@has_permissions(administrator=True)
async def max_value(ctx: SlashInteraction):
    voices = bot.voice_clients
    if voices:
        vc = voices[0]
        details_player["volume"] = "high"
        await vc.set_filter(Filter(vc.filter, volume=5))
        await ctx.reply("🤣 Сделал...", ephemeral=True)
    else:
        await ctx.reply("🤷‍♂️ Плейлист бота не играет!", ephemeral=True)


async def voice_leave(member: discord.member.Member, before: discord.member.VoiceState,  # noqa
                      after: VoiceState):
    if before.channel and (not after.channel or before.channel != after.channel):
        vc: VoiceChannel = before.channel
        if bot.user in vc.members and len(vc.members) == 1:
            if not bot.voice_clients:
                await vc.members[0].edit(voice_channel=None)
            else:
                vc_bot = bot.voice_clients[0]
                playlist.clear()
                await vc_bot.stop()
                await vc_bot.disconnect()
