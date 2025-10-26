# 📚 GLOSARIO - Sistema Experto para Plataformas EdTech

Este documento define los conceptos clave utilizados en el desarrollo del sistema experto para diagnóstico de problemas en plataformas de educación virtual.

---

## 🧠 Conceptos de Sistemas Expertos

### **Sistema Experto**
Programa de inteligencia artificial que emula la capacidad de toma de decisiones de un experto humano en un dominio específico. En este proyecto, el sistema diagnostica problemas técnicos en plataformas educativas basándose en síntomas reportados.

**Ejemplo**: Un usuario reporta "no puedo iniciar sesión" → el sistema analiza síntomas, navegador y estado del servidor → diagnostica "credenciales incorrectas" con 95% de confianza → sugiere "restablecer contraseña".

### **Base de Conocimiento (Knowledge Base)**
Repositorio estructurado que contiene el conocimiento del dominio en forma de hechos y reglas. En este proyecto, incluye:
- **Hechos (Facts)**: Información sobre síntomas, estado del sistema, información del navegador, etc.
- **Reglas (Rules)**: Condiciones lógicas que relacionan síntomas con diagnósticos y soluciones.

**Ubicación en el proyecto**: `knowledge_base/`

**Ejemplo**: La base contiene 20+ reglas como "SI navegador=IE Y síntoma=no_login ENTONCES causa=navegador_incompatible" y hechos como `Symptom(type="login", description="cannot_login")`.

### **Motor de Inferencia (Inference Engine)**
Componente que procesa las reglas de la base de conocimiento para llegar a conclusiones. Utiliza algoritmos de razonamiento para:
- Evaluar condiciones de las reglas
- Ejecutar acciones cuando las condiciones se cumplen
- Generar diagnósticos basados en los hechos declarados

**Implementación**: Proporcionado por la librería `Experta`

**Ejemplo**: El motor recibe `Symptom(type="video")` y `SystemInfo(browser="Chrome")` → evalúa 5 reglas de video → encuentra coincidencia con regla de caché → ejecuta acción que declara `Diagnosis(cause="browser", solution="limpiar caché")`.

### **Hechos (Facts)**
Representaciones de información conocida sobre el problema actual. Tipos de hechos en este sistema:
- `Symptom`: Síntomas reportados por el usuario
- `SystemInfo`: Información del navegador y sistema operativo
- `ServerStatus`: Estado del servidor y métricas de rendimiento
- `Diagnosis`: Resultado del diagnóstico generado por el sistema

**Ubicación**: `knowledge_base/facts.py`

**Ejemplo**: `Symptom(type="chat", description="messages_not_sending", severity="high")` o `SystemInfo(browser="Firefox", os="Windows", connection_type="wifi")`.

### **Reglas (Rules)**
Declaraciones lógicas del tipo "SI [condiciones] ENTONCES [acciones]". Cada regla evalúa patrones de hechos y genera diagnósticos cuando se cumplen las condiciones.

**Ejemplo**:
```python
@Rule(Symptom(type="login", description="cannot_login"), 
      SystemInfo(browser="IE"))
def cannot_login_ie(self):
    self.declare(Diagnosis(...))
```

**Ubicación**: `knowledge_base/rules/`

### **Encadenamiento Hacia Adelante (Forward Chaining)**
Estrategia de inferencia utilizada por Experta donde el motor comienza con los hechos conocidos y aplica reglas para derivar nuevas conclusiones hasta alcanzar un objetivo o agotar las reglas aplicables.

**Ejemplo**: Hechos iniciales: [video_no_carga, navegador=Chrome] → Regla 1 activa: declara [problema_reproducción] → Regla 2 activa: declara [revisar_extensiones] → No más reglas aplicables → Fin.

### **Pattern Matching**
Proceso mediante el cual el motor de inferencia compara los hechos declarados con las condiciones de las reglas para determinar cuáles son aplicables. Experta utiliza el algoritmo RETE para optimizar este proceso.

