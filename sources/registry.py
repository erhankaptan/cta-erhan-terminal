# sources/registry.py
# CTA ERHAN Terminali - Doğrulanmış Kaynak Envanteri ve Registry

SOURCES_REGISTRY = [
    {
        "source_id": "SRC_X_001",
        "source_name": "Macro & Futures Feed X",
        "source_type": "X",
        "organization": "Primary Channel",
        "account": "@MacroTerminal_Example",
        "canonical_url": "https://x.com/MacroTerminal_Example",
        "access_method": "X_API_V2_POLL",
        "product_scope": ["ES", "NQ", "CL", "GC"],
        "topic_scope": ["macro", "futures", "liquidity"],
        "priority": 1,
        "poll_interval_minutes": 60,  # Saatte 1 defa (Rate limit ve ban riskine karşı güvenli periyot)
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    {
        "source_id": "SRC_RSS_001",
        "source_name": "Global Energy & Commodities RSS",
        "source_type": "RSS",
        "organization": "Energy Wire",
        "canonical_url": "https://example.com/energy-feed.rss",
        "access_method": "RSS_FETCH",
        "product_scope": ["CL", "MCL", "NG"],
        "topic_scope": ["energy", "inventory", "supplies"],
        "priority": 2,
        "poll_interval_minutes": 30,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    {
        "source_id": "SRC_INST_001",
        "source_name": "Institutional Research Portal",
        "source_type": "INSTITUTIONAL_WEB",
        "organization": "Global Macro Research",
        "canonical_url": "https://example.com/research/insights",
        "access_method": "HTTP_SCRAPE_TARGET",
        "product_scope": ["ES", "NQ", "RTY", "YM", "6E"],
        "topic_scope": ["central_banks", "rates", "flow"],
        "priority": 1,
        "poll_interval_minutes": 240,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    {
        "source_id": "SRC_PDF_001",
        "source_name": "Commitments of Traders (COT) Proxy Report",
        "source_type": "PDF",
        "organization": "CFTC Official",
        "canonical_url": "https://example.com/reports/cot_proxy.pdf",
        "access_method": "PDF_DOWNLOAD_PARSE",
        "product_scope": ["ES", "NQ", "CL", "GC", "6E"],
        "topic_scope": ["cot", "managed_money", "positions"],
        "priority": 1,
        "poll_interval_minutes": 1440,  # Günlük / Haftalık periyot
        "enabled": True,
        "verification_status": "VERIFIED",
    }
]

def get_sources_by_product(product_code: str):
    """Seçilen ürüne göre ilgili kaynakları filtreler (Fail-Closed uyumlu)."""
    matched = []
    for src in SOURCES_REGISTRY:
        if src["enabled"] and product_code in src["product_scope"]:
            matched.append(src)
    return matched