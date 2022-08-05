from config import client_id, client_secret
import tekore as tk
from math import ceil
import discord
import wavelink

playlist = []
details_player = {"status": "play", "volume": "low"}
position = 0

spotify = tk.Spotify(tk.request_client_token(client_id, client_secret))


async def read_url(url):
    if url[:25] == "https://open.spotify.com/":
        read_spotify(url)
    elif url[:24] == "https://www.youtube.com/":
        await read_youtube(url)
    else:
        await read_youtube(url)


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
        spotify_add(track)


def spotify_add(track):
    artists = ""
    for i in track.artists:
        artists += f"{i.name}, "
    artists = artists[:-2]

    track_for_playlist = {"name": track.name,
                          "artists": artists,
                          "time": ceil(track.duration_ms / 1000),
                          "img": track.album.images[0].url}
    playlist.append(track_for_playlist)


async def read_youtube(url):
    track = await wavelink.YouTubeTrack.search(url, return_first=True)
    track_for_playlist = {"name": track.title,
                          "artists": track.author,
                          "time": ceil(track.duration),
                          "img": track.thumb}
    playlist.append(track_for_playlist)


def read_status(member: discord.member.Member):
    for activity in member.activities:

        if str(activity.type) == "ActivityType.listening" and activity.name == "Spotify":
            track = spotify.track(activity.track_id)

            spotify_add(track)


def streem_youtube():
    pass
