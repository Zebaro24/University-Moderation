from ...utils import print_ds
from ...timetable.additional_func import check_data
from .function import day_info_ds

from dislash import MessageInteraction, ResponseType

from datetime import timedelta


async def button_timetable(interaction: MessageInteraction):
    if interaction.component.custom_id[:14] == "timetable_next":
        date_text = (check_data(interaction.component.custom_id[15:]) + timedelta(1)).strftime('%Y:%m:%d')
        print_ds(f"Запрос на {date_text} от {interaction.author.display_name}")

        day_info = day_info_ds(date_text, True)
        await interaction.message.edit(embed=day_info["embed"], components=day_info["components"])
        await interaction.reply(type=ResponseType.DeferredUpdateMessage)
    elif interaction.component.custom_id[:15] == "timetable_early":
        date_text = (check_data(interaction.component.custom_id[16:]) - timedelta(1)).strftime('%Y:%m:%d')
        print_ds(f"Запрос на {date_text} от {interaction.author.display_name}")

        day_info = day_info_ds(date_text, True)
        await interaction.message.edit(embed=day_info["embed"], components=day_info["components"])
        await interaction.reply(type=ResponseType.DeferredUpdateMessage)
