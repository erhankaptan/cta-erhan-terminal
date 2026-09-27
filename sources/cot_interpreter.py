# sources/cot_interpreter.py
"""COT yorumlama motoru (5 kategori -> yon, momentum, konsensus, non-reportable)."""
from __future__ import annotations
from typing import Any, Dict, Optional

PRIMARY_BY_TYPE = {
    "TFF": "LEVERAGED_FUNDS",
    "DIS": "MANAGED_MONEY",
}

TFF_CATEGORIES = [
    "DEALER_INTERMEDIARY",
    "ASSET_MANAGER",
    "LEVERAGED_FUNDS",
    "OTHER_REPORTABLES",
    "NON_REPORTABLE",
]
DIS_CATEGORIES = [
    "PRODUCER_MERCHANT",
    "SWAP_DEALER",
    "MANAGED_MONEY",
    "OTHER_REPORTABLE",
    "NON_REPORTABLE",
]


def _net(cat: Optional[Dict[str, Any]]) -> int:
    if not cat:
        return 0
    net = cat.get("net")
    if net is not None:
        try:
            return int(net)
        except (TypeError, ValueError):
            pass
    long_v = cat.get("long") or 0
    short_v = cat.get("short") or 0
    try:
        return int(long_v) - int(short_v)
    except (TypeError, ValueError):
        return 0


def interpret(
    categories: Dict[str, Dict[str, Any]],
    *,
    report_type: str = "TFF",
    prev_categories: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    primary_cat = PRIMARY_BY_TYPE.get(report_type.upper(), "LEVERAGED_FUNDS")
    primary_net = _net(categories.get(primary_cat))

    if primary_net > 0:
        cot_yon = "YUKSELIS"
    elif primary_net < 0:
        cot_yon = "DUSUS"
    else:
        cot_yon = "NOTR"

    change_by_category: Dict[str, int] = {}
    if prev_categories:
        for cat_name in categories.keys():
            new_net = _net(categories.get(cat_name))
            old_net = _net(prev_categories.get(cat_name))
            change_by_category[cat_name] = new_net - old_net

    primary_change = change_by_category.get(primary_cat, 0)

    if primary_net > 0 and primary_change > 0:
        momentum = "GUCLENIYOR"
    elif primary_net < 0 and primary_change < 0:
        momentum = "GUCLENIYOR"
    elif primary_change != 0:
        momentum = "ZAYIFLIYOR"
    else:
        momentum = "SABIT"

    if report_type.upper() == "TFF":
        trio = ["DEALER_INTERMEDIARY", "ASSET_MANAGER", "LEVERAGED_FUNDS"]
    else:
        trio = ["PRODUCER_MERCHANT", "SWAP_DEALER", "MANAGED_MONEY"]

    directions = []
    for c in trio:
        n = _net(categories.get(c))
        if n > 0:
            directions.append("L")
        elif n < 0:
            directions.append("S")
        else:
            directions.append("F")

    if len(set(directions)) == 1:
        consensus = "UYUMLU"
    elif len(set(directions)) == 2:
        consensus = "KARISIK"
    else:
        consensus = "CELISKILI"

    nr_net = _net(categories.get("NON_REPORTABLE"))
    nr_change = change_by_category.get("NON_REPORTABLE", 0)

    if abs(nr_net) < 1000 and nr_change == 0:
        non_reportable = "YOK"
    elif nr_net > 0 and nr_change > 0:
        non_reportable = "TERS_INDIKATOR_UYARI_ASIRI_IYIMSER"
    elif nr_net < 0 and nr_change < 0:
        non_reportable = "TERS_INDIKATOR_UYARI_ASIRI_KOTUMSER"
    elif nr_net > 0:
        non_reportable = "TERS_INDIKATOR_UYARI_POZITIF"
    elif nr_net < 0:
        non_reportable = "TERS_INDIKATOR_UYARI_NEGATIF"
    else:
        non_reportable = "NOTR"

    if primary_net > 0 and momentum == "GUCLENIYOR":
        primary_signal = "BULLISH"
    elif primary_net < 0 and momentum == "GUCLENIYOR":
        primary_signal = "BEARISH"
    elif primary_net > 0:
        primary_signal = "WEAK_BULLISH"
    elif primary_net < 0:
        primary_signal = "WEAK_BEARISH"
    else:
        primary_signal = "NEUTRAL"

    net_by_category = {c: _net(categories.get(c)) for c in categories.keys()}

    return {
        "cot_yon": cot_yon,
        "momentum": momentum,
        "consensus": consensus,
        "non_reportable": non_reportable,
        "primary_signal": primary_signal,
        "primary_category": primary_cat,
        "net_by_category": net_by_category,
        "change_by_category": change_by_category,
    }


def all_category_names(report_type: str) -> list:
    if report_type.upper() == "TFF":
        return list(TFF_CATEGORIES)
    return list(DIS_CATEGORIES)