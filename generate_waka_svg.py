import requests
import os

api_key = os.getenv("WAKATIME_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}

os.makedirs("badges", exist_ok=True)

# Get Total Code Time
try:
    res = requests.get("https://wakatime.com/api/v1/users/current/stats/last_7_days", headers=headers)
    res.raise_for_status()
    code_time = res.json()["data"]["human_readable_total"]
except Exception as e:
    code_time = "N/A"

# Get Total LOC
try:
    res = requests.get("https://wakatime.com/api/v1/users/current/all_time_since_today", headers=headers)
    res.raise_for_status()
    loc = f'{res.json()["data"]["total_lines"]:,} LOC'
except Exception as e:
    loc = "N/A"

def make_svg(label, message, filename):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="190" height="28">
  <linearGradient id="grad" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#2b2b2b" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect rx="5" width="190" height="28" fill="#21262d"/>
  <rect rx="5" width="95" height="28" fill="#2d333b"/>
  <rect rx="5" x="95" width="95" height="28" fill="#21262d"/>
  <path fill="url(#grad)" d="M0 0h190v28H0z"/>
  <g fill="#fff" text-anchor="middle"
     font-family="Segoe UI, Ubuntu, sans-serif"
     font-size="13">
    <text x="47.5" y="19" fill="#c9d1d9">{label}</text>
    <text x="142.5" y="19" fill="#fff">{message}</text>
  </g>
</svg>"""
    with open(f"badges/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)

make_svg("💻 Code Time", code_time, "waka-code-time.svg")
make_svg("📈 LOC", loc, "waka-loc.svg")
