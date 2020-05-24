import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from apikey import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET
import json

import pprint

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

results = sp.search(q='weezer', limit=20,type='track')
print(results['tracks']['items'])