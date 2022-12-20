from discord_bot.main_discord import bot, slash
import dislash
import discord

from config import ds_bug_channel, discord_guild


@slash.slash_command(description="Исправить ошибку голосового канала")
async def fix(ctx: dislash.interactions.app_command_interaction.SlashInteraction):
    vc = ctx.author.voice
    if vc:
        channel = vc.channel
        await channel.edit(rtc_region="rotterdam")
        await ctx.reply("✅ Регион был сменен!", delete_after=5)
    else:
        await ctx.reply("⚠ Вы не находитесь в голосовом канале", delete_after=5)


@slash.slash_command(description="Удалить сообщение",
                     options=[dislash.Option("count", "Количество сообщений", dislash.OptionType.INTEGER, True)])
@dislash.has_permissions(administrator=True)
async def clear(ctx: dislash.interactions.app_command_interaction.SlashInteraction, count: int):
    if not 0 < count <= 5000:
        await ctx.reply("⚠ Можно удалить сообщения в пределах от 1 до 5000!", delete_after=5)
        return
    else:
        await ctx.channel.purge(limit=count)
        await ctx.reply("✅ Сообщения были удалены!", delete_after=5)


@slash.slash_command(description="Сообщить о баге!",
                     options=[
                         dislash.Option("text", "Суть бага и как его воспроизвести", dislash.OptionType.INTEGER, True)])
async def bug(ctx: dislash.interactions.app_command_interaction.SlashInteraction, text: str):
    await ctx.reply("✅ Баг был отправлен.\n"
                    "⚜ Спасибо что помогаешь улучшить этого Discord, Telegram бота!", ephemeral=True)
    embed = discord.Embed(title=f"⚠ {ctx.author.display_name} нашел баг ⚠", description=f"**Суть бага:**\n{text}",
                          color=discord.Color.orange())
    await ctx.guild.get_channel(ds_bug_channel).send(embed=embed, content=f"{ctx.author.mention}")


@slash.slash_command(description="Перекинуть всех в другой голосовой канал!")
@dislash.has_permissions(administrator=True)
async def goto(ctx: dislash.interactions.app_command_interaction.SlashInteraction):
    guild: discord.guild.Guild = ctx.guild
    print(guild.voice_channels)
    options = []
    for channel in ctx.guild.voice_channels:
        options.append(dislash.SelectOption(label=channel.name, value=channel.id, emoji="👤"))
    await ctx.reply("Выбирай...",
                    components=[dislash.SelectMenu(custom_id="goto", placeholder="Куда переместить?", options=options)],
                    ephemeral=True)
