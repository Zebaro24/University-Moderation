from discord_bot.main_discord import bot as bot_ds
from config import discord_guild, ds_chanel_id
from asyncio import run_coroutine_threadsafe


def telegram_to_ds(message):
    channel = bot_ds.get_guild(discord_guild).get_channel(ds_chanel_id)
    run_coroutine_threadsafe(channel.send(f"**{message.chat.first_name}** : {message.text}"), bot_ds.loop)
