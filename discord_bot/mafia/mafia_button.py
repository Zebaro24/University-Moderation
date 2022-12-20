from config import mafia_players, mafia_voice_channel_id, mafia_color, music_channel_id, discord_guild
from discord_bot.mafia.mafia_start import update_start_message, start_game, mafia_start
from discord_bot.main_discord import bot
from dislash import ResponseType
from discord import Embed
from discord_bot.music.music_commands import play
from datetime import datetime, timedelta
from time import sleep


async def button_mafia(interaction):
    if interaction.message.created_at + timedelta(hours=1) < datetime.utcnow():
        await mafia_start(interaction.channel).cr_await
        sleep(0.1)
    if interaction.component.custom_id == "mafia_info":
        description = "Роли «в закрытую» раздаются в начале игры в случайном порядке. " \
                      "Части игроков достаются роли законопослушных мирных граждан во главе с шерифом, " \
                      "наделенным особыми полномочиями, " \
                      "а так же возможны роли (по случайности) доктор и кастомные роли у которых есть своя способность. " \
                      "Это команда мирных жителей. Другим достаются роли мафии и тоже кастомные роли (по случайности). " \
                      "Цель каждой команды — найти всех противников и отправить их в нокаут.\n" \
                      "**Основные правила игры понятны, а остачу узнаете по ходу игры!**"
        embed = Embed(title="Правила игры", description=description, color=mafia_color)
        await interaction.reply(embed=embed, ephemeral=True)

    elif interaction.component.custom_id == "mafia_join":
        if interaction.author in mafia_players:
            del mafia_players[interaction.author]
            await update_start_message(interaction.message)
            await interaction.reply(f"{interaction.author.mention} вышел с игры, вот гад...", delete_after=1.5)
            return
        if len(mafia_players) > 18:
            await interaction.reply("Уже максимальное количество игроков!", delete_after=5)
            return
        if vc := interaction.author.voice:
            if vc.channel.id != mafia_voice_channel_id:
                await interaction.reply("Вы находитесь не в том голосовом канале!", delete_after=5)
                return
        else:
            await interaction.reply("Зайдите в голосовой канал мафии для игры!", delete_after=5)
            return
        mafia_players[interaction.author] = {"want_play": False}
        await update_start_message(interaction.message)
        await interaction.reply(f"{interaction.author.mention} присоединился", delete_after=2)

    elif interaction.component.custom_id == "mafia_play":
        if interaction.author in mafia_players:
            mafia_players[interaction.author]["want_play"] = True
            if len(mafia_players) >= 4:
                start_game_bool = True
                for i in mafia_players.values():
                    if not i["want_play"]:
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

    elif interaction.component.custom_id[:8] == "mafia_DJ":
        if not (interaction.author in mafia_players and
                "role" in mafia_players[interaction.author] and
                "DJ" == mafia_players[interaction.author]["role"]):
            await interaction.reply("Вы не являетесь диджеям!")
            return
        if not mafia_players[interaction.author]["ability"]:
            await interaction.reply("На сегодня уже хватит!")
            return

        member = bot.get_guild(discord_guild).get_member(interaction.author.id)
        if interaction.component.custom_id[9:] == "amogus":
            await play(bot.get_channel(music_channel_id), "https://www.youtube.com/watch?v=5DlROhT8NgU", member)
        elif interaction.component.custom_id[9:] == "dam":
            await play(bot.get_channel(music_channel_id), "камень я не дам", member)
        elif interaction.component.custom_id[9:] == "toilet":
            await play(bot.get_channel(music_channel_id), "Копатыч не умрёт в туалете!", member)

        await interaction.reply("Включаю! Сейчас будет разнос!")
        mafia_players[interaction.author]["ability"] = False
