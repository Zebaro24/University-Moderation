from timetable.additional_func import day_info, check_data
import dislash
from discord import Embed
from config import discord_color


def day_info_ds(date_text, buttons=None):
    day = day_info(check_data(date_text), "ds")
    if buttons:
        bt_1 = dislash.Button(custom_id=f'timetable_early_{date_text}', label="Прошлый",
                              style=dislash.ButtonStyle.blurple)
        bt_2 = dislash.Button(custom_id=f'timetable_next_{date_text}', label="Следующий",
                              style=dislash.ButtonStyle.blurple)
        components = [dislash.ActionRow(bt_1, bt_2)]
    else:
        components = None
    embed = Embed(title=day["title"], description=day["main_text"], color=discord_color)
    return {"embed": embed, "components": components}
