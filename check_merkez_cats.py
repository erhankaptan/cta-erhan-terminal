import json

with open("/mnt/cta_terminal/cme_cot_raw_export.json", "r", encoding="utf-8") as f:
    export = json.load(f)

entry = export.get("symbols", {}).get("ES", {})
obs = entry.get("weekly_observations", [])
for o in obs:
    cats = o.get("categories", {})
    oi = o.get("open_interest", entry.get("open_interest"))
    lf = cats.get("LEVERAGED_FUNDS", {})
    print(o.get("as_of_date"), "| kategori_sayisi=", len(cats), "| OI=", oi, "| LEVERAGED_FUNDS=", lf)
