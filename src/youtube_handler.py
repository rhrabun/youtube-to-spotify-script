import os
from colorama import Fore, Style

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class YoutubeHandler(object):
    def __init__(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "youtube_client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)


    def get_playlists(self):
        request = self.youtube.playlists().list(
            part="snippet,contentDetails",
            maxResults=50,
            mine=True
        )
        response = request.execute()

        playlists_dict = {}

        for index, item in enumerate(response['items']):
            playlist_name = item['snippet']['title']
            playlist_id = item['id']

            playlists_dict.update({playlist_name: playlist_id})

        return playlists_dict


    def get_songs_in_playlist(self, playlists_dict):
        # Array containing all playlists with all videos - [{playlist: ['title1', 'title2']}, ...]
        all_videos_in_playlists_array = []

        youtube_vid_url = 'https://www.youtube.com/watch?v='

        for playlist_name, playlist_id in playlists_dict.items():
            print(Fore.GREEN +
                  f'Scanning playlist "{playlist_name}"' + Style.RESET_ALL)
            # Array of videos for one particular playlist
            videos_array = []

            # Get first 50 videos in playlist
            request = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=50,
                playlistId=playlist_id
            )
            response = request.execute()

            for item in response['items']:
                song_title = item['snippet']['title']
                song_url = youtube_vid_url + item['contentDetails']['videoId']
                videos_array.append(song_title)

            # If there are more than one page - parse through all of them
            nextPageToken = ''

            try:
                nextPageToken = response['nextPageToken']
                print('Finished first page, moving to second')
            except KeyError:
                print('Only one page of songs')

            while nextPageToken:
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    maxResults=50,
                    pageToken=nextPageToken,
                    playlistId=playlist_id
                )
                response = request.execute()
                # print(response)

                for item in response['items']:
                    song_title = item['snippet']['title']
                    song_url = youtube_vid_url + \
                        item['contentDetails']['videoId']

                    videos_array.append(song_title)

                try:
                    nextPageToken = response['nextPageToken']
                    print('finished another page, moving forward')
                except KeyError:
                    print('Finished last page in playlist')
                    nextPageToken = None

            all_videos_in_playlists_array.append({playlist_name: videos_array})
            print(
                Fore.RED + f'Finished scanning playlist "{playlist_name}"\n' + Style.RESET_ALL)

        print(Fore.CYAN + 'Finished scanning all playlists' + Style.RESET_ALL)
        
        return all_videos_in_playlists_array


    def main(self):
        playlists_dict = self.get_playlists()

        all_videos_in_playlists_array = self.get_songs_in_playlist(
            playlists_dict)

        return all_videos_in_playlists_array
