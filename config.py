from os import environ

# <----Global Configs---->
DISCORD_API = "<DISCORD_API>"  # noqa
TELEGRAM_API = "<DEBUG_2_TELEGRAM_API>"  # noqa

discord_guild = 881075518336819221

# <----Discord Configs---->
# {Global}
discord_color = 14480382  # 279628  # Можно поменять
activityText = "microwave phonk"

# {Roles}
role_channel_id = 881077605506359316
role_message_id = 1025777450489221230

ROLES = {
    "👥": 1025707645644054548,  # mafia
    "🔫": 1025705324935659540,  # cs:go
    "⛏": 1025705144823857163,  # minecraft
    "🧑‍🎤": 1025705214768066630,  # genshin impact
    "🎲": 1025705637444857907,  # games
    "📻": 1025725215226986556,  # voice
}

# {Music}
client_id = "<SPOTIFY_CLIENT_ID>"  # noqa
client_secret = "<SPOTIFY_CLIENT_SECRET>"  # noqa

music_channel_id = 903714153515077705

music_colour = 7506394
music_button_colour = 1  # blurple

# {Mafia}
mafia_channel_id = 1025711413190201364
mafia_channel_webhook = "1025681370179178546/Shb8QpjkKun1HyZknXJgcsOE0_Xj9Esj6Oe6WhklEhTfHvCa96uCYGA_k1rqotXY_514"  # noqa
mafia_chat = 1025712176616448010
mafia_statistics = 1025712272334671942
mafia_voice_channel_id = 1025712410637643877
mafia_color = 10038562
mafia_button_colour = 4
mafia_players = {}

# {Create Voice}
create_category = 915265807762722846
create_text = 915267141182316604
create_voice = 915265808362508318

# {Version}
version_channel = 1025711214782840873

# <----Telegram Configs---->
# {Timetable}
timetable_time = ["08:00 - 09:20", "09:40 - 11:00", "11:25 - 12:45", "13:10 - 14:30", "14:50 - 16:10", "16:25 - 17:45",
                  "18:00 - 19:20"]

# <----General---->
tg_chanel_id = -1001530372815
ds_chanel_id = 1025712585447854172
ds_chanel_webhook = "1025712749298319420/3t-DxmbpadaxqhbqqlYCui2KBfLyjKh0WmVKFcQO3z-kQZ5fI75tRwkecN1UnhEKe0xa"  # for telegram # noqa
ds_bug_channel = 1025712937983279155
distance_learning = True

# {Database}
DB_NAME = '<DB_USER_NAME>'  # noqa
DB_USER = '<DB_USER_NAME>'  # noqa
DB_PASS = '<DB_PASS>'  # noqa
DB_HOST = '<DB_HOST>'  # noqa
DB_PORT = '"<DB_PORT>"'  # noqa

# <----Debug Configs---->
if "SERVER" in environ:
    debug = False
else:
    debug = True

if debug:
    from config_debug import *  # noqa
