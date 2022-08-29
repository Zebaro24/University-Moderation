# Импорт Discord функций
from discord_bot.main_discord import slash
import dislash


# Команда для изменения цвета RGB Димы
@slash.slash_command(description="Изменить цвет RGB ленты Димы",
                     options=[dislash.Option("color", "Цвет", dislash.OptionType.STRING, True)])
async def rgb(ctx, color):
    await ctx.reply(f"RGB Димы было изменено на: {color}")
    # Использования апи RGB Ленты
