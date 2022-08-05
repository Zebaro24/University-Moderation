import requests
from config import DISCORD_API
from time import sleep

# 1) Watch Together
# 2) Word Snacks
# 3) Sketch Heads
# 4) Know What I Meme
# 5) Ask Away

# https://gist.github.com/GeneralSadaf/42d91a2b6a93a7db7a39208f2d8b53ad
target_id = [880218394199220334, 879863976006127627, 902271654783242291, 950505761862189096, 976052223358406656]

url = 'https://discord.com/api/v8/channels/994019845597298711/invites'
body = {"max_age": 300,
        "max_uses": 0,
        "target_application_id": target_id[0],
        "target_type": 2,
        "temporary": True}
headers = {
    'authorization': f"Bot {DISCORD_API}"
}
for i in target_id:
    body["target_application_id"] = i
    x = requests.post(url, json=body, headers=headers)
    print(f"https://discord.gg/{x.json()['code']}")

