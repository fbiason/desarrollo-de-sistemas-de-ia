from experta import KnowledgeEngine
from .facts import Symptom, SystemInfo, ServerStatus, Diagnosis
from .facts import LOGIN_SYMPTOMS, VIDEO_SYMPTOMS, CHAT_SYMPTOMS, CONTENT_SYMPTOMS
from .rules import EdTechRules

class EdTechExpertSystem(KnowledgeEngine, EdTechRules):
    """Expert system for diagnosing issues in educational technology platforms."""
    
    def __init__(self):
        super().__init__()
        self.diagnosis_result = None
    
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
        
        # Add symptoms to the knowledge base
        for symptom in symptoms_data.get("symptoms", []):
            self.declare(Symptom(**symptom))
        
        # Add system information if available
        if "system_info" in symptoms_data:
            self.declare(SystemInfo(**symptoms_data["system_info"]))
        else:
            self.declare(SystemInfo())  # Default system info
        
        # Add server status if available
        if "server_status" in symptoms_data:
            self.declare(ServerStatus(**symptoms_data["server_status"]))
        else:
            self.declare(ServerStatus())  # Default server status
        
        # Run the inference engine
        self.run()
        
        # Return the diagnosis result
        if self.diagnosis_result:
            return self.diagnosis_result
        else:
            return {
                "diagnosis": "Unknown issue",
                "cause": "Could not determine cause",
                "solution": "Please contact technical support for assistance.",
                "confidence": 0
            }
    
    def get_available_symptoms(self):
        """
        Return a list of all symptoms the system can diagnose.
        
        Returns:
            dict: Categories of symptoms the system can recognize
        """
        return {
            "login": LOGIN_SYMPTOMS,
            "video": VIDEO_SYMPTOMS,
            "chat": CHAT_SYMPTOMS,
            "content": CONTENT_SYMPTOMS
        }

    # Override the default run_all method to capture the diagnosis
    def run_all(self):
        """Run all rules and store the diagnosis."""
        super().run_all()
        
        # Get the most confident diagnosis
        diagnoses = [fact for fact in self.facts.values() if isinstance(fact, Diagnosis)]
        if diagnoses:
            # Sort by confidence (highest first)
            best_diagnosis = sorted(diagnoses, key=lambda x: x.get("confidence", 0), reverse=True)[0]
            self.diagnosis_result = {
                "diagnosis": best_diagnosis.get("problem_type"),
                "cause": best_diagnosis.get("cause"),
                "solution": best_diagnosis.get("solution"),
                "confidence": best_diagnosis.get("confidence", 0)
            }
        
        return self
