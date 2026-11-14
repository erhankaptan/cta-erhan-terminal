from core.signal_engine import get_cot_extremity_info, _get_cot_data

for u in ["ES", "NQ", "GC", "6E", "CL"]:
    data = _get_cot_data(u)
    ext = get_cot_extremity_info(u)
    print(f"{u}: skor={data['score']:+.4f} | ekstremite={ext}")
