from discord_bot.main_discord import bot
from wavelink import player, Filter
from dislash.interactions.message_interaction import MessageInteraction
from discord_bot.music.music_read import playlist, details_player, read_status
from random import shuffle
from dislash import ResponseType
from config import mafia_voice_channel_id


async def button_music(interaction: MessageInteraction):
    voices = bot.voice_clients
    if voices:
        vc: player.Player = voices[0]

        if interaction.author.voice and interaction.author.voice.channel.id == mafia_voice_channel_id:
            await interaction.reply("💢 В данный момент нельзя использовать эти кнопки...", ephemeral=True)
            return

        if interaction.component.custom_id == "music_play":
            details_player["status"] = "play"
            await vc.resume()
            await interaction.reply(type=ResponseType.DeferredUpdateMessage)

        elif interaction.component.custom_id == "music_pause":
            details_player["status"] = "pause"
            await vc.pause()
            await interaction.reply(type=ResponseType.DeferredUpdateMessage)

        elif interaction.component.custom_id == "music_skip":
            await vc.stop()
            await interaction.reply(f"🪗 {interaction.author.mention} переключил музяку...", delete_after=6)

        elif interaction.component.custom_id == "music_shuffle":
            first = [playlist[0]]
            rest = playlist[1:]
            shuffle(rest)
            playlist.clear()
            playlist.extend(first)
            playlist.extend(rest)
            await interaction.reply(f"🥢 {interaction.author.mention} захотел перемешать песни...", delete_after=6)

        elif interaction.component.custom_id == "music_conn":
            read_status(bot.get_guild(interaction.guild_id).get_member(interaction.author.id))
            await interaction.reply(f"🔥 {interaction.author.mention} включил топовый музон со спутифуя...",
                                    delete_after=6)

        elif interaction.component.custom_id == "music_stop":
            playlist.clear()
            await vc.stop()
            await vc.disconnect()
            await interaction.reply(f"😤 {interaction.author.mention} остановил всю дискотеку...", delete_after=6)

        elif interaction.component.custom_id == "music_low":
            details_player["volume"] = "low"
            await vc.set_filter(Filter(vc.filter, volume=0.015))
            await interaction.reply(f"🤏 {interaction.author.mention} понизил громкость на минимум...\n"
                                    f"**(падажи 5 сек по братски)**", delete_after=6)

        elif interaction.component.custom_id == "music_med":
            details_player["volume"] = "med"
            await vc.set_filter(Filter(vc.filter, volume=0.15))
            await interaction.reply(f"🫄 {interaction.author.mention} изменил громкость на нормич...\n"
                                    f"**(падажи 5 сек громкость прибавлю)**", delete_after=6)

        elif interaction.component.custom_id == "music_high":
            details_player["volume"] = "high"
            await vc.set_filter(Filter(vc.filter, volume=0.6))
            await interaction.reply(f"🦻 {interaction.author.mention} изменил громкость на ||тікай з села||...\n"
                                    f"**(ебанько, падажи 5 сек я в бункер спрячусь🪖)**", delete_after=6)
