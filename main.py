import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from apikey import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,DISCORD_TOKEN
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(DISCORD_TOKEN)