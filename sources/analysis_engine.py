# sources/analysis_engine.py
from __future__ import annotations

from typing import Any, Dict, List

from sources.evidence_pool import global_evidence_pool

try:
    from sources.cot_interpreter import interpret_cot
    COT_INTERPRETER_AVAILABLE = True
except ImportError:
    COT_INTERPRETER_AVAILABLE = False


# ============================================================
# Micro ürün → Ana ürün eşleştirmesi
# CFTC micro kontratları ayrı raporlamaz; ana ürünün COT'unu kullanırız.
# ============================================================
MICRO_TO_MAIN = {
    "MES": "ES",    # Micro S&P 500 → S&P 500 E-mini
    "MNQ": "NQ",    # Micro Nasdaq 100 → Nasdaq 100 E-mini
    "MCL": "CL",    # Micro Ham Petrol → Ham Petrol
    "MGC": "GC",    # Micro Altın → Altın
}


def _hesapla_guc(kanit_sayisi: int) -> str:
    if kanit_sayisi >= 20:
        return "GÜÇLÜ"
    if kanit_sayisi >= 10:
        return "ORTA"
    if kanit_sayisi >= 5:
        return "ZAYIF"
    return "YETERSİZ"


def _hesapla_belirsizlik(kaynak_sayisi: int) -> str:
    if kaynak_sayisi >= 4:
        return "DÜŞÜK"
    if kaynak_sayisi >= 2:
        return "ORTA"
    return "YÜKSEK"


def _hesapla_catisma(kanitlar: List[Dict[str, Any]]) -> str:
    return "YOK"


def _hesapla_rejim(kanit_sayisi: int, cot_mevcut: bool) -> str:
    if not cot_mevcut:
        return "BİLİNMİYOR"
    if kanit_sayisi >= 20:
        return "TRENDING"
    return "BİLİNMİYOR"


def run_analysis_for_product(product_code: str) -> Dict[str, Any]:
    product_code = product_code.upper().strip()

    # --- Micro ürün → Ana ürün mapping ---
    lookup_code = MICRO_TO_MAIN.get(product_code, product_code)

    # --- Havuzdan oku ---
    try:
        evidences = global_evidence_pool.get_evidence_for_product(lookup_code)
    except Exception as e:
        return {
            "product": product_code,
            "synthesis_state": "INSUFFICIENT",
            "confidence": "YETERSİZ",
            "strength": "YETERSİZ",
            "uncertainty": "YÜKSEK",
            "conflict": "YOK",
            "regime": "BİLİNMİYOR",
            "reason": f"EvidencePool OKUMA HATASI: {type(e).__name__}: {e}",
            "evidence_count": 0,
            "evidence_ids": [],
            "cot": {"available": False, "summary": {}, "details": {}},
        }

    count = len(evidences)

    # --- Boş havuz ---
    if count == 0:
        return {
            "product": product_code,
            "synthesis_state": "INSUFFICIENT",
            "confidence": "YETERSİZ",
            "strength": "YETERSİZ",
            "uncertainty": "YÜKSEK",
            "conflict": "YOK",
            "regime": "BİLİNMİYOR",
            "reason": "Havuzda doğrulanmış kanıt bulunamadı.",
            "evidence_count": 0,
            "evidence_ids": [],
            "cot": {"available": False, "summary": {}, "details": {}},
        }

    # --- Evidence ID listesi ---
    evidence_ids = [
        e.get("evidence_id", f"REC_{i}")
        for i, e in enumerate(evidences)
    ]

    # --- COT verisini bul ve yorumla ---
    cot_evidences = [
        e for e in evidences
        if isinstance(e, dict) and e.get("source_type") == "COT"
    ]

    cot_result: Dict[str, Any] = {
        "available": False,
        "summary": {},
        "details": {},
    }

    if cot_evidences and COT_INTERPRETER_AVAILABLE:
        cot_meta = cot_evidences[0].get("metadata") or {}
        if isinstance(cot_meta, dict) and cot_meta:
            try:
                cot_result = interpret_cot(cot_meta, product_code)
            except Exception as e:
                cot_result = {
                    "available": False,
                    "summary": {"interpretation": f"COT yorum hatası: {e}"},
                    "details": {},
                }

    cot_mevcut = bool(cot_result.get("available", False))

    # --- Güç, belirsizlik, çatışma, rejim ---
    kaynak_sayisi = len({e.get("source_id") for e in evidences if e.get("source_id")})
    strength = _hesapla_guc(count)
    uncertainty = _hesapla_belirsizlik(kaynak_sayisi)
    conflict = _hesapla_catisma(evidences)
    regime = _hesapla_rejim(count, cot_mevcut)

    # --- Synthesis state (COT bazlı) ---
    if count == 0:
        synthesis_state = "INSUFFICIENT"
        confidence = "YETERSİZ"
        reason = "Havuzda kanıt yok."
    elif not cot_mevcut:
        synthesis_state = "INSUFFICIENT"
        confidence = "YETERSİZ"
        reason = "COT verisi bulunamadı, yön belirlenemiyor."
    else:
        detaylar = cot_result.get("details", {}) or {}
        cta_proxy = detaylar.get("cta_proxy", {}) or {}
        cta_net = cta_proxy.get("net", 0)

        if cta_net > 0:
            synthesis_state = "BULLISH"
            confidence = "MODERATE"
            reason = f"CTA proxy net long ({cta_net}). {count} kanıt doğrulandı."
        elif cta_net < 0:
            synthesis_state = "BEARISH"
            confidence = "MODERATE"
            reason = f"CTA proxy net short ({cta_net}). {count} kanıt doğrulandı."
        else:
            synthesis_state = "NEUTRAL"
            confidence = "DÜŞÜK"
            reason = f"CTA proxy nötr. {count} kanıt doğrulandı."

    # --- Çıktı ---
    return {
        "product": product_code,
        "synthesis_state": synthesis_state,
        "confidence": confidence,
        "strength": strength,
        "uncertainty": uncertainty,
        "conflict": conflict,
        "regime": regime,
        "reason": reason,
        "evidence_count": count,
        "evidence_ids": evidence_ids,
        "evidences": evidences,
        "cot": cot_result,
    }