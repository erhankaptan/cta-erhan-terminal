# sources/freshness.py
# CTA ERHAN Terminali - Freshness ve Kaynak Sağlık Kontrolü

from datetime import datetime, timedelta

def check_source_freshness(source_registry_item: dict, last_success_timestamp: str):
    """
    Kaynak tipine ve son başarılı çekim zamanına göre tazelik (freshness) durumunu belirler.
    Fail-Closed ilkesine göre eski veri yeni gibi sunulmaz.
    """
    if not last_success_timestamp:
        return "UNAVAILABLE", "Never successfully fetched"

    try:
        last_time = datetime.fromisoformat(last_success_timestamp)
        now = datetime.utcnow()
        age_delta = now - last_time
        
        source_type = source_registry_item.get("source_type")
        poll_interval = source_registry_item.get("poll_interval_minutes", 60)
        
        # Kaynak tipine göre esneme payı (tazelik limiti)
        # X ve RSS dakikalık/saatlik, PDF günlük/haftalık beklenir.
        max_allowed_age_minutes = poll_interval * 2  
        
        age_minutes = age_delta.total_seconds() / 60.0

        if age_minutes <= max_allowed_age_minutes:
            return "HEALTHY", f"Fresh (Age: {int(age_minutes)} mins)"
        elif age_minutes <= (max_allowed_age_minutes * 3):
            return "STALE", f"Stale data (Age: {int(age_minutes)} mins)"
        else:
            return "FAILED", f"Outdated / Expired (Age: {int(age_minutes)} mins)"
            
    except Exception as e:
        return "UNAVAILABLE", f"Freshness check error: {str(e)}"