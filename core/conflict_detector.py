"""
CTA ERHAN TERMİNALİ — Conflict Detector
=========================================
CONFLICT tespiti için bağımsız modül.

Bir varlık için:
- Bull (yukarı) ağırlığı ve Bear (aşağı) ağırlığı hesaplanır
- Her iki taraf anlamlı güçte ise → CONFLICT

Kurallar:
    1. En az 2 farklı kaynak türü olmalı
    2. Bull ağırlığı ≥ 0.20
    3. Bear ağırlığı ≥ 0.20
    4. Oran (min/max) ≥ 0.50

Kullanım:
    from core.conflict_detector import detect_conflict
    is_conflict, details = detect_conflict(bull_weight, bear_weight, source_types)
"""

from typing import Set, Dict, Tuple, List
from dataclasses import dataclass


# ============================================================
# EŞİKLER (V1)
# ============================================================

MIN_SOURCE_TYPES = 2            # En az kaç farklı kaynak türü
MIN_SIDE_WEIGHT = 0.20          # Her taraf için min ağırlık
CONFLICT_RATIO = 0.50           # Zıt taraf oranı eşiği


# ============================================================
# DETAY MODELİ
# ============================================================

@dataclass
class ConflictDetails:
    """Conflict tespit detayları."""
    is_conflict: bool
    bull_weight: float
    bear_weight: float
    ratio: float
    source_type_count: int
    reason: str

    def to_dict(self) -> Dict:
        return {
            "is_conflict": self.is_conflict,
            "bull_weight": self.bull_weight,
            "bear_weight": self.bear_weight,
            "ratio": round(self.ratio, 4),
            "source_type_count": self.source_type_count,
            "reason": self.reason,
        }


# ============================================================
# ANA FONKSİYON
# ============================================================

def detect_conflict(
    bull_weight: float,
    bear_weight: float,
    source_types: Set[str],
) -> ConflictDetails:
    """
    İki yön arasında CONFLICT var mı?

    Args:
        bull_weight: Yukarı yönlü kanıtların toplam ağırlığı
        bear_weight: Aşağı yönlü kanıtların toplam ağırlığı
        source_types: Kanıtlarda geçen kaynak türleri (X, COT, RSS)

    Returns:
        ConflictDetails
    """
    source_count = len(source_types)

    # 1. Kaynak çeşitliliği kontrolü
    if source_count < MIN_SOURCE_TYPES:
        return ConflictDetails(
            is_conflict=False,
            bull_weight=bull_weight,
            bear_weight=bear_weight,
            ratio=0.0,
            source_type_count=source_count,
            reason=f"Yetersiz kaynak çeşitliliği: {source_count} (min {MIN_SOURCE_TYPES})",
        )

    # 2. Bir taraf sıfırsa → CONFLICT yok
    if bull_weight == 0 or bear_weight == 0:
        return ConflictDetails(
            is_conflict=False,
            bull_weight=bull_weight,
            bear_weight=bear_weight,
            ratio=0.0,
            source_type_count=source_count,
            reason="Bir taraf sıfır, çelişki yok",
        )

    # 3. Her iki taraf da min ağırlık üstünde mi?
    if bull_weight < MIN_SIDE_WEIGHT or bear_weight < MIN_SIDE_WEIGHT:
        return ConflictDetails(
            is_conflict=False,
            bull_weight=bull_weight,
            bear_weight=bear_weight,
            ratio=0.0,
            source_type_count=source_count,
            reason=(
                f"Bir taraf zayıf: "
                f"bull={bull_weight:.3f}, bear={bear_weight:.3f} "
                f"(min {MIN_SIDE_WEIGHT})"
            ),
        )

    # 4. Oran kontrolü
    max_w = max(bull_weight, bear_weight)
    min_w = min(bull_weight, bear_weight)
    ratio = min_w / max_w if max_w > 0 else 0.0

    if ratio < CONFLICT_RATIO:
        return ConflictDetails(
            is_conflict=False,
            bull_weight=bull_weight,
            bear_weight=bear_weight,
            ratio=ratio,
            source_type_count=source_count,
            reason=(
                f"Oran düşük: {ratio:.2f} (min {CONFLICT_RATIO}), "
                f"bir taraf baskın"
            ),
        )

    # 5. CONFLICT
    return ConflictDetails(
        is_conflict=True,
        bull_weight=bull_weight,
        bear_weight=bear_weight,
        ratio=ratio,
        source_type_count=source_count,
        reason=(
            f"CONFLICT: bull={bull_weight:.3f}, bear={bear_weight:.3f}, "
            f"ratio={ratio:.2f} ≥ {CONFLICT_RATIO}"
        ),
    )


# ============================================================
# YARDIMCI: AĞIRLIKLARI HESAPLA
# ============================================================

def calculate_side_weights(
    evidences: List,
) -> Tuple[float, float, Set[str]]:
    """
    Kanıtlardan bull/bear ağırlıklarını ve kaynak türlerini hesapla.

    Args:
        evidences: Evidence listesi

    Returns:
        (bull_weight, bear_weight, source_types)
    """
    from core.synthesis_engine import _effective_weight
    from core.evidence_models import DIRECTION_SCORE

    bull_weight = 0.0
    bear_weight = 0.0
    source_types: Set[str] = set()

    for ev in evidences:
        w = _effective_weight(ev)
        d = DIRECTION_SCORE.get(ev.direction, 0)

        source_types.add(ev.source_type)

        if d > 0:
            bull_weight += w
        elif d < 0:
            bear_weight += w

    return bull_weight, bear_weight, source_types


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Conflict Detector Test")
    print("=" * 60)

    # Test 1: Dengeli çelişki
    print("\n1. Dengeli çelişki (bull=0.5, bear=0.45)")
    r = detect_conflict(0.50, 0.45, {"X", "COT", "RSS"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Reason: {r.reason}")

    # Test 2: Bir taraf baskın
    print("\n2. Baskın (bull=0.8, bear=0.1)")
    r = detect_conflict(0.80, 0.10, {"X", "COT"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Reason: {r.reason}")

    # Test 3: Bir taraf zayıf
    print("\n3. Zayıf bear (bull=0.7, bear=0.15)")
    r = detect_conflict(0.70, 0.15, {"X", "COT"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Reason: {r.reason}")

    # Test 4: Tek kaynak türü
    print("\n4. Tek kaynak türü (X)")
    r = detect_conflict(0.50, 0.45, {"X"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Reason: {r.reason}")

    # Test 5: Bir taraf sıfır
    print("\n5. Tek yönlü (bull=0.6, bear=0.0)")
    r = detect_conflict(0.60, 0.0, {"X", "COT"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Reason: {r.reason}")

    # Test 6: Tam denge
    print("\n6. Tam denge (bull=0.5, bear=0.5)")
    r = detect_conflict(0.50, 0.50, {"X", "COT", "RSS"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Ratio: {r.ratio:.2f}")
    print(f"   Reason: {r.reason}")

    # Test 7: 3 X + 1 COT (gerçekçi)
    print("\n7. Gerçekçi: 3 X bullish, 1 COT bearish")
    # X: 0.35 * 0.9 = 0.315 (tek tweet ağırlığı değil, toplam)
    # Ama 3 X toplamı farklı olur, basit hesap:
    r = detect_conflict(0.30, 0.25, {"X", "COT"})
    print(f"   Conflict: {r.is_conflict}")
    print(f"   Ratio: {r.ratio:.2f}")

    print("\n" + "=" * 60)
    print("Tüm testler tamamlandı")