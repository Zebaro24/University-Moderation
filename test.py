import requests
from config import DISCORD_API

api = "fltz8l4gcuyuzsr38bw0ceo3t58pn28v4agzsv35j1ictpsplwcuonde796ecbrw"

url = 'https://w2g.tv/rooms/create.json'
body = {"w2g_api_key": api,
        "share": "https://www.youtube.com/watch?v=3y3DlxDsh0Y",
        "bg_color": "#00ff00",
        "bg_opacity": "50"}


x = requests.post(url, json=body).json()
print(x)
print(f"https://w2g.tv/rooms/{x['streamkey']}")
