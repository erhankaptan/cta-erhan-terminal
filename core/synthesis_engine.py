"""
CTA ERHAN TERMİNALİ — Synthesis Engine
========================================
Deterministik Python sentez motoru.

Her varlık için:
- Kanıtları toplar
- Ağırlıklı yön skoru hesaplar
- 5 durumdan birini üretir: BULLISH/BEARISH/NEUTRAL/CONFLICT/INSUFFICIENT

Formül V1:
    w_i = base_weight_i × freshness_i
    S_asset = Σ(w_i × direction_i) / Σ(w_i)

LLM KULLANMAZ. Saf Python.
"""

import math
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict

from core.evidence_models import (
    Evidence,
    DIRECTION_SCORE,
    DIRECTION_BULLISH,
    DIRECTION_BEARISH,
    DIRECTION_NEUTRAL,
    DIRECTION_UNKNOWN,
)


# ============================================================
# BAZ AĞIRLIKLAR (V1)
# ============================================================

BASE_WEIGHTS = {
    "COT": 0.45,
    "X": 0.35,
    "RSS": 0.20,
}


# ============================================================
# FRESHNESS DECAY (tazelik azalma hızı)
# ============================================================

DECAY_LAMBDA = {
    "COT": 0.005,   # yavaş azalır (haftalık)
    "X": 0.035,     # hızlı azalır (günlük)
    "RSS": 0.020,   # orta
}


# ============================================================
# DURUM SABİTLERİ
# ============================================================

STATE_BULLISH = "BULLISH"
STATE_BEARISH = "BEARISH"
STATE_NEUTRAL = "NEUTRAL"
STATE_CONFLICT = "CONFLICT"
STATE_INSUFFICIENT = "INSUFFICIENT"


# ============================================================
# EŞİKLER
# ============================================================

SCORE_THRESHOLD = 0.35          # |S| > 0.35 → BULLISH/BEARISH
MIN_EVIDENCE = 1                # Min kanıt sayısı  ← DEĞİŞTİ (2→1)
MIN_SOURCE_TYPES = 1            # Min kaynak türü   ← DEĞİŞTİ (2→1)
MIN_CONFLICT_WEIGHT = 0.35      # Zıt taraf ağırlık eşiği
MIN_TOTAL_WEIGHT = 0.20         # Toplam ağırlık eşiği
CONFLICT_RATIO = 0.70           # Zıt taraf oranı


# ============================================================
# SONUÇ MODELİ
# ============================================================

@dataclass
class SynthesisResult:
    """Varlık bazlı sentez sonucu."""
    asset_code: str
    state: str
    score: float
    confidence: int
    uncertainty: int
    evidence_count: int
    source_type_count: int
    total_weight: float
    bull_weight: float
    bear_weight: float
    reasons: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    generated_at: str = ""

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def _freshness(source_type: str, published_at: str) -> float:
    """
    Tazelik katsayısı: 0.10 - 1.00

    f = e^(-λ × age_hours)
    """
    lam = DECAY_LAMBDA.get(source_type, 0.020)
    try:
        pub = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        if pub.tzinfo is None:
            pub = pub.replace(tzinfo=timezone.utc)
        age_hours = max(0.0, (datetime.now(timezone.utc) - pub).total_seconds() / 3600)
    except Exception:
        age_hours = 24.0  # Bilinmeyen tarih → varsayılan

    raw = math.exp(-lam * age_hours)
    return round(max(0.10, min(1.00, raw)), 4)


def _effective_weight(evidence: Evidence) -> float:
    """w_i = base_weight × freshness"""
    base = BASE_WEIGHTS.get(evidence.source_type, 0.10)
    fresh = _freshness(evidence.source_type, evidence.published_at)
    return base * fresh


def _score_to_state(score: float) -> str:
    """Skor → durum."""
    if score >= SCORE_THRESHOLD:
        return STATE_BULLISH
    if score <= -SCORE_THRESHOLD:
        return STATE_BEARISH
    return STATE_NEUTRAL


def _calculate_confidence(
    score: float,
    source_type_count: int,
    total_weight: float,
    is_conflict: bool,
) -> int:
    """
    Confidence = 0.45×Agreement + 0.35×Diversity + 0.20×Strength
    → 0-100
    """
    agreement = min(1.0, abs(score))
    diversity = min(1.0, source_type_count / 3)
    strength = min(1.0, total_weight / 0.75)

    raw = 0.45 * agreement + 0.35 * diversity + 0.20 * strength

    if is_conflict:
        raw = min(raw, 0.45)

    return int(round(max(0.0, min(1.0, raw)) * 100))


# ============================================================
# ANA FONKSİYON
# ============================================================

