from dislash import Option, OptionChoice, OptionType, interactions
from discord_bot.main_discord import slash
from requests import post
from config import DISCORD_API

# Словарь с активностями Discord
activities = [{"name": "Watch Together", "id": 880218394199220334},
              {"name": "Word Snacks", "id": 879863976006127627},
              {"name": "Sketch Heads", "id": 902271654783242291},
              {"name": "Know What I Meme", "id": 950505761862189096},
              {"name": "Ask Away", "id": 976052223358406656}]
headers = {'authorization': f"Bot {DISCORD_API}"}


# Запуск активности
@slash.slash_command(description="Запустить игру или просмотр Youtube",
                     options=[Option("activity", "Выберите активность из списка", OptionType.STRING, True,
                                     [OptionChoice(i["name"], i) for i in activities])])
async def game(ctx: interactions.app_command_interaction.SlashInteraction, activity):
    if not ctx.author.voice:
        await ctx.reply("Ты не находишься в голосовом канале", delete_after=5)
        return
    await ctx.channel.trigger_typing()
    url = f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites'
    body = {"max_age": 300,
            "max_uses": 0,
            "target_application_id": activity["id"],
            "target_type": 2,
            "temporary": True}

    response = post(url, json=body, headers=headers).json()
    await ctx.reply(f"[{activity['name']}](https://discord.gg/{response['code']}) - Действует 5 мин.", delete_after=300)
    head = {"type": "text/javascript"}
    response = post("https://sinoptik.ua/informers_js.php?title=4&amp;wind=3&amp;cities=303028915&amp;lang=ru",
                    headers=head).json()
    print(response)
