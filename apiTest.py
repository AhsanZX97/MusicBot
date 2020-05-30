import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from apikey import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET
import spotipy.util as util
import json

import pprint

#client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,)
#token = client_credentials_manager.get_access_token()

token = util.prompt_for_user_token("kingpiccy","playlist-modify-public playlist-modify-private",client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri='http://localhost:8080/') 
sp = spotipy.Spotify(auth=token)
track = sp.search(q='baby powder jenevieve', limit=1,type='track')
track_uri = [ track['tracks']['items'][0]['uri'] ]

#sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#results = sp.search(q='offset', limit=1,type='artist')
#artistId = results['artists']['items'][0]['id']
#latestRelease = sp.artist_albums(artistId,country='US',limit=1)
#print(latestRelease)




playlist = sp.user_playlist_create(user="kingpiccy",name="Test playlist")

sp.user_playlist_add_tracks("kingpiccy", playlist['id'], track_uri)
