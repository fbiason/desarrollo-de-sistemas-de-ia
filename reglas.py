# reglas.py - Base de conocimiento y motor de inferencia

from experta import KnowledgeEngine, Rule, MATCH, TEST
from modelos import Symptom, SystemInfo, ServerStatus, Diagnosis
from modelos import LOGIN_SYMPTOMS, VIDEO_SYMPTOMS, CHAT_SYMPTOMS, CONTENT_SYMPTOMS
from knowledge_base.rules import LoginRules, VideoRules, ChatRules, ContentRules


class EdTechExpertSystem(KnowledgeEngine, LoginRules, VideoRules, ChatRules, ContentRules):
    """
    Sistema experto para diagnosticar problemas en plataformas de tecnología educativa.
    
    Hereda de:
    - KnowledgeEngine: Motor de inferencia de Experta
    - LoginRules: Reglas para problemas de inicio de sesión
    - VideoRules: Reglas para problemas de video
    - ChatRules: Reglas para problemas de chat
    - ContentRules: Reglas para problemas de contenido
    """
    
    def __init__(self):
        super().__init__()
        self.diagnosis_result = None

    def _collect_diagnoses(self):
        """Recolecta todos los diagnósticos generados durante la inferencia."""
        return [f for f in self.facts.values() if isinstance(f, Diagnosis)]

    def diagnose(self, symptoms_data):
        """
        Ejecuta el sistema experto con los síntomas proporcionados.
        
        Args:
            symptoms_data (dict): Diccionario con síntomas e información del sistema
                Ejemplo: {
                    "symptoms": [{"type": "login", "description": "cannot_login"}],
                    "system_info": {"browser": "Chrome", "browser_version": "90.0"},
                    "server_status": {"is_online": True}
                }
        
        Returns:
            list: Lista de diagnósticos con causa y solución
        """
        # Resetear el motor para un nuevo diagnóstico
        self.reset()
        
        # Declarar los síntomas como hechos
        for symptom in symptoms_data.get("symptoms", []):
            self.declare(Symptom(**symptom))
        
        # Declarar información del sistema
        if "system_info" in symptoms_data:
            self.declare(SystemInfo(**symptoms_data["system_info"]))
        else:
            self.declare(SystemInfo())
        
        # Declarar estado del servidor
        if "server_status" in symptoms_data:
            self.declare(ServerStatus(**symptoms_data["server_status"]))
        else:
            self.declare(ServerStatus())

        # Ejecutar el motor de inferencia
        self.run()
        
        # Recolectar todos los diagnósticos generados
        diagnosis = self._collect_diagnoses()

        # Formatear resultados
        results = [
            {
                "diagnosis": d.get("problem_type"),
                "cause": d.get("cause"),
                "solution": d.get("solution"),
                "confidence": float(d.get("confidence") or 0.0)
            }
            for d in diagnosis
        ]
        return results

    
    def get_available_symptoms(self):
        """Retorna los síntomas disponibles por categoría."""
        return {
            "login": LOGIN_SYMPTOMS,
            "video": VIDEO_SYMPTOMS,
            "chat": CHAT_SYMPTOMS,
            "content": CONTENT_SYMPTOMS
        }

    def run_all(self):
        """Ejecuta todas las reglas y selecciona el mejor diagnóstico."""
        super().run_all()
        
        diagnoses = [fact for fact in self.facts.values() if isinstance(fact, Diagnosis)]
        if diagnoses:
            # Seleccionar el diagnóstico con mayor confianza
            best_diagnosis = sorted(diagnoses, key=lambda x: x.get("confidence", 0), reverse=True)[0]
            self.diagnosis_result = {
                "diagnosis": best_diagnosis.get("problem_type"),
                "cause": best_diagnosis.get("cause"),
                "solution": best_diagnosis.get("solution"),
                "confidence": best_diagnosis.get("confidence", 0)
            }
        
        return self
