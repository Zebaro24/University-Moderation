from config import mafia_players
from discord_bot.mafia.mafia_start import update_start_message, start_game
from discord_bot.main_discord import bot
from dislash import ResponseType


async def button_mafia(interaction):
    if interaction.component.custom_id == "mafia_info":
        await interaction.reply("Правила", ephemeral=True)

    elif interaction.component.custom_id == "mafia_join":
        if interaction.author in [i["player"] for i in mafia_players]:
            await interaction.reply("Вы уже присоединились", delete_after=1.5)
            return
        if len(mafia_players) > 18:
            await interaction.reply("Уже максимальное количество игроков!", delete_after=5)
            return
        player = {"player": interaction.author, "want_play": False}
        mafia_players.append(player)
        await update_start_message(interaction.message)
        await interaction.reply(f"{interaction.author.mention} присоединился", delete_after=2)

    elif interaction.component.custom_id == "mafia_play":
        if interaction.author in [i["player"] for i in mafia_players]:
            for i in range(len(mafia_players)):
                if interaction.author == mafia_players[i]["player"]:
                    mafia_players[i]["want_play"] = True
                    if len(mafia_players) >= 4:
                        start_game_bool = True
                        for j in mafia_players:
                            if not j["want_play"]:
                                start_game_bool = False
                    else:
                        start_game_bool = False

                    if start_game_bool:
                        await interaction.message.edit(components=[])
                        await interaction.reply(type=ResponseType.DeferredUpdateMessage)
                        bot.loop.create_task(start_game())

                    else:
                        await interaction.reply("Ждем остальных игроков", delete_after=1.5)

                    await update_start_message(interaction.message)
        else:
            await interaction.reply("Вы еще не присоединились", delete_after=1.5)
