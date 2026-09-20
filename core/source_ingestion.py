import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class SourceIngestionManager:
    def __init__(self):
        pass

    def fetch_from_api(self, url: str) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat()
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return {
                    "source_id": url,
                    "status": "available",
                    "timestamp": timestamp,
                    "content": response.text,
                    "error": None
                }
            else:
                return {
                    "source_id": url,
                    "status": "access_failure",
                    "timestamp": timestamp,
                    "content": None,
                    "error": f"HTTP Error Status: {response.status_code}"
                }
        except Exception as e:
            return {
                "source_id": url,
                "status": "unavailable",
                "timestamp": timestamp,
                "content": None,
                "error": str(e)
            }

    def fetch_from_local_file(self, filepath: str) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat()
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                return {
                    "source_id": filepath,
                    "status": "available",
                    "timestamp": timestamp,
                    "content": content,
                    "error": None
                }
            except Exception as e:
                return {
                    "source_id": filepath,
                    "status": "partial_retrieval",
                    "timestamp": timestamp,
                    "content": None,
                    "error": str(e)
                }
        else:
            return {
                "source_id": filepath,
                "status": "missing",
                "timestamp": timestamp,
                "content": None,
                "error": "File not found"
            }