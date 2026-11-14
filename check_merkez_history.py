import json

with open("/mnt/cta_terminal/cme_cot_raw_export.json", "r", encoding="utf-8") as f:
    export = json.load(f)

symbols = export.get("symbols", {})
for code in ["ES", "NQ", "GC", "6E", "CL"]:
    entry = symbols.get(code, {})
    obs = entry.get("weekly_observations", [])
    dates = [o.get("as_of_date") for o in obs]
    print(f"{code}: {len(obs)} gozlem -> {dates}")
