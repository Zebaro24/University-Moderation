# Импорт функций Discord
from discord_bot.main_discord import slash

from discord import Embed
from dislash import interactions


# Команда помощи
@slash.slash_command(name="help", description="Помощь по боту")
async def help_comm(ctx: interactions.app_command_interaction.SlashInteraction):
    description = "Здесь вы узнаете основные функции бота и как он работает.\n" \
                  "Бот находится в стадии разработке и доработки,\n" \
                  "над ним ведутся тестирования, если найдете баг или какую то неточность,\n" \
                  "а так же какое то предложение насчет бота,\n" \
                  "то опишите суть бага через команду `/bug <text>`."
    embed = Embed(title="╔═════════ Помощник по использованию бота ═════════╗", description=description)
    embed.add_field(name="🧩 Музыка",
                    value="Бот способен воспроизводить треки из таких платформ как YouTube и Spotify, по сути вам этих платформ хватит.\n"
                          "Основные команды и включение музыки работает только в канале музыка.\n"
                          "> Перечисление команд:\n"
                          "> `/play <url>` - Добавляет трек в плейлист, и запускает его.\n"
                          "> `/add <url>` - Добавляет трек в плейлист.\n"
                          "> `/pause` - Ставит трек на паузу.\n"
                          "> `/resume` - Снимает трек с паузы.\n"
                          "> `/skip` - Пропускает трек.\n"
                          "> `/fix` - Чинит голосовой канал.\n", inline=False)
    embed.add_field(name="🧩 Свой голосовой",
                    value="Суть заключается в том чтобы каждый мог создать свой голосовой канал и в нем иметь свою власть.\n"
                          "Под этим словом я имею:\n"
                          "мутить, выключать звук, менять название канала, запрещать участникам подключатся к каналу,\n"
                          "а так же делать невидимым канал для участников.\n"
                          "Чтобы создать свой голосовой канал вам просто следует зайти в голосовой канал **[+] Создать голос**.",
                    inline=False)
    embed.add_field(name="🧩 Выдача ролей",
                    value="Так же есть канал под названием **определение-ролей**,\n"
                          "в нем есть сообщение в котором Emoji и напротив него написано какую роль дает этот Emoji,\n"
                          "если нажать эго под сообщением то вам будет выдана или убрана эта роль.", inline=False)
    embed.add_field(name="🧩 Пересылка телеграм",
                    value="Есть текстовый канал который полностью дублирует нашу универовскую телеграм группу.\n"
                          "Так же этот текстовый канал работает и в обратную сторону.", inline=False)
    embed.add_field(name="🧩 Игра в мафию",
                    value="Все вы знаете такую настольную игру как мафия,\n"
                          "вот мы ее скопировали и перенесли в дискорд,\n"
                          "так же добавили дополнительные роли которые сделают веселее вашу игру.\n"
                          "Все остальное вы узнаете в канале **мафия-текст**.", inline=False)
    # embed.add_field(name="🧩 Игры Discord и YouTube",
    #                 value="В дискорде появилась новая функция,\n"
    #                       "которая позволяет играть в игры вместе с учасниками голосового канала.\n"
    #                       "Эта функция находится в стадии разработки,\n"
    #                       "поэтому я реализовал ее с помощью бота.\n"
    #                       "Чтобы ее использовать введите `/game <activity>` - активность выбираете из списка.",
    #                 inline=False)
    # Или я или Дима потом сделает
    # embed.add_field(name="🧩 Игра в шпиона",
    #                 value="У нас есть так же игра шпион...\n"
    #                       "`Дима не забудь здесь написать какой-то текст.`", inline=False)
    embed.add_field(name="🧩 Посмотреть расписание",
                    value="Для нашего удобства в телеграме и здесь есть команды\n"
                          "которые помогут узнать расписание на дни учебы.\n"
                          "> Перечисление команд:\n"
                          "> `/now_day` - Показывает расписание на сегодняшний день.\n"
                          "> `/now_week` - Показывает расписание на эту неделю.\n"
                          "> `/next_week` - Показывает расписание на следующую неделю.\n", inline=False)
    # Нет возможности сделать
    # embed.add_field(name="🧩 Мероприятия по парам",
    #                 value="В случаях когда у нас наступает дистанционка, я буду создавать вам мероприятия по парам.\n"
    #                       "За день до будут создаваться в дискорде ячейки мероприятий которые будут в себе вмещать название,\n"
    #                       "время и остальную важную информацию по паре.", inline=False)

    # Посчитали ненужным
    # embed.add_field(name="🧩 Система балов",
    #                 value="Так как из за использования не по назначению своих возможностей на сервере,\n"
    #                       "у нас вводится система балов за которую вы будете получать разные плюшки.\n"
    #                       "Система будет работать по принципу: Заработал - используй.\n"
    #                       "То есть вы можете копить на разные плюшки которые описаны в канале **плюшки-за-балы**.\n"
    #                       "Как получать балы так же написано в том канале.", inline=False)
    embed.set_footer(text="Zebaro, а так же помощник WHITE",
                     icon_url="https://cdn.discordapp.com/avatars/294549334165291009/1d29952ac10200ea8acbcc3f939ff90a.webp")
    await ctx.reply(embed=embed)
