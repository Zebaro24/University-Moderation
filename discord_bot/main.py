import discord
import config
from discord.message import Message
import roles

# intents_g: discord.flags.Intents = discord.Intents.default()

# intents_g.members = True

client = discord.Client()  # intents=intents_g)


@client.event
async def on_ready():
    print(f"Bot was started: {client.user}")
    await offline_role()


# Все ивенты: https://discordpy.readthedocs.io/en/latest/api.html#event-reference
@client.event
async def on_message(message: Message):
    # Если автор совпадает с клиентом то вернуть
    # Чтобы бот не считывал свои сообщения
    if message.author == client.user:
        return
    # Не забывать await
    # await message.channel.send("sdsdsds")  # Отправить в канал
    # await message.author.send("sasasa")  # Отправить в личку

    if message.content[0:2] == "cl" and type(message.channel) != discord.channel.DMChannel:
        try:
            num = int(message.content[3:])
        except ValueError:
            num = 5
        await message.channel.purge(limit=num)

    print(message.author)
    channel: discord.TextChannel = client.get_channel(995704829416583200)  # Канал по id
    await channel.send("sdsds")  # Отправка в канал по id

    # client.get_user("Zebaro#9282")

    print(message.channel.id)  # Id канала

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


    # message.id = 996541038686642226
    # for i in roles.ROLES.keys():
    #     await message.add_reaction(i)


# Реализовать добавление ролей пока бот был выключен
async def offline_role():
    message: Message = await client.get_guild(config.discord_guild).get_channel(roles.chanel_id).fetch_message(
        roles.message_id)
    # for i in roles.ROLES.keys():
    #    await message.add_reaction(i)

    for reaction in message.reactions:
        if reaction.count != 1:
            async for user in reaction.users():
                if user.id != client.user.id:
                    member = await client.get_guild(config.discord_guild).fetch_member(user.id)
                    await message.remove_reaction(reaction, member)

                    if str(reaction.emoji) not in roles.ROLES:
                        await member.send(
                            embed=discord.Embed(title="Этой роли не существует!", color=config.discord_color))

                    else:
                        role: discord.Role = client.get_guild(config.discord_guild).get_role(
                            roles.ROLES[str(reaction.emoji)])
                        if roles.ROLES[str(reaction.emoji)] in [i.id for i in member.roles]:
                            await member.remove_roles(role)
                            await member.send(
                                embed=discord.Embed(title=f"Роль **{role.name}** была убрана!",
                                                    color=config.discord_color))
                        else:
                            await member.add_roles(role)
                            await member.send(
                                embed=discord.Embed(title=f"Роль **{role.name}** была добавлена!",
                                                    color=config.discord_color))


# roles
@client.event
async def on_raw_reaction_add(payload: discord.raw_models.RawReactionActionEvent):

    if payload.message_id != roles.message_id or payload.guild_id != config.discord_guild or payload.channel_id != roles.chanel_id:
        return
    if payload.member == client.user:
        return

    message: Message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)


    if str(payload.emoji) not in roles.ROLES:
        await payload.member.send(embed=discord.Embed(title="Этой роли не существует!", color=config.discord_color))
        return

    role: discord.Role = payload.member.guild.get_role(roles.ROLES[str(payload.emoji)])
    # Если у чела есть эта роль
    if roles.ROLES[str(payload.emoji)] in [i.id for i in payload.member.roles]:
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


def start():
    client.run(config.DISCORD_API)


if __name__ == '__main__':
    start()
