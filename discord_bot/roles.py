# Конфиги
import config
import roles_config

# Функции
import discord
from discord_bot.main import bot


# Реализовать добавление ролей пока бот был выключен
async def offline_role(cache_bot):
    guild = cache_bot.get_guild(config.discord_guild)
    message: discord.Message = await guild.get_channel(roles_config.chanel_id).fetch_message(roles_config.message_id)
    # for i in roles.ROLES.keys():
    #    await message.add_reaction(i)

    for reaction in message.reactions:
        if reaction.count != 1:
            async for user in reaction.users():
                if user.id != cache_bot.user.id:
                    member = await guild.fetch_member(user.id)
                    await message.remove_reaction(reaction, member)

                    if str(reaction.emoji) not in roles_config.ROLES:
                        await member.send(
                            embed=discord.Embed(title="Этой роли не существует!", color=config.discord_color))

                    else:
                        role: discord.Role = guild.get_role(
                            roles_config.ROLES[str(reaction.emoji)])
                        if roles_config.ROLES[str(reaction.emoji)] in [i.id for i in member.roles]:
                            await member.remove_roles(role)
                            await member.send(
                                embed=discord.Embed(title=f"Роль **{role.name}** была убрана!",
                                                    color=config.discord_color))
                        else:
                            await member.add_roles(role)
                            await member.send(
                                embed=discord.Embed(title=f"Роль **{role.name}** была добавлена!",
                                                    color=config.discord_color))


# Добавлять, убирать роль при клике на реакцию
@bot.event
async def on_raw_reaction_add(payload: discord.raw_models.RawReactionActionEvent):
    if payload.message_id != roles_config.message_id or payload.guild_id != config.discord_guild or payload.channel_id != roles_config.chanel_id:
        return
    if payload.member == bot.user:
        return

    message: discord.Message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)

    if str(payload.emoji) not in roles_config.ROLES:
        await payload.member.send(embed=discord.Embed(title="Этой роли не существует!", color=config.discord_color))
        return

    role: discord.Role = payload.member.guild.get_role(roles_config.ROLES[str(payload.emoji)])
    # Если у чела есть эта роль
    if roles_config.ROLES[str(payload.emoji)] in [i.id for i in payload.member.roles]:
        await payload.member.remove_roles(role)
        await payload.member.send(
            embed=discord.Embed(title=f"Роль **{role.name}** была убрана!", color=config.discord_color))

    else:
        await payload.member.add_roles(role)
        await payload.member.send(
            embed=discord.Embed(title=f"Роль **{role.name}** была добавлена!", color=config.discord_color))


'''
    guild: discord.guild.Guild = message.guild
    member: discord.member.Member = payload.member  # utils.get(message.guild.members, id=payload.user_id)

    print(member.roles)
    print(f"Информацтия сервера: {guild.fetch_member(payload.member)}")
    print(f"gggg{member}")
    await payload.member.send("dd")
    try:
        emoji = str(payload.emoji)
        print(emoji)
        role = utils.get(message.guild.members, id=roles.ROLES[emoji])
        print(role)
        await member.add_roles(role)
    except:
        print("net roli")
'''
