from src.youtube_handler import YoutubeHandler
from src.spotify_handler import SpotifyHandler


def main():
    youtube = YoutubeHandler()

    all_songs_arr = youtube.main()

    spotify = SpotifyHandler()

    spotify.main(all_songs_arr)


if __name__ == "__main__":
    main()
