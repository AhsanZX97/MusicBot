import sys
import spotipy
import spotipy.util as util
from apikey import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, DISCORD_TOKEN
import discord
from db import db

client = discord.Client()

global sp, token, playlist

token = util.prompt_for_user_token("kingpiccy", "playlist-modify-public playlist-modify-private",
                                   client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri='http://localhost:8080/')
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

    if message.content == '?test':
        await message.channel.send(db.list_collection_names())

    if message.content.startswith('?create '):
        if playlist is None:
            msg = message.content[8:].strip()
            if len(msg) > 50:
                await message.channel.send("playlist name needs to be less than 50 characters")
            else:
                playlist = sp.user_playlist_create(
                    user="kingpiccy", name=msg, public=True)
                info = {'id': playlist['id'], 'users': []}
                db.history.insert_one(info)
                await message.channel.send("Playlist created: " + playlist['external_urls']['spotify'])
                await message.channel.send("type ?end to end this playlist adding session")
        else:
            await message.channel.send("There is already a playlist in session")
    if message.content.startswith('?add '):
        if playlist is None:
            await message.channel.send("No playlist in session")
        else:
            msg = message.content[5:].strip()
            track = sp.search(q=msg, limit=1, type='track')
            if len(track['tracks']['items']) == 0:
                await message.channel.send("Song not found, learn to type you bozo")
            else:
                track_uri = [track['tracks']['items'][0]['uri']]
                users = db.history.find_one({'id': playlist['id']})['users']
                addUser = {}
                notFound = True
                for user in users:
                    if user['id'] == message.author.id:
                        if len(user['song']) >= 3:
                            await message.channel.send("You have already added 3 songs to the playlist")
                            return
                        else:
                            notFound = False
                            user['song'].append(track_uri[0])
                            addUser = {
                                '$set': {'users': [{'id': message.author.id, 'song': user['song']}]}}
                if notFound:
                    addUser = {
                        '$set': {'users': [{'id': message.author.id, 'song': [track_uri[0]]}]}}
                db.history.update_one({'id': playlist['id']}, addUser)
                sp.user_playlist_add_tracks(
                    "kingpiccy", playlist['id'], track_uri)
                await message.channel.send("Song added: " + track['tracks']['items'][0]['external_urls']['spotify'])

    if message.content == '?end':
        await message.channel.send("Playlist adding session has been ended. Here is the final playlist: " + playlist['external_urls']['spotify'])
        playlist = None
    if message.content.startswith('?remove '):
        if playlist is None:
            await message.channel.send("No playlist in session")
        else:
            msg = message.content[8:].strip()
            if msg not in ["1", "2", "3"]:
                await message.channel.send("To remove a track, specify the order of number you want to remove. e.g 1 is the first track you added and 3 is the last")
                return
            num = int(msg)
            users = db.history.find_one({'id': playlist['id']})['users']
            addUser = {}
            uri = ""
            notFound = True
            for user in users:
                if user['id'] == message.author.id:
                    notFound = False
                    if num > len(user['song']):
                        await message.channel.send("You haven't added " + num + "songs")
                        return
                    uri = user['song'][num-1] # spotipy.exceptions.SpotifyException: http status: 400, code:-1 - https://api.spotify.com/v1/users/kingpiccy/playlists/1I4yio3w1G34CpbgIqeCNX/tracks: JSON body contains an invalid track uri: spotify:track:s
                    del user['song'][num-1]
                    addUser = {'$set': {'users': [{'id': message.author.id, 'song': user['song']}]}}
            if notFound:
                await message.channel.send("You haven't even added a track")
                return
            db.history.update_one({'id': playlist['id']}, addUser)
            sp.user_playlist_remove_all_occurrences_of_tracks("kingpiccy", playlist['id'], uri)
            await message.channel.send("Song removed")
    if message.content.startswith('?view '):
        msg = message.content[6:].strip()
        playlists = sp.current_user_playlists(limit=50, offset=0)['items']
        found = False
        for p in playlists:
            if p['name'] == msg:
                found = True
                await message.channel.send(p['external_urls']['spotify'])
        if found == False:
            await message.channel.send('Playlist not found')
    if message.content == '?current':
        if playlist is None:
            await message.channel.send("No playlist in session")
        else:
            await message.channel.send("Current playlist in session: " + playlist['external_urls']['spotify'])
    if message.content.startswith('?modify '):
        msg = message.content[8:].strip()
        playlists = sp.current_user_playlists(limit=50, offset=0)['items']
        found = False
        for p in playlists:
            if p['name'] == msg:
                found = True
                await message.channel.send("Now modifiying playlist: " + p['external_urls']['spotify'])
                playlist = p
        if found == False:
            await message.channel.send('Playlist not found')

client.run(DISCORD_TOKEN)
