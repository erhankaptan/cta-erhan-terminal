"""
CTA ERHAN TERMİNALİ — Confidence Engine
=========================================
Kanıt güveni hesabı için bağımsız modül.

Confidence = 0.45 × Agreement + 0.35 × Diversity + 0.20 × Strength
→ 0-100

ÖNEMLİ:
- "Doğruluk olasılığı" DEĞİL
- "Kanıt güveni" = kanıtların kalite ve mutabakat seviyesi

Kullanım:
    from core.confidence_engine import calculate_confidence
    confidence = calculate_confidence(
        direction_score=0.62,
        source_type_count=3,
        total_weight=0.85,
        is_conflict=False,
    )
    # → 82
"""

from typing import Dict
from dataclasses import dataclass


# ============================================================
# AĞIRLIK SABİTLERİ
# ============================================================

WEIGHT_AGREEMENT = 0.45
WEIGHT_DIVERSITY = 0.35
WEIGHT_STRENGTH = 0.20

# Eşikler
MAX_DIVERSITY_SOURCES = 3       # 3+ kaynak = max diversity
STRENGTH_NORMALIZER = 0.75      # 0.75+ ağırlık = max strength

# Conflict durumunda tavan
CONFLICT_CONFIDENCE_CAP = 45


# ============================================================
# DETAY MODELİ
# ============================================================

@dataclass
class ConfidenceDetails:
    """Confidence hesap detayları."""
    confidence: int          # 0-100
    uncertainty: int         # 100 - confidence
    agreement: float         # 0.0 - 1.0
    diversity: float         # 0.0 - 1.0
    strength: float          # 0.0 - 1.0
    is_conflict: bool
    note: str

    def to_dict(self) -> Dict:
        return {
            "confidence": self.confidence,
            "uncertainty": self.uncertainty,
            "agreement": round(self.agreement, 4),
            "diversity": round(self.diversity, 4),
            "strength": round(self.strength, 4),
            "is_conflict": self.is_conflict,
            "note": self.note,
        }


# ============================================================
# ALT HESAPLAR
# ============================================================

def _agreement(direction_score: float) -> float:
    """
    Agreement = |S_asset|
    Ne kadar güçlü yön skoru → o kadar uyumlu
    """
    return min(1.0, abs(direction_score))


def _diversity(source_type_count: int) -> float:
    """
    Diversity = min(source_types, 3) / 3
    X + COT + RSS = 3 → max çeşitlilik
    """
    return min(1.0, source_type_count / MAX_DIVERSITY_SOURCES)


def _strength(total_weight: float) -> float:
    """
    Strength = min(1, total_weight / 0.75)
    0.75+ toplam ağırlık = max güç
    """
    return min(1.0, total_weight / STRENGTH_NORMALIZER)


# ============================================================
# ANA FONKSİYON
# ============================================================

def calculate_confidence(
    direction_score: float,
    source_type_count: int,
    total_weight: float,
    is_conflict: bool = False,
) -> ConfidenceDetails:
    """
    Kanıt güveni hesapla.

    Args:
        direction_score: Varlık yön skoru (-1.00 ile +1.00 arası)
        source_type_count: Farklı kaynak türü sayısı (X, COT, RSS)
        total_weight: Toplam effective ağırlık
        is_conflict: CONFLICT durumunda mı?

    Returns:
        ConfidenceDetails
    """
    # Alt puanlar
    agreement = _agreement(direction_score)
    diversity = _diversity(source_type_count)
    strength = _strength(total_weight)

    # Ana formül
    raw = (
        WEIGHT_AGREEMENT * agreement
        + WEIGHT_DIVERSITY * diversity
        + WEIGHT_STRENGTH * strength
    )

    # Conflict durumunda tavan uygula
    if is_conflict:
        raw = min(raw, CONFLICT_CONFIDENCE_CAP / 100.0)

    # 0-100'e çevir
    confidence = int(round(max(0.0, min(1.0, raw)) * 100))
    uncertainty = 100 - confidence

    # Not
    if is_conflict:
        note = f"CONFLICT tavanı uygulandı ({CONFLICT_CONFIDENCE_CAP})"
    elif confidence >= 80:
        note = "Yüksek kanıt güveni"
    elif confidence >= 60:
        note = "Orta kanıt güveni"
    elif confidence >= 40:
        note = "Düşük kanıt güveni"
    else:
        note = "Çok düşük kanıt güveni"

    return ConfidenceDetails(
        confidence=confidence,
        uncertainty=uncertainty,
        agreement=agreement,
        diversity=diversity,
        strength=strength,
        is_conflict=is_conflict,
        note=note,
    )


# ============================================================
# YARDIMCI: İNSAN-OKUNUR ETİKET
# ============================================================

def confidence_label(confidence: int) -> str:
    """Confidence → Türkçe etiket."""
    if confidence >= 80:
        return "ÇOK YÜKSEK"
    if confidence >= 60:
        return "YÜKSEK"
    if confidence >= 40:
        return "ORTA"
    if confidence >= 20:
        return "DÜŞÜK"
    return "ÇOK DÜŞÜK"


def uncertainty_label(uncertainty: int) -> str:
    """Uncertainty → Türkçe etiket."""
    if uncertainty >= 80:
        return "ÇOK YÜKSEK"
    if uncertainty >= 60:
        return "YÜKSEK"
    if uncertainty >= 40:
        return "ORTA"
    if uncertainty >= 20:
        return "DÜŞÜK"
    return "ÇOK DÜŞÜK"


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Confidence Engine Test")
    print("=" * 60)

    test_cases = [
        # (direction_score, source_count, total_weight, is_conflict, açıklama)
        (1.00, 3, 0.90, False, "Tüm kaynaklar uyumlu, yüksek ağırlık"),
        (0.62, 3, 0.85, False, "İyi uyum, yüksek ağırlık"),
        (0.40, 2, 0.50, False, "Orta uyum, orta ağırlık"),
        (0.10, 3, 0.80, False, "Zayıf uyum, yüksek ağırlık"),
        (0.05, 2, 0.30, False, "Çok zayıf uyum"),
        (0.50, 3, 0.90, True,  "CONFLICT durumu (tavan 45)"),
        (1.00, 1, 0.40, False, "Tek kaynak"),
    ]

    for i, (score, src, weight, conflict, desc) in enumerate(test_cases, 1):
        d = calculate_confidence(score, src, weight, conflict)
        print(f"\n{i}. {desc}")
        print(f"   Girdi: score={score:+.2f}, src={src}, weight={weight}, conflict={conflict}")
        print(f"   → Confidence: {d.confidence} ({confidence_label(d.confidence)})")
        print(f"   → Uncertainty: {d.uncertainty} ({uncertainty_label(d.uncertainty)})")
        print(f"   → Agreement: {d.agreement:.2f}, Diversity: {d.diversity:.2f}, Strength: {d.strength:.2f}")
        print(f"   → {d.note}")

    # Dağılım kontrolü
    print("\n" + "=" * 60)
    print("Dağılım Kontrolü")
    print("=" * 60)
    for score in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        d = calculate_confidence(score, 3, 0.85, False)
        print(f"   score={score:.1f} → conf={d.confidence}")

    print("\n" + "=" * 60)
    print("Tüm testler tamamlandı")