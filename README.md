# Youtube to Spotify script

## Description
The idea of the script is to help to move to Spotify service without spending lots of time synchronizing music between Youtube and Spotify. Script will scan Youtube account, find all playlists and create same playlists in Spotify

###### Note, that due to differences in Youtube videos names a lot of videos won't be found in Spotify.

## Usage
1. Configure credentials in Google API Console(token - not sure if needed and Oauth secrets)
2. Download client secrets file from console(`youtube_client_secret.json`)
1. Create `secrets.py` file in root folder
3. Fill in Spotify username as defined in `example.secrets.py`
4. Run `main.py`.

## Requirements
* Python3.7+ ([See here how to additionally install new version of Python without breaking dependencies](https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/))
* Modules from `requirements.txt` file
