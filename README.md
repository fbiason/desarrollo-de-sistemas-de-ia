# 🧠 Sistema Experto para Plataformas de Educación Virtual

Este sistema experto ayuda a detectar y diagnosticar problemas comunes en plataformas de educación virtual, como problemas de inicio de sesión, carga de contenido, reproducción de videos e interacción en chats.

---

## ✨ Características principales

- 🧩 **Base de conocimiento** con hechos sobre problemas comunes  
- ⚙️ **Motor de inferencia** basado en reglas (*rule engine*) para identificar causas probables  
- 🌐 **API REST** para integración con otras aplicaciones o sistemas  
- 💬 **Interfaz de usuario moderna** con dashboard en tiempo real  
- 📊 **Visualización de estadísticas** con gráficos interactivos  

---

## 📦 Requisitos

- Python **3.7+**  
- Flask **2.3.0**  
- Experta **1.9.4** *(motor de reglas basado en CLIPS)*  
- Chart.js *(para gráficos en el dashboard)*  

---

## 📂 Estructura del Proyecto

```
PROYECTO/
├── app.py                # Archivo principal con todos los endpoints de la API
├── requirements.txt      # Librerías necesarias para ejecutar el proyecto
├── README.md             # Instrucciones de uso y configuración
├── Funcionamiento.md     # Explicación detallada del flujo interno del sistema
├── data/                 # Datos de entrada, bases de conocimiento o registros auxiliares
├── knowledge_base/       # Reglas organizadas por categoría (login, video, chat, contenido)
├── services/             # Servicios de diagnóstico e historial 
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Archivos HTML o plantillas Jinja2
└── .gitignore            # Exclusiones de control de versiones

    
```

---

## 🏗️ Configuración del entorno

### 1️⃣ Clonar el repositorio
git clone https://github.com/fbiason/desarrollo-de-sistemas-de-ia.git

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

**Opción 1: Ejecutar solo el backend (API)**
```bash
python app.py
```

Abrí tu navegador en:
👉 **http://127.0.0.1:5000**

---

## 🚀 Uso

### Interfaz Web
Accedé a la interfaz completa con dashboard en:
- **http://localhost:5000**

### API REST
Podés usar los siguientes endpoints:

**POST** `/api/diagnose` - Diagnosticar un problema
```json
{
  "symptoms": [{
    "type": "login",
    "description": "cannot_login"
  }],
  "system_info": {
    "browser": "Chrome",
    "connection_type": "wifi"
  }
}
```

**GET** `/api/diagnosis` - Obtener historial de diagnósticos

---

## 📊 Dashboard

El sistema incluye un dashboard interactivo que muestra:
- 📈 **Estadísticas generales**: Total de diagnósticos, confianza alta/media/baja
- 📊 **Gráficos**: Problemas por tipo, causas identificadas, confianza promedio
- 📝 **Historial**: Últimos 10 diagnósticos realizados

---

## 📖 Documentación Adicional

Para entender cómo funciona el sistema experto internamente, consultá:
- **Funcionamiento.md** - Explicación detallada de la arquitectura y motor de inferencia

---
