# Импорт Discord функций
from discord_bot.main_discord import slash
from discord_bot.timetable.function import day_info_ds
from timetable.additional_func import list_days_by_text


# Команда для показа расписания на день
@slash.slash_command(description="Показать расписание на этот день")
async def now_day(ctx):
    date_text = list_days_by_text("now_day")[0]
    day_info = day_info_ds(date_text, True)
    await ctx.reply(embed=day_info["embed"], components=day_info["components"])


@slash.slash_command(description="Показать расписание на эту неделю")
async def now_week(ctx):
    list_days = list_days_by_text("now_week")
    for date_text in list_days:
        day_info = day_info_ds(date_text, False)
        await ctx.reply(embed=day_info["embed"], components=day_info["components"])


@slash.slash_command(description="Показать расписание на следующую неделю")
async def next_week(ctx):
    list_days = list_days_by_text("next_week")
    for date_text in list_days:
        day_info = day_info_ds(date_text, False)
        await ctx.reply(embed=day_info["embed"], components=day_info["components"])
