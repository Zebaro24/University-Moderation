from config import create_voice, create_text, create_category
from discord_bot.main_discord import bot
from discord.member import Member, VoiceState
from discord.utils import get
import discord

who_channel = {}
control_sound = {}


async def delete_excess(guild):
    category: discord.channel.CategoryChannel = get(guild.categories, id=create_category)
    for i in category.voice_channels:
        if i.id != create_voice:
            await i.delete()


async def create_channel(member):
    category: discord.channel.CategoryChannel = get(member.guild.categories, id=create_category)
    voice_channel = await category.create_voice_channel(f"<---{member.display_name}--->")
    who_channel[member] = voice_channel
    await voice_channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True)
    member_voice = {"mute": member.voice.mute, "deaf": member.voice.deaf}
    control_sound[member] = member_voice
    await member.move_to(voice_channel)


async def delete_channel(member):
    if member in who_channel.keys():
        await who_channel[member].delete()
        del who_channel[member]


# Создание канала при <перемещении> с одного канала в другой или <простого захода>.
# Удаление канала при <перемещении> со своего канала в другой или <простого выхода>.
# Сохранить статус мута и звука при <перемещении> с любого канала кроме созданных и при <простого захода>.
# Возобновить статус мута и звука при <перемещении> с созданного канала в любой другой и при <выходе и заходе в другой канал>.


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    category: discord.channel.CategoryChannel = get(member.guild.categories, id=create_category)
    # {----Есть и <before> и <after>----}
    if after.channel and before.channel:  # Есть и <before> и <after>
        if after.channel.id == before.channel.id:
            return

        before_in_create = before.channel.id in [i.id for i in category.voice_channels]
        if before_in_create and before.channel.id != create_voice:
            await member.edit(mute=control_sound[member]["mute"], deafen=control_sound[member]["deaf"])
            del control_sound[member]
            await delete_channel(member)

        after_in_create = after.channel.id in [i.id for i in category.voice_channels]
        if after_in_create and after.channel.id != create_voice:
            member_voice = {"mute": member.voice.mute, "deaf": member.voice.deaf}
            control_sound[member] = member_voice

        if after.channel.id == create_voice:
            await create_channel(member)

    # {----Есть только <after>----}
    elif after.channel:

        if after.channel.id == create_voice:
            await create_channel(member)
            return

        after_in_create = after.channel.id in [i.id for i in category.voice_channels]
        if after_in_create:
            member_voice = {"mute": member.voice.mute, "deaf": member.voice.deaf}
            control_sound[member] = member_voice
        elif member in control_sound.keys():
            await member.edit(mute=control_sound[member]["mute"], deafen=control_sound[member]["deaf"])
            del control_sound[member]

    # {----Есть только <before>----}
    elif before.channel:
        before_in_create = before.channel.id in [i.id for i in category.voice_channels]
        if before.channel.id != create_voice and before_in_create:
            await delete_channel(member)

    # [i.id for i in category.voice_channels]
