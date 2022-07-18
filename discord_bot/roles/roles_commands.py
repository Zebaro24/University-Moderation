# Конфиги
from config import discord_guild, discord_color
from config import role_channel_id, role_message_id, ROLES
from utils import print_ds

# Функции
import discord
from discord_bot.main_discord import bot


# Реализовать добавление ролей пока бот был выключен
async def offline_role(cache_bot):
    print_ds("Проверка добавленых реакций")
    guild = cache_bot.get_guild(discord_guild)
    message: discord.Message = await guild.get_channel(role_channel_id).fetch_message(role_message_id)
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
                            embed=discord.Embed(title="Этой роли не существует!", color=discord_color))

                    else:
                        role: discord.Role = guild.get_role(
                            ROLES[str(reaction.emoji)])
                        if ROLES[str(reaction.emoji)] in [i.id for i in member.roles]:
                            await member.remove_roles(role)
                            await member.send(
                                embed=discord.Embed(title=f"Роль **{role.name}** была убрана!", color=discord_color))
                        else:
                            await member.add_roles(role)
                            await member.send(
                                embed=discord.Embed(title=f"Роль **{role.name}** была добавлена!", color=discord_color))
    print_ds("Проверка прошла успешно")


# Добавлять, убирать роль при клике на реакцию
@bot.event
async def on_raw_reaction_add(payload: discord.raw_models.RawReactionActionEvent):
    if payload.message_id != role_message_id or payload.guild_id != discord_guild or payload.channel_id != role_channel_id:
        return
    if payload.member == bot.user:
        return

    message: discord.Message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)

    if str(payload.emoji) not in ROLES:
        await payload.member.send(embed=discord.Embed(title="Этой роли не существует!", color=discord_color))
        return

    role: discord.Role = payload.member.guild.get_role(ROLES[str(payload.emoji)])
    # Если у чела есть эта роль
    if ROLES[str(payload.emoji)] in [i.id for i in payload.member.roles]:
        await payload.member.remove_roles(role)
        await payload.member.send(
            embed=discord.Embed(title=f"Роль **{role.name}** была убрана!", color=discord_color))

    else:
        await payload.member.add_roles(role)
        await payload.member.send(
            embed=discord.Embed(title=f"Роль **{role.name}** была добавлена!", color=discord_color))