**Ejemplo**: Regla busca `Symptom(type="login") & SystemInfo(browser="IE")` → Motor compara con hechos actuales → Encuentra coincidencia → Marca regla como aplicable.

### **Confianza (Confidence)**
Valor numérico (0.0 a 1.0) que indica el nivel de certeza del diagnóstico. Valores más altos representan mayor confianza en la solución propuesta.

**Ejemplo**: Diagnóstico con múltiples síntomas coincidentes: `confidence=0.95` (95%). Diagnóstico con síntomas ambiguos: `confidence=0.60` (60%).

---

## 🌐 Tecnologías Web y API

### **API REST (RESTful API)**
Interfaz de programación de aplicaciones que sigue los principios de la arquitectura REST (Representational State Transfer). Permite la comunicación entre el cliente y el servidor mediante peticiones HTTP estándar.

**Endpoints del proyecto**:
- `POST /api/diagnose`: Ejecuta el diagnóstico
- `GET /api/diagnosis`: Obtiene el historial de diagnósticos

**Ejemplo**: Cliente envía `POST /api/diagnose` con síntomas en JSON → Servidor procesa → Responde con `{"diagnosis": {...}, "confidence": 0.9}` en formato JSON.

### **Flask**
Framework web minimalista de Python utilizado para crear la API REST y servir la interfaz web del sistema experto.

**Versión**: Flask 2.3.0

**Características utilizadas**:
- Enrutamiento de URLs (`@app.route`)
- Manejo de peticiones JSON (`request.get_json()`)
- Respuestas JSON (`jsonify()`)
- Renderizado de templates (`render_template()`)
- Logging para depuración

**Archivo principal**: `app.py`

**Ejemplo**: `@app.route('/api/diagnose', methods=['POST'])` define un endpoint que responde a peticiones POST en la ruta `/api/diagnose`.

### **Endpoint**
Punto de acceso específico de una API que responde a peticiones HTTP. Cada endpoint tiene una URL única y un método HTTP asociado (GET, POST, PUT, DELETE, etc.).

**Ejemplo**: `POST http://localhost:5000/api/diagnose` es un endpoint que acepta datos de diagnóstico. `GET http://localhost:5000/api/diagnosis` devuelve el historial.

### **JSON (JavaScript Object Notation)**
Formato ligero de intercambio de datos utilizado para la comunicación entre el cliente y el servidor. Estructura basada en pares clave-valor.

**Ejemplo de petición**:
```json
{
  "symptoms": [{"type": "login", "description": "cannot_login"}],
  "system_info": {"browser": "Chrome", "connection_type": "wifi"}
}
```

### **HTTP Methods**
Métodos estándar del protocolo HTTP utilizados en la API:
- **GET**: Recuperar información (historial de diagnósticos)
- **POST**: Enviar datos para procesamiento (ejecutar diagnóstico)

**Ejemplo**: `GET /api/diagnosis` → solo lee datos, no modifica nada. `POST /api/diagnose` → envía síntomas y crea un nuevo diagnóstico.

### **Status Codes HTTP**
Códigos numéricos que indican el resultado de una petición HTTP:
- **200 OK**: Petición exitosa
- **400 Bad Request**: Error en los datos enviados
- **500 Internal Server Error**: Error en el servidor

**Ejemplo**: Diagnóstico exitoso retorna `200 OK`. Envío sin síntomas retorna `400 Bad Request: "symptoms" field is required`. Error en el motor retorna `500 Internal Server Error`.

---

## 🐍 Librerías y Frameworks Python

### **Experta**
Librería de Python para crear sistemas expertos basados en reglas. Es un port de CLIPS (C Language Integrated Production System) a Python.

**Versión**: 1.9.4

**Componentes principales**:
- `KnowledgeEngine`: Clase base para el motor de inferencia
- `Fact`: Clase para representar hechos
- `Rule`: Decorador para definir reglas
- `Field`: Define campos en los hechos

**Documentación**: Basada en el paradigma de programación basada en reglas

