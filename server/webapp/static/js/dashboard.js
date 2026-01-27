// CyberGuard dashboard interactions

document.addEventListener('DOMContentLoaded', function () {
	initHeroStats();
	initNetworkTrafficChart();
	initActivityFeed();
	initThreatTimeline();
});

function safeSetText(id, value) {
	var el = document.getElementById(id);
	if (el) el.textContent = value;
}

function initHeroStats() {
	fetch('/api/stats')
		.then(function (res) { return res.ok ? res.json() : null; })
		.then(function (data) {
			if (!data || !data.success || !data.stats) return;
			var s = data.stats;
			safeSetText('cg-active-endpoints', s.active_employees != null ? s.active_employees : '--');
			safeSetText('cg-active-threats', s.active_alerts != null ? s.active_alerts : '--');
			safeSetText('cg-topbar-endpoints', s.active_employees != null ? s.active_employees : '--');
			safeSetText('cg-topbar-threats', s.active_alerts != null ? s.active_alerts : '--');

			try {
				var bottomBar = document.getElementById('cg-bottom-notification');
				if (bottomBar && typeof s.active_alerts === 'number' && s.active_alerts > 0) {
					var iconEl = document.getElementById('cg-bottom-notification-icon');
					var msgEl = document.getElementById('cg-bottom-notification-message');
					if (iconEl) iconEl.textContent = '⚠️';
					if (msgEl) msgEl.textContent = 'There are ' + s.active_alerts + ' active security alerts requiring review.';
					bottomBar.style.display = 'flex';
				}
			} catch (e) {
				console.error('Failed to update bottom notification bar', e);
			}
		})
		.catch(function (err) {
			console.error('Failed to load stats', err);
		});
}

function initNetworkTrafficChart() {
	var canvas = document.getElementById('cg-network-traffic-chart');
	if (!canvas || !window.Chart) return;
	var ctx = canvas.getContext('2d');
	new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
			datasets: [
				{
					label: 'Upload (MB/s)',
					data: [40, 80, 120, 60, 90, 50],
					borderColor: '#00F0FF',
					backgroundColor: 'rgba(0, 240, 255, 0.15)',
					fill: true,
					tension: 0.4
				},
				{
					label: 'Download (MB/s)',
					data: [120, 160, 220, 180, 140, 100],
					borderColor: '#B026FF',
					backgroundColor: 'rgba(176, 38, 255, 0.15)',
					fill: true,
					tension: 0.4
				}
			]
		},
		options: {
			responsive: true,
			plugins: {
				legend: { position: 'top', labels: { color: '#E0E7FF', font: { size: 11 } } },
				title: { display: false }
			},
			scales: {
				x: { ticks: { color: '#8B92B8', font: { size: 10 } }, grid: { color: 'rgba(45,53,97,0.4)', borderColor: 'rgba(45,53,97,0.7)' } },
				y: { ticks: { color: '#8B92B8', font: { size: 10 } }, grid: { color: 'rgba(45,53,97,0.4)', borderColor: 'rgba(45,53,97,0.7)' } }
			}
		}
	});
}

function initActivityFeed() {
	var feed = document.getElementById('cg-activity-feed');
	if (!feed) return;

	fetch('/api/alerts')
		.then(function (res) { return res.ok ? res.json() : null; })
		.then(function (data) {
			if (!data || !data.success || !Array.isArray(data.alerts)) return;
			feed.innerHTML = '';
			data.alerts.forEach(function (a) {
				var item = document.createElement('div');
				item.className = 'cg-activity-item';
				var sevDot = document.createElement('div');
				sevDot.className = 'cg-badge-dot ' + (a.severity === 'high' || a.severity === 'critical' ? 'red' : a.severity === 'medium' ? 'yellow' : 'green');
				var icon = document.createElement('div');
				icon.className = 'cg-activity-icon';
				icon.textContent = '⚠️';
				var meta = document.createElement('div');
				meta.className = 'cg-activity-meta';
				var title = document.createElement('div');
				title.className = 'cg-activity-title';
				title.textContent = a.type + ' · ' + (a.username || 'endpoint');
				var sub = document.createElement('div');
				sub.className = 'cg-activity-sub';
				sub.textContent = a.message;
				meta.appendChild(title);
				meta.appendChild(sub);
				var time = document.createElement('div');
				time.className = 'cg-activity-time';
				time.textContent = a.timestamp;
				item.appendChild(sevDot);
				item.appendChild(meta);
				item.appendChild(time);
				feed.appendChild(item);
			});
		})
		.catch(function (err) {
			console.error('Failed to load alerts', err);
		});
}

function initThreatTimeline() {
	var container = document.getElementById('cg-threat-timeline');
	if (!container) return;
	container.innerHTML = '';
	var demo = [
		{ severity: 'Critical', endpoint: 'WKS-105', time: '14:32', status: 'Open', type: 'Malware C&C' },
		{ severity: 'High', endpoint: 'SRV-DB-01', time: '13:58', status: 'Investigating', type: 'SQL Injection' },
		{ severity: 'Medium', endpoint: 'LAP-ENG-12', time: '12:44', status: 'Resolved', type: 'Port Scan' }
	];
	demo.forEach(function (e) {
		var row = document.createElement('div');
		row.style.display = 'flex';
		row.style.alignItems = 'center';
		row.style.justifyContent = 'space-between';
		row.style.padding = '6px 0';
		var left = document.createElement('div');
		left.style.fontSize = '12px';
		left.textContent = e.time + ' · ' + e.type + ' · ' + e.endpoint;
		var right = document.createElement('div');
		right.style.fontSize = '11px';
		right.textContent = e.status;
		row.appendChild(left);
		row.appendChild(right);
		container.appendChild(row);
	});
}
