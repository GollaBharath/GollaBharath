from datetime import datetime
import pytz

# Set IST timezone
tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(tz)
current_time = now.strftime("%I:%M %p")  # Format: 01:23 PM

# Badge content
label = "🕛 Local Time"
message = current_time

# Colors and SVG style
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
</svg>
"""

# Write to SVG file
with open("local-time.svg", "w", encoding="utf-8") as f:
    f.write(svg)
