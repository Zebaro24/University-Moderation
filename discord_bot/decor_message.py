# Импорт настроек
from config import discord_color

# Импорт функций Discord
from discord_bot.main_discord import slash, bot
from discord import Color, Embed, Message, HTTPException, NotFound
from dislash import OptionChoice, Option, OptionType, SlashInteraction, has_permissions

# Цвета Embeds
choice_color = [OptionChoice("Красный", Color.red()),
                OptionChoice("Темный красный", Color.dark_red()),
                OptionChoice("Синий", Color.blue()),
                OptionChoice("Темный синий", Color.dark_blue()),
                OptionChoice("Зеленый", Color.green()),
                OptionChoice("Темный зеленый", Color.dark_green()),
                OptionChoice("Оранжевый", Color.orange()),
                OptionChoice("Темный оранжевый", Color.dark_orange()),
                OptionChoice("Золотой", Color.gold()),
                OptionChoice("Темный золотой", Color.dark_gold()),
                OptionChoice("Пурпурный", Color.magenta()),
                OptionChoice("Темный пурпурный", Color.dark_magenta()),
                OptionChoice("Бирюзовый", Color.teal()),
                OptionChoice("Темный бирюзовый", Color.dark_teal()),
                OptionChoice("Самый светлый серый", Color.lighter_grey()),
                OptionChoice("Светлый серый", Color.light_grey()),
                OptionChoice("Темный серый", Color.dark_grey()),
                OptionChoice("Самый темный серый", Color.darker_grey()),
                OptionChoice("Размытый синий", Color.blurple()),
                OptionChoice("Темная тема", Color.dark_theme()),
                OptionChoice("Пурпуровый", Color.purple())]


# Команда создания красивого сообщения
@slash.slash_command(description="Создать красивое сообщения",
                     options=[Option("title", "Заголовок", OptionType.STRING, True),
                              Option("text", "Основной текст", OptionType.STRING, True),
                              Option("color", "Основной цвет", OptionType.STRING, False, choice_color),
                              Option("thumbnail", "Небольшая картинка слева (ссылка)", OptionType.STRING),
                              Option("image", "Большая картинка снизу (ссылка)", OptionType.STRING)])
@has_permissions(administrator=True)
async def set_message(ctx: SlashInteraction, title, text,
                      color=discord_color,
                      thumbnail=None, image=None):
    embed = Embed(title=title, description=text, color=color)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    try:
        await ctx.channel.send(embed=embed)
    except HTTPException:
        await ctx.reply("Изображения не были найдены")
    else:
        await ctx.reply("Сообщения отправлено!", ephemeral=True)


# Команда редактирования красивого сообщения
@slash.slash_command(description="Создать красивое сообщения",
                     options=[Option("id_channel", "ID - Канала", OptionType.STRING, True),
                              Option("id_message", "ID - Сообщения", OptionType.STRING, True),
                              Option("title", "Заголовок", OptionType.STRING),
                              Option("text", "Основной текст", OptionType.STRING),
                              Option("color", "Основной цвет", OptionType.STRING, False, choice_color),
                              Option("thumbnail", "Небольшая картинка слева (ссылка)",
                                     OptionType.STRING),
                              Option("image", "Большая картинка снизу (ссылка)", OptionType.STRING)])
@has_permissions(administrator=True)
async def update_message(ctx: SlashInteraction, id_channel, id_message,
                         title=None,
                         text=None, color=None, thumbnail=None, image=None):
    channel = await bot.fetch_channel(id_channel)
    message: Message = await channel.fetch_message(id_message)
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
    except NotFound:
        await ctx.reply("Сообщение не было найдено")
    except HTTPException:
        await ctx.reply("Изображения не были найдены")
    else:
        await ctx.reply("Сообщение было изменено")
