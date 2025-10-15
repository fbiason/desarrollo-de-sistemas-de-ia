# app_visual.py - Código para lanzar la interfaz conectada al backend

"""
Este archivo configura Flask para servir la interfaz visual del sistema experto.
La interfaz se conecta al backend definido en main.py para realizar diagnósticos.
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template

# Crear aplicación Flask con rutas personalizadas
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

@app.route('/')
def index():
    """Renderiza la página principal de la interfaz"""
    return render_template('index.html')

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Iniciando interfaz visual del Sistema Experto")
    print("=" * 60)
    print("📍 URL: http://127.0.0.1:5000")
    print("💡 Presiona CTRL+C para detener el servidor")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
