const fs = require('fs');
const https = require('https');

const userId = '972801524092776479'; // 👈 Replace this

const url = `https://api.lanyard.rest/v1/users/${userId}`;

const statusColors = {
  online: 'brightgreen',
  offline: 'lightgray',
  idle: 'yellow',
  dnd: 'red',
};

const statusIcons = {
  online: '🟢',
  offline: '🔴',
  idle: '🌙',
  dnd: '🛑',
};

https.get(url, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      const status = json.data.discord_status;

      const color = statusColors[status] || 'lightgray';
      const icon = statusIcons[status] || '❔';

      const label = 'Discord';
      const message = `${icon} ${status.charAt(0).toUpperCase() + status.slice(1)}`;
      const badge = `
<svg xmlns="http://www.w3.org/2000/svg" width="160" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="160" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="70" height="20" fill="#555"/>
    <rect x="70" width="90" height="20" fill="#${color === 'brightgreen' ? '4c1' : color === 'red' ? 'e05d44' : color === 'yellow' ? 'dfb317' : '9f9f9f'}"/>
    <rect width="160" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana" font-size="11">
    <text x="35" y="14">${label}</text>
    <text x="115" y="14">${message}</text>
  </g>
</svg>`;

      fs.writeFileSync('discord-status.svg', badge.trim());
      console.log('Updated discord-status.svg');
    } catch (err) {
      console.error('Error parsing Lanyard response', err);
    }
  });
});
