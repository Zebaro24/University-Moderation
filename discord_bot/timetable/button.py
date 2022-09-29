from dislash.interactions.message_interaction import MessageInteraction
from discord_bot.timetable.function import day_info_ds
from timetable.additional_func import check_data
from utils import print_ds
from datetime import timedelta
import dislash


async def button_timetable(interaction: MessageInteraction):
    if interaction.component.custom_id[:14] == "timetable_next":
        date_text = (check_data(interaction.component.custom_id[15:]) + timedelta(1)).strftime('%Y:%m:%d')
        print_ds(f"Запрос на {date_text} от {interaction.author.display_name}")

        day_info = day_info_ds(date_text, True)
        await interaction.message.edit(embed=day_info["embed"], components=day_info["components"])
        await interaction.reply(type=dislash.ResponseType.DeferredUpdateMessage)
    elif interaction.component.custom_id[:15] == "timetable_early":
        date_text = (check_data(interaction.component.custom_id[16:]) - timedelta(1)).strftime('%Y:%m:%d')
        print_ds(f"Запрос на {date_text} от {interaction.author.display_name}")

        day_info = day_info_ds(date_text, True)
        await interaction.message.edit(embed=day_info["embed"], components=day_info["components"])
        await interaction.reply(type=dislash.ResponseType.DeferredUpdateMessage)
