from config import discord_guild, version_channel, discord_color
import version
from discord import Embed


async def check_version(bot):
    channel = bot.get_guild(discord_guild).get_channel(version_channel)
    if channel.topic != version.version_numbering:
        await channel.edit(topic=version.version_numbering)
        embed = Embed(title=f"Обновлено до версии: {version.version_numbering}\n"
                            f"Тема обновления: {version.version_title}",
                      description=version.version_description,
                      color=discord_color)
        await channel.send(embed=embed)
