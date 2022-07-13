from config import DISCORD_API
import discord
from roles import create_message

bot = discord.Client()


@bot.event
async def on_ready():
    print(f"Bot was started: {bot.user}")
    await create_message(bot)
    await bot.close()


bot.run(DISCORD_API)
