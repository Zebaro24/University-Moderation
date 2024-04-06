# Импорт функций Discord
from discord_bot.main_discord import bot
from discord_bot.music.music_button import button_music
from discord_bot.mafia.mafia_button import button_mafia
from discord_bot.timetable.button import button_timetable

from dislash import MessageInteraction


# Тригер нажатия кнопки
@bot.event
async def on_button_click(interaction: MessageInteraction):
    # await interaction.reply(type=dislash.ResponseType.DeferredUpdateMessage) - В случае если нету ответа
    if interaction.component.custom_id[:5] == "mafia":
        await button_mafia(interaction)
    elif interaction.component.custom_id[:5] == "music":
        await button_music(interaction)
    elif interaction.component.custom_id[:9] == "timetable":
        await button_timetable(interaction)
    else:
        pass
