import json
import os
from datetime import datetime

class StorageManager:
    def __init__(self, storage_dir="data_store"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        self.records_file = os.path.join(self.storage_dir, "canonical_records.json")
        self._init_files()

    def _init_files(self):
        if not os.path.exists(self.records_file):
            with open(self.records_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_record(self, record_id: str, data: dict, provenance: str, version: int) -> bool:
        with open(self.records_file, "r", encoding="utf-8") as f:
            records = json.load(f)
        
        # Duplicate ve eski verinin üzerine yazmayı engelleme kontrolü
        for rec in records:
            if rec["record_id"] == record_id:
                return False

        new_record = {
            "record_id": record_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
            "provenance": provenance,
            "version": version
        }
        records.append(new_record)

        with open(self.records_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
        return True

    def load_records(self) -> list:
        if not os.path.exists(self.records_file):
            return []
        with open(self.records_file, "r", encoding="utf-8") as f:
            return json.load(f)