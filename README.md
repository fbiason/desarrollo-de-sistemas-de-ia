# Sistema Experto para Plataformas de Educación Virtual

Este sistema experto ayuda a detectar y diagnosticar problemas comunes en plataformas de educación virtual, como problemas de inicio de sesión, carga de contenido, reproducción de videos e interacción en chats.

## Características

- Base de conocimiento con hechos sobre problemas comunes
- Motor de inferencia basado en reglas para identificar causas de problemas
- API REST para integración con otras aplicaciones
- Interfaz de usuario simple para consultas directas

## Requisitos

- Python 3.7+
- Flask
- Experta (motor de reglas basado en CLIPS)

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicación: `python app.py`

## Uso

Acceder a la interfaz web en `http://localhost:5000` o utilizar la API REST en `http://localhost:5000/api/diagnose`.

## Estructura del proyecto

```
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
```