**Ejemplo**: `class EdTechExpertSystem(KnowledgeEngine):` crea un motor. `@Rule(Symptom(type="login"))` define una regla. `self.declare(Fact(...))` agrega un hecho.

### **Werkzeug**
Librería WSGI (Web Server Gateway Interface) utilizada por Flask para manejar peticiones HTTP, enrutamiento y utilidades web.

**Versión**: 2.3.0

**Ejemplo**: Werkzeug parsea la petición HTTP entrante, extrae headers, cookies y parámetros, y los pone a disposición de Flask mediante el objeto `request`.

### **Jinja2**
Motor de templates utilizado por Flask para renderizar páginas HTML dinámicas con datos del servidor.

**Versión**: 3.1.2

**Uso en el proyecto**: Renderizado de `templates/index.html`

**Ejemplo**: `{{ diagnosis.problem_type }}` en HTML se reemplaza con el valor real como "login" o "video" al renderizar la página.

### **Pytest**
Framework de testing para Python utilizado para escribir y ejecutar pruebas unitarias del sistema experto.

**Versión**: 7.4.0

**Ejemplo**: `def test_login_diagnosis():` define una prueba. `assert result['cause'] == 'browser'` verifica que el diagnóstico sea correcto. Ejecutar con `pytest tests/`.

### **Frozendict**
Estructura de datos inmutable (diccionario congelado) utilizada internamente por Experta para garantizar la inmutabilidad de los hechos.

**Versión**: 1.2

**Ejemplo**: Un `Fact(type="login")` se almacena internamente como frozendict para que no pueda ser modificado accidentalmente durante la inferencia.

---

## 🏗️ Arquitectura y Patrones de Diseño

### **Arquitectura en Capas**
Organización del código en capas con responsabilidades específicas:
1. **Capa de Presentación**: Templates HTML y archivos estáticos
2. **Capa de API**: Endpoints REST en `app.py`
3. **Capa de Servicios**: Lógica de negocio en `services/`
4. **Capa de Conocimiento**: Base de conocimiento en `knowledge_base/`

**Ejemplo**: Usuario hace clic en "Diagnosticar" → `index.html` (Presentación) → `POST /api/diagnose` (API) → `DiagnosisService` (Servicios) → `EdTechExpertSystem` (Conocimiento).

### **Separación de Responsabilidades (Separation of Concerns)**
Principio de diseño que divide el sistema en módulos independientes, cada uno con una responsabilidad específica:
- `expert_system.py`: Motor de inferencia
- `facts.py`: Definición de hechos
- `rules/`: Reglas por categoría (login, video, chat, content)
- `services/`: Servicios de diagnóstico e historial

**Ejemplo**: `login_rules.py` solo maneja reglas de login, no de video. `HistoryService` solo gestiona historial, no ejecuta diagnósticos. Cada módulo tiene una única responsabilidad.

### **Patrón Service**
Patrón de diseño que encapsula la lógica de negocio en clases de servicio:
- `DiagnosisService`: Ejecuta diagnósticos y gestiona síntomas
- `HistoryService`: Gestiona el historial de diagnósticos

**Ejemplo**: `DiagnosisService.run_diagnosis(symptoms)` encapsula toda la lógica: validar síntomas, crear motor, declarar hechos, ejecutar inferencia, retornar resultado.

### **Herencia Múltiple**
Técnica de programación orientada a objetos donde una clase hereda de múltiples clases padre. Utilizada en `EdTechExpertSystem` que hereda de:
- `KnowledgeEngine` (de Experta)
- `LoginRules`, `VideoRules`, `ChatRules`, `ContentRules`

**Ejemplo**: `class EdTechExpertSystem(KnowledgeEngine, LoginRules, VideoRules):` hereda el motor de `KnowledgeEngine` y todas las reglas de `LoginRules` y `VideoRules`.

---

## 📊 Conceptos del Dominio (EdTech)

### **EdTech (Educational Technology)**
Tecnología educativa. Uso de herramientas tecnológicas para facilitar el aprendizaje y la enseñanza. Este sistema diagnostica problemas en plataformas EdTech.

