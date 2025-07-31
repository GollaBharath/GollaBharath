from datetime import datetime
import pytz

def generate_time_svg():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    time_str = now.strftime("%I:%M %p")  # Example: 01:34 PM

    svg = f"""<svg width="160" height="40" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="8" fill="#0f172a"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="monospace" font-size="14" fill="white">
    🕒 {time_str} IST
  </text>
</svg>
"""
    with open("local-time.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_time_svg()
