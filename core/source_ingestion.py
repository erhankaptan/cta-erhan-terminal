import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class SourceIngestionManager:
    def __init__(self):
        pass

    def fetch_from_api(self, url: str) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat()
        
        # Nitter ve diğer sitelerin bizi bot sanıp engellememesi için tarayıcı kimliği ekliyoruz
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            # Timeout süresini 5'ten 15'e çıkardık, çünkü Nitter bazen yavaş yanıt verir
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return {
                    "source_id": url,
                    "status": "available",
                    "timestamp": timestamp,
                    "content": response.text, # Tickmill RSS'i için response.text kalmalı!
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
