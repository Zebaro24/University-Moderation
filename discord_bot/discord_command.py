from ..config import ds_bug_channel
from .main_discord import slash

from discord import Embed, Guild, Color
from dislash import has_permissions, SlashInteraction, Option, OptionType, SelectOption, SelectMenu


@slash.slash_command(description="Исправить ошибку голосового канала")
async def fix(ctx: SlashInteraction):
    vc = ctx.author.voice
    if vc:
        channel = vc.channel
        await channel.edit(rtc_region="rotterdam")
        await ctx.reply("✅ Регион был сменен!", delete_after=5)
    else:
        await ctx.reply("⚠ Вы не находитесь в голосовом канале", delete_after=5)


@slash.slash_command(description="Удалить сообщение",
                     options=[Option("count", "Количество сообщений", OptionType.INTEGER, True)])
@has_permissions(administrator=True)
async def clear(ctx: SlashInteraction, count: int):
    if not 0 < count <= 5000:
        await ctx.reply("⚠ Можно удалить сообщения в пределах от 1 до 5000!", delete_after=5)
        return
    else:
        await ctx.channel.purge(limit=count)
        await ctx.reply("✅ Сообщения были удалены!", delete_after=5)


@slash.slash_command(description="Сообщить о баге!",
                     options=[
                         Option("text", "Суть бага и как его воспроизвести", OptionType.INTEGER, True)])
async def bug(ctx: SlashInteraction, text: str):
    await ctx.reply("✅ Баг был отправлен.\n"
                    "⚜ Спасибо что помогаешь улучшить этого Discord, Telegram бота!", ephemeral=True)
    embed = Embed(title=f"⚠ {ctx.author.display_name} нашел баг ⚠", description=f"**Суть бага:**\n{text}",
                  color=Color.orange())
    await ctx.guild.get_channel(ds_bug_channel).send(embed=embed, content=f"{ctx.author.mention}")


@slash.slash_command(description="Перекинуть всех в другой голосовой канал!")
@has_permissions(administrator=True)
async def goto(ctx: SlashInteraction):
    guild: Guild = ctx.guild
    print(guild.voice_channels)
    options = []
    for channel in ctx.guild.voice_channels:
        options.append(SelectOption(label=channel.name, value=channel.id, emoji="👤"))
    await ctx.reply("Выбирай...",
                    components=[SelectMenu(custom_id="goto", placeholder="Куда переместить?", options=options)],
                    ephemeral=True)
