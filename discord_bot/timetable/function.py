from config import discord_color
from timetable.additional_func import day_info, check_data

from discord import Embed
from dislash import Button, ButtonStyle, ActionRow


def day_info_ds(date_text, buttons=None):
    day = day_info(check_data(date_text), "ds")
    if buttons:
        bt_1 = Button(custom_id=f'timetable_early_{date_text}', label="Прошлый",
                      style=ButtonStyle.blurple)
        bt_2 = Button(custom_id=f'timetable_next_{date_text}', label="Следующий",
                      style=ButtonStyle.blurple)
        components = [ActionRow(bt_1, bt_2)]
    else:
        components = None
    embed = Embed(title=day["title"], description=day["main_text"], color=discord_color)
    return {"embed": embed, "components": components}
