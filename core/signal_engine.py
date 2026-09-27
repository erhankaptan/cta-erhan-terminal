"""
CTA ERHAN KARAR MOTORU — Signal Engine
=======================================
Faz 2A sinyal uretim motoru.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from core.signals_db import global_signals_db


# ============================================================
# SABITLER (HIPOTEZ — backtest ile kalibre edilecek)
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"

WEIGHTS_DEFAULT = {"COT": 0.50, "Radar": 0.35, "Tickmill": 0.15}
WEIGHTS_COT_FRESH = {"COT": 0.60, "Radar": 0.25, "Tickmill": 0.15}

THRESHOLD_STRONG = 0.60
THRESHOLD_NORMAL = 0.25
CONFIDENCE_MIN = 55.0
CONFIDENCE_STRONG = 75.0

CONFLICT_ABS_THRESHOLD = 0.45
CONFLICT_PENALTY = 0.70
WEAK_CONFLICT_PENALTY = 0.85

COT_FRESH_HOURS = 48
RADAR_TTL_HOURS = 4
TICKMILL_TTL_HOURS = 24
COT_MAX_DAYS = 7

OFFLIST_CONFIDENCE_CAP = 60.0

MAJOR_PRODUCTS = ["ES", "NQ", "CL", "GC", "6E"]


# ============================================================
# YARDIMCI
# ============================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_float(v, default: float = 0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _load_synthesis_snapshot() -> dict:
    f = SNAPSHOTS_DIR / "latest.json"
    if not f.exists():
        return {}
    try:
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}


# ============================================================
# SKOR TOPLAMA
# ============================================================

def get_cot_score(product: str) -> float:
    """COT skoru -1..+1 (LEVERAGED_FUNDS / MANAGED_MONEY net'inden)."""
    try:
        from sources.evidence_pool import global_evidence_pool
        evs = [e for e in global_evidence_pool.get_evidence_for_product(product)
               if e.get("source_type") == "COT"]
        if not evs:
            return 0.0

        # Kategorili kayitlari bul (MERKEZ), en yeni tarihli olani sec
        candidates = []
        for e in evs:
            meta = e.get("metadata") or {}
            if isinstance(meta, dict) and meta.get("categories"):
                candidates.append(e)

        if not candidates:
            return 0.0

        # En yeni published_at'li kaydi sec
        candidates.sort(key=lambda x: x.get("published_at") or "", reverse=True)
        chosen = candidates[0]
        meta = chosen.get("metadata") or {}

        # Fallback zinciri
        primary = meta.get("interpreter", {}).get("primary_category", "LEVERAGED_FUNDS")
        cats = meta.get("categories", {})

        fallback_order = [primary, "MANAGED_MONEY", "LEVERAGED_FUNDS",
                          "SWAP_DEALER", "OTHER_REPORTABLE", "OTHER_REPORTABLES"]

        net = 0.0
        for cat_name in fallback_order:
            cat = cats.get(cat_name, {})
            long_v = _safe_float(cat.get("long"))
            short_v = _safe_float(cat.get("short"))
            candidate_net = long_v - short_v
            if candidate_net != 0:
                net = candidate_net
                break

        # Hala sifirsa, ilk dolu kategoriyi al
        if net == 0.0:
            for cat_name, cat in cats.items():
                long_v = _safe_float(cat.get("long"))
                short_v = _safe_float(cat.get("short"))
                if long_v + short_v > 0:
                    net = long_v - short_v
                    break

        score = max(-1.0, min(1.0, net / 200000.0))
        return score
    except Exception:
        return 0.0


def get_radar_score(product: str) -> float:
    """Radar skoru -0.75..+0.75 (synthesis snapshot'tan)."""
    snap = _load_synthesis_snapshot()
    results = snap.get("results", {})
    r = results.get(product) or results.get(product.upper())
    if not r:
        return 0.0
    score = _safe_float(r.get("score"))
    return max(-0.75, min(0.75, score))


def get_tickmill_score(product: str) -> float:
    """
    Tickmill RSS'ten sentiment skoru (-1..+1).
    data/rss/*.json dosyalarindan okur (GitHub Actions zaten cekiyor).
    """
    import glob
    import json as _json

    # Ürün → keyword eşlemesi
    PRODUCT_KEYWORDS = {
        "ES": ["s&p 500", "s&p500", "sp500", "spx", "e-mini s&p", "s&p"],
        "NQ": ["nasdaq", "ndx", "nas100"],
        "YM": ["dow", "djia", "us30"],
        "RTY": ["russell", "rut"],
        "NK": ["nikkei", "jp225"],
        "ZT": ["2-year", "2y note", "ust 2y"],
        "ZF": ["5-year", "5y note", "ust 5y"],
        "ZN": ["10-year", "10y note", "ust 10y", "us10y", "treasury"],
        "ZB": ["30-year", "30y bond", "ust bond"],
        "UB": ["ultra bond"],
        "ZQ": ["fed funds"],
        "6E": ["eurusd", "eur/usd", "euro", "eur "],
        "6J": ["usdjpy", "jpy", "yen"],
        "6B": ["gbpusd", "sterling", "cable", "gbp"],
        "6A": ["audusd", "aussie", "aud/usd", "aud "],
        "6C": ["usdcad", "loonie", "cad/usd", "cad "],
        "6N": ["nzdusd", "kiwi", "nzd"],
        "6S": ["usdchf", "swissy", "swiss franc", "chf"],
        "DXY": ["dxy", "dollar index", "us dollar"],
        "CL": ["crude", "wti", "oil"],
        "NG": ["natural gas", "natgas", "nat gas", "gas "],
        "HO": ["heating oil", "ulsd"],
        "RB": ["rbob", "gasoline"],
        "BZ": ["brent"],
        "GC": ["gold", "xauusd", "xau"],
        "SI": ["silver", "xagusd", "xag"],
        "HG": ["copper"],
        "PL": ["platinum"],
        "PA": ["palladium"],
        "ZC": ["corn"],
        "ZS": ["soybean"],
        "ZW": ["wheat"],
        "ZM": ["soybean meal"],
        "ZL": ["soybean oil"],
        "KE": ["kansas wheat", "hrw"],
    }

    BULL = ["bullish", "buy", "long", "upside", "rally", "risk on",
            "constructive", "outperform", "overweight", "higher"]
    BEAR = ["bearish", "sell", "short", "downside", "selloff",
            "risk off", "defensive", "underweight", "caution", "lower"]

    try:
        # En son 10 RSS dosyasini oku (en yeni once)
        rss_files = sorted(glob.glob(str(DATA_DIR / "rss" / "*.json")), reverse=True)[:10]
        if not rss_files:
            return 0.0

        product_kw = PRODUCT_KEYWORDS.get(product, [])
        if not product_kw:
            return 0.0

        bc = sc = 0
        for rss_file in rss_files:
            try:
                with open(rss_file, "r", encoding="utf-8") as f:
                    items = _json.load(f)
            except Exception:
                continue

            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue
                if item.get("source") != "Tickmill":
                    continue

                title = (item.get("title_en") or item.get("title_tr") or "").lower()
                content = (item.get("content_en") or item.get("content_tr") or "").lower()
                text = title + " " + content

                if not any(kw in text for kw in product_kw):
                    continue

                bc += sum(text.count(w) for w in BULL)
                sc += sum(text.count(w) for w in BEAR)

        total = bc + sc
        if total == 0:
            return 0.0

        score = (bc - sc) / total
        return max(-1.0, min(1.0, score))
    except Exception:
        return 0.0
        
        # Yön skoru (-1..+1)
        score = (bc - sc) / total
        return max(-1.0, min(1.0, score))
    except Exception as e:
        return 0.0


# ============================================================
# CELISKI
# ============================================================

def detect_conflict(cot_score: float, radar_score: float) -> tuple:
    if (abs(cot_score) > CONFLICT_ABS_THRESHOLD and
        abs(radar_score) > CONFLICT_ABS_THRESHOLD and
        cot_score * radar_score < 0):
        return True, ["COT", "Radar"], CONFLICT_PENALTY
    if cot_score * radar_score < 0:
        return False, ["COT", "Radar"], WEAK_CONFLICT_PENALTY
    return False, [], 1.0


# ============================================================
# SKOR
# ============================================================

def compute_weighted_score(cot_score, radar_score, tickmill_score, cot_age_hours=999):
    if cot_age_hours <= COT_FRESH_HOURS:
        weights = WEIGHTS_COT_FRESH.copy()
    else:
        weights = WEIGHTS_DEFAULT.copy()
    raw = (weights["COT"] * cot_score +
           weights["Radar"] * radar_score +
           weights["Tickmill"] * tickmill_score)
    return raw, weights


def compute_confidence(cot_score, radar_score, tickmill_score, is_conflict,
                       cot_age_hours, radar_age_hours, tickmill_age_hours,
                       non_rep_confirms=False):
    signs = [
        1 if cot_score > 0 else (-1 if cot_score < 0 else 0),
        1 if radar_score > 0 else (-1 if radar_score < 0 else 0),
        1 if tickmill_score > 0 else (-1 if tickmill_score < 0 else 0),
    ]
    nonzero = [s for s in signs if s != 0]
    if nonzero:
        dominant = max(set(nonzero), key=nonzero.count)
        uyum = nonzero.count(dominant) / 3.0
    else:
        uyum = 0.0

    kalite = 0.5
    if abs(cot_score) > 0.5:
        kalite += 0.2
    if abs(radar_score) > 0.4:
        kalite += 0.2
    if non_rep_confirms:
        kalite += 0.1
    kalite = min(1.0, kalite)

    tazelik = 1.0
    if cot_age_hours > COT_FRESH_HOURS:
        tazelik -= 0.2
    if radar_age_hours > RADAR_TTL_HOURS:
        tazelik -= 0.3
    if tickmill_age_hours > TICKMILL_TTL_HOURS:
        tazelik -= 0.2
    tazelik = max(0.0, tazelik)

    celiski = 1.0 if is_conflict else 0.0

    conf = (0.40 * uyum + 0.30 * kalite + 0.20 * tazelik + 0.10 * (1 - celiski)) * 100.0
    return round(conf, 1)


def classify_signal(score: float, confidence: float) -> str:
    if confidence < CONFIDENCE_MIN:
        return "BEKLE"
    if score >= THRESHOLD_STRONG and confidence >= CONFIDENCE_STRONG:
        return "GÜÇLÜ AL"
    if score >= THRESHOLD_NORMAL:
        return "AL"
    if score <= -THRESHOLD_STRONG and confidence >= CONFIDENCE_STRONG:
        return "GÜÇLÜ SAT"
    if score <= -THRESHOLD_NORMAL:
        return "SAT"
    return "BEKLE"


def classify_signal_type(weights: dict) -> tuple:
    cot_w = weights.get("COT", 0)
    radar_w = weights.get("Radar", 0)
    if cot_w > 0.40 and radar_w <= 0.30:
        return "cot_based", "cot", "until_new_cot"
    if radar_w > 0.30 and cot_w <= 0.45:
        return "radar_based", "radar", "4h"
    return "mixed", "cot", "mixed"


# ============================================================
# ANA FONKSIYON
# ============================================================

def calculate_signal(product, *, is_offlist=False, price_at_signal=None,
                     atr_at_signal=None, cot_age_hours=0.0, radar_age_hours=0.0,
                     tickmill_age_hours=0.0, non_rep_confirms=False):
    product = product.upper().strip()

    cot_score = get_cot_score(product)
    radar_score = get_radar_score(product)
    tickmill_score = get_tickmill_score(product)

    is_conflict, conflict_sources, penalty = detect_conflict(cot_score, radar_score)

    raw_score, weights = compute_weighted_score(cot_score, radar_score, tickmill_score, cot_age_hours)

    if is_conflict:
        raw_score = 0.0
    final_score = raw_score

    confidence = compute_confidence(cot_score, radar_score, tickmill_score,
                                    is_conflict, cot_age_hours, radar_age_hours,
                                    tickmill_age_hours, non_rep_confirms)
    confidence = confidence * penalty

    if is_offlist:
        confidence = min(confidence, OFFLIST_CONFIDENCE_CAP)
    confidence = round(confidence, 1)

    signal = classify_signal(final_score, confidence)
    signal_type, primary_source, validity_reason = classify_signal_type(weights)

    now = datetime.now(timezone.utc)
    if signal_type == "cot_based":
        expires = now + timedelta(days=COT_MAX_DAYS)
    elif signal_type == "radar_based":
        expires = now + timedelta(hours=RADAR_TTL_HOURS)
    else:
        expires = min(now + timedelta(hours=RADAR_TTL_HOURS),
                      now + timedelta(days=COT_MAX_DAYS))

    return {
        "product": product,
        "signal": signal,
        "raw_score": round(raw_score, 4),
        "final_score": round(final_score, 4),
        "confidence": confidence,
        "cot_score": round(cot_score, 4),
        "radar_score": round(radar_score, 4),
        "tickmill_score": round(tickmill_score, 4),
        "weights_used": weights,
        "is_conflict": is_conflict,
        "conflict_sources": conflict_sources,
        "signal_type": signal_type,
        "primary_source": primary_source,
        "validity_reason": validity_reason,
        "price_at_signal": price_at_signal,
        "atr_at_signal": atr_at_signal,
        "created_at": now.isoformat(),
        "expires_at": expires.isoformat(),
        "independent_evidence_count": 3 - (1 if is_conflict else 0),
        "source_ages": {"COT": cot_age_hours, "Radar": radar_age_hours, "Tickmill": tickmill_age_hours},
    }


def calculate_and_log(product: str, **kwargs) -> Dict[str, Any]:
    sig = calculate_signal(product, **kwargs)
    sig["signal_id"] = global_signals_db.log_signal(sig)
    return sig


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Signal Engine Test")
    print("=" * 60)
    for product in MAJOR_PRODUCTS:
        sig = calculate_signal(product)
        print(f"\n[{product}] {sig['signal']} | Guven %{sig['confidence']}")
        print(f"  Skor: {sig['final_score']:+.4f}")
        print(f"  COT: {sig['cot_score']:+.3f} | Radar: {sig['radar_score']:+.3f} | Tickmill: {sig['tickmill_score']:+.3f}")
        print(f"  Tip: {sig['signal_type']} | Validity: {sig['validity_reason']}")
        print(f"  Celiski: {sig['is_conflict']} {sig['conflict_sources']}")
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)