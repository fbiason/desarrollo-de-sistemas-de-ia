from knowledge_base.expert_system import EdTechExpertSystem
from services.history_service import HistoryService


class DiagnosisService:
    @staticmethod
    def run(data, persist: bool = True):
        engine = EdTechExpertSystem()

        diagnosis = engine.diagnose(data)
        best_diagnosis = max(diagnosis, key=lambda d: d["confidence"], default=None)

        if persist:
            HistoryService.append(best_diagnosis)
        return best_diagnosis

    @staticmethod
    def list_symptoms():
        engine = EdTechExpertSystem()
        return {"symptoms": engine.get_available_symptoms()}

    @staticmethod
    def history():
        return HistoryService.load()