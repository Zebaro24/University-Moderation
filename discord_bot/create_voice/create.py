from config import create_voice, create_text
from discord_bot.main_discord import bot
from discord.member import Member, VoiceState
from discord.utils import get
import discord


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    print(member)
    print(after)
    if not before.channel and before.channel.id == create_voice:
        print("Выход")
        return
    if not after.channel or after.channel.id != create_voice:
        print("Выход")
        return

    category: discord.channel.CategoryChannel = get(member.guild.categories, id=1009823176362045440)
    voice_channel = await category.create_voice_channel(f"<---{member.display_name}--->")
    # perm = discord.Permissions()
    await voice_channel.set_permissions(member, manage_channels=True, manage_permissions=True, kick_members=True)
    await member.move_to(voice_channel)
