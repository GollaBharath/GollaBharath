const fs = require("fs");
const https = require("https");

const STATS_BASE_URL = "https://stats.gollabharath.me";

/**
 * Make an HTTPS GET request and return parsed JSON
 */
function fetchJSON(url) {
	return new Promise((resolve, reject) => {
		https
			.get(url, (res) => {
				let data = "";
				res.on("data", (chunk) => {
					data += chunk;
				});
				res.on("end", () => {
					try {
						resolve(JSON.parse(data));
					} catch (err) {
						reject(err);
					}
				});
			})
			.on("error", reject);
	});
}

/**
 * Generate Local Time Badge SVG
 */
async function updateLocalTimeBadge() {
	try {
		const data = await fetchJSON(`${STATS_BASE_URL}/time`);
		const currentTime = data.time;

		const label = "🕛 Local Time";
		const message = currentTime;

		const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="190" height="28">
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
    <text x="47.5" y="19" fill="#c9d1d9">${label}</text>
    <text x="142.5" y="19" fill="#fff">${message}</text>
  </g>
</svg>
`;

		fs.writeFileSync("local-time.svg", svg);
		console.log("✅ Updated local-time.svg");
	} catch (err) {
		console.error("❌ Error updating local time badge:", err);
	}
}

/**
 * Generate Spotify Badge SVG
 */
async function updateSpotifyBadge() {
	try {
		const data = await fetchJSON(`${STATS_BASE_URL}/stats/spotify`);
		const isPlaying = data.data.is_playing;

		let songText;
		if (isPlaying && data.data.current_track) {
			const track = data.data.current_track;
			songText = track.name;
		} else {
			songText = "Offline";
		}

		// HTML escape the text
		songText = songText
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;")
			.replace(/'/g, "&#39;");

		const leftColor = "#1DB954";
		const rightColor = isPlaying ? "#1DB954" : "#9e9e9e";
		const textColor = "#ffffff";

		const baseWidth = 120;
		const charWidth = 7;
		const textLength = songText.length * charWidth;
		const totalWidth = Math.max(240, baseWidth + textLength + 20);

		let marqueeSvg = "";
		let textElement = "";

		if (textLength > totalWidth - baseWidth - 10 && isPlaying) {
			marqueeSvg = `
        <g transform="translate(${baseWidth}, 0)">
            <text y="19" fill="${textColor}">
                <tspan>
                    <animate attributeName="x" from="${totalWidth}" to="-${textLength}" dur="10s" repeatCount="indefinite" />
                    ${songText}
                </tspan>
            </text>
        </g>
        `;
		} else {
			textElement = `<text x="${
				baseWidth + 5
			}" y="19" fill="${textColor}">${songText}</text>`;
		}

		const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${totalWidth}" height="28">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="${totalWidth}" height="28" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="${baseWidth}" height="28" fill="${leftColor}"/>
    <rect x="${baseWidth}" width="${
			totalWidth - baseWidth
		}" height="28" fill="${rightColor}"/>
    <rect width="${totalWidth}" height="28" fill="url(#b)"/>
  </g>
  <g fill="${textColor}" font-family="Segoe UI, sans-serif" font-size="13">
    <text x="30" y="19" fill="${textColor}">Spotify</text>
    ${textElement}
    ${marqueeSvg}
  </g>
</svg>`;

		fs.writeFileSync("spotify-status.svg", svg);
		console.log("✅ Updated spotify-status.svg");
	} catch (err) {
		console.error("❌ Error updating Spotify badge:", err);
	}
}

/**
 * Generate Discord Badge SVG
 */
async function updateDiscordBadge() {
	try {
		const data = await fetchJSON(`${STATS_BASE_URL}/stats/discord`);
		const status = data.data.discord_status;

		const statusColors = {
			online: "4c1",
			idle: "dfb317",
			dnd: "e05d44",
			offline: "9f9f9f",
		};

		const statusIcons = {
			online: "🟢",
			idle: "🌙",
			dnd: "⛔",
			offline: "🔘",
		};

		const color = statusColors[status] || "9f9f9f";
		const icon = statusIcons[status] || "❔";

		const label = "Discord";
		const message = `${icon} ${
			status.charAt(0).toUpperCase() + status.slice(1)
		}`;

		const badge = `
<svg xmlns="http://www.w3.org/2000/svg" width="160" height="28">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="160" height="28" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="70" height="28" fill="#5865F2"/>
    <rect x="70" width="90" height="28" fill="#${color}"/>
    <rect width="160" height="28" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana, Geneva, sans-serif" font-size="11">
    <text x="35" y="19">${label}</text>
    <text x="115" y="19">${message}</text>
  </g>
</svg>`;

		fs.writeFileSync("discord-status.svg", badge.trim());
		console.log("✅ Updated discord-status.svg");
	} catch (err) {
		console.error("❌ Error updating Discord badge:", err);
	}
}

/**
 * Main execution
 */
async function main() {
	console.log("🚀 Starting badge updates...\n");

	await updateLocalTimeBadge();
	await updateSpotifyBadge();
	await updateDiscordBadge();

	console.log("\n✨ All badges updated successfully!");
}

main();
