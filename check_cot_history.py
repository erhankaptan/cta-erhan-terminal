from sources.evidence_pool import global_evidence_pool as pool

urunler = ["ES", "NQ", "GC", "6E", "CL"]
for u in urunler:
    evs = [e for e in pool.get_evidence_for_product(u) if e.get("source_type") == "COT"]
    dates = sorted(set(e.get("published_at", "") for e in evs))
    print(f"{u}: {len(dates)} farkli rapor tarihi -> {dates}")
