# sources/terminal_bridge.py
# CTA ERHAN Terminali - UI ve Arka Plan Motoru Köprüsü

from sources.registry import SOURCES_REGISTRY, get_sources_by_product
from sources.ingestion import run_ingestion_pipelineForProduct
from sources.normalization import normalize_raw_record
from sources.evidence_pool import global_evidence_pool
from sources.freshness import check_source_freshness
from sources.analysis_engine import run_analysis_for_product

def execute_terminal_sync(product_code: str):
    """
    Kullanıcı ürün seçtiğinde tetiklenen ana köprü fonksiyonu.
    Veri çeker, normalleştirir, havuza atar, tazeliği denetler ve sentezi üretir.
    """
    # 1. Ham veri çek
    raw_results = run_ingestion_pipelineForProduct(product_code)
    
    # 2. Normalizasyon ve Kanıt Havuzuna Aktarım
    for raw in raw_results:
        if raw.get("status") == "SUCCESS":
            sources_match = [s for s in SOURCES_REGISTRY if s["source_id"] == raw["source_id"]]
            p_scope = sources_match[0]["product_scope"] if sources_match else [product_code]
            
            norm = normalize_raw_record(raw, p_scope)
            if norm:
                global_evidence_pool.add_normalized_record(norm)

    # 3. Analiz ve Sentez Üretimi
    synthesis_result = run_analysis_for_product(product_code)
    
    # 4. Kaynak Sağlık/Tazelik Raporu
    health_report = []
    for src in get_sources_by_product(product_code):
        # Örnek simüle edilmiş son başarılı çekim zamanı
        status, msg = check_source_freshness(src, src.get("last_success", "2026-09-14T20:00:00"))
        health_report.append({
            "source_id": src["source_id"],
            "source_name": src["source_name"],
            "status": status,
            "message": msg
        })

    return {
        "product": product_code,
        "synthesis": synthesis_result,
        "health": health_report,
        "evidence_pool_size": len(global_evidence_pool.get_evidence_for_product(product_code))
    }