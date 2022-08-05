from discord_bot.main_discord import bot
from discord_bot.music.music_button import button_music
import dislash


@bot.event
async def on_button_click(interaction: dislash.interactions.message_interaction.MessageInteraction):
    if interaction.component.custom_id[:5] == "mafia":
        pass
    elif interaction.component.custom_id[:5] == "music":
        await button_music(interaction)
    else:
        pass
