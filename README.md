# 🧠 Sistema Experto para Plataformas de Educación Virtual

Este sistema experto ayuda a detectar y diagnosticar problemas comunes en plataformas de educación virtual, como problemas de inicio de sesión, carga de contenido, reproducción de videos e interacción en chats.

---

## ✨ Características principales

- 🧩 **Base de conocimiento** con hechos sobre problemas comunes.  
- ⚙️ **Motor de inferencia** basado en reglas (*rule engine*) para identificar causas probables.  
- 🌐 **API REST** para integración con otras aplicaciones o sistemas.  
- 💬 **Interfaz de usuario simple y funcional** para consultas directas.  

---

## 📦 Requisitos

- Python **3.7+**  
- Flask  
- Experta *(motor de reglas basado en CLIPS)*  

---

## 🏗️ Configuración del entorno

### 1️⃣ Clonar el repositorio
git clone https://github.com/fbiason/desarrollo-de-sistemas-de-ia.git
cd desarrollo-de-sistemas-de-ia

### 2️⃣ Crear un entorno virtual

Windows

python -m venv venv
venv\Scripts\activate


Linux / macOS

python3 -m venv venv
source venv/bin/activate

### 3️⃣ Instalar las dependencias
pip install --upgrade pip
pip install -r requirements.txt

### ▶️ Ejecución de la aplicación

Asegurate de tener el entorno virtual activado.

Ejecutá la app:

python app.py


Abrí tu navegador en:
👉 http://127.0.0.1:5000

🚀 Uso

Podés acceder a la interfaz web en
http://localhost:5000
o utilizar la API REST en
http://localhost:5000/api/diagnose.

"""
📂 Estructura del proyecto
sistema_experto/
├── app.py                  # Aplicación principal Flask
├── knowledge_base/
│   ├── __init__.py
│   ├── facts.py            # Definición de hechos
│   └── rules.py            # Reglas del sistema experto
├── static/                 # Archivos estáticos para la interfaz web
│   ├── css/
│   └── js/
├── templates/              # Plantillas HTML
└── tests/                  # Pruebas unitarias
"""