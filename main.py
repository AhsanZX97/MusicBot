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
        msg = message.content[8:]
        if len(msg) > 50:
            await message.channel.send("playlist name needs to be less than 50 characters")
        else:
            playlist = sp.user_playlist_create(user="kingpiccy",name=msg,public=True)
            await message.channel.send("Playlist created: " + playlist['external_urls']['spotify'])

client.run(DISCORD_TOKEN)