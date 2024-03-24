# Конфиги
from ...config import discord_guild, discord_color
from ...config import role_channel_id, role_message_id, ROLES

# Функции
from ..main_discord import bot
from discord import Message, Embed, Role, RawReactionActionEvent


# Реализовать добавление ролей пока бот был выключен
async def offline_role(cache_bot):
    guild = cache_bot.get_guild(discord_guild)
    message: Message = await guild.get_channel(role_channel_id).fetch_message(role_message_id)
    # for i in roles.ROLES.keys():
    #    await message.add_reaction(i)

    for reaction in message.reactions:
        if reaction.count != 1:
            async for user in reaction.users():
                if user.id != cache_bot.user.id:
                    member = await guild.fetch_member(user.id)
                    await message.remove_reaction(reaction, member)

                    if str(reaction.emoji) not in ROLES:
                        await member.send(
                            embed=Embed(title="Этой роли не существует!", color=discord_color))

                    else:
                        role: Role = guild.get_role(
                            ROLES[str(reaction.emoji)])
                        if ROLES[str(reaction.emoji)] in [i.id for i in member.roles]:
                            await member.remove_roles(role)
                            await member.send(
                                embed=Embed(title=f"Роль **{role.name}** была убрана!", color=discord_color))
                        else:
                            await member.add_roles(role)
                            await member.send(
                                embed=Embed(title=f"Роль **{role.name}** была добавлена!", color=discord_color))


# Добавлять, убирать роль при клике на реакцию
@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    if payload.message_id != role_message_id or payload.guild_id != discord_guild or payload.channel_id != role_channel_id:
        return
    if payload.member == bot.user:
        return

    message: Message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)

    if str(payload.emoji) not in ROLES:
        await payload.member.send(embed=Embed(title="Этой роли не существует!", color=discord_color))
        return

    role: Role = payload.member.guild.get_role(ROLES[str(payload.emoji)])
    # Если у чела есть эта роль
    if ROLES[str(payload.emoji)] in [i.id for i in payload.member.roles]:
        await payload.member.remove_roles(role)
        await payload.member.send(
            embed=Embed(title=f"Роль **{role.name}** была убрана!", color=discord_color))

    else:
        await payload.member.add_roles(role)
        await payload.member.send(
            embed=Embed(title=f"Роль **{role.name}** была добавлена!", color=discord_color))
