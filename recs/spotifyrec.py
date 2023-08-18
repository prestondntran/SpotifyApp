import datetime
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

# activate virtual environment
# source /Users/prestontran/Desktop/CSProjects/SpotifyApp/venv/bin/activate

# initializes spotify
def initSpotify():
    global cid, secret, spotify, accessToken, tokenExpire, tokenUrl
    cid = "ae328a2376be443b8900255a982bdfa4"
    secret = "ad93d72f6c484783aaf8f27a39646b4b"
    spotify = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret))

    accessToken = None
    tokenExpire = datetime.datetime.now()
    tokenUrl = "https://accounts.spotify.com/api/token"

    authorize()

# request an access token if token has expired
def authorize():
    global accessToken, tokenExpire
    url = tokenUrl
    data = f"grant_type=client_credentials&client_id={cid}&client_secret={secret}"
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}

    response = requests.post(url, data = data, headers = headers)

    # gets new token and time until expiration
    data = response.json()
    token = data["access_token"]
    expires = datetime.datetime.now() + datetime.timedelta(seconds = data['expires_in'])
    accessToken = token
    tokenExpire = expires

# checks if token has expired and requests if necessary
def getToken():
    global accessToken, tokenExpire
    now = datetime.datetime.now()
    if tokenExpire < now or accessToken == None:
        authorize()
        return getToken()
    return accessToken

# gets artist ID given name
def getArtistId(name, index):
    #getToken()
    response = spotify.search(name, 10, 0, "artist", None)
    return response["artists"]["items"][int(index)]["id"]

# gets track ID given name
def getTrackId(name, index):
    #getToken()
    response = spotify.search(name, 10, 0, "track", None)
    return response["tracks"]["items"][int(index)]["id"]

# search for tracks based on query
def search(name, searchType):
    #getToken()
    response = spotify.search(name, 10, 0, searchType, None)
    allTracks = []
    if (searchType == "track"):
        # loop through tracks and get metadata
        for i in range(len(response['tracks']['items'])):
            track_name = response['tracks']['items'][i]['name']
            artist_name = response['tracks']['items'][i]['artists'][0]['name']
            try:
                image = response['tracks']['items'][i]['album']['images'][0]['url']
            except IndexError:
                image = ""

            tracks = [track_name, artist_name, image]
            allTracks.append(tracks)
    elif (searchType == "artist"):
        # loop through artists and get metadata
        for i in range(len(response['artists']['items'])):
            artist_name = response['artists']['items'][i]['name']
            try:
                image = response['artists']['items'][i]['images'][0]['url']
            except IndexError:
                image = ""

            tracks = [artist_name, image]
            allTracks.append(tracks)

    return allTracks

# gets song recommendations based on specified parameters
def getRecs(name, index, searchType):
    #getToken()
    initSpotify()
    recs = []

    # get recommendations based on search type
    if (searchType == "artist"):
        response = spotify.recommendations(seed_artists = [getArtistId(name, index)], limit = 10)
    elif (searchType == "track"):
        response = spotify.recommendations(seed_tracks = [getTrackId(name, index)], limit = 10)
    else:
        response = spotify.recommendations(seed_genres = [name], limit = 10)

    # loop through tracks and get metadata
    if response:
        for i in range(len(response['tracks'])):
            track_name = response['tracks'][i]['name']
            artist_name = response['tracks'][i]['artists'][0]['name']
            image = response['tracks'][i]['album']['images'][0]['url']

            tracks = [track_name, artist_name, image]
            recs.append(tracks)

    return recs

# get available genre seeds
def getGenreSeeds():
    return spotify.recommendation_genre_seeds()