import sys
import spotipy
import spotipy.util as util
from apikey import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,DISCORD_TOKEN
import discord

client = discord.Client()

global sp, token, playlist

token = util.prompt_for_user_token("kingpiccy","playlist-modify-public playlist-modify-private",client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri='http://localhost:8080/') 
sp = spotipy.Spotify(auth=token)

playlist = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global playlist

    if message.author == client.user:
        return

    if message.content.startswith('?create '):
        if playlist is None:
            msg = message.content[8:]
            if len(msg) > 50:
                await message.channel.send("playlist name needs to be less than 50 characters")
            else:
                playlist = sp.user_playlist_create(user="kingpiccy",name=msg,public=True)
                await message.channel.send("Playlist created: " + playlist['external_urls']['spotify'])
                await message.channel.send("type ?end to end this playlist adding session")
        else:
            await message.channel.send("There is already a playlist in session")
    if message.content.startswith('?add '):
        if playlist is None:
            await message.channel.send("No playlist in session")
        else:
            msg = message.content[5:]
            track = sp.search(q=msg, limit=1,type='track')
            track_uri = [ track['tracks']['items'][0]['uri'] ]
            sp.user_playlist_add_tracks("kingpiccy", playlist['id'], track_uri)
            await message.channel.send("Song added: " + track['tracks']['items'][0]['external_urls']['spotify'])
    if message.content == '?end':
        await message.channel.send("Playlist adding session has been ended. Here is the final playlist: " + playlist['external_urls']['spotify'])
        playlist = None
    if message.content.startswith('?remove '):
        if playlist is None:
            await message.channel.send("No playlist in session")
        else:
            msg = message.content[8:]
            track = sp.search(q=msg, limit=1,type='track')
            track_uri = [ track['tracks']['items'][0]['uri'] ]
            sp.user_playlist_remove_all_occurrences_of_tracks("kingpiccy",playlist['id'],track_uri)
            await message.channel.send("Song removed")

client.run(DISCORD_TOKEN)