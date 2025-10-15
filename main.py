# main.py - Archivo principal con todos los endpoints de la API

import collections
import collections.abc
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, "Sequence"):
    collections.Sequence = collections.abc.Sequence

from flask import Flask, request, jsonify, render_template
import logging
from services.diagnosis_service import DiagnosisService

# Configurar Flask con las rutas de la carpeta interfaz
app = Flask(__name__,
            template_folder='interfaz/templates',
            static_folder='interfaz/static')
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

VALID_BROWSERS = {"Chrome", "Firefox", "Edge", "Safari", "IE", "Other"}
VALID_CONNECTIONS = {"wifi", "ethernet", "cellular", "slow_wifi"}

@app.route("/")
def index():
    """Ruta principal - Renderiza la interfaz web"""
    return render_template("index.html")

@app.post("/api/diagnose")
def diagnose():
    """Endpoint para diagnosticar problemas"""
    try:
        data = request.get_json(silent=True)
        if not data or "symptoms" not in data:
            return jsonify({"error": "Debe enviar 'symptoms' y 'system_info'"}), 400

        symptoms = data.get("symptoms")
        sysinfo = data.get("system_info", {})
        if not isinstance(symptoms, list) or not symptoms:
            return jsonify({"error": "'symptoms' debe ser lista no vacía"}), 400

        browser = sysinfo.get("browser")
        conn = sysinfo.get("connection_type")
        if browser not in VALID_BROWSERS:
            return jsonify({"error": f"Navegador inválido: {browser}", "allowed": sorted(VALID_BROWSERS)}), 400
        if conn not in VALID_CONNECTIONS:
            return jsonify({"error": f"Conexión inválida: {conn}", "allowed": sorted(VALID_CONNECTIONS)}), 400

        result = DiagnosisService.run(data, persist=True)

        print(result)
        return jsonify(result), 200

    except Exception as e:
        app.logger.exception("Error en /api/diagnose")
        return jsonify({"error": str(e)}), 500

@app.get("/api/diagnosis")
def get_history():
    """Endpoint para obtener el historial de diagnósticos"""
    try:
        diagnosis_history = DiagnosisService.history()
        return jsonify(diagnosis_history), 200
    except Exception as e:
        app.logger.exception("Error al obtener historial")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
