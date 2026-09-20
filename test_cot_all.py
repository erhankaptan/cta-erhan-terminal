from sources.adapters.cftc_cot import fetch_cftc_cot, normalize_cot

products = [
    "ES", "MES", "NQ", "MNQ", "RTY", "YM",
    "CL", "MCL", "NG",
    "GC", "MGC", "SI", "HG", "PL",
    "6E", "6J", "6B", "6A", "6C", "6S",
    "ZC", "ZS", "ZW", "ZL", "ZM",
]

print(f"{'URUN':6s} | {'MARKET':55s} | {'CTA NET':>12s} | {'CHANGE':>10s} | YON")
print("-" * 120)

for p in products:
    try:
        raw = fetch_cftc_cot(p)
        if not raw:
            print(f"{p:6s} | {'VERI YOK':55s} | {'-':>12s} | {'-':>10s} | -")
            continue
        norm = normalize_cot(raw[0], p)
        meta = norm["metadata"]
        market = meta["market"][:55]
        cta_net = meta["cta_proxy"]["net"]
        cta_change = meta["cta_proxy"]["change_net"]
        yon = meta["cot_yon"]
        print(f"{p:6s} | {market:55s} | {cta_net:>12,d} | {cta_change:>+10,d} | {yon}")
    except Exception as e:
        print(f"{p:6s} | HATA: {type(e).__name__}: {e}")