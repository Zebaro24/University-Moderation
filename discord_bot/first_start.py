from config import DISCORD_API
from utils import print_ds
from discord_bot.roles.roles_commands import create_message
import discord

bot = discord.Client()


@bot.event
async def on_ready():
    print_ds(f"Бот был запущен под именем: {bot.user}")
    await create_message(bot)
    await bot.close()


bot.run(DISCORD_API)
