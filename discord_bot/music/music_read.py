from ...config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, discord_guild, music_channel_id
from ..main_discord import bot

from discord import Member
from wavelink import YouTubePlaylist, YouTubeTrack

from math import ceil
import tekore as tk

playlist = []
details_player = {"status": "play", "volume": "low"}
position = 0

spotify = tk.Spotify(tk.request_client_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))


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


async def read_youtube(url, stream=False):
    # ----------------------------------------Нужен фикс (возможно пофиксил)----------------------------------------
    try:
        tracks_search = await YouTubeTrack.search(url)
    except Exception as error:
        print(f"Error read_youtube: {error}")
        await bot.get_guild(discord_guild).get_channel(music_channel_id).send(
            "Не валидная ссылка...", delete_after=3)
        return
    if not tracks_search:
        await bot.get_guild(discord_guild).get_channel(music_channel_id).send(
            " Трек не был найден на YouTube...", delete_after=3)
        return
    if type(tracks_search) == YouTubePlaylist:
        # noinspection PyTypeChecker
        youtube_playlist: YouTubePlaylist = tracks_search
        tracks = youtube_playlist.tracks
    else:
        tracks = [tracks_search[0]]
        if stream:
            return tracks[0]

    for track in tracks:
        track_for_playlist = {"name": track.title,
                              "artists": track.author,
                              "time": ceil(track.duration),
                              "img": track.thumb,
                              "track": track}
        playlist.append(track_for_playlist)
    # ------------------------------------------------------------------------------------------


def read_status(member: Member):
    for activity in member.activities:

        if str(activity.type) == "ActivityType.listening" and activity.name == "Spotify":
            track = spotify.track(activity.track_id)

            spotify_add(track)


def streem_youtube():
    pass
