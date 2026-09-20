# sources/scheduler.py
# CTA ERHAN Terminali - Arka Plan Otomatik Yenileme (Scheduler)

import time
import threading
from sources.registry import SOURCES_REGISTRY
from sources.ingestion import fetch_raw_data_from_source
from sources.normalization import normalize_raw_record
from sources.evidence_pool import global_evidence_pool

class BackgroundScheduler:
    def __init__(self):
        self._running = False
        self._thread = None

    def start_scheduler(self):
        """Arka plan otomatik veri yenileme döngüsünü başlatır."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop_scheduler(self):
        self._running = False

    def _run_loop(self):
        """Registry'deki poll_interval değerlerine göre periyodik ingestion tetikler."""
        while self._running:
            for source in SOURCES_REGISTRY:
                if not source.get("enabled", True):
                    continue
                
                # Gerçek ingestion ve normalizasyon zinciri
                raw = fetch_raw_data_from_source(source)
                if raw.get("status") == "SUCCESS":
                    norm = normalize_raw_record(raw, source.get("product_scope", []))
                    if norm:
                        global_evidence_pool.add_normalized_record(norm)
            
            # Tüm kaynaklar tarandıktan sonra güvenli bekleme periyodu (Örn: 60 saniye / test döngüsü)
            time.sleep(60)

# Global Scheduler Örneği
global_scheduler = BackgroundScheduler()