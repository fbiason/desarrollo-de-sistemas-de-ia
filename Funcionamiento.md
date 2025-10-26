# 🧠 Cómo Funciona el Sistema Experto

## 📋 Índice
1. [Arquitectura General](#arquitectura-general)
2. [Flask API - Capa de Presentación](#flask-api---capa-de-presentación)
3. [Componentes Principales](#componentes-principales)
4. [Flujo de Ejecución](#flujo-de-ejecución)
5. [Motor de Inferencia](#motor-de-inferencia)
6. [Base de Conocimiento](#base-de-conocimiento)
7. [Cálculo de Confianza](#cálculo-de-confianza)

---

## 🏗️ Arquitectura General

El sistema experto está construido sobre **Experta** (un motor de reglas basado en CLIPS para Python) y sigue una arquitectura de tres capas:

```
┌─────────────────────────────────────┐
│     Capa de Presentación            │
│   (Flask API + Interfaz Web)        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Capa de Servicio                │
│   (DiagnosisService)                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Capa de Conocimiento            │
│   (EdTechExpertSystem)              │
│   - Motor de Inferencia             │
│   - Base de Hechos (Facts)          │
│   - Base de Reglas (Rules)          │
└─────────────────────────────────────┘
```

---

## 🌐 Flask API - Capa de Presentación

Flask es el framework web que actúa como **puente entre el usuario y el sistema experto**. Proporciona una API REST que recibe peticiones HTTP y retorna diagnósticos en formato JSON.

### Archivo Principal: `app.py`

#### **Inicialización**
```python
from flask import Flask, request, jsonify, render_template
from services.diagnosis_service import DiagnosisService

app = Flask(__name__)
```

### **Endpoints Disponibles**

#### 1. **GET /** - Interfaz Web
```python
@app.route("/")
def index():
    return render_template("index.html")
```
- **Función**: Sirve la página HTML con el formulario de diagnóstico
- **Acceso**: `http://localhost:5000/`

#### 2. **POST /api/diagnose** - Ejecutar Diagnóstico
```python
@app.post("/api/diagnose")
def diagnose():
    # 1. Recibir datos JSON
    data = request.get_json()
    
    # 2. Validar entrada
    if not data or "symptoms" not in data:
        return jsonify({"error": "..."}), 400
    
    # 3. Validar navegador y conexión
    if browser not in VALID_BROWSERS:
        return jsonify({"error": "..."}), 400
    
    # 4. Ejecutar sistema experto
    result = DiagnosisService.run(data, persist=True)
    
    # 5. Retornar diagnóstico
    return jsonify(result), 200
```

**Entrada esperada:**
```json
{
  "symptoms": [
    {"type": "login", "description": "cannot_login", "severity": "high"}
  ],
  "system_info": {
    "browser": "Chrome",
    "connection_type": "wifi"
  },
  "server_status": {
    "is_online": true
  }
}
```

**Salida:**
```json
{
  "diagnosis": "login",
  "cause": "browser",
  "solution": "Estás usando Internet Explorer. Cambiá a Chrome...",
  "confidence": 0.95
}
```

#### 3. **GET /api/diagnosis** - Historial
```python
@app.get("/api/diagnosis")
def get_history():
    diagnosis_history = DiagnosisService.history()
    return jsonify(diagnosis_history), 200
```
- **Función**: Retorna todos los diagnósticos previos
- **Salida**: Lista de diagnósticos con timestamps

### **Validaciones Implementadas**

Flask valida los datos antes de pasarlos al sistema experto:

```python
VALID_BROWSERS = {"Chrome", "Firefox", "Edge", "Safari", "IE", "Other"}
VALID_CONNECTIONS = {"wifi", "ethernet", "cellular", "slow_wifi"}
```

**Validaciones realizadas:**
1. ✅ Presencia de campos obligatorios (`symptoms`)
2. ✅ Tipo de datos correcto (lista de síntomas)
3. ✅ Navegador válido
4. ✅ Tipo de conexión válido

**Respuestas de error:**
- `400 Bad Request`: Datos inválidos o faltantes
- `500 Internal Server Error`: Error en el sistema experto

### **Flujo de una Petición**

```
Usuario → Frontend (JavaScript)
              ↓
         POST /api/diagnose
              ↓
         Flask recibe JSON
              ↓
         Validaciones (app.py)
              ↓
         DiagnosisService.run()
              ↓
         EdTechExpertSystem.diagnose()
              ↓
         Reglas evalúan hechos
              ↓
         Diagnosis generado
              ↓
         Flask retorna JSON
              ↓
         Frontend muestra resultado
```

### **Manejo de Errores**

```python
try:
    result = DiagnosisService.run(data, persist=True)
    return jsonify(result), 200
except Exception as e:
    app.logger.exception("Error en /api/diagnose")
    return jsonify({"error": str(e)}), 500
```

Flask captura excepciones y retorna mensajes de error apropiados al cliente.

---

## 🔧 Componentes Principales

### 1. **Facts (Hechos)** - `knowledge_base/facts.py`

Los hechos representan el conocimiento sobre el estado actual del sistema. Hay 4 tipos:

#### **Symptom (Síntoma)**
```python
Symptom(
    type="login",              # Tipo: login, video, chat, content
    description="cannot_login", # Descripción específica
    severity="medium",          # Gravedad: low, medium, high
    frequency="sometimes"       # Frecuencia: rarely, sometimes, always
)
```

#### **SystemInfo (Información del Sistema)**
```python
SystemInfo(
    browser="Chrome",           # Navegador del usuario
    browser_version="90.0",     # Versión del navegador
    operating_system="Windows", # Sistema operativo
    device_type="desktop",      # Tipo: desktop, mobile, tablet
    connection_type="wifi"      # Conexión: wifi, ethernet, cellular
)
```

#### **ServerStatus (Estado del Servidor)**
```python
ServerStatus(
    is_online=True,            # ¿Servidor en línea?
    response_time=500,         # Tiempo de respuesta (ms)
    reported_issues=0          # Número de problemas reportados
)
```

#### **Diagnosis (Diagnóstico)**
```python
Diagnosis(
    problem_type="login",      # Tipo de problema diagnosticado
    cause="browser",           # Causa: server, browser, user, network, etc.
    solution="...",            # Solución recomendada
    confidence=0.95            # Nivel de confianza (0.0 - 1.0)
)
```

---

### 2. **Rules (Reglas)** - `knowledge_base/rules/`

Las reglas son el "cerebro" del sistema. Cada regla tiene:
- **Condiciones** (IF): Qué hechos deben estar presentes
- **Acciones** (THEN): Qué diagnóstico declarar

#### Ejemplo de Regla Real:

```python
@Rule(
    Symptom(type="login", description="cannot_login"),
    SystemInfo(browser="IE")
)
def cannot_login_ie(self):
    self.declare(
        Diagnosis(
            problem_type="login",
            cause="browser",
            solution="Estás usando Internet Explorer. Cambiá a Chrome, Firefox, Edge o Safari.",
            confidence=0.95
        )
    )
```

**Traducción:** 
- **SI** el usuario no puede iniciar sesión **Y** está usando Internet Explorer
- **ENTONCES** el problema es el navegador (confianza: 95%)

#### Tipos de Reglas por Categoría:

1. **LoginRules** (`login_rules.py`) - 15+ reglas
   - Problemas de credenciales
   - Navegadores incompatibles
   - Conexión lenta
   - Cuenta bloqueada

2. **VideoRules** (`video_rules.py`) - 12+ reglas
   - Video no carga
   - Buffering constante
   - Problemas de audio
   - Calidad pobre

3. **ChatRules** (`chat_rules.py`) - 10+ reglas
   - Mensajes no se envían
   - Notificaciones no funcionan
   - Lag en el chat

4. **ContentRules** (`content_rules.py`) - 8+ reglas
   - Contenido no carga
   - Enlaces rotos
   - Acceso denegado

---

### 3. **EdTechExpertSystem** - `knowledge_base/expert_system.py`

Es el motor principal que hereda de:
- `KnowledgeEngine` (de Experta)
- `LoginRules`, `VideoRules`, `ChatRules`, `ContentRules`

#### Método Principal: `diagnose()`

```python
def diagnose(self, symptoms_data):
    # 1. Resetear el motor
    self.reset()
    
    # 2. Declarar los síntomas como hechos
    for symptom in symptoms_data.get("symptoms", []):
        self.declare(Symptom(**symptom))
    
    # 3. Declarar información del sistema
    self.declare(SystemInfo(**symptoms_data["system_info"]))
    
    # 4. Declarar estado del servidor
    self.declare(ServerStatus(**symptoms_data["server_status"]))
    
    # 5. Ejecutar el motor de inferencia
    self.run()
    
    # 6. Recolectar todos los diagnósticos generados
    diagnosis = self._collect_diagnoses()
    
    # 7. Retornar resultados ordenados por confianza
    return sorted(diagnosis, key=lambda d: d["confidence"], reverse=True)
```

---

## 🔄 Flujo de Ejecución

### Paso a Paso:

```
1. Usuario completa el formulario web (index.html)
   ↓
2. JavaScript envía POST a /api/diagnose con JSON
   ↓
3. Flask recibe la solicitud en app.py (endpoint diagnose())
   ↓
4. Flask valida los datos de entrada:
   - Campos obligatorios presentes
   - Navegador válido
   - Tipo de conexión válido
   ↓
5. Flask llama a DiagnosisService.run(data, persist=True)
   ↓
6. DiagnosisService llama a EdTechExpertSystem.diagnose()
   ↓
7. EdTechExpertSystem ejecuta:
   a. Declara hechos (Symptom, SystemInfo, ServerStatus)
   b. Motor de inferencia (RETE) evalúa TODAS las reglas
   c. Reglas que coinciden declaran Diagnosis
   ↓
8. Sistema recolecta todos los Diagnosis generados
   ↓
9. Selecciona el diagnóstico con mayor confianza
   ↓
10. DiagnosisService guarda en historial (HistoryService)
   ↓
11. Flask convierte resultado a JSON con jsonify()
   ↓
12. Flask retorna HTTP 200 con el diagnóstico
   ↓
13. JavaScript recibe JSON y muestra resultado en la interfaz
```

### Ejemplo Concreto:

**Entrada del Usuario:**
```json
{
  "symptoms": [{
    "type": "login",
    "description": "cannot_login"
  }],
  "system_info": {
    "browser": "IE",
    "connection_type": "wifi"
  },
  "server_status": {
    "is_online": true
  }
}
```

**Proceso Interno:**
1. Motor declara: `Symptom(type="login", description="cannot_login")`
2. Motor declara: `SystemInfo(browser="IE")`
3. Motor ejecuta todas las reglas de LoginRules
4. **Regla `cannot_login_ie` coincide** (95% confianza)
5. Motor declara: `Diagnosis(problem_type="login", cause="browser", ...)`

**Salida:**
```json
{
  "diagnosis": "login",
  "cause": "browser",
  "solution": "Estás usando Internet Explorer. Cambiá a Chrome, Firefox, Edge o Safari.",
  "confidence": 0.95
}
```

---

## ⚙️ Motor de Inferencia

El motor de inferencia de **Experta** funciona con el algoritmo **RETE** (encadenamiento hacia adelante):

### Características:

1. **Forward Chaining (Encadenamiento hacia adelante)**
   - Parte de los hechos conocidos
   - Aplica reglas hasta llegar a conclusiones
   - Opuesto a backward chaining (partir de la conclusión)

2. **Pattern Matching (Coincidencia de Patrones)**
   - Compara hechos actuales con condiciones de las reglas
   - Usa `MATCH` para capturar valores
   - Usa `TEST` para validaciones adicionales

3. **Conflict Resolution (Resolución de Conflictos)**
   - Si múltiples reglas coinciden, se ejecutan todas
   - Cada regla puede declarar su propio Diagnosis
   - El sistema selecciona el de mayor confianza

### Ejemplo de Pattern Matching Avanzado:

```python
@Rule(
    Symptom(type="login", description="cannot_login"),
    SystemInfo(browser=MATCH.br),  # Captura el valor del navegador
    TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari"))  # Valida
)
def cannot_login_good_browser(self, br):
    # br contiene el navegador capturado
    self.declare(Diagnosis(...))
```

---

## 📚 Base de Conocimiento

### Síntomas Reconocidos:

| Categoría | Síntomas |
|-----------|----------|
| **Login** | cannot_login, forgot_password, account_locked, invalid_credentials, registration_failed |
| **Video** | video_not_loading, video_buffering, video_quality_poor, audio_issues, playback_controls_not_working |
| **Chat** | messages_not_sending, cannot_see_messages, notification_issues, emoji_not_working, chat_lag |
| **Content** | content_not_loading, missing_files, broken_links, formatting_issues, access_denied_to_content |

### Causas Identificadas:

| Tipo | Descripción |
|------|-------------|
| **server** | Problema del servidor |
| **browser** | Problema del navegador |
| **user** | Problema del usuario o configuración |
| **network** | Problema de red/conectividad |
| **device** | Problema del dispositivo/audio |
| **permissions** | Falta de permisos o rol |
| **link** | Problema con el enlace |

---

## 🎯 Cálculo de Confianza

El nivel de confianza (0.0 - 1.0) se asigna manualmente en cada regla según:

### Criterios:

1. **Confianza Alta (0.85 - 1.0)**
   - Síntoma muy específico
   - Causa claramente identificable
   - Ejemplo: IE + cannot_login = 0.95

2. **Confianza Media (0.60 - 0.84)**
   - Síntoma con múltiples causas posibles
   - Información del sistema parcial
   - Ejemplo: video_buffering + slow_wifi = 0.75

3. **Confianza Baja (0.40 - 0.59)**
   - Síntoma genérico
   - Falta información del contexto
   - Ejemplo: content_not_loading sin más datos = 0.50

### Selección del Mejor Diagnóstico:

```python
# Si múltiples reglas generan diagnósticos
best_diagnosis = max(diagnosis, key=lambda d: d["confidence"])
```

El sistema siempre retorna el diagnóstico con **mayor confianza**.

---

## 🔍 Ventajas del Enfoque

1. **Modularidad**: Reglas separadas por categoría
2. **Extensibilidad**: Fácil agregar nuevas reglas
3. **Transparencia**: Cada regla es legible y auditable
4. **Mantenibilidad**: Cambios en reglas no afectan el motor
5. **Escalabilidad**: Soporta cientos de reglas sin degradación

---

## 📝 Ejemplo Completo de Diagnóstico

### Entrada:
```json
{
  "symptoms": [{
    "type": "video",
    "description": "video_buffering",
    "severity": "high",
    "frequency": "always"
  }],
  "system_info": {
    "browser": "Chrome",
    "connection_type": "slow_wifi",
    "device_type": "desktop"
  },
  "server_status": {
    "is_online": true,
    "response_time": 450
  }
}
```

### Reglas Evaluadas:
1. ✅ `video_buffering_slow_wifi` → Confianza: 0.88
2. ✅ `video_buffering_general` → Confianza: 0.65
3. ❌ `video_buffering_server_down` → No coincide (servidor online)

### Diagnóstico Seleccionado:
```json
{
  "diagnosis": "video",
  "cause": "network",
  "solution": "El video se corta por WiFi lento. Acercate al router, usá Ethernet o bajá la calidad del video.",
  "confidence": 0.88
}
```

### Visualización en la Interfaz:
- **Barra de confianza**: Verde (88%)
- **Causa**: Problema de la red/conectividad
- **Solución**: Recomendaciones específicas

---

## 🚀 Conclusión

Este sistema experto combina:
- **Flask API REST** (capa de presentación y comunicación HTTP)
- **Lógica declarativa** (reglas IF-THEN basadas en CLIPS)
- **Motor de inferencia RETE** (algoritmo eficiente de pattern matching)
- **Base de conocimiento** (hechos + reglas organizadas por categoría)
- **Validaciones robustas** (entrada, navegadores, conexiones)
- **Persistencia de datos** (historial de diagnósticos)

### Ventajas de la Arquitectura:

1. **Separación de responsabilidades**:
   - Flask maneja HTTP y validaciones
   - DiagnosisService coordina la lógica de negocio
   - EdTechExpertSystem contiene el conocimiento experto

2. **Escalabilidad**:
   - Fácil agregar nuevos endpoints
   - Fácil agregar nuevas reglas sin modificar Flask
   - Soporta múltiples usuarios concurrentes

3. **Mantenibilidad**:
   - Código modular y bien comentado
   - Reglas legibles y auditables
   - Logs detallados para debugging

4. **Extensibilidad**:
   - API REST permite integración con otras aplicaciones
   - Frontend puede ser reemplazado sin cambiar el backend
   - Nuevas categorías de problemas se agregan fácilmente

El resultado es un sistema **inteligente, mantenible y escalable** para diagnosticar problemas en plataformas educativas virtuales, accesible desde cualquier navegador web.
