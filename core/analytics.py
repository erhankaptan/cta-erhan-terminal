from typing import List, Dict, Any
from collections import Counter
from datetime import datetime

class AnalyticsEngine:
    def __init__(self, pool: List[Any], findings: List[Dict[str, Any]]):
        self.pool = pool
        self.findings = findings

    def generate_summary_report(self) -> Dict[str, Any]:
        total_records = len(pool_len := self.pool)
        
        # Kaynak dağılımı analizi
        sources = [r.provenance for r in self.pool]
        source_counts = dict(Counter(sources))

        # Zaman aralığı analizi
        timestamps = [r.timestamp for r in self.pool if r.timestamp]
        oldest = min(timestamps) if timestamps else "Veri Yok"
        newest = max(timestamps) if timestamps else "Veri Yok"

        # Basit içerik / kelime frekans eğilimi
        all_text = ""
        for r in self.pool:
            all_text += str(r.data_payload) + " "
        
        words = [w.lower().strip(".,!?\"'()[]{}") for w in all_text.split() if len(w) > 3]
        top_words = Counter(words).most_common(5)

        report = {
            "Toplam Kayit Sayisi": total_records,
            "Kaynak Dagilimi": source_counts,
            "En Eski Kayit": oldest,
            "En Yeni Kayit": newest,
            "En Sik Gecen Kelimeler": top_words,
            "Bulgu Sayisi": len(self.findings)
        }
        return report

    def export_report_to_desktop(self, report: Dict[str, Any]) -> str:
        import os
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "cta_analytics_report.json")
        
        try:
            import json
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=4)
            return f"Rapor başarıyla masaüstüne kaydedildi: {file_path}"
        except Exception as e:
            return f"Rapor kaydedilirken hata oluştu: {str(e)}"