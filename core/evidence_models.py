"""
CTA ERHAN TERMİNALİ — Evidence Models
=======================================
Kanıt havuzunun temel veri modeli.
X, COT ve RSS kaynaklarından gelen her iddia bu formata dönüşür.

12 alanlı canonical model.
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import json


# ============================================================
# YÖN SABİTLERİ
# ============================================================

DIRECTION_BULLISH = "BULLISH"
DIRECTION_BEARISH = "BEARISH"
DIRECTION_NEUTRAL = "NEUTRAL"
DIRECTION_UNKNOWN = "UNKNOWN"

VALID_DIRECTIONS = {
    DIRECTION_BULLISH,
    DIRECTION_BEARISH,
    DIRECTION_NEUTRAL,
    DIRECTION_UNKNOWN,
}

DIRECTION_SCORE = {
    DIRECTION_BULLISH: 1,
    DIRECTION_BEARISH: -1,
    DIRECTION_NEUTRAL: 0,
    DIRECTION_UNKNOWN: 0,
}


# ============================================================
# KAYNAK TİPLERİ
# ============================================================

SOURCE_TYPE_X = "X"
SOURCE_TYPE_COT = "COT"
SOURCE_TYPE_RSS = "RSS"

VALID_SOURCE_TYPES = {
    SOURCE_TYPE_X,
    SOURCE_TYPE_COT,
    SOURCE_TYPE_RSS,
}


# ============================================================
# CANONICAL EVIDENCE — 12 ALAN
# ============================================================

@dataclass
class Evidence:
    """
    Kanonik kanıt modeli.

    Bir tweet, RSS makalesi veya COT satırı bu formata dönüşür.
    Her evidence TEK BİR varlığa bağlıdır.
    Aynı tweet birden fazla varlık için birden fazla evidence üretebilir.
    """

    # --- Zorunlu alanlar (10) ---
    evidence_id: str
    """Benzersiz kimlik. Örn: "x_123456_gc", "cot_2026-09-15_gc" """

    source_type: str
    """X / COT / RSS"""

    source_name: str
    """Kaynak adı. Örn: "@wayneterprises", "CFTC COT", "Tickmill" """

    source_document_id: str
    """Kaynak dokümanı ID. Örn: tweet_id, RSS guid, COT report key"""

    asset_code: str
    """Futures kontrat kodu. Örn: "GC", "CL", "ES" """

    direction: str
    """BULLISH / BEARISH / NEUTRAL / UNKNOWN"""

    claim_text: str
    """Çıkarılan iddia. Örn: "Gold CTA positioning is long" """

    supporting_text: str
    """İddiayı destekleyen alıntı. Örn: "Gold signal: Long" """

    published_at: str
    """Kaynak yayın zamanı (UTC ISO format)"""

    ingested_at: str
    """Sisteme alınma zamanı (UTC ISO format)"""

    # --- Opsiyonel / sonradan eklenen (2) ---
    extraction_confidence: float = 0.0
    """0.00 - 1.00. AI/OCR ne kadar emin?"""

    source_url: Optional[str] = None
    """Kaynak URL (Streamlit'te link için)"""

    # ========================================================
    # VALIDASYON
    # ========================================================

    def validate(self) -> tuple[bool, list[str]]:
        """Kanıtı doğrula. (is_valid, errors) döner."""
        errors = []

        # Zorunlu alanlar
        if not self.evidence_id:
            errors.append("evidence_id boş")
        if not self.source_type:
            errors.append("source_type boş")
        elif self.source_type not in VALID_SOURCE_TYPES:
            errors.append(f"geçersiz source_type: {self.source_type}")
        if not self.source_name:
            errors.append("source_name boş")
        if not self.source_document_id:
            errors.append("source_document_id boş")
        if not self.asset_code:
            errors.append("asset_code boş")
        if not self.direction:
            errors.append("direction boş")
        elif self.direction not in VALID_DIRECTIONS:
            errors.append(f"geçersiz direction: {self.direction}")
        if not self.claim_text:
            errors.append("claim_text boş")
        if not self.published_at:
            errors.append("published_at boş")
        if not self.ingested_at:
            errors.append("ingested_at boş")

        # Confidence kontrolü
        if not (0.0 <= self.extraction_confidence <= 1.0):
            errors.append(
                f"extraction_confidence 0-1 arası olmalı: {self.extraction_confidence}"
            )

        return (len(errors) == 0, errors)

    def is_valid(self) -> bool:
        """Basit geçerlilik kontrolü."""
        return self.validate()[0]

    # ========================================================
    # SERIALIZE
    # ========================================================

    def to_dict(self) -> Dict[str, Any]:
        """Dict'e çevir."""
        return asdict(self)

    def to_json(self) -> str:
        """JSON string'e çevir."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Evidence":
        """Dict'ten Evidence oluştur."""
        return cls(
            evidence_id=data.get("evidence_id", ""),
            source_type=data.get("source_type", ""),
            source_name=data.get("source_name", ""),
            source_document_id=data.get("source_document_id", ""),
            asset_code=data.get("asset_code", ""),
            direction=data.get("direction", "UNKNOWN"),
            claim_text=data.get("claim_text", ""),
            supporting_text=data.get("supporting_text", ""),
            published_at=data.get("published_at", ""),
            ingested_at=data.get("ingested_at", ""),
            extraction_confidence=float(data.get("extraction_confidence", 0.0)),
            source_url=data.get("source_url"),
        )

    # ========================================================
    # YARDIMCI
    # ========================================================

    def direction_score(self) -> int:
        """Yön skoru: BULLISH=+1, BEARISH=-1, NEUTRAL=0"""
        return DIRECTION_SCORE.get(self.direction, 0)

    def age_hours(self) -> float:
        """Kaç saat önce yayımlandı?"""
        try:
            pub = datetime.fromisoformat(self.published_at.replace("Z", "+00:00"))
            if pub.tzinfo is None:
                pub = pub.replace(tzinfo=timezone.utc)
            delta = datetime.now(timezone.utc) - pub
            return max(0.0, delta.total_seconds() / 3600)
        except Exception:
            return 0.0


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def create_evidence_id(source_type: str, source_document_id: str, asset_code: str) -> str:
    """
    Benzersiz evidence_id üret.

    Örnek:
        create_evidence_id("X", "123456", "GC") → "x_123456_gc"
        create_evidence_id("COT", "2026-09-15", "CL") → "cot_2026-09-15_cl"
    """
    st = source_type.lower().strip()
    doc = str(source_document_id).strip().replace(" ", "_")
    asset = asset_code.lower().strip()
    return f"{st}_{doc}_{asset}"


def now_utc_iso() -> str:
    """Şu anki UTC zamanı ISO formatında."""
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# KONTROL
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Evidence Model Test")
    print("=" * 60)

    # Test 1: Geçerli evidence
    ev = Evidence(
        evidence_id=create_evidence_id("X", "188900001", "GC"),
        source_type="X",
        source_name="@wayneterprises",
        source_document_id="188900001",
        asset_code="GC",
        direction="BULLISH",
        claim_text="Gold CTA positioning remains long",
        supporting_text="Gold CTA signal: Long",
        published_at="2026-09-16T01:10:00+00:00",
        ingested_at=now_utc_iso(),
        extraction_confidence=0.88,
        source_url="https://x.com/wayneterprises/status/188900001",
    )

    print("\n1. Test Evidence:")
    print(f"   ID: {ev.evidence_id}")
    print(f"   Yön skoru: {ev.direction_score()}")
    print(f"   Yaş (saat): {ev.age_hours():.2f}")

    valid, errors = ev.validate()
    print(f"   Geçerli mi? {valid}")
    if errors:
        for e in errors:
            print(f"     - {e}")

    # Test 2: JSON serialize
    print("\n2. JSON Serialize:")
    json_str = ev.to_json()
    print(json_str[:200] + "...")

    # Test 3: Deserialize
    print("\n3. Deserialize:")
    ev2 = Evidence.from_dict(json.loads(json_str))
    print(f"   ID eşleşti mi? {ev2.evidence_id == ev.evidence_id}")

    # Test 4: Geçersiz evidence
    print("\n4. Geçersiz Evidence Testi:")
    bad_ev = Evidence(
        evidence_id="",
        source_type="INVALID",
        source_name="",
        source_document_id="",
        asset_code="",
        direction="WRONG",
        claim_text="",
        supporting_text="",
        published_at="",
        ingested_at="",
        extraction_confidence=1.5,
    )
    valid, errors = bad_ev.validate()
    print(f"   Geçerli mi? {valid}")
    print(f"   Hata sayısı: {len(errors)}")
    for e in errors:
        print(f"     - {e}")

    # Test 5: COT evidence
    print("\n5. COT Evidence:")
    cot_ev = Evidence(
        evidence_id=create_evidence_id("COT", "2026-09-15", "GC"),
        source_type="COT",
        source_name="CFTC COT",
        source_document_id="2026-09-15",
        asset_code="GC",
        direction="BULLISH",
        claim_text="Leveraged Funds net long increased",
        supporting_text="Net position: +13,000 contracts",
        published_at="2026-09-15T19:30:00+00:00",
        ingested_at=now_utc_iso(),
        extraction_confidence=0.98,
    )
    print(f"   ID: {cot_ev.evidence_id}")
    print(f"   Geçerli mi? {cot_ev.is_valid()}")