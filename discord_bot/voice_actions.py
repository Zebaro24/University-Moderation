import discord
from discord_bot.main_discord import bot
import discord_bot.create_voice as voice
import discord_bot.music.music_commands as music
import discord_bot.mafia.mafia_voice as mafia
from database_func import db_run, control_sound


async def voice_save(member: discord.member.Member):
    if member.id not in control_sound and member.voice:
        member_voice = {"mute": member.voice.mute, "deaf": member.voice.deaf}
        control_sound[member.id] = member_voice
        db_run(f"INSERT INTO control_sound VALUES ({member.id},{member.voice.mute},{member.voice.deaf})")


async def voice_return(member: discord.member.Member, delete=True):
    if member.id in control_sound and member.voice:
        await member.edit(mute=control_sound[member.id]["mute"], deafen=control_sound[member.id]["deaf"])
        if delete:
            del control_sound[member.id]
            db_run(f"DELETE FROM control_sound WHERE id={member.id}")


@bot.event
async def on_voice_state_update(member: discord.member.Member, before: discord.member.VoiceState,
                                after: discord.member.VoiceState):
    if member == bot.user:
        return
    if await mafia.mafia_game(member, before, after):
        return
    await music.voice_leave(member, before, after)
    await voice.create(member, before, after)
