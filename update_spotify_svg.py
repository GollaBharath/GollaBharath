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
    is_playing = bool(track_data)
    song_text = "Now Playing" if is_playing else "Offline"
    right_color = "#1DB954" if is_playing else "#9e9e9e"
    circle_color = "#ffffff" if is_playing else "#2e2e2e"
    circle_border = "#0f0f0f" if is_playing else "#5e5e5e"

    svg = f'''<svg width="180" height="28" viewBox="0 0 180 28" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="180" height="28" rx="6" fill="#1DB954"/>
  <rect x="90" y="0" width="90" height="28" rx="6" fill="{right_color}"/>
  <text x="12" y="18" fill="white" font-family="Segoe UI, sans-serif" font-size="13" font-weight="bold">Spotify</text>
  <circle cx="108" cy="14" r="5" fill="{circle_color}" stroke="{circle_border}" stroke-width="2"/>
  <text x="120" y="18" fill="white" font-family="Segoe UI, sans-serif" font-size="13">{song_text}</text>
</svg>
'''
    with open("spotify-status.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    token = get_access_token()
    track_data = get_current_playing(token)
    generate_svg(track_data)

if __name__ == "__main__":
    main()
