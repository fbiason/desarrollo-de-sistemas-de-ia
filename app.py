# Parche de compatibilidad para Experta con Python 3.10+
# Experta usa collections.Mapping que fue movido a collections.abc
import collections
import collections.abc
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, "Sequence"):
    collections.Sequence = collections.abc.Sequence

# Importaciones de Flask para crear la API REST
from flask import Flask, request, jsonify, render_template
import logging
# Servicio que ejecuta el sistema experto
from services.diagnosis_service import DiagnosisService

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Configuración de logging para depuración
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# Valores válidos para validación de entrada
VALID_BROWSERS = {"Chrome", "Firefox", "Edge", "Safari", "IE", "Other"}
VALID_CONNECTIONS = {"wifi", "ethernet", "cellular", "slow_wifi"}

# ========== ENDPOINTS ==========

@app.route("/")
def index():
    """Ruta principal que sirve la interfaz web del sistema experto."""
    return render_template("index.html")

@app.post("/api/diagnose")
def diagnose():
    """
    Endpoint principal para ejecutar el diagnóstico del sistema experto.
    
    Recibe:
        JSON con estructura:
        {
            "symptoms": [{"type": "login", "description": "cannot_login", ...}],
            "system_info": {"browser": "Chrome", "connection_type": "wifi", ...},
            "server_status": {"is_online": true, ...}
        }
    
    Retorna:
        JSON con el diagnóstico:
        {
            "diagnosis": "login",
            "cause": "browser",
            "solution": "...",
            "confidence": 0.95
        }
    """
    try:
        # 1. Obtener datos JSON de la petición
        data = request.get_json(silent=True)
        
        # 2. Validar que existan los campos obligatorios
        if not data or "symptoms" not in data:
            return jsonify({"error": "Debe enviar 'symptoms' y 'system_info'"}), 400

        # 3. Extraer síntomas e información del sistema
        symptoms = data.get("symptoms")
        sysinfo = data.get("system_info", {})
        
        # 4. Validar que symptoms sea una lista no vacía
        if not isinstance(symptoms, list) or not symptoms:
            return jsonify({"error": "'symptoms' debe ser lista no vacía"}), 400

        # 5. Validar navegador y tipo de conexión
        browser = sysinfo.get("browser")
        conn = sysinfo.get("connection_type")
        if browser not in VALID_BROWSERS:
            return jsonify({"error": f"Navegador inválido: {browser}", "allowed": sorted(VALID_BROWSERS)}), 400
        if conn not in VALID_CONNECTIONS:
            return jsonify({"error": f"Conexión inválida: {conn}", "allowed": sorted(VALID_CONNECTIONS)}), 400

        # 6. Ejecutar el sistema experto y guardar en historial
        result = DiagnosisService.run(data, persist=True)

        # 7. Log del resultado para depuración
        print(result)
        
        # 8. Retornar diagnóstico en formato JSON
        return jsonify(result), 200

    except Exception as e:
        # Manejo de errores: log y respuesta HTTP 500
        app.logger.exception("Error en /api/diagnose")
        return jsonify({"error": str(e)}), 500

@app.get("/api/diagnosis")
def get_history():
    """
    Endpoint para obtener el historial de diagnósticos previos.
    
    Retorna:
        JSON con lista de diagnósticos anteriores:
        [
            {"diagnosis": "login", "cause": "browser", "timestamp": "...", ...},
            {"diagnosis": "video", "cause": "network", "timestamp": "...", ...}
        ]
    """
    try:
        # Obtener historial desde el servicio
        diagnosis_history = DiagnosisService.history()
        return jsonify(diagnosis_history), 200
    except Exception as e:
        # Manejo de errores
        app.logger.exception("Error al obtener historial")
        return jsonify({"error": str(e)}), 500

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Ejecutar servidor Flask en modo debug
    # Accesible en http://localhost:5000
    app.run(debug=True)