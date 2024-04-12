from os import getenv

# <----Global Configs---->
DISCORD_API = getenv("DISCORD_API")
TELEGRAM_API = getenv("TELEGRAM_API")

discord_guild = 883022109599760434

# <----Discord Configs---->
# {Global}
discord_color = 14480382  # 279628  # Можно поменять
activityText = "microwave phonk"

# {Roles}
role_channel_id = 883051068152512562
role_message_id = 1167189883761217610

ROLES = {
    "👥": 1167188980580765746,  # mafia
    "🔫": 1167189103977181184,  # cs:go
    "⛏": 1167189176106623117,  # minecraft
    "🧑‍🎤": 1167189304259391518,  # genshin impact
    "🎲": 1167189472761364621,  # games
    "📻": 1167189510510084166,  # voice
}

# {Music}
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

music_channel_id = 883064876472348692

music_colour = 7506394
music_button_colour = 1  # blurple

# {Mafia}
mafia_channel_id = 1167191796577742919
mafia_channel_webhook = "1167191524577136670/rizv3WLUMiNmpK2tks4tGVdTFT99g8gTjWS3xtXAliYta_9aDhoAp9Pfq3cWGodBQzl5"  # noqa
mafia_chat = 1167191850612949093
mafia_statistics = 1167192140145754152
mafia_voice_channel_id = 1167192252578267196
mafia_color = 10038562
mafia_button_colour = 4
mafia_players = {}

# {Create Voice}
create_category = 1167195220270649384
create_text = 915267141182316604
create_voice = 1167195436281503776

# {Version}
version_channel = 883022109599760437

# <----Telegram Configs---->
# {Timetable}
timetable_time = ["08:00 - 09:20",
                  "09:40 - 11:00",
                  "11:25 - 12:45",
                  "13:10 - 14:30",
                  "14:50 - 16:10",
                  "16:25 - 17:45",
                  "18:00 - 19:20"]

# <----General---->
tg_chanel_id = -1001561199499
ds_chanel_id = 1025712585447854172  # ❗️
ds_chanel_webhook = "1025712749298319420/3t-DxmbpadaxqhbqqlYCui2KBfLyjKh0WmVKFcQO3z-kQZ5fI75tRwkecN1UnhEKe0xa"  # for telegram # noqa  # ❗️
ds_bug_channel = 883022109599760437
distance_learning = True

# {Database}
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT"))

# <----Debug Configs---->
debug = True if getenv("DEBUG") == "TRUE" else False
server_bool = True if getenv("SERVER") == "TRUE" else False

server_address = getenv("SERVER_ADDRESS")
webhook_tg_port = int(getenv("UNIVER_MODER_TG_PORT"))
webhook_ds_port = int(getenv("UNIVER_MODER_DS_PORT"))

if debug:
    from config_debug import *  # noqa
