import json
data = json.load(open("/mnt/cta_terminal/cme_cot_raw_export.json", encoding="utf-8"))
es = data["symbols"]["ES"]
obs = es["weekly_observations"][0]
print("as_of:", obs.get("as_of_date"))
cats = obs.get("categories", {})
tl = ts = 0
for k, v in cats.items():
    l = v.get("long", 0) or 0
    s = v.get("short", 0) or 0
    print(f"{k:25s} long={l:>12,} short={s:>12,} net={v.get('net')}")
    tl += l
    ts += s
print("TOPLAM LONG:", tl)
print("TOPLAM SHORT:", ts)
print("FARK:", tl - ts)
