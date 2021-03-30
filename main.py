import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
USER_ID = os.getenv('USER_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

def generate_access_token():
    """Generate new access token"""

    url = f'https://accounts.spotify.com/api/token/'
    request_body={'grant_type':'refresh_token', 'refresh_token':REFRESH_TOKEN}
    response=requests.post(url, data=request_body, auth =(CLIENT_ID, CLIENT_SECRET))
    response_json = response.json()

    return response_json['access_token']


def generate_songs(genres="sleep", artists="2CiO7xWdwPMDlVwlt9qa1f,73aKnLT4O8G2pBEfdlQzrE,6TeBxtluBMQixZcKkJ3ZrB,6HCnsY0Rxi3cg53xreoAIm"):
    """
    Generate 50 random songs from seed_genres and seed_artists
    Genres and artists must be a comma separated string of ids or strings
    """
    access_token = generate_access_token()
    spotify_uris = []

    base_endpoint = "https://api.spotify.com/v1/recommendations?"
    limit = 50
    seed_genres = genres
    seed_artists = artists

    api_endpoint = f'{base_endpoint}limit={limit}&seed_genres={seed_genres}&seed_artists={seed_artists}'

    headers = {"Content-Type":"application/json", "Authorization":f"Bearer {access_token}"}
    response = requests.get(api_endpoint, headers = headers)

    json_response = response.json()

    for track in json_response["tracks"]:
        spotify_uris.append(track["uri"])

    return spotify_uris

def generate_playlist():

    access_token = generate_access_token()

    # Set up params to create playlist
    url = f"https://api.spotify.com/v1/users/{USER_ID}/playlists"
    headers = {"Content-Type":"application/json", "Authorization":f"Bearer {access_token}"}
    data = json.dumps({
        "name": "Nightly Generated Playlist v3",
        "public": False
    })

    # Create playlist
    response = requests.post(
        url=url,
        data=data,
        headers=headers
        )


    # Select created playlist by id
    playlist_id = response.json()['id']
    playlist_endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    # Set up params
    request_body = json.dumps({
        "uris": generate_songs()
    })

    response = requests.post(
        url=playlist_endpoint_url,
        data=request_body,
        headers=headers
        )
    
def get_playlist_song_uris():

    song_uris = []
    access_token = generate_access_token()
    playlist_id = "6kbIK82rzYl7coLLjPcAtE" 
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization":f"Bearer {access_token}"}

    response = requests.get(url=playlist_url, headers=headers)
    json_response = response.json()


    for song in json_response['items']:
        song_uris.append(song['track']['uri'])

    return song_uris
    

def delete_songs_in_playlist():

    song_uris = get_playlist_song_uris()



get_playlist_song_uris()