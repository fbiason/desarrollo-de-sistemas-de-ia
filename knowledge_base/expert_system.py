from experta import KnowledgeEngine
from .facts import Symptom, SystemInfo, ServerStatus, Diagnosis
from .facts import LOGIN_SYMPTOMS, VIDEO_SYMPTOMS, CHAT_SYMPTOMS, CONTENT_SYMPTOMS
import json
from .rules import LoginRules, VideoRules, ChatRules, ContentRules

class EdTechExpertSystem(KnowledgeEngine, LoginRules, VideoRules, ChatRules, ContentRules):
    """Expert system for diagnosing issues in educational technology platforms."""
    
    def __init__(self):
        super().__init__()
        self.diagnosis_result = None

    def _collect_diagnoses(self):
        return [f for f in self.facts.values() if isinstance(f, Diagnosis)]

    def diagnose(self, symptoms_data):
        """
        Run the expert system with the provided symptoms.
        
        Args:
            symptoms_data (dict): Dictionary containing symptoms and system information
                Example: {
                    "symptoms": [{"type": "login", "description": "cannot_login"}],
                    "system_info": {"browser": "Chrome", "browser_version": "90.0"},
                    "server_status": {"is_online": True}
                }
        
        Returns:
            dict: Diagnosis result with problem cause and solution
        """
        self.reset()
        
        for symptom in symptoms_data.get("symptoms", []):
            self.declare(Symptom(**symptom))
        
        if "system_info" in symptoms_data:
            self.declare(SystemInfo(**symptoms_data["system_info"]))
        else:
            self.declare(SystemInfo())
        
        if "server_status" in symptoms_data:
            self.declare(ServerStatus(**symptoms_data["server_status"]))
        else:
            self.declare(ServerStatus())

        self.run()
        diagnosis =  self._collect_diagnoses()

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
        return {
            "login": LOGIN_SYMPTOMS,
            "video": VIDEO_SYMPTOMS,
            "chat": CHAT_SYMPTOMS,
            "content": CONTENT_SYMPTOMS
        }

    def run_all(self):
        super().run_all()
        
        diagnoses = [fact for fact in self.facts.values() if isinstance(fact, Diagnosis)]
        if diagnoses:
            best_diagnosis = sorted(diagnoses, key=lambda x: x.get("confidence", 0), reverse=True)[0]
            self.diagnosis_result = {
                "diagnosis": best_diagnosis.get("problem_type"),
                "cause": best_diagnosis.get("cause"),
                "solution": best_diagnosis.get("solution"),
                "confidence": best_diagnosis.get("confidence", 0)
            }
        
        return self
