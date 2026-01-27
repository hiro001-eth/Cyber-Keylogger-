// Enhanced dashboard functionality
import Chart from 'chart.js/auto'

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts()
    setupRealTimeUpdates()
    setupEventListeners()
})

function initializeCharts() {
    const activityCtx = document.getElementById('activityChart')
    if (activityCtx) {
        new Chart(activityCtx, {
            type: 'line',
            data: {
                labels: ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
                datasets: [
                    {
                        label: "Keystrokes per Hour",
                        data: [100, 200, 500, 800, 600, 300],
                        borderColor: "#0078D4",
                        backgroundColor: "rgba(0, 120, 212, 0.2)",
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: "Script Detections",
                        data: [0, 2, 1, 5, 3, 0],
                        borderColor: "#FF4444",
                        backgroundColor: "rgba(255, 68, 68, 0.2)",
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: true, text: 'User Activity Overview' }
                }
            }
        })
    }
}

function setupRealTimeUpdates() {
    // WebSocket connection for real-time updates
    const ws = new WebSocket('ws://localhost:5000/ws')
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data)
        updateDashboard(data)
    }
    
    ws.onerror = function(error) {
        console.error('WebSocket error:', error)
    }
}

function updateDashboard(data) {
    // Update dashboard with real-time data
    if (data.type === 'keystroke') {
        updateKeystrokeCount(data.count)
    } else if (data.type === 'alert') {
        showAlert(data.message)
    }
}

function updateKeystrokeCount(count) {
    const countElement = document.getElementById('keystroke-count')
    if (countElement) {
        countElement.textContent = count
    }
}

function showAlert(message) {
    const alertContainer = document.getElementById('alert-container')
    if (alertContainer) {
        const alert = document.createElement('div')
        alert.className = 'alert alert-warning'
        alert.textContent = message
        alertContainer.appendChild(alert)
        
        setTimeout(() => alert.remove(), 5000)
    }
}

function setupEventListeners() {
    // Setup any additional event listeners
    const logoutBtn = document.getElementById('logout-btn')
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            window.location.href = '/logout'
        })
    }
} 