**Ejemplo**: Plataformas como Moodle, Canvas, Google Classroom, Zoom para educación. Este sistema diagnostica problemas técnicos que estudiantes y profesores enfrentan al usarlas.

### **Síntomas Categorizados**
Clasificación de problemas según el área afectada:
- **Login**: Problemas de autenticación y acceso
- **Video**: Problemas de reproducción multimedia
- **Chat**: Problemas de mensajería y comunicación
- **Content**: Problemas de carga y acceso a contenido

**Ejemplo**: Usuario reporta "no puedo ver el video de la clase" → categoría: **Video**. Usuario reporta "mis mensajes no se envían" → categoría: **Chat**.

### **Causas de Problemas**
Origen de los problemas diagnosticados:
- **Server**: Problemas del servidor (caído, mantenimiento, alta carga)
- **Browser**: Problemas del navegador (incompatible, desactualizado, caché)
- **User**: Problemas del usuario (credenciales, red, permisos)

**Ejemplo**: Video no carga + navegador IE → causa: **Browser** (navegador incompatible). Login falla + servidor caído → causa: **Server**. Chat no funciona + conexión lenta → causa: **User** (problema de red).

### **Diagnóstico**
Resultado del análisis del sistema experto que incluye:
- **Tipo de problema**: Categoría del problema (login, video, etc.)
- **Causa**: Origen del problema (server, browser, user)
- **Solución**: Pasos recomendados para resolver el problema
- **Confianza**: Nivel de certeza del diagnóstico (0.0 a 1.0)

**Ejemplo**: `{"problem_type": "video", "cause": "browser", "solution": "Actualizar navegador o usar Chrome/Firefox", "confidence": 0.85, "timestamp": "2025-10-26T17:30:00"}`

---

## 🔧 Conceptos de Desarrollo

### **Virtual Environment (venv)**
Entorno aislado de Python que contiene sus propias dependencias independientes del sistema. Permite gestionar versiones de librerías específicas para el proyecto.

**Comando de activación**:
- Windows: `venv\Scripts\activate`
- Linux/macOS: `source venv/bin/activate`

**Ejemplo**: Proyecto A usa Flask 2.3.0, Proyecto B usa Flask 3.0.0. Cada uno tiene su propio venv con su versión de Flask sin conflictos.

### **requirements.txt**
Archivo que lista todas las dependencias del proyecto con sus versiones específicas. Facilita la instalación reproducible del entorno.

**Instalación**: `pip install -r requirements.txt`

**Ejemplo**: Contenido del archivo: `Flask==2.3.0`, `experta==1.9.4`, `pytest==7.4.0`. Ejecutar `pip install -r requirements.txt` instala exactamente estas versiones.

### **Logging**
Sistema de registro de eventos y errores del sistema. Utilizado para depuración y monitoreo.

**Niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Ejemplo**: `app.logger.info("Diagnóstico ejecutado exitosamente")` registra información. `app.logger.error("Error al procesar síntomas")` registra un error en la consola.

### **Exception Handling**
Manejo de errores mediante bloques `try-except` para capturar y gestionar excepciones sin que el sistema se detenga.

**Ejemplo**: `try: engine.run() except Exception as e: return {"error": str(e)}, 500` captura cualquier error durante la inferencia y retorna un mensaje en lugar de crashear.

### **Validación de Entrada**
Proceso de verificar que los datos recibidos cumplen con el formato y valores esperados antes de procesarlos.

**Validaciones implementadas**:
- Navegadores válidos: Chrome, Firefox, Edge, Safari, IE, Other
- Tipos de conexión: wifi, ethernet, cellular, slow_wifi
- Estructura de síntomas (lista no vacía)

**Ejemplo**: Si usuario envía `browser="Netscape"` → sistema rechaza con error 400. Si envía `symptoms=[]` (vacío) → error "symptoms cannot be empty".

### **Persistencia de Datos**
Almacenamiento de información de forma permanente. En este proyecto, el historial de diagnósticos se guarda en archivos JSON.

