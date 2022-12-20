from discord_bot.main_discord import bot
from dislash import MessageInteraction
from discord_bot.mafia.mafia_menu import mafia_select

@bot.event
async def on_dropdown(inter: MessageInteraction):
    element_id = inter.select_menu.custom_id.split("_")[0]
    if element_id == "mafia":
        await mafia_select(inter)
    elif element_id == "goto":
        channel_to = inter.guild.get_channel(int(inter.select_menu.selected_options[0].value))
        if not channel_to:
            await inter.reply("Такого голосового канала не существует!", ephemeral=True)
        if vc := inter.author.voice:
            for people in vc.channel.members:
                await people.move_to(channel_to)
        else:
            await inter.reply("Вы не подключены к голосовому каналу!",ephemeral=True)