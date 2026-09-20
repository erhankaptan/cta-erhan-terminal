import time
import os
import json
import threading
from datetime import datetime, timedelta
from core.logger import SystemLogger

class CatchUpScheduler:
    def __init__(self, integration_engine, interval_hours=1, state_file="last_run.json"):
        self.engine = integration_engine
        self.interval_hours = interval_hours
        self.state_file = state_file
        self.logger = SystemLogger()
        self._stop_event = threading.Event()

    def get_last_run_time(self) -> datetime:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data["last_run"])
            except Exception:
                pass
        return datetime.now() - timedelta(hours=24)

    def save_last_run_time(self, run_time: datetime):
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump({"last_run": run_time.isoformat()}, f)
        except Exception as e:
            self.logger.error(f"Zamanlayıcı durumu kaydedilemedi: {e}")

    def catch_up_and_run(self, target_url: str):
        self.logger.info("Zamanlayıcı başlatıldı: Geriye dönük telafi (Catch-up) kontrolü yapılıyor...")
        last_run = self.get_last_run_time()
        now = datetime.now()

        next_due = last_run + timedelta(hours=self.interval_hours)
        missed_cycles = 0

        while next_due <= now:
            missed_cycles += 1
            self.logger.info(f"Kaçırılan periyot telafi ediliyor -> Hedef Zaman: {next_due.strftime('%Y-%m-%d %H:%M')}")
            
            result = self.engine.ingest_and_process_url(target_url)
            self.logger.info(f"Telafi Ingestion Sonucu: {result['status']}")
            
            next_due += timedelta(hours=self.interval_hours)

        if missed_cycles > 0:
            self.logger.info(f"Toplam {missed_cycles} adet kaçırılan periyot başarıyla telafi edildi!")
        else:
            self.logger.info("Kaçırılan periyot yok, sistem güncel.")

        self.save_last_run_time(now)

    def start_background_loop(self, target_url: str):
        """Terminal açıkken arka planda periyodik olarak çalışmaya devam eden döngü"""
        def background_worker():
            while not self._stop_event.is_set():
                # Belirlenen aralıkta bir uyu (Test için saniyeye çevrilebilir, normalde interval_hours * 3600)
                # Şimdilik örnek olarak 1 saatlik (3600 sn) bekleme koyuyoruz
                time.sleep(self.interval_hours * 3600)
                if self._stop_event.is_set():
                    break
                self.logger.info("Arka plan periyodik veri çekme tetiklendi...")
                res = self.engine.ingest_and_process_url(target_url)
                self.save_last_run_time(datetime.now())
                self.logger.info(f"Periyodik Ingestion Sonucu: {res['status']}")

        t = threading.Thread(target=background_worker, daemon=True)
        t.start()
        self.logger.info("Arka plan periyodik görev yöneticisi aktif.")

    def stop(self):
        self._stop_event.set()