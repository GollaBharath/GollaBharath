const fs = require('fs');
const https = require('https');

const userId = '972801524092776479'; // 👈 Your Discord user ID

const url = `https://api.lanyard.rest/v1/users/${userId}`;

const statusColors = {
  online: '4c1',       // bright green
  idle: 'dfb317',      // yellow
  dnd: 'e05d44',       // red
  offline: '9f9f9f',   // gray
};

const statusIcons = {
  online: '🟢',
  idle: '🌙',
  dnd: '⛔',
  offline: '🔘',
};

https.get(url, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      const status = json.data.discord_status;

      const color = statusColors[status] || '9f9f9f';
      const icon = statusIcons[status] || '❔';

      const label = 'Discord';
      const message = `${icon} ${status.charAt(0).toUpperCase() + status.slice(1)}`;

      const badge = `
<svg xmlns="http://www.w3.org/2000/svg" width="160" height="28">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="160" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <!-- Left: Discord Blue -->
    <rect width="70" height="20" fill="#5865F2"/>
    <!-- Right: Dynamic -->
    <rect x="70" width="90" height="20" fill="#${color}"/>
    <rect width="160" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana, Geneva, sans-serif" font-size="11">
    <text x="35" y="14">${label}</text>
    <text x="115" y="14">${message}</text>
  </g>
</svg>`;

      fs.writeFileSync('discord-status.svg', badge.trim());
      console.log('✅ Updated discord-status.svg');
    } catch (err) {
      console.error('❌ Error parsing Lanyard response:', err);
    }
  });
});
