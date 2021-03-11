from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
id = "a6edcfd7ffa64322a8dbf87ef7cc924e"
secret = "6a75648b949d457cbc91474ae9b7523f"

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=id,
        client_secret=secret,
        redirect_uri="http://example.com/callback/",
        show_dialog=True,
        cache_path="token.txt"
))

user_id = sp.current_user()['id']
print(sp.current_user())


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]
year = date.split("-")[0]
song_url = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_url.append(uri)
    except IndexError:
        print(f"{song} not in spotify...")
playlist = sp.user_playlist_create(user=user_id, name=date + " Billboard 100", public=False, description='Top billboard songs in my birthday')

sp.user_playlist_add_tracks(user=id, playlist_id=playlist["id"], tracks=song_url)