import os, json

_HISTORY_PATH = "data/responses.json"

class HistoryService:
    @staticmethod
    def _ensure_dir():
        d = os.path.dirname(_HISTORY_PATH)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    @staticmethod
    def load():
        if not os.path.exists(_HISTORY_PATH):
            return []
        try:
            with open(_HISTORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        except Exception:
            return []

    @staticmethod
    def append(entry: dict):
        HistoryService._ensure_dir()
        data = HistoryService.load()
        data.append(entry)
        with open(_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