**Ejemplo**: Cada diagnóstico se guarda en `data/diagnosis_history.json`. Al reiniciar el servidor, el historial persiste y puede ser consultado mediante `GET /api/diagnosis`.

---

## 🎨 Frontend y Visualización

### **Dashboard**
Interfaz visual que presenta información resumida y métricas del sistema en tiempo real.

**Componentes**:
- Estadísticas generales
- Gráficos de distribución
- Historial de diagnósticos

**Ejemplo**: El dashboard muestra "Total de diagnósticos: 45", "Problemas más comunes: Video (40%)", gráfico de barras con tipos de problemas, y lista de últimos 10 diagnósticos.

### **Chart.js**
Librería JavaScript para crear gráficos interactivos en el navegador.

**Tipos de gráficos utilizados**:
- Gráficos de barras (problemas por tipo)
- Gráficos circulares (causas identificadas)
- Gráficos de línea (tendencias)

**Ejemplo**: `new Chart(ctx, {type: 'bar', data: {labels: ['Login', 'Video', 'Chat'], datasets: [{data: [15, 25, 10]}]}})` crea un gráfico de barras mostrando 15 problemas de login, 25 de video, 10 de chat.

### **Responsive Design**
Diseño web que se adapta a diferentes tamaños de pantalla (escritorio, tablet, móvil).

**Ejemplo**: En escritorio, el dashboard muestra 3 columnas con gráficos. En móvil, se reorganiza a 1 columna vertical. Usa CSS media queries: `@media (max-width: 768px) { .dashboard { flex-direction: column; } }`.

### **SPA (Single Page Application)**
Aplicación web que carga una única página HTML y actualiza dinámicamente el contenido mediante JavaScript sin recargar la página completa.

**Ejemplo**: Usuario hace clic en "Diagnosticar" → JavaScript envía petición AJAX → recibe respuesta → actualiza solo la sección de resultados sin recargar toda la página.

---

## 🔄 Conceptos de Flujo de Datos

### **Request-Response Cycle**
Ciclo de comunicación entre cliente y servidor:
1. Cliente envía petición HTTP
2. Servidor procesa la petición
3. Servidor envía respuesta HTTP
4. Cliente procesa la respuesta

**Ejemplo**: Usuario envía `POST /api/diagnose` con síntomas (1) → Flask recibe y ejecuta `DiagnosisService` (2) → Servidor retorna JSON con diagnóstico (3) → JavaScript muestra resultado en pantalla (4).

### **Serialización/Deserialización**
Proceso de convertir objetos Python a formato JSON (serialización) y viceversa (deserialización) para la comunicación entre cliente y servidor.

**Ejemplo**: Objeto Python `{"cause": "browser", "confidence": 0.9}` → serialización con `jsonify()` → string JSON `"{\"cause\": \"browser\", \"confidence\": 0.9}"` → envío al cliente → deserialización con `JSON.parse()` → objeto JavaScript.

### **Estado del Sistema (System State)**
Conjunto de hechos declarados en un momento dado que representa el conocimiento actual del sistema experto.

**Ejemplo**: Estado inicial: `[Symptom(type="login"), SystemInfo(browser="Chrome")]`. Después de ejecutar reglas: `[Symptom(...), SystemInfo(...), Diagnosis(cause="user", solution="....")]`.

### **Ciclo de Inferencia**
Proceso iterativo del motor de inferencia:
1. **Match**: Identificar reglas aplicables
2. **Select**: Seleccionar una regla para ejecutar
3. **Execute**: Ejecutar la acción de la regla
4. **Repeat**: Repetir hasta que no haya más reglas aplicables

**Ejemplo**: Iteración 1: Match encuentra 3 reglas aplicables → Select elige regla de login → Execute declara diagnóstico → Iteración 2: Match no encuentra más reglas → Fin.

---

## 📝 Conceptos de Documentación

### **Markdown**
Lenguaje de marcado ligero utilizado para formatear documentación de forma legible.

