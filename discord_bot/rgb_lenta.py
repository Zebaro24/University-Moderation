from discord_bot.main_discord import slash
from dislash import Option, OptionType


@slash.slash_command(description="Изменить цвет RGB ленты Димы",
                     options=[Option("color", "Цвет", OptionType.STRING, True)])
async def game(ctx, color):
    await ctx.reply(f"RGB Димы было изменено на: {color}")
    # Использования апи RGB Ленты
