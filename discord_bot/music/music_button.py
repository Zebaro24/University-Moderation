from discord_bot.main_discord import bot
from wavelink import player, Filter
from dislash.interactions.message_interaction import MessageInteraction
from discord_bot.music.music_read import playlist, details_player, read_status
from random import shuffle


async def button_music(interaction: MessageInteraction):
    voices = bot.voice_clients
    if voices:
        vc: player.Player = voices[0]

        if interaction.component.custom_id == "music_play":
            details_player["status"] = "play"
            await vc.resume()

        elif interaction.component.custom_id == "music_pause":
            details_player["status"] = "pause"
            await vc.pause()

        elif interaction.component.custom_id == "music_skip":
            await vc.stop()

        elif interaction.component.custom_id == "music_shuffle":
            first = [playlist[0]]
            rest = playlist[1:]
            shuffle(rest)
            playlist.clear()
            playlist.extend(first)
            playlist.extend(rest)

        elif interaction.component.custom_id == "music_conn":
            read_status(bot.get_guild(interaction.guild_id).get_member(interaction.author.id))

        elif interaction.component.custom_id == "music_stop":
            playlist.clear()
            await vc.stop()

        elif interaction.component.custom_id == "music_low":
            details_player["volume"] = "low"
            await vc.set_filter(Filter(vc.filter, volume=0.015))

        elif interaction.component.custom_id == "music_med":
            details_player["volume"] = "med"
            await vc.set_filter(Filter(vc.filter, volume=0.15))

        elif interaction.component.custom_id == "music_high":
            details_player["volume"] = "high"
            await vc.set_filter(Filter(vc.filter, volume=5))

        await interaction.reply("Ок", delete_after=3)
