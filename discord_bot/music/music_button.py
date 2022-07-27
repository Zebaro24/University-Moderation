from discord_bot.main_discord import bot
import dislash

@bot.event
async def on_button_click(interaction: dislash.interactions.message_interaction.MessageInteraction):
    if interaction.component.custom_id[:5] != "music":
        print("gg")
        return
    print("hh")
    if interaction.component.custom_id == "music_play":
        pass
    elif interaction.component.custom_id == "music_pause":
        voice: discord.voice_client.VoiceClient = bot.voice_clients
        if voice:
            voice[0].pause()