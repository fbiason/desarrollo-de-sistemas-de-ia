// Dashboard para visualización de diagnósticos
let problemTypeChart, causeChart, confidenceChart;
let diagnosisHistory = [];

// Inicializar dashboard al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    loadHistory();
    updateDashboard();
});

// Inicializar gráficos con Chart.js
function initializeCharts() {
    // Gráfico de Problemas por Tipo
    const ctxProblemType = document.getElementById('problemTypeChart').getContext('2d');
    problemTypeChart = new Chart(ctxProblemType, {
        type: 'doughnut',
        data: {
            labels: ['Login', 'Video', 'Chat', 'Contenido'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: [
                    '#0d6efd',
                    '#dc3545',
                    '#ffc107',
                    '#198754'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 10,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Causas
    const ctxCause = document.getElementById('causeChart').getContext('2d');
    causeChart = new Chart(ctxCause, {
        type: 'doughnut',
        data: {
            labels: ['Servidor', 'Navegador', 'Usuario', 'Red', 'Dispositivo', 'Permisos'],
            datasets: [{
                data: [0, 0, 0, 0, 0, 0],
                backgroundColor: [
                    '#e74c3c',
                    '#3498db',
                    '#f39c12',
                    '#9b59b6',
                    '#1abc9c',
                    '#34495e'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 10,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Confianza Promedio
    const ctxConfidence = document.getElementById('confidenceChart').getContext('2d');
    confidenceChart = new Chart(ctxConfidence, {
        type: 'bar',
        data: {
            labels: ['Login', 'Video', 'Chat', 'Contenido'],
            datasets: [{
                label: 'Confianza Promedio (%)',
                data: [0, 0, 0, 0],
                backgroundColor: [
                    'rgba(13, 110, 253, 0.7)',
                    'rgba(220, 53, 69, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(25, 135, 84, 0.7)'
                ],
                borderColor: [
                    '#0d6efd',
                    '#dc3545',
                    '#ffc107',
                    '#198754'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Cargar historial desde el servidor
async function loadHistory() {
    try {
        const response = await fetch('/api/diagnosis');
        if (response.ok) {
            diagnosisHistory = await response.json();
            updateDashboard();
        }
    } catch (error) {
        console.error('Error al cargar historial:', error);
    }
}

// Actualizar dashboard con nuevos datos
function updateDashboard() {
    updateStatistics();
    updateCharts();
    updateHistoryTable();
}

// Actualizar estadísticas generales
function updateStatistics() {
    const total = diagnosisHistory.length;
    const highConf = diagnosisHistory.filter(d => d.confidence >= 0.85).length;
    const mediumConf = diagnosisHistory.filter(d => d.confidence >= 0.60 && d.confidence < 0.85).length;
    const lowConf = diagnosisHistory.filter(d => d.confidence < 0.60).length;

    document.getElementById('total-diagnoses').textContent = total;
    document.getElementById('high-confidence').textContent = highConf;
    document.getElementById('medium-confidence').textContent = mediumConf;
    document.getElementById('low-confidence').textContent = lowConf;
}

// Actualizar gráficos
function updateCharts() {
    // Contar problemas por tipo
    const problemCounts = {
        login: 0,
        video: 0,
        chat: 0,
        content: 0
    };

    // Contar causas
    const causeCounts = {
        server: 0,
        browser: 0,
        user: 0,
        network: 0,
        device: 0,
        permissions: 0,
        link: 0
    };

    // Sumar confianza por tipo para calcular promedio
    const confidenceSum = {
        login: 0,
        video: 0,
        chat: 0,
        content: 0
    };

    const confidenceCount = {
        login: 0,
        video: 0,
        chat: 0,
        content: 0
    };

    diagnosisHistory.forEach(diagnosis => {
        // Contar tipos de problemas
        if (problemCounts.hasOwnProperty(diagnosis.diagnosis)) {
            problemCounts[diagnosis.diagnosis]++;
            confidenceSum[diagnosis.diagnosis] += diagnosis.confidence;
            confidenceCount[diagnosis.diagnosis]++;
        }

        // Contar causas
        if (causeCounts.hasOwnProperty(diagnosis.cause)) {
            causeCounts[diagnosis.cause]++;
        }
    });

    // Actualizar gráfico de tipos de problemas
    problemTypeChart.data.datasets[0].data = [
        problemCounts.login,
        problemCounts.video,
        problemCounts.chat,
        problemCounts.content
    ];
    problemTypeChart.update();

    // Actualizar gráfico de causas
    causeChart.data.datasets[0].data = [
        causeCounts.server,
        causeCounts.browser,
        causeCounts.user,
        causeCounts.network,
        causeCounts.device,
        causeCounts.permissions
    ];
    causeChart.update();

    // Calcular y actualizar confianza promedio
    const avgConfidence = [
        confidenceCount.login > 0 ? (confidenceSum.login / confidenceCount.login) * 100 : 0,
        confidenceCount.video > 0 ? (confidenceSum.video / confidenceCount.video) * 100 : 0,
        confidenceCount.chat > 0 ? (confidenceSum.chat / confidenceCount.chat) * 100 : 0,
        confidenceCount.content > 0 ? (confidenceSum.content / confidenceCount.content) * 100 : 0
    ];

    confidenceChart.data.datasets[0].data = avgConfidence;
    confidenceChart.update();
}

// Actualizar tabla de historial
function updateHistoryTable() {
    const tbody = document.getElementById('history-table');
    
    if (diagnosisHistory.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No hay diagnósticos aún</td></tr>';
        return;
    }

    // Mostrar últimos 10 diagnósticos
    const recentDiagnoses = diagnosisHistory.slice(-10).reverse();
    
    tbody.innerHTML = recentDiagnoses.map(diagnosis => {
        const confidenceClass = getConfidenceClass(diagnosis.confidence);
        const confidencePercentage = Math.round(diagnosis.confidence * 100);
        const timestamp = new Date().toLocaleString('es-AR', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });

        return `
            <tr>
                <td><span class="badge bg-primary">${getProblemTypeText(diagnosis.diagnosis)}</span></td>
                <td>${getCauseText(diagnosis.cause)}</td>
                <td><span class="badge ${confidenceClass}">${confidencePercentage}%</span></td>
                <td><small class="text-muted">${timestamp}</small></td>
            </tr>
        `;
    }).join('');
}

// Agregar nuevo diagnóstico al historial
function addDiagnosis(diagnosis) {
    diagnosisHistory.push(diagnosis);
    updateDashboard();
}

// Obtener clase CSS según nivel de confianza
function getConfidenceClass(confidence) {
    if (confidence >= 0.85) return 'bg-success';
    if (confidence >= 0.60) return 'bg-warning';
    return 'bg-danger';
}

// Obtener texto del tipo de problema
function getProblemTypeText(type) {
    const types = {
        'login': 'Login',
        'video': 'Video',
        'chat': 'Chat',
        'content': 'Contenido',
        'unknown': 'Desconocido'
    };
    return types[type] || 'N/A';
}

// Obtener texto de la causa
function getCauseText(cause) {
    const causes = {
        server: 'Servidor',
        browser: 'Navegador',
        user: 'Usuario',
        link: 'Enlace',
        network: 'Red',
        device: 'Dispositivo',
        permissions: 'Permisos',
        unknown: 'Desconocida'
    };
    return causes[cause] || 'N/A';
}

// Exportar función para que index.js pueda actualizar el dashboard
window.updateDashboardWithNewDiagnosis = addDiagnosis;
