import os
import requests
import base64
import html

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

    if is_playing:
        song_name = track_data["item"]["name"]
        artists = ", ".join([artist["name"] for artist in track_data["item"]["artists"]])
        song_text = f"{song_name} - {artists}"
    else:
        song_text = "Offline"

    song_text = html.escape(song_text)

    left_color = "#555555"
    right_color = "#1DB954" if is_playing else "#9e9e9e"
    text_color = "#ffffff"

    base_width = 120
    char_width = 7
    text_length = len(song_text) * char_width
    total_width = max(240, base_width + text_length + 20)

    marquee_svg = ""
    if len(song_text) > 30 and is_playing:
        marquee_svg = f'''
        <g transform="translate({base_width}, 0)">
            <text y="19" fill="{text_color}">
                <tspan>
                    <animate attributeName="x" from="{total_width}" to="-{text_length}" dur="10s" repeatCount="indefinite" />
                    {song_text}
                </tspan>
            </text>
        </g>
        '''
        text_element = ""  # Don't show static text if marquee is active
    else:
        text_element = f'<text x="{base_width + 5}" y="19" fill="{text_color}">{song_text}</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="28">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="{total_width}" height="28" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="{base_width}" height="28" fill="{left_color}"/>
    <rect x="{base_width}" width="{total_width - base_width}" height="28" fill="{right_color}"/>
    <rect width="{total_width}" height="28" fill="url(#b)"/>
  </g>
  <g fill="{text_color}" font-family="Segoe UI, sans-serif" font-size="13">
    <text x="10" y="19" fill="{text_color}">Spotify</text>
    {text_element}
    {marquee_svg}
  </g>
</svg>'''

    with open("spotify-status.svg", "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    token = get_access_token()
    track_data = get_current_playing(token)
    generate_svg(track_data)

if __name__ == "__main__":
    main()
