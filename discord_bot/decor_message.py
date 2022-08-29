# Импорт настроек
from config import discord_color

# Импорт функций Discord
from discord_bot.main_discord import slash, bot
import dislash
import discord

# Цвета Embeds
choice_color = [dislash.OptionChoice("Красный", discord.colour.Color.red()),
                dislash.OptionChoice("Темный красный", discord.colour.Color.dark_red()),
                dislash.OptionChoice("Синий", discord.colour.Color.blue()),
                dislash.OptionChoice("Темный синий", discord.colour.Color.dark_blue()),
                dislash.OptionChoice("Зеленый", discord.colour.Color.green()),
                dislash.OptionChoice("Темный зеленый", discord.colour.Color.dark_green()),
                dislash.OptionChoice("Оранжевый", discord.colour.Color.orange()),
                dislash.OptionChoice("Темный оранжевый", discord.colour.Color.dark_orange()),
                dislash.OptionChoice("Золотой", discord.colour.Color.gold()),
                dislash.OptionChoice("Темный золотой", discord.colour.Color.dark_gold()),
                dislash.OptionChoice("Пурпурный", discord.colour.Color.magenta()),
                dislash.OptionChoice("Темный пурпурный", discord.colour.Color.dark_magenta()),
                dislash.OptionChoice("Бирюзовый", discord.colour.Color.teal()),
                dislash.OptionChoice("Темный бирюзовый", discord.colour.Color.dark_teal()),
                dislash.OptionChoice("Самый светлый серый", discord.colour.Color.lighter_grey()),
                dislash.OptionChoice("Светлый серый", discord.colour.Color.light_grey()),
                dislash.OptionChoice("Темный серый", discord.colour.Color.dark_grey()),
                dislash.OptionChoice("Самый темный серый", discord.colour.Color.darker_grey()),
                dislash.OptionChoice("Размытый синий", discord.colour.Color.blurple()),
                dislash.OptionChoice("Темная тема", discord.colour.Color.dark_theme()),
                dislash.OptionChoice("Пурпуровый", discord.colour.Color.purple())]


# Команда создания красивого сообщения
@slash.slash_command(description="Создать красивое сообщения",
                     options=[dislash.Option("title", "Заголовок", dislash.OptionType.STRING, True),
                              dislash.Option("text", "Основной текст", dislash.OptionType.STRING, True),
                              dislash.Option("color", "Основной цвет", dislash.OptionType.STRING, False, choice_color),
                              dislash.Option("thumbnail", "Небольшая картинка слева (ссылка)",
                                             dislash.OptionType.STRING),
                              dislash.Option("image", "Большая картинка снизу (ссылка)", dislash.OptionType.STRING)])
@dislash.has_permissions(administrator=True)
async def set_message(ctx: dislash.interactions.app_command_interaction.SlashInteraction, title, text,
                      color=discord_color,
                      thumbnail=None, image=None):
    embed = discord.Embed(title=title, description=text, color=color)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    try:
        await ctx.channel.send(embed=embed)
    except discord.errors.HTTPException:
        await ctx.reply("Изображения не были найдены")
    else:
        await ctx.reply("Сообщения отправлено!", ephemeral=True)


# Команда редактирования красивого сообщения
@slash.slash_command(description="Создать красивое сообщения",
                     options=[dislash.Option("id_channel", "ID - Канала", dislash.OptionType.STRING, True),
                              dislash.Option("id_message", "ID - Сообщения", dislash.OptionType.STRING, True),
                              dislash.Option("title", "Заголовок", dislash.OptionType.STRING),
                              dislash.Option("text", "Основной текст", dislash.OptionType.STRING),
                              dislash.Option("color", "Основной цвет", dislash.OptionType.STRING, False, choice_color),
                              dislash.Option("thumbnail", "Небольшая картинка слева (ссылка)",
                                             dislash.OptionType.STRING),
                              dislash.Option("image", "Большая картинка снизу (ссылка)", dislash.OptionType.STRING)])
@dislash.has_permissions(administrator=True)
async def update_message(ctx: dislash.interactions.app_command_interaction.SlashInteraction, id_channel, id_message,
                         title=None,
                         text=None, color=None, thumbnail=None, image=None):
    channel = await bot.fetch_channel(id_channel)
    message: discord.Message = await channel.fetch_message(id_message)
    embed = message.embeds[0]

    if title:
        embed.title = title
    if text:
        embed.description = text
    if color:
        embed.color = color
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)

    try:
        await message.edit(embed=embed)
    except discord.errors.NotFound:
        await ctx.reply("Сообщение не было найдено")
    except discord.errors.HTTPException:
        await ctx.reply("Изображения не были найдены")
    else:
        await ctx.reply("Сообщение было изменено")
