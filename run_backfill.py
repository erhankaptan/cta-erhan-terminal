from sources.merkez_cot_loader import load_merkez_snapshot
from core.signal_engine import get_cot_extremity_info, _get_cot_data

added = load_merkez_snapshot()
print(f"[BACKFILL] Yeni eklenen evidence satiri: {added}")
print("-" * 40)

for u in ["ES", "NQ", "GC", "6E", "CL"]:
    data = _get_cot_data(u)
    ext = get_cot_extremity_info(u)
    print(f"{u}: skor={data['score']:+.4f} | ekstremite={ext}")
