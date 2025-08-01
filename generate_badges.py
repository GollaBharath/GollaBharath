import requests
import json
import os

api_key = os.getenv("WAKATIME_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Create badges folder if not exists
os.makedirs("badges", exist_ok=True)

# 1. Total Code Time (last 7 days)
res = requests.get("https://wakatime.com/api/v1/users/current/stats/last_7_days", headers=headers)
total_time = res.json()["data"]["human_readable_total"]

with open("badges/total_time.json", "w") as f:
    json.dump({
        "schemaVersion": 1,
        "label": "Code Time",
        "message": total_time,
        "color": "blue"
    }, f)

# 2. All-time lines of code
res = requests.get("https://wakatime.com/api/v1/users/current/all_time_since_today", headers=headers)
loc = f'{res.json()["data"]["total_lines"]:,} LOC'

with open("badges/loc.json", "w") as f:
    json.dump({
        "schemaVersion": 1,
        "label": "Lines of Code",
        "message": loc,
        "color": "green"
    }, f)
