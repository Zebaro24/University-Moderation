import discord
import main_constants
from discord.ext import commands

bot = discord.Client()


@bot.event
async def on_ready():
    print('we have logged in as {0.user}'.format(bot))


@bot.event
async def on_typing(channel, user, when):
    await channel.send(user.name)
    print("f")


if __name__ == '__main__':
    bot.run(main_constants.DISCORD_API)
