from telebot import TeleBot

TELEGRAM_API = "<DEBUG_2_TELEGRAM_API>"  # noqa

bot = TeleBot(TELEGRAM_API)
tg_chanel_id = -1001530372815

# while True:
#     text = input("Текст: ")
#     bot.send_message(id_channel, text)

bot.send_message(tg_chanel_id, "*В бота было добавлено расписание на следующую неделю, можете пользоваться.*\n\n"
                               "*Было сокращено написания таких пар:*\n"
                               "\"БЖ та ОХП\" - Безпека життєдіяльності та основи охорони праці\n"
                               "\"ОВТ та М\" - Основи вимірювальної техніки та метрології\n\n"
                               "Удачи в учебе\nZebaro😉",
                 parse_mode='Markdown')
