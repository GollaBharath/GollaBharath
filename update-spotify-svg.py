import requests
import base64
import json
from datetime import datetime

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REFRESH_TOKEN = "your_refresh_token"

SVG_PATH = "spotify-status.svg"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

def get_current_track(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if r.status_code == 204:
        return None
    return r.json()

def generate_svg(track_data):
    if not track_data:
        text = "Not listening to anything"
    else:
        song = track_data["item"]["name"]
        artist = ", ".join([a["name"] for a in track_data["item"]["artists"]])
        text = f"🎵 {song} — {artist}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="50">
  <rect width="100%" height="100%" fill="#1DB954" rx="10"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="14" font-family="monospace">{text}</text>
</svg>'''
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    token = get_access_token()
    track = get_current_track(token)
    generate_svg(track)

if __name__ == "__main__":
    main()
