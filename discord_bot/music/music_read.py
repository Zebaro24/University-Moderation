from config import client_id, client_secret
import tekore as tk
from math import ceil
import yt_dlp

playlist = []
position = 0
spotify = tk.Spotify(tk.request_client_token(client_id, client_secret))
ydl_opts = {
    'format': 'bestaudio/best',
    "postprocessors":
        [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
}


def read_url(url):
    if url[:25] == "https://open.spotify.com/":
        read_spotify(url)
    elif url[:24] == "https://www.youtube.com/":
        read_youtube(url)


def read_spotify(url):
    if url[:31] == "https://open.spotify.com/track/":
        track_id = url[31:]
        spotify_playlist = [spotify.track(track_id)]
    elif url[:34] == "https://open.spotify.com/playlist/":
        playlist_id = url[34:]
        items = spotify.playlist(playlist_id).tracks.items
        spotify_playlist = [i.track for i in items]
    else:
        spotify_playlist = []

    for track in spotify_playlist:
        artists = ""
        for i in track.artists:
            artists += f"{i.name}, "
        artists = artists[:-2]

        '''text = f"ytsearch:{artists} - {track.name}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, False)
            print(info)
            streem = str(info["entries"][0]["formats"][3]["url"])'''

        track_for_playlist = {"name": track.name,
                              "artists": artists,
                              "time": ceil(track.duration_ms / 1000),
                              "img": track.album.images[0].url,
                              "streem": None}
        playlist.append(track_for_playlist)


def read_youtube(url):
    pass


def streem_youtube():
    pass
