# Импорт настроек
from config import create_voice, create_category

# Импорт функций Discord
from discord_bot.main_discord import bot
from discord.utils import get
import discord

who_channel = {}
control_sound = {}  # В базу данных!!!


# Удаление созданных лишних каналов при запуске
async def delete_excess(guild):
    category: discord.channel.CategoryChannel = get(guild.categories, id=create_category)
    for i in category.voice_channels:
        if i.id != create_voice:
            await i.delete()


# Создание голосового канала
async def create_channel(member):
    category: discord.channel.CategoryChannel = get(member.guild.categories, id=create_category)
    voice_channel = await category.create_voice_channel(f"<---{member.display_name}--->")
    who_channel[member] = {"voice": voice_channel, "member_mute": {}}
    await voice_channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True)
    member_voice = {"mute": member.voice.mute, "deaf": member.voice.deaf}
    control_sound[member] = member_voice
    await member.move_to(voice_channel)


# Удаление голосового канала
async def delete_channel(member, before, after):
    if member in who_channel.keys():
        delete_elem = who_channel[member]["voice"]
        del who_channel[member]
        await delete_elem.delete()
    else:
        for i, j in who_channel.items():
            if j["voice"].id == before.channel.id:
                print(member.voice)
                who_channel[i]["member_mute"][member] = {}
                if member.voice:
                    who_channel[i]["member_mute"][member]["mute"] = member.voice.mute
                    who_channel[i]["member_mute"][member]["deaf"] = member.voice.deaf
    if after.channel:
        await member.edit(mute=control_sound[member]["mute"], deafen=control_sound[member]["deaf"])
        del control_sound[member]


# Сохранение муза и звука при входе в голосовой канал
async def voice_in(member, after):
    member_voice = {"mute": member.voice.mute, "deaf": member.voice.deaf}
    control_sound[member] = member_voice

    for i in who_channel.values():
        if i["voice"].id == after.channel.id:
            if member in i["member_mute"].keys():
                await member.edit(mute=i["member_mute"][member]["mute"], deafen=i["member_mute"][member]["deaf"])
                return
    await member.edit(mute=False, deafen=False)


# Создание канала при <перемещении> с одного канала в другой или <простого захода>.
# Удаление канала при <перемещении> со своего канала в другой или <простого выхода>.
# Сохранить статус мута и звука при <перемещении> с любого канала кроме созданных и при <простого захода>.
# Возобновить статус мута и звука при <перемещении> с созданного канала в любой другой и при <выходе и заходе в другой канал>.

# Любое взаимодействие с голосовыми каналами
@bot.event
async def on_voice_state_update(member: discord.member.Member, before: discord.member.VoiceState,
                                after: discord.member.VoiceState):
    # {----Есть и <before> и <after>----}
    if after.channel and before.channel:  # Есть и <before> и <after>
        if after.channel.id == before.channel.id:
            return

        if before.channel.id in [i["voice"].id for i in who_channel.values()]:  # Если before в списке созданных
            await delete_channel(member, before, after)

        if after.channel.id in [i["voice"].id for i in who_channel.values()]:  # Если after в списке созданных
            await voice_in(member, after)

        if after.channel.id == create_voice:
            await create_channel(member)

    # {----Есть только <after>----} только вход
    elif after.channel:
        for i, j in who_channel.items():  # Проверка на выход из голосового канала и запомнить данные мута для входа обратно
            if member in j["member_mute"].keys():
                if not j["member_mute"][member]:
                    who_channel[i]["member_mute"][member]["mute"] = member.voice.mute
                    who_channel[i]["member_mute"][member]["deaf"] = member.voice.deaf

        if after.channel.id == create_voice:
            await create_channel(member)

        elif after.channel.id in [i["voice"].id for i in who_channel.values()]:  # Если after в списке созданных
            await voice_in(member, after)

        elif member in control_sound.keys():
            await member.edit(mute=control_sound[member]["mute"], deafen=control_sound[member]["deaf"])
            del control_sound[member]

    # {----Есть только <before>----} только выход
    elif before.channel:
        if before.channel.id in [i["voice"].id for i in who_channel.values()]:  # Если before в списке созданных
            await delete_channel(member, before, after)

    # [i.id for i in category.voice_channels]
