import requests as r
import os
import time
from colorama import Fore, Style

import secrets

import spotipy
import spotipy.util as util

username = secrets.spotify_username


not_added_songs = []


class SpotifyHandler(object):
    def __init__(self):
        scope = 'playlist-modify-public'

        try:
            token = util.prompt_for_user_token(username, scope)
        except:
            os.remove(f'cache-{username}')
            token = util.prompt_for_user_token(username)

        self.spotifyObject = spotipy.Spotify(auth=token)


    def create_playlist(self, playlist_name):
        response = self.spotifyObject.user_playlist_create(
            username,
            playlist_name)
        print(
            Fore.GREEN + f'Created playlist {playlist_name} with id {response["id"]}' + Style.RESET_ALL)

        return response['id']


    def search_song(self, song_title):
        print(f'Searching for song "{song_title}"')
        response = self.spotifyObject.search(song_title, type="track")

        song_id = ''
        try:
            song_id = response['tracks']['items'][0]['id']
            print(f'Song id is {song_id}')
        except IndexError:
            print(
                Fore.RED + f'Could not find track with title "{song_title}"' + Style.RESET_ALL)
            song_id = None

        return song_id


    def add_to_playlist(self, playlist_id, songs_arr):
        for song in songs_arr:
            song_id = self.search_song(song)
            if song_id:
                response = self.spotifyObject.user_playlist_add_tracks(
                    username, playlist_id, [song_id])
                print(response)
            else:
                not_added_songs.append(song)


    def main(self, all_songs_arr):
        # [{'playlist_name1': ['song1', 'song2', 'song3']}, {'playlist_name2': ['song4', 'song5']}]

        # Get dict {'playlist_name1': ['song1', 'song2', 'song3']}
        for playlist_dict in all_songs_arr:
            # Get playlist name and songs array from dict
            for key in playlist_dict:
                playlist_name = key
                songs_arr = playlist_dict[playlist_name]
                playlist_id = self.create_playlist(playlist_name)
                try:
                    self.add_to_playlist(playlist_id, songs_arr)
                except:
                    print('API Rate exceeded, waiting 10 sec')
                    time.sleep(10)

        print("Couldn't add these songs:")
        print(not_added_songs)
