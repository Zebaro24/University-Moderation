from os import environ

# <----Global Configs---->
DISCORD_API = "<DISCORD_API>"  # "<DEBUG_DISCORD_API>" # noqa
TELEGRAM_API = ""  # "<DEBUG_2_TELEGRAM_API>" # noqa

discord_guild = 0  # <---Первоначальная замена

# <----Discord Configs---->
# {Global}
discord_color = 16777215  # Можно поменять

# {Roles}
role_channel_id = 0  # <---Первоначальная замена
role_message_id = 0  # Получим с roles/roles_first.py

ROLES = {
    "💻": 0,  # programming
    "🏳️‍🌈": 0,  # genshin
    "⛏": 0,  # minecraft
}

# {Music}
client_id = "<SPOTIFY_CLIENT_ID>"  # noqa
client_secret = "<SPOTIFY_CLIENT_SECRET>"  # noqa

music_channel_id = 0

music_colour = 7506394
music_button_colour = 1  # blurple

# {Mafia}
mafia_channel_id = 0  # <---Первоначальная замена
mafia_channel_webhook = ""
mafia_chat = 0
mafia_statistics = 0
mafia_voice_channel_id = 0
mafia_color = 10038562
mafia_button_colour = 4
mafia_players = {}

# {Create Voice}
create_category = 0
create_text = 0
create_voice = 0

# {Version}
version_channel = 0

# <----Telegram Configs---->
# {Timetable}
timetable_time = ["08:00 - 09:20", "09:40 - 11:00", "11:25 - 12:45", "13:10 - 14:30", "14:50 - 16:10", "16:25 - 17:45",
                  "18:00 - 19:20"]

# <----General---->
tg_chanel_id = 0  # -1001530372815
ds_chanel_id = 0
ds_chanel_webhook = ""  # for telegram
ds_bug_channel = 0
distance_learning = True

# {Database}
DB_NAME = '<DB_USER_NAME>'  # noqa
DB_USER = '<DB_USER_NAME>'  # noqa
DB_PASS = '<DB_PASS>'  # noqa
DB_HOST = '<DB_HOST>'  # noqa
DB_PORT = '"<DB_PORT>"'  # noqa

# <----Debug Configs---->
if "debug" in environ:
    debug = environ["debug"]
else:
    debug = True

if debug:
    from config_debug import *  # noqa
