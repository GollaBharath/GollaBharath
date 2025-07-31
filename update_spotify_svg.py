import os
import requests
import base64

def get_access_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

    token_url = "https://accounts.spotify.com/api/token"
    credentials = f"{client_id}:{client_secret}"
    headers = {
        "Authorization": "Basic " + base64.b64encode(credentials.encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()["access_token"]

def get_current_playing(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    response = requests.get(url, headers=headers)
    if response.status_code == 204:
        return None
    response.raise_for_status()
    return response.json()

def generate_svg(track_data):
    if not track_data:
        title = "Not Listening"
        artist = ""
    else:
        item = track_data["item"]
        title = item["name"]
        artist = ", ".join(artist["name"] for artist in item["artists"])

    svg = f"""<svg width="300" height="60" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#1DB954" rx="8"/>
  <text x="10" y="25" font-size="14" fill="white" font-family="Verdana">🎵 Spotify Now Playing</text>
  <text x="10" y="45" font-size="12" fill="white" font-family="Verdana">{title} - {artist}</text>
</svg>
"""
    with open("spotify-status.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    token = get_access_token()
    track_data = get_current_playing(token)
    generate_svg(track_data)

if __name__ == "__main__":
    main()
