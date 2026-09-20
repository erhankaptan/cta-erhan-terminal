from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import json

class StructuredInformation:
    def __init__(self, raw_data: Any, provenance: str, data_payload: Dict[str, Any], timestamp: Optional[str] = None):
        self.raw_data = raw_data
        self.provenance = provenance
        self.data_payload = data_payload
        self.timestamp = timestamp or datetime.now().isoformat()

class IntegrationEngine:
    def __init__(self, storage_file="cta_pool.json"):
        self.storage_file = storage_file
        self.pool: List[StructuredInformation] = []
        self.load_pool_from_disk()
        
        self.findings: List[Dict[str, Any]] = []
        from core.query import PoolQueryEngine
        from core.analytics import AnalyticsEngine
        self.query_engine = PoolQueryEngine(self.pool)
        self.analytics = AnalyticsEngine(self.pool, self.findings)
        from core.logger import SystemLogger
        self.logger = SystemLogger()

    def load_pool_from_disk(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data_list = json.load(f)
                    for item in data_list:
                        record = StructuredInformation(
                            raw_data=item.get("raw_data"),
                            provenance=item.get("provenance"),
                            data_payload=item.get("data_payload"),
                            timestamp=item.get("timestamp")
                        )
                        self.pool.append(record)
            except Exception:
                pass

    def save_pool_to_disk(self):
        try:
            data_list = []
            for r in self.pool:
                data_list.append({
                    "raw_data": r.raw_data,
                    "provenance": r.provenance,
                    "data_payload": r.data_payload,
                    "timestamp": r.timestamp
                })
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def validate_payload(self, data: Any) -> bool:
        """Gelen verinin geçerli bir şemaya sahip olup olmadığını denetler"""
        if data is None:
            return False
        if isinstance(data, (dict, list)):
            if len(data) == 0:
                return False
            return True
        return False

    def ingest_and_process_url(self, url: str) -> Dict[str, Any]:
        try:
            import urllib.request
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                raw_content = response.read().decode('utf-8')
                data = json.loads(raw_content)
            
            if not self.validate_payload(data):
                self.logger.error(f"Geçersiz veri şeması reddedildi -> URL: {url}")
                return {"status": "error", "message": "Şema doğrulama başarısız: Geçersiz veya boş veri yapısı."}
            
            payload = data if isinstance(data, dict) else {"items": data}
            structured = StructuredInformation(
                raw_data=data,
                provenance=f"live_api:{url}",
                data_payload=payload
            )
            
            self.pool.append(structured)
            self.save_pool_to_disk()
            self.logger.info(f"Başarılı ingestion ve doğrulama -> {structured.provenance}")
            return {"status": "success", "provenance": structured.provenance}
        except Exception as e:
            self.logger.error(f"Ingestion sırasında hata oluştu ({url}): {str(e)}")
            return {"status": "error", "message": str(e)}

    def ingest_all_from_config(self, config_file="config.json") -> Dict[str, Any]:
        """config.json dosyasındaki tüm kaynakları sırayla çeker ve işler"""
        if not os.path.exists(config_file):
            return {"status": "error", "message": "config.json dosyası bulunamadı."}
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            
            sources = config_data.get("sources", [])
            success_count = 0
            error_count = 0
            
            for url in sources:
                result = self.ingest_and_process_url(url)
                if result["status"] == "success":
                    success_count += 1
                else:
                    error_count += 1
                    
            return {
                "status": "success",
                "total_sources": len(sources),
                "successful": success_count,
                "failed": error_count
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search_pool(self, keyword: str) -> List[Dict[str, Any]]:
        matched_records = self.query_engine.search_by_keyword(keyword)
        results = []
        for idx, record in enumerate(matched_records):
            results.append({
                "record_id": idx + 1,
                "provenance": record.provenance,
                "snippet": str(record.data_payload),
                "timestamp": record.timestamp
            })
        return results

    def generate_report(self) -> Dict[str, Any]:
        return self.analytics.generate_summary_report()