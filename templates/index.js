// Datos de los síntomas disponibles
const symptoms = {
    login: [
        { id: "cannot_login", text: "No puedo iniciar sesión" },
        { id: "forgot_password", text: "Olvidé mi contraseña" },
        { id: "account_locked", text: "Mi cuenta está bloqueada" },
        { id: "invalid_credentials", text: "Credenciales inválidas" },
        { id: "registration_failed", text: "No puedo registrarme" }
    ],
    video: [
        { id: "video_not_loading", text: "El video no carga" },
        { id: "video_buffering", text: "El video se detiene constantemente" },
        { id: "video_quality_poor", text: "La calidad del video es mala" },
        { id: "audio_issues", text: "Problemas con el audio" },
        { id: "playback_controls_not_working", text: "Los controles de reproducción no funcionan" }
    ],
    chat: [
        { id: "messages_not_sending", text: "No puedo enviar mensajes" },
        { id: "cannot_see_messages", text: "No veo los mensajes de otros" },
        { id: "notification_issues", text: "No recibo notificaciones" },
        { id: "emoji_not_working", text: "Los emojis no funcionan" },
        { id: "chat_lag", text: "El chat tiene mucho retraso" }
    ],
    content: [
        { id: "content_not_loading", text: "El contenido no carga" },
        { id: "missing_files", text: "Faltan archivos" },
        { id: "broken_links", text: "Enlaces rotos" },
        { id: "formatting_issues", text: "Problemas de formato" },
        { id: "access_denied_to_content", text: "Acceso denegado al contenido" }
    ]
};

// Actualizar opciones de problemas específicos cuando cambia el tipo de problema
document.getElementById('problem-type').addEventListener('change', function() {
    const problemType = this.value;
    const specificIssueSelect = document.getElementById('specific-issue');
    
    // Limpiar opciones actuales
    specificIssueSelect.innerHTML = '';
    
    // Agregar nuevas opciones basadas en el tipo de problema
    if (symptoms[problemType]) {
        specificIssueSelect.disabled = false;
        
        // Agregar opción por defecto
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = 'Seleccione el problema específico';
        specificIssueSelect.appendChild(defaultOption);
        
        // Agregar opciones de síntomas
        symptoms[problemType].forEach(symptom => {
            const option = document.createElement('option');
            option.value = symptom.id;
            option.textContent = symptom.text;
            specificIssueSelect.appendChild(option);
        });
    } else {
        specificIssueSelect.disabled = true;
    }
});

// Manejar el envío del formulario
document.getElementById('diagnosis-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Mostrar indicador de carga
    document.querySelector('.loading').style.display = 'block';
    document.querySelector('.result-card').style.display = 'none';
    
    // Recopilar datos del formulario
    const problemType = document.getElementById('problem-type').value;
    const specificIssue = document.getElementById('specific-issue').value;
    const browser = document.getElementById('browser').value;
    const connection = document.getElementById('connection').value;
    
    // Crear objeto de datos para enviar al servidor
    const data = {
        symptoms: [
            {
                type: problemType,
                description: specificIssue,
                severity: "medium",
                frequency: "sometimes"
            }
        ],
        system_info: {
            browser: browser || "Unknown",
            browser_version: "Unknown",
            connection_type: connection || "Unknown",
            device_type: "desktop",
            operating_system: navigator.platform
        },
        server_status: {
            is_online: true,
            response_time: 500,
            reported_issues: 0
        }
    };
    
    // Enviar solicitud al servidor
    fetch('/api/diagnose', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Ocultar indicador de carga
        document.querySelector('.loading').style.display = 'none';
        
        // Mostrar resultados
        document.querySelector('.result-card').style.display = 'block';
        
        // Actualizar contenido de resultados
        document.getElementById('diagnosis-title').textContent = 
            `Diagnóstico: ${getProblemTypeText(result.diagnosis)}`;
        document.getElementById('diagnosis-cause').textContent = 
            getCauseText(result.cause);
        document.getElementById('diagnosis-solution').textContent = 
            result.solution;
        
        // Actualizar indicador de confianza
        const confidencePercentage = Math.round(result.confidence * 100);
        document.getElementById('confidence-percentage').textContent = 
            `${confidencePercentage}%`;
        document.getElementById('confidence-bar').style.width = 
            `${confidencePercentage}%`;
        
        // Cambiar color del indicador según nivel de confianza
        const confidenceBar = document.getElementById('confidence-bar');
        if (confidencePercentage < 40) {
            confidenceBar.style.background = 'linear-gradient(90deg, #ff6b6b, #dc3545)'; // Rojo
            document.getElementById('confidence-percentage').className = 'fw-bold text-danger';
        } else if (confidencePercentage < 70) {
            confidenceBar.style.background = 'linear-gradient(90deg, #ffd166, #ffc107)'; // Amarillo
            document.getElementById('confidence-percentage').className = 'fw-bold text-warning';
        } else {
            confidenceBar.style.background = 'linear-gradient(90deg, #06d6a0, #198754)'; // Verde
            document.getElementById('confidence-percentage').className = 'fw-bold text-success';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.querySelector('.loading').style.display = 'none';
        
        // Mostrar tarjeta de error
        document.querySelector('.result-card').style.display = 'block';
        document.querySelector('.result-card .card-header').classList.remove('bg-success');
        document.querySelector('.result-card .card-header').classList.add('bg-danger');
        document.querySelector('.result-card .card-header h5').textContent = 'Error en el diagnóstico';
        
        document.getElementById('diagnosis-title').textContent = 'No se pudo completar el diagnóstico';
        document.getElementById('diagnosis-cause').textContent = 'Error de comunicación con el servidor';
        document.getElementById('diagnosis-solution').textContent = 
            'Por favor, intente nuevamente. Si el problema persiste, contacte al soporte técnico.';
        
        document.getElementById('confidence-percentage').textContent = '0%';
        document.getElementById('confidence-bar').style.width = '0%';
        document.getElementById('confidence-bar').style.backgroundColor = '#dc3545';
        
        // Registrar el error para depuración
        console.log('Datos enviados:', data);
    });
});

// Función para obtener texto descriptivo del tipo de problema
function getProblemTypeText(problemType) {
    const types = {
        'login': 'Problema de inicio de sesión',
        'video': 'Problema con reproducción de video',
        'chat': 'Problema de chat',
        'content': 'Problema de acceso a contenido',
        'unknown': 'Problema desconocido'
    };
    return types[problemType] || 'Problema no identificado';
}

// Función para obtener texto descriptivo de la causa
function getCauseText(cause) {
    const causes = {
        server:      'Problema del servidor',
        browser:     'Problema del navegador',
        user:        'Problema del usuario o de configuración',
        link:        'Problema con el enlace',
        network:     'Problema de la red/conectividad',
        device:      'Problema del dispositivo/audio',
        permissions: 'Falta de permisos o rol',
        unknown:     'Causa desconocida'
    };
    return causes[cause] || 'Causa no identificada';
}
