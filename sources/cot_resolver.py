# sources/cot_resolver.py
"""
COT kategorisi + net pozisyon cozumleme -- hem anlik skor
(core/signal_engine.py) hem de tarihsel ekstremite hesaplamasi
(sources/cot_extremity.py) AYNI kategori secim mantigini kullansin diye
TEK bir yerde toplandi (eskiden bu mantik sadece core/signal_engine.py
icine gomuluydu, baska hicbir yerden erisilemezdi -- iki ayri yerde
kopyalanirsa zamanla birbirinden sapma riski olurdu).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

FALLBACK_ORDER = [
    "LEVERAGED_FUNDS", "MANAGED_MONEY", "SWAP_DEALER",
    "OTHER_REPORTABLE", "OTHER_REPORTABLES",
]


def _safe_float(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def resolve_category_net(
    categories: Dict[str, Any], primary: Optional[str] = None,
) -> Tuple[Optional[str], float]:
    """Verilen kategoriler icinde (once `primary`, sonra FALLBACK_ORDER
    sirasiyla) ilk SIFIR-OLMAYAN net'i veren kategoriyi doner. Hepsi
    sifirsa, long+short toplami pozitif olan ilk kategoriyi alir (tamamen
    bos/veri yoksa (None, 0.0) doner)."""
    order = ([primary] if primary else []) + FALLBACK_ORDER
    for cat_name in order:
        cat = categories.get(cat_name, {})
        long_v = _safe_float(cat.get("long"))
        short_v = _safe_float(cat.get("short"))
        net = long_v - short_v
        if net != 0:
            return cat_name, net

    for cat_name, cat in categories.items():
        long_v = _safe_float(cat.get("long"))
        short_v = _safe_float(cat.get("short"))
        if long_v + short_v > 0:
            return cat_name, long_v - short_v

    return None, 0.0


def get_cot_evidence_rows(product: str) -> List[Dict[str, Any]]:
    """Urunun TUM COT evidence kayitlarini (her biri bir haftalik CFTC
    raporu) rapor tarihine gore ESKIDEN-YENIYE sirali dondurur.

    Her satir: {report_date, category, net, open_interest}.

    GUVENLIK: evidence_pool/metadata eksik/bozuksa o satir sessizce
    atlanir, exception firlatilmaz (cagiran taraf -- ekstremite
    hesaplamasi -- "yetersiz veri" olarak dogru yorumlar)."""
    from sources.evidence_pool import global_evidence_pool

    evs = [
        e for e in global_evidence_pool.get_evidence_for_product(product)
        if e.get("source_type") == "COT"
    ]
    rows: List[Dict[str, Any]] = []
    for e in evs:
        meta = e.get("metadata") or {}
        if not isinstance(meta, dict):
            continue
        categories = meta.get("categories")
        if not isinstance(categories, dict) or not categories:
            continue

        interp = meta.get("interpreter") or {}
        primary = interp.get("primary_category") if isinstance(interp, dict) else None
        cat_name, net = resolve_category_net(categories, primary)
        if cat_name is None:
            continue

        report_date = meta.get("report_date") or e.get("published_at") or ""
        if not report_date:
            continue
        oi_raw = meta.get("open_interest")
        oi = _safe_float(oi_raw) if oi_raw not in (None, "") else None

        rows.append({
            "report_date": report_date,
            "category": cat_name,
            "net": net,
            "open_interest": oi,
        })

    rows.sort(key=lambda r: r["report_date"])
    return rows