def synthesize_asset(
    asset_code: str,
    evidences: List[Evidence],
) -> SynthesisResult:
    """
    Tek varlık için sentez üret.

    Args:
        asset_code: "GC", "CL", vs.
        evidences: Bu varlığa ait kanıtlar

    Returns:
        SynthesisResult
    """
    asset = asset_code.upper().strip()

    # Geçerli kanıtları filtrele
    valid: List[Evidence] = []
    for ev in evidences:
        if ev.asset_code.upper().strip() != asset:
            continue
        if ev.direction == DIRECTION_UNKNOWN:
            continue
        if not ev.is_valid():
            continue
        valid.append(ev)

    # --- INSUFFICIENT KONTROLÜ ---

    # 1. Kanıt sayısı
    if len(valid) < MIN_EVIDENCE:
        return SynthesisResult(
            asset_code=asset,
            state=STATE_INSUFFICIENT,
            score=0.0,
            confidence=0,
            uncertainty=100,
            evidence_count=len(valid),
            source_type_count=0,
            total_weight=0.0,
            bull_weight=0.0,
            bear_weight=0.0,
            reasons=[f"Yetersiz kanıt: {len(valid)} (min {MIN_EVIDENCE})"],
            evidence_ids=[e.evidence_id for e in valid],
        )

    # 2. Kaynak çeşitliliği
    source_types = {e.source_type for e in valid}
    if len(source_types) < MIN_SOURCE_TYPES:
        return SynthesisResult(
            asset_code=asset,
            state=STATE_INSUFFICIENT,
            score=0.0,
            confidence=20,
            uncertainty=80,
            evidence_count=len(valid),
            source_type_count=len(source_types),
            total_weight=0.0,
            bull_weight=0.0,
            bear_weight=0.0,
            reasons=[f"Yetersiz kaynak çeşitliliği: {len(source_types)} (min {MIN_SOURCE_TYPES})"],
            evidence_ids=[e.evidence_id for e in valid],
        )

    # --- AĞIRLIKLI HESAP ---

    total_weight = 0.0
    signed_weight = 0.0
    bull_weight = 0.0
    bear_weight = 0.0

    for ev in valid:
        w = _effective_weight(ev)
        d = DIRECTION_SCORE.get(ev.direction, 0)

        total_weight += w
        signed_weight += w * d

        if d > 0:
            bull_weight += w
        elif d < 0:
            bear_weight += w

    # 3. Toplam ağırlık kontrolü
    if total_weight < MIN_TOTAL_WEIGHT:
        return SynthesisResult(
            asset_code=asset,
            state=STATE_INSUFFICIENT,
            score=0.0,
            confidence=20,
            uncertainty=80,
            evidence_count=len(valid),
            source_type_count=len(source_types),
            total_weight=round(total_weight, 4),
            bull_weight=round(bull_weight, 4),
            bear_weight=round(bear_weight, 4),
            reasons=[f"Yetersiz toplam ağırlık: {total_weight:.3f}"],
            evidence_ids=[e.evidence_id for e in valid],
        )

    # --- SKOR ---
    score = signed_weight / total_weight

    # --- CONFLICT KONTROLÜ ---
    is_conflict = False
    if (
        bull_weight >= MIN_CONFLICT_WEIGHT
        and bear_weight >= MIN_CONFLICT_WEIGHT
        and len(source_types) >= MIN_SOURCE_TYPES
    ):
        max_w = max(bull_weight, bear_weight)
        min_w = min(bull_weight, bear_weight)
        ratio = min_w / max_w if max_w > 0 else 0.0

        if ratio >= CONFLICT_RATIO:
            is_conflict = True

    # --- DURUM ---
    if is_conflict:
        state = STATE_CONFLICT
    else:
        state = _score_to_state(score)

    # --- CONFIDENCE ---
    confidence = _calculate_confidence(
        score=score,
        source_type_count=len(source_types),
        total_weight=total_weight,
        is_conflict=is_conflict,
    )
    uncertainty = 100 - confidence

    # --- REASONS ---
    reasons = [
        f"Kanıt sayısı: {len(valid)}",
        f"Kaynak türü: {', '.join(sorted(source_types))}",
        f"Yön skoru: {score:+.3f}",
        f"Yukarı ağırlık: {bull_weight:.3f}",
        f"Aşağı ağırlık: {bear_weight:.3f}",
        f"Toplam ağırlık: {total_weight:.3f}",
    ]
    if is_conflict:
        reasons.append(
            f"ÇELİŞKİ: her iki taraf da anlamlı güçte "
            f"(oran: {min_w/max_w:.2f})"
        )

    return SynthesisResult(
        asset_code=asset,
        state=state,
        score=round(score, 4),
        confidence=confidence,
        uncertainty=uncertainty,
        evidence_count=len(valid),
        source_type_count=len(source_types),
        total_weight=round(total_weight, 4),
        bull_weight=round(bull_weight, 4),
        bear_weight=round(bear_weight, 4),
        reasons=reasons,
        evidence_ids=[e.evidence_id for e in valid],
    )


# ============================================================
# TOPLU SENTEZ
# ============================================================

