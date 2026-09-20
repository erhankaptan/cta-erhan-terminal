# sources/adapters/cftc_cot.py
from __future__ import annotations

import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import requests


CFTC_TFF_ENDPOINT = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
CFTC_DISAGG_ENDPOINT = "https://publicreporting.cftc.gov/resource/72hh-3qpy.json"


PRODUCT_TO_CFTC_MARKET: Dict[str, Dict[str, str]] = {
    "ES":  {"report": "TFF", "market": "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE"},
    "MES": {"report": "TFF", "market": "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE"},
    "NQ":  {"report": "TFF", "market": "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE"},
    "MNQ": {"report": "TFF", "market": "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE"},
    "RTY": {"report": "TFF", "market": "RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE"},
    "YM":  {"report": "TFF", "market": "DJIA x $5 - CHICAGO BOARD OF TRADE"},
    "6E":  {"report": "TFF", "market": "EURO FX - CHICAGO MERCANTILE EXCHANGE"},
    "6J":  {"report": "TFF", "market": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE"},
    "6B":  {"report": "TFF", "market": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"},
    "6A":  {"report": "TFF", "market": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "6C":  {"report": "TFF", "market": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "6S":  {"report": "TFF", "market": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE"},
    "GC":  {"report": "DISAGG", "market": "GOLD - COMMODITY EXCHANGE INC."},
    "MGC": {"report": "DISAGG", "market": "GOLD - COMMODITY EXCHANGE INC."},
    "SI":  {"report": "DISAGG", "market": "SILVER - COMMODITY EXCHANGE INC."},
    "PL":  {"report": "DISAGG", "market": "PLATINUM - NEW YORK MERCANTILE EXCHANGE"},
    "HG":  {"report": "DISAGG", "market": "COPPER- #1 - COMMODITY EXCHANGE INC."},
    "CL":  {"report": "DISAGG", "market": "WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE"},
    "MCL": {"report": "DISAGG", "market": "WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE"},
    "NG":  {"report": "DISAGG", "market": "HENRY HUB LAST DAY FIN - NEW YORK MERCANTILE EXCHANGE"},
    "ZC":  {"report": "DISAGG", "market": "CORN - CHICAGO BOARD OF TRADE"},
    "ZW":  {"report": "DISAGG", "market": "WHEAT-SRW - CHICAGO BOARD OF TRADE"},
    "ZS":  {"report": "DISAGG", "market": "SOYBEANS - CHICAGO BOARD OF TRADE"},
    "ZM":  {"report": "DISAGG", "market": "SOYBEAN MEAL - CHICAGO BOARD OF TRADE"},
    "ZL":  {"report": "DISAGG", "market": "SOYBEAN OIL - CHICAGO BOARD OF TRADE"},
}


COT_COOLDOWN_DAYS = 6


def make_cot_evidence_id(report_date: str, market: str, category: str = "LEV_MONEY") -> str:
    base = f"cftc_cot|{report_date}|{market}|{category}"
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:24]
    return f"EV_COT_{digest}"


def should_fetch_cot(product_code: str, pool) -> bool:
    try:
        evidences = pool.get_evidence_for_product(product_code)
    except Exception:
        return True

    cot_records = [
        e for e in evidences
        if isinstance(e, dict) and e.get("source_type") == "COT"
    ]
    if not cot_records:
        return True

    latest = max(
        (e.get("ingested_at") or "" for e in cot_records),
        default="",
    )
    if not latest:
        return True

    try:
        last_dt = datetime.fromisoformat(latest.replace("Z", "+00:00"))
        if last_dt.tzinfo is None:
            last_dt = last_dt.replace(tzinfo=timezone.utc)
    except Exception:
        return True

    age = datetime.now(timezone.utc) - last_dt
    return age >= timedelta(days=COT_COOLDOWN_DAYS)


def fetch_cftc_cot(product_code: str) -> Optional[List[Dict[str, Any]]]:
    product_code = product_code.upper().strip()
    mapping = PRODUCT_TO_CFTC_MARKET.get(product_code)

    if not mapping:
        return None

    report_type = mapping["report"]
    market_filter = mapping["market"]

    if report_type == "TFF":
        endpoint = CFTC_TFF_ENDPOINT
    elif report_type == "DISAGG":
        endpoint = CFTC_DISAGG_ENDPOINT
    else:
        return None

    params = {
        "$where": f"upper(market_and_exchange_names) = '{market_filter.upper()}'",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": 1,
    }

    try:
        resp = requests.get(endpoint, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[COT] Fetch failed for {product_code} ({report_type}): {type(e).__name__}: {e}")
        return None

    if not isinstance(data, list) or not data:
        print(f"[COT] Empty result for {product_code} (filter: {market_filter})")
        return None

    return data



def normalize_cot(raw: Dict[str, Any], product_code: str) -> Dict[str, Any]:
    report_date = str(raw.get("report_date_as_yyyy_mm_dd", ""))[:10]
    market_name = str(raw.get("market_and_exchange_names", ""))
    report_week = str(raw.get("yyyy_report_week_ww", ""))

    def _num_multi(*keys: str) -> int:
        for k in keys:
            v = raw.get(k)
            if v is None:
                continue
            try:
                return int(float(v))
            except Exception:
                continue
        return 0

    cta_long = _num_multi(
        "lev_money_positions_long_all", "lev_money_positions_long",
        "m_money_positions_long_all", "m_money_positions_long",
    )
    cta_short = _num_multi(
        "lev_money_positions_short_all", "lev_money_positions_short",
        "m_money_positions_short_all", "m_money_positions_short",
    )
    cta_net = cta_long - cta_short

    cta_change_long = _num_multi(
        "change_in_lev_money_long_all", "change_in_lev_money_long",
        "change_in_m_money_long_all", "change_in_m_money_long",
    )
    cta_change_short = _num_multi(
        "change_in_lev_money_short_all", "change_in_lev_money_short",
        "change_in_m_money_short_all", "change_in_m_money_short",
    )
    cta_change_net = cta_change_long - cta_change_short

    dealer_long = _num_multi(
        "dealer_positions_long_all", "dealer_positions_long",
        "swap__positions_long_all", "swap_positions_long_all",
    )
    dealer_short = _num_multi(
        "dealer_positions_short_all", "dealer_positions_short",
        "swap__positions_short_all", "swap_positions_short_all",
    )
    dealer_net = dealer_long - dealer_short

    inst_long = _num_multi(
        "asset_mgr_positions_long_all", "asset_mgr_positions_long",
        "prod_merc_positions_long", "producer_positions_long",
    )
    inst_short = _num_multi(
        "asset_mgr_positions_short_all", "asset_mgr_positions_short",
        "prod_merc_positions_short", "producer_positions_short",
    )
    inst_net = inst_long - inst_short

    oi = _num_multi("open_interest_all", "open_interest")

    if cta_net > 0:
        cot_yon = "YUKSELIS"
    elif cta_net < 0:
        cot_yon = "DUSUS"
    else:
        cot_yon = "NOTR"

    if cta_change_net > 0 and cta_net > 0:
        momentum = "GUCLENIYOR"
    elif cta_change_net < 0 and cta_net < 0:
        momentum = "GUCLENIYOR"
    elif cta_change_net != 0:
        momentum = "ZAYIFLIYOR"
    else:
        momentum = "SABIT"

    directions = []
    for net_val in (cta_net, dealer_net, inst_net):
        if net_val > 0:
            directions.append("LONG")
        elif net_val < 0:
            directions.append("SHORT")
        else:
            directions.append("FLAT")

    if len(set(directions)) == 1:
        consensus = "UYUMLU"
    elif len(set(directions)) == 2:
        consensus = "KARISIK"
    else:
        consensus = "CELISKILI"

    title = f"CFTC COT | {market_name} | {report_date}"

    content_lines = [
        f"Report Date: {report_date}",
        f"Report Week: {report_week}",
        f"Market: {market_name}",
        f"Open Interest: {oi}",
        f"CTA Proxy: long={cta_long} short={cta_short} net={cta_net} change={cta_change_net}",
        f"Dealer: long={dealer_long} short={dealer_short} net={dealer_net}",
        f"Institutional: long={inst_long} short={inst_short} net={inst_net}",
    ]
    content = "\n".join(content_lines)

    evidence_id = make_cot_evidence_id(
        report_date=report_date,
        market=market_name,
        category="CTA_PROXY",
    )

    return {
        "evidence_id": evidence_id,
        "product": product_code,
        "source_id": "SRC_COT_CFTC",
        "source_type": "COT",
        "publisher": "CFTC",
        "author": "",
        "published_at": report_date,
        "title": title,
        "content": content,
        "canonical_url": CFTC_TFF_ENDPOINT,
        "metadata": {
            "report_date": report_date,
            "report_week": report_week,
            "market": market_name,
            "open_interest": oi,
            "cta_proxy": {
                "long": cta_long,
                "short": cta_short,
                "net": cta_net,
                "change_long": cta_change_long,
                "change_short": cta_change_short,
                "change_net": cta_change_net,
            },
            "dealer": {
                "long": dealer_long,
                "short": dealer_short,
                "net": dealer_net,
            },
            "institutional": {
                "long": inst_long,
                "short": inst_short,
                "net": inst_net,
            },
            "cot_yon": cot_yon,
            "momentum": momentum,
            "consensus": consensus,
            "provenance": {
                "publisher": "CFTC",
                "report_type": "TFF" if "asset_mgr" in str(raw).lower() else "DISAGG",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        },
    }