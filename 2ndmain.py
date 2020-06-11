import sys
import spotipy
import spotipy.util as util
from apikey import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, DISCORD_TOKEN, USERNAME
import discord
from db import db

client = discord.Client()

global sp, token, playlist

token = util.prompt_for_user_token("kingpiccy", "playlist-modify-public playlist-modify-private",client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri='http://localhost:8080/')
sp = spotipy.Spotify(auth=token)

playlist = None
total = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global playlist, total

    if message.author == client.user:
        return

    if "music.apple.com" in message.content:
        await message.channel.send(len(message.embeds))
        for embed in message.embeds:
            await message.channel.send(embed.title.split(" ").join("%20").split("%20by%20"))

client.run(DISCORD_TOKEN)