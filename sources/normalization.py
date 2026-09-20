# sources/normalization.py
# CTA ERHAN Terminali - Normalizasyon Katmanı (Canonical Record)

from datetime import datetime

def normalize_raw_record(raw_record: dict, product_scope: list):
    """
    Ham veriyi (RAW) ortak formata (Canonical Record) dönüştürür.
    Ham veri asla değiştirilmez; normalize katman bunun üzerine kurulur.
    """
    # Fail-Closed: Eğer ham veri çekilemediyse veya hata aldıysa normalizasyon boş döner
    if raw_record.get("status") != "SUCCESS":
        return None

    canonical_record = {
        "record_id": f"REC_{raw_record['source_id']}_{int(datetime.utcnow().timestamp())}",
        "source_id": raw_record["source_id"],
        "source_type": raw_record["source_type"],
        "publisher": raw_record.get("canonical_url", "Unknown"),
        "author": raw_record.get("author", "Unknown"),
        "published_at": raw_record.get("ingested_at"),
        "ingested_at": datetime.utcnow().isoformat(),
        "title": f"Data feed from {raw_record['source_id']}",
        "content": raw_record.get("raw_content", ""),
        "canonical_url": raw_record["canonical_url"],
        "product_scope": product_scope,
        "topic_scope": ["general", "market_feed"],
        "raw_reference": raw_record
    }
    
    return canonical_record