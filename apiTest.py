import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from apikey import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET
import spotipy.util as util
import json

import pprint

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
token = client_credentials_manager.get_access_token()
sp = spotipy.Spotify(auth=token)
print(sp.me())
#sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#results = sp.search(q='offset', limit=1,type='artist')
#artistId = results['artists']['items'][0]['id']
#latestRelease = sp.artist_albums(artistId,country='US',limit=1)
#print(latestRelease)




#sp.user_playlist_create(user="kingpiccy",name="Test playlist",)