**Archivos del proyecto**:
- `README.md`: Instrucciones de instalación y uso
- `Funcionamiento.md`: Explicación técnica del sistema
- `GLOSARIO.md`: Este documento

**Ejemplo**: `# Título` crea encabezado nivel 1. `**negrita**` hace texto en negrita. `` `código` `` formatea como código inline. `- item` crea lista con viñetas.

### **Docstrings**
Cadenas de documentación en Python que describen el propósito y uso de funciones, clases y módulos.

**Formato utilizado**: Docstrings de Google/NumPy style

**Ejemplo**:
```python
def run_diagnosis(symptoms):
    """Ejecuta el diagnóstico basado en síntomas.
    
    Args:
        symptoms (list): Lista de síntomas reportados
    
    Returns:
        dict: Diagnóstico con causa y solución
    """
```

### **Comentarios Inline**
Comentarios dentro del código que explican líneas o bloques específicos para facilitar la comprensión.

**Ejemplo**: `# Validar que los síntomas no estén vacíos` o `engine.run()  # Ejecutar el motor de inferencia` explican qué hace cada línea de código.

---

## 🔐 Conceptos de Seguridad y Buenas Prácticas

### **Input Validation**
Validación de datos de entrada para prevenir inyecciones, errores y comportamientos inesperados.

**Ejemplo**: Antes de procesar, verificar: `if browser not in VALID_BROWSERS: return error`. Rechazar entradas como `<script>alert('hack')</script>` en campos de texto.

### **Error Handling**
Manejo robusto de errores que previene la exposición de información sensible y mantiene el sistema funcionando.

**Ejemplo**: En lugar de mostrar `KeyError: 'symptoms' at line 45 in diagnosis_service.py`, retornar mensaje genérico: `{"error": "Invalid request format"}` sin exponer detalles internos.

### **.gitignore**
Archivo que especifica qué archivos y directorios deben ser ignorados por el control de versiones Git.

**Exclusiones comunes**:
- `venv/`: Entorno virtual
- `__pycache__/`: Archivos compilados de Python
- `*.pyc`: Bytecode de Python
- `.env`: Variables de entorno sensibles

**Ejemplo**: Contenido del archivo: `venv/`, `__pycache__/`, `*.pyc`, `.env`. Git no sube estos archivos al repositorio, evitando subir dependencias o claves secretas.

---

## 🚀 Conceptos de Deployment

### **Debug Mode**
Modo de desarrollo de Flask que proporciona:
- Recarga automática al cambiar código
- Mensajes de error detallados
- Debugger interactivo

**⚠️ Advertencia**: Nunca usar en producción

**Ejemplo**: `app.run(debug=True)` activa el modo debug. Al modificar `app.py` y guardar, el servidor se reinicia automáticamente. Si hay error, muestra traceback completo en el navegador.

### **Localhost**
Dirección IP local (127.0.0.1) que apunta al propio equipo. Utilizada para desarrollo local.

**URL del proyecto**: `http://localhost:5000` o `http://127.0.0.1:5000`

**Ejemplo**: Ejecutar `python app.py` inicia servidor en `http://localhost:5000`. Solo tú puedes acceder desde tu navegador. Otros dispositivos en la red no pueden acceder.

### **Port**
Número que identifica un punto de comunicación específico en un servidor. Flask usa por defecto el puerto 5000.

**Ejemplo**: `app.run(port=5000)` usa puerto 5000 → URL: `http://localhost:5000`. Si cambias a `port=8080` → URL: `http://localhost:8080`. Puertos comunes: 80 (HTTP), 443 (HTTPS), 5000 (Flask).

---

## 📚 Referencias y Recursos

- **CLIPS**: C Language Integrated Production System (inspiración para Experta)
- **RETE Algorithm**: Algoritmo eficiente de pattern matching usado en sistemas expertos
- **REST**: Representational State Transfer (arquitectura de APIs)
- **WSGI**: Web Server Gateway Interface (estándar Python para aplicaciones web)

---

**Última actualización**: Octubre 2025  
**Versión del proyecto**: 1.0
