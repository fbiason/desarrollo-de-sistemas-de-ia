// Funcionalidad adicional para el sistema experto

document.addEventListener('DOMContentLoaded', function() {
    // Detectar automáticamente el navegador del usuario
    detectBrowser();
    
    // Añadir animación a la tarjeta de resultados
    const resultCard = document.querySelector('.result-card');
    if (resultCard) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'style' && 
                    resultCard.style.display === 'block') {
                    resultCard.classList.add('fade-in');
                    setTimeout(() => {
                        resultCard.classList.add('show');
                    }, 100);
                }
            });
        });
        
        observer.observe(resultCard, { attributes: true });
    }
});

// Función para detectar el navegador del usuario
function detectBrowser() {
    const browserSelect = document.getElementById('browser');
    if (!browserSelect) return;
    
    const userAgent = navigator.userAgent;
    let browser = '';
    
    if (userAgent.indexOf("Chrome") > -1 && userAgent.indexOf("Edg") === -1) {
        browser = "Chrome";
    } else if (userAgent.indexOf("Safari") > -1 && userAgent.indexOf("Chrome") === -1) {
        browser = "Safari";
    } else if (userAgent.indexOf("Firefox") > -1) {
        browser = "Firefox";
    } else if (userAgent.indexOf("Edg") > -1) {
        browser = "Edge";
    } else if (userAgent.indexOf("MSIE") > -1 || userAgent.indexOf("Trident/") > -1) {
        browser = "IE";
    } else {
        browser = "Other";
    }
    
    // Seleccionar automáticamente el navegador detectado
    for (let i = 0; i < browserSelect.options.length; i++) {
        if (browserSelect.options[i].value === browser) {
            browserSelect.selectedIndex = i;
            break;
        }
    }
}

// Función para detectar problemas de conexión
function checkConnectionSpeed() {
    const connectionSelect = document.getElementById('connection');
    if (!connectionSelect || connectionSelect.value) return;
    
    // Intentar estimar la velocidad de conexión
    const startTime = new Date().getTime();
    const imageUrl = 'https://www.google.com/images/phd/px.gif'; // Imagen pequeña de Google
    
    const img = new Image();
    img.onload = function() {
        const endTime = new Date().getTime();
        const duration = endTime - startTime;
        
        // Estimar tipo de conexión basado en la velocidad
        let connection = '';
        if (duration < 100) {
            connection = 'ethernet';
        } else if (duration < 300) {
            connection = 'wifi';
        } else {
            connection = 'slow_wifi';
        }
        
        // Seleccionar la conexión estimada
        for (let i = 0; i < connectionSelect.options.length; i++) {
            if (connectionSelect.options[i].value === connection) {
                connectionSelect.selectedIndex = i;
                break;
            }
        }
    };
    
    img.onerror = function() {
        // Si hay error, podría ser una conexión inestable
        for (let i = 0; i < connectionSelect.options.length; i++) {
            if (connectionSelect.options[i].value === 'slow_wifi') {
                connectionSelect.selectedIndex = i;
                break;
            }
        }
    };
    
    img.src = imageUrl + '?t=' + new Date().getTime();
}

// Función para verificar el estado del servidor
function checkServerStatus() {
    // Esta función podría hacer una petición simple para verificar
    // si el servidor de la plataforma educativa está respondiendo correctamente
    // En un entorno real, esto se conectaría a un endpoint de estado del servidor
    
    return new Promise((resolve) => {
        // Simulamos una verificación del servidor
        setTimeout(() => {
            // En un caso real, esto sería el resultado de una petición al servidor
            const isOnline = Math.random() > 0.1; // 90% de probabilidad de que esté online
            const responseTime = isOnline ? Math.floor(Math.random() * 1000) + 100 : 5000;
            
            resolve({
                isOnline: isOnline,
                responseTime: responseTime,
                lastMaintenance: isOnline ? "hace 7 días" : "reciente"
            });
        }, 300);
    });
}
