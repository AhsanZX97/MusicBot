import spotipy
from apikey import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET
import spotipy.util as util

token = util.prompt_for_user_token("kingpiccy","playlist-modify-public playlist-modify-private",client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri='http://localhost:8080/') 
sp = spotipy.Spotify(auth=token)
track = sp.search(q='baby powder jenevieve', limit=1,type='track')
track_uri = [ track['tracks']['items'][0]['uri'] ]

playlist = sp.user_playlist_create(user="kingpiccy",name="Test playlist")

sp.user_playlist_add_tracks("kingpiccy", playlist['id'], track_uri)