def synthesize_all(
    evidences: List[Evidence],
    asset_codes: Optional[List[str]] = None,
) -> Dict[str, SynthesisResult]:
    """
    Tüm varlıklar için sentez üret.

    Args:
        evidences: Tüm kanıtlar
        asset_codes: Hangi varlıklar? (None = kanıtlardan otomatik)

    Returns:
        {asset_code: SynthesisResult}
    """
    if asset_codes is None:
        asset_codes = sorted({e.asset_code for e in evidences})

    results = {}
    for code in asset_codes:
        asset_evidences = [e for e in evidences if e.asset_code == code]
        results[code] = synthesize_asset(code, asset_evidences)

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    from datetime import timedelta

    print("=" * 60)
    print("Synthesis Engine Test")
    print("=" * 60)

    now = datetime.now(timezone.utc)
    recent = (now - timedelta(hours=1)).isoformat()
    old = (now - timedelta(days=3)).isoformat()

    # ========================================================
    # Test 1: 3 kaynak BULLISH → BULLISH
    # ========================================================
    print("\n1. Test: Tüm kaynaklar BULLISH")
    evidences = [
        Evidence(
            evidence_id="x_001_gc",
            source_type="X", source_name="@test",
            source_document_id="001", asset_code="GC",
            direction="BULLISH", claim_text="Gold long",
            supporting_text="", published_at=recent,
            ingested_at=recent, extraction_confidence=0.9,
        ),
        Evidence(
            evidence_id="cot_001_gc",
            source_type="COT", source_name="CFTC",
            source_document_id="001", asset_code="GC",
            direction="BULLISH", claim_text="Net long",
            supporting_text="", published_at=recent,
            ingested_at=recent, extraction_confidence=0.98,
        ),
        Evidence(
            evidence_id="rss_001_gc",
            source_type="RSS", source_name="Tickmill",
            source_document_id="001", asset_code="GC",
            direction="BULLISH", claim_text="Altın yukarı",
            supporting_text="", published_at=recent,
            ingested_at=recent, extraction_confidence=0.7,
        ),
    ]
    r = synthesize_asset("GC", evidences)
    print(f"   State: {r.state}")
    print(f"   Score: {r.score}")
    print(f"   Confidence: {r.confidence}")
    print(f"   Evidence: {r.evidence_count}")

    # ========================================================
    # Test 2: 2 BULLISH, 1 BEARISH → karışık
    # ========================================================
    print("\n2. Test: Karışık (2 Bull + 1 Bear)")
    evidences[1].direction = "BEARISH"
    r = synthesize_asset("GC", evidences)
    print(f"   State: {r.state}")
    print(f"   Score: {r.score}")
    print(f"   Bull: {r.bull_weight}, Bear: {r.bear_weight}")

    # ========================================================
    # Test 3: Sadece 1 kaynak → INSUFFICIENT
    # ========================================================
    print("\n3. Test: Sadece 1 kanıt → INSUFFICIENT")
    r = synthesize_asset("GC", [evidences[0]])
    print(f"   State: {r.state}")
    print(f"   Reasons: {r.reasons}")

    # ========================================================
    # Test 4: COT + RSS bearish → BEARISH
    # ========================================================
    print("\n4. Test: COT + RSS BEARISH")
    bears = [
        Evidence(
            evidence_id="cot_002_cl",
            source_type="COT", source_name="CFTC",
            source_document_id="002", asset_code="CL",
            direction="BEARISH", claim_text="Net short",
            supporting_text="", published_at=recent,
            ingested_at=recent, extraction_confidence=0.98,
        ),
        Evidence(
            evidence_id="rss_002_cl",
            source_type="RSS", source_name="Tickmill",
            source_document_id="002", asset_code="CL",
            direction="BEARISH", claim_text="Petrol düşüş",
            supporting_text="", published_at=recent,
            ingested_at=recent, extraction_confidence=0.7,
        ),
    ]
    r = synthesize_asset("CL", bears)
    print(f"   State: {r.state}")
    print(f"   Score: {r.score}")
    print(f"   Confidence: {r.confidence}")

    # ========================================================
    # Test 5: Eski COT → freshness etkisi
    # ========================================================
    print("\n5. Test: Eski COT + yeni X")
    ev_old = Evidence(
        evidence_id="cot_old_es",
        source_type="COT", source_name="CFTC",
        source_document_id="old", asset_code="ES",
        direction="BULLISH", claim_text="Old COT long",
        supporting_text="", published_at=old,
        ingested_at=old, extraction_confidence=0.95,
    )
    ev_new = Evidence(
        evidence_id="x_new_es",
        source_type="X", source_name="@test",
        source_document_id="new", asset_code="ES",
        direction="BEARISH", claim_text="Recent bearish",
        supporting_text="", published_at=recent,
        ingested_at=recent, extraction_confidence=0.8,
    )
    r = synthesize_asset("ES", [ev_old, ev_new])
    print(f"   State: {r.state}")
    print(f"   Score: {r.score}")
    print(f"   Bull: {r.bull_weight}, Bear: {r.bear_weight}")
    print(f"   → Eski COT ağırlığı düştü, yeni X kazandı")

    # ========================================================
    # Test 6: Toplu sentez
    # ========================================================
    print("\n6. Test: Toplu sentez")
    all_ev = evidences + bears + [ev_old, ev_new]
    results = synthesize_all(all_ev)
    print(f"   Toplam varlık: {len(results)}")
    for code, res in results.items():
        print(f"     {code}: {res.state} (score={res.score:.3f}, conf={res.confidence})")