import re
from typing import Dict, Any

class DataValidator:
    @staticmethod
    def sanitize_text(text: str) -> str:
        if not text:
            return ""
        # HTML taglerini ve zararlı olabilecek karakterleri temizleme
        clean_text = re.sub(r'<[^>]*>', '', text)
        # Fazla boşlukları ve satır sonlarını normalize etme
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    @staticmethod
    def validate_canonical_data(data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict):
            return False
        if "parsed_text" not in data:
            return False
        # Minimum uzunluk ve içerik kontrolü
        if len(str(data["parsed_text"])) == 0:
            return False
        return True