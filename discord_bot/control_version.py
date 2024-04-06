# Импорт настроек и информации о версии
from config import discord_guild, version_channel, discord_color, debug
from version import version_numbering, version_title, version_description

# Создание красивого сообщения
from discord import Embed


# Проверка версии и отправление информации об обновлении
async def check_version(bot):
    channel = bot.get_guild(discord_guild).get_channel(version_channel)
    if channel.topic != version_numbering and not debug:
        await channel.edit(topic=version_numbering)
        embed = Embed(title=f"Обновлено до версии: {version_numbering}\n"
                            f"Тема обновления: {version_title}",
                      description=version_description,
                      color=discord_color)
        await channel.send(embed=embed)
