import requests
import os

# --- Configuration ---
WAKATIME_API_KEY = os.getenv("WAKATIME_API_KEY")
HEADERS = {"Authorization": f"Bearer {WAKATIME_API_KEY}"}
API_URL = "https://wakatime.com/api/v1/users/current/all_time_since_today"
OUTPUT_DIR = "badges"

# --- Helper Function ---
def format_loc(n):
    """Formats large numbers into a more readable string (e.g., 1.3 million)."""
    if n < 1_000_000:
        return f"{n:,}"
    
    millions = n / 1_000_000
    return f"{millions:.1f} million"

# --- SVG Generation Function ---
def make_svg(label, message, filename):
    """Generates a dynamic-width SVG badge."""
    font_family = "Segoe UI, Ubuntu, sans-serif"
    font_size = 13
    padding_x = 15
    char_width_multiplier = 7.5 
    
    # Calculate widths of the two parts of the badge
    label_width = (len(label) * char_width_multiplier) + (padding_x * 2)
    message_width = (len(message) * char_width_multiplier) + (padding_x * 2)
    total_width = label_width + message_width
    
    # Calculate x positions for the text
    label_text_x = label_width / 2
    message_text_x = label_width + (message_width / 2)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="28">
  <linearGradient id="grad" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#2b2b2b" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  
  <rect rx="5" width="{total_width}" height="28" fill="#21262d"/>
  <rect rx="5" width="{label_width}" height="28" fill="#2d333b"/>
  <path fill="url(#grad)" d="M0 0h{total_width}v28H0z"/>
  
  <g fill="#fff" text-anchor="middle" font-family="{font_family}" font-size="{font_size}">
    <text x="{label_text_x}" y="19" fill="#c9d1d9">{label}</text>
    <text x="{message_text_x}" y="19" fill="#fff">{message}</text>
  </g>
</svg>"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ Generated {filename}")

# --- Main Logic ---
def main():
    """Fetches WakaTime data and generates SVG badges."""
    try:
        res = requests.get(API_URL, headers=HEADERS)
        res.raise_for_status()
        data = res.json()["data"]
        
        # 1. Code Time Badge
        code_time = data.get("text", "N/A")
        if code_time != "N/A":
            make_svg("Code Time", code_time, "waka-code-time.svg")

        # 2. Lines of Code (LOC) Badge
        total_lines = data.get("total_lines")
        if total_lines is not None:
            message = f"{format_loc(total_lines)} Lines of code"
            make_svg("From Hello World I've written", message, "waka-loc.svg")
        else:
             make_svg("Lines of Code", "N/A", "waka-loc.svg")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching WakaTime data: {e}")
        make_svg("Code Time", "N/A", "waka-code-time.svg")
        make_svg("Lines of Code", "N/A", "waka-loc.svg")
    except (KeyError, TypeError) as e:
        print(f"❌ Error parsing WakaTime data: {e}")
        make_svg("Code Time", "N/A", "waka-code-time.svg")
        make_svg("Lines of Code", "N/A", "waka-loc.svg")


if __name__ == "__main__":
    main()