import discord
import main_constants
from discord.ext import commands

bot = commands.Bot(command_prefix='?', description=main_constants.description_discord_bot)

@bot.commands
async def on_command(ctx, left: int, right: int):
    print(ctx)

@bot.event
async def on_ready(channel, user, when):
    print(f'we have logged in as {bot.user}')


if __name__ == '__main__':
    bot.run(main_constants.DISCORD_API)


