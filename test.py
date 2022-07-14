import tekore as tk
import yt_dlp

client_id = "<SPOTIFY_CLIENT_ID>"
client_secret = "<SPOTIFY_CLIENT_SECRET>"

track_url = "https://open.spotify.com/track/4ZOjdqmXLuwHDQUn9WWoFR?si=1c74a00c69734a06"
if track_url[:31] == "https://open.spotify.com/track/":
    track_id = track_url[31:]
else:
    track_id = ""

spotify = tk.Spotify(tk.request_client_token(client_id, client_secret))
track = spotify.track(track_id)

text = "ytsearch:"

for i in track.artists:
    text += f"{i.name}, "
text = text[:-2]
text += f" - {track.name}"
print(text)
print(track.album.images[0].url)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(text, False)
    print(info["entries"][0]["formats"][3]["url"])
