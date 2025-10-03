from flask import Flask, request, jsonify, render_template
import logging
from knowledge_base.expert_system import EdTechExpertSystem

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

expert_system = EdTechExpertSystem()

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """API endpoint for diagnosing problems."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract problem symptoms from request
        symptoms = data.get('symptoms', [])
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # Run the expert system with the provided symptoms
        diagnosis = expert_system.diagnose(data)  # Pasar todo el objeto data
        
        return jsonify({
            "diagnosis": diagnosis.get("diagnosis", "Unknown issue"),
            "cause": diagnosis.get("cause", "Could not determine cause"),
            "solution": diagnosis.get("solution", "No solution available"),
            "confidence": diagnosis.get("confidence", 0)
        })
    except Exception as e:
        app.logger.error(f"Error en diagnóstico: {str(e)}")
        return jsonify({"error": f"Error en el procesamiento: {str(e)}"}), 500

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Return the list of possible symptoms the system can diagnose."""
    return jsonify({
        "symptoms": expert_system.get_available_symptoms()
    })

if __name__ == '__main__':
    app.run(debug=True)
