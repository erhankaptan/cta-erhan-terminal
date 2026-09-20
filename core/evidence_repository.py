"""
CTA ERHAN TERMİNALİ — Evidence Repository
==========================================
SQLite tabanlı kanıt deposu.
X, COT, RSS evidence'lerini saklar ve sorgular.

Kullanım:
    from core.evidence_repository import EvidenceRepository

    repo = EvidenceRepository()
    repo.save(evidence)                  # Kayıt
    results = repo.get_for_asset("GC")   # Sorgu
    count = repo.count()                 # Sayım
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from core.evidence_models import Evidence


# ============================================================
# VARSAYILAN VERİTABANI YOLU
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_DB = PROJECT_ROOT / "data" / "evidence.db"


# ============================================================
# EVIDENCE REPOSITORY
# ============================================================

class EvidenceRepository:

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path or DEFAULT_DB).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    # ========================================================
    # BAĞLANTI
    # ========================================================

    def _connection(self):
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=30.0,
            check_same_thread=False,
        )
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.row_factory = sqlite3.Row
        return conn

    # ========================================================
    # ŞEMA
    # ========================================================

    def _init_db(self):
        with self._connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evidences (
                    evidence_id TEXT PRIMARY KEY,
                    source_type TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    source_document_id TEXT NOT NULL,
                    asset_code TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    claim_text TEXT NOT NULL,
                    supporting_text TEXT,
                    published_at TEXT NOT NULL,
                    ingested_at TEXT NOT NULL,
                    extraction_confidence REAL NOT NULL DEFAULT 0.0,
                    source_url TEXT
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ev_asset
                ON evidences(asset_code)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ev_source_type
                ON evidences(source_type)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ev_published
                ON evidences(published_at DESC)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ev_asset_pub
                ON evidences(asset_code, published_at DESC)
            """)

            conn.commit()

    # ========================================================
    # KAYIT (INSERT)
    # ========================================================

    def save(self, evidence: Evidence) -> bool:
        """
        Evidence kaydet.

        Aynı evidence_id zaten varsa → güncellemez, atlar (dedup).
        Döner: True (yeni kayıt) / False (zaten vardı)
        """
        valid, errors = evidence.validate()
        if not valid:
            raise ValueError(f"Geçersiz evidence: {errors}")

        with self._connection() as conn:
            try:
                conn.execute("""
                    INSERT INTO evidences (
                        evidence_id, source_type, source_name,
                        source_document_id, asset_code, direction,
                        claim_text, supporting_text,
                        published_at, ingested_at,
                        extraction_confidence, source_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    evidence.evidence_id,
                    evidence.source_type,
                    evidence.source_name,
                    evidence.source_document_id,
                    evidence.asset_code,
                    evidence.direction,
                    evidence.claim_text,
                    evidence.supporting_text,
                    evidence.published_at,
                    evidence.ingested_at,
                    evidence.extraction_confidence,
                    evidence.source_url,
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Duplicate evidence_id
                return False

    def save_many(self, evidences: List[Evidence]) -> Dict[str, int]:
        """Birden fazla evidence kaydet."""
        result = {"new": 0, "skipped": 0, "errors": 0}
        for ev in evidences:
            try:
                if self.save(ev):
                    result["new"] += 1
                else:
                    result["skipped"] += 1
            except Exception:
                result["errors"] += 1
        return result

    # ========================================================
    # SORGU (SELECT)
    # ========================================================

    def get_by_id(self, evidence_id: str) -> Optional[Evidence]:
        """ID ile tek evidence al."""
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM evidences WHERE evidence_id = ?",
                (evidence_id,),
            ).fetchone()
            return self._row_to_evidence(row) if row else None

    def get_for_asset(
        self,
        asset_code: str,
        limit: int = 100,
        hours_back: Optional[int] = None,
    ) -> List[Evidence]:
        """
        Varlığa göre evidence al.

        Args:
            asset_code: Futures kodu (GC, CL, vs.)
            limit: Maksimum kayıt
            hours_back: Sadece son X saat (None = hepsi)
        """
        asset = asset_code.upper().strip()
        query = "SELECT * FROM evidences WHERE asset_code = ?"
        params: List[Any] = [asset]

        if hours_back is not None:
            query += " AND ingested_at >= datetime('now', ?)"
            params.append(f"-{hours_back} hours")

        query += " ORDER BY published_at DESC LIMIT ?"
        params.append(limit)

        with self._connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_evidence(r) for r in rows]

    def get_by_source_type(
        self,
        source_type: str,
        limit: int = 100,
    ) -> List[Evidence]:
        """Kaynak tipine göre evidence al (X / COT / RSS)."""
        st = source_type.upper().strip()
        with self._connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM evidences
                WHERE source_type = ?
                ORDER BY published_at DESC
                LIMIT ?
                """,
                (st, limit),
            ).fetchall()
            return [self._row_to_evidence(r) for r in rows]

    def get_all(self, limit: int = 500) -> List[Evidence]:
        """Tüm evidence'leri al."""
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT * FROM evidences ORDER BY published_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [self._row_to_evidence(r) for r in rows]

    # ========================================================
    # SAYIM
    # ========================================================

    def count(self, asset_code: Optional[str] = None) -> int:
        """Kayıt sayısı."""
        with self._connection() as conn:
            if asset_code:
                row = conn.execute(
                    "SELECT COUNT(*) FROM evidences WHERE asset_code = ?",
                    (asset_code.upper().strip(),),
                ).fetchone()
            else:
                row = conn.execute("SELECT COUNT(*) FROM evidences").fetchone()
            return int(row[0])

    def count_by_asset(self) -> Dict[str, int]:
        """Varlık bazında sayım."""
        with self._connection() as conn:
            rows = conn.execute(
                """
                SELECT asset_code, COUNT(*) as cnt
                FROM evidences
                GROUP BY asset_code
                ORDER BY cnt DESC
                """
            ).fetchall()
            return {r["asset_code"]: r["cnt"] for r in rows}

    def count_by_source_type(self) -> Dict[str, int]:
        """Kaynak tipine göre sayım."""
        with self._connection() as conn:
            rows = conn.execute(
                """
                SELECT source_type, COUNT(*) as cnt
                FROM evidences
                GROUP BY source_type
                """
            ).fetchall()
            return {r["source_type"]: r["cnt"] for r in rows}

    # ========================================================
    # SİLME
    # ========================================================

    def delete(self, evidence_id: str) -> bool:
        """Tek evidence sil."""
        with self._connection() as conn:
            cursor = conn.execute(
                "DELETE FROM evidences WHERE evidence_id = ?",
                (evidence_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_all(self) -> int:
        """Tüm evidence'leri sil (test için)."""
        with self._connection() as conn:
            cursor = conn.execute("DELETE FROM evidences")
            conn.commit()
            return cursor.rowcount

    # ========================================================
    # YARDIMCI
    # ========================================================

    @staticmethod
    def _row_to_evidence(row: sqlite3.Row) -> Evidence:
        """SQLite row → Evidence."""
        return Evidence(
            evidence_id=row["evidence_id"],
            source_type=row["source_type"],
            source_name=row["source_name"],
            source_document_id=row["source_document_id"],
            asset_code=row["asset_code"],
            direction=row["direction"],
            claim_text=row["claim_text"],
            supporting_text=row["supporting_text"] or "",
            published_at=row["published_at"],
            ingested_at=row["ingested_at"],
            extraction_confidence=row["extraction_confidence"],
            source_url=row["source_url"],
        )


# ============================================================
# KONTROL
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Evidence Repository Test")
    print("=" * 60)

    # Test DB (geçici)
    test_db = PROJECT_ROOT / "data" / "test_evidence.db"
    if test_db.exists():
        test_db.unlink()

    repo = EvidenceRepository(str(test_db))
    print(f"\nDB yolu: {repo.db_path}")

    # Test 1: Kayıt
    print("\n1. Kayıt Testi")
    ev1 = Evidence(
        evidence_id="x_test_001_gc",
        source_type="X",
        source_name="@wayneterprises",
        source_document_id="test_001",
        asset_code="GC",
        direction="BULLISH",
        claim_text="Gold long",
        supporting_text="Gold signal: Long",
        published_at="2026-09-16T01:10:00+00:00",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        extraction_confidence=0.88,
        source_url="https://x.com/test",
    )
    saved = repo.save(ev1)
    print(f"   Kaydedildi mi? {saved}")
    print(f"   Toplam kayıt: {repo.count()}")

    # Test 2: Duplicate (aynı ID)
    print("\n2. Duplicate Testi")
    saved_again = repo.save(ev1)
    print(f"   Tekrar kaydedildi mi? {saved_again} (False olmalı)")
    print(f"   Toplam kayıt: {repo.count()}")

    # Test 3: Farklı asset
    print("\n3. Farklı Asset")
    ev2 = Evidence(
        evidence_id="x_test_002_cl",
        source_type="X",
        source_name="@wayneterprises",
        source_document_id="test_002",
        asset_code="CL",
        direction="BEARISH",
        claim_text="Crude oil short",
        supporting_text="WTI bearish",
        published_at="2026-09-16T02:00:00+00:00",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        extraction_confidence=0.75,
    )
    repo.save(ev2)
    print(f"   Toplam kayıt: {repo.count()}")

    # Test 4: COT evidence
    print("\n4. COT Evidence")
    ev3 = Evidence(
        evidence_id="cot_test_gc",
        source_type="COT",
        source_name="CFTC COT",
        source_document_id="2026-09-15",
        asset_code="GC",
        direction="BULLISH",
        claim_text="Leveraged Funds long",
        supporting_text="Net: +13,000",
        published_at="2026-09-15T19:30:00+00:00",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        extraction_confidence=0.98,
    )
    repo.save(ev3)
    print(f"   Toplam kayıt: {repo.count()}")

    # Test 5: Sorgu — asset bazlı
    print("\n5. GC Evidence Sorgusu")
    gc_evidences = repo.get_for_asset("GC")
    print(f"   GC kanıt sayısı: {len(gc_evidences)}")
    for ev in gc_evidences:
        print(f"     - {ev.evidence_id} ({ev.source_type}) → {ev.direction}")

    # Test 6: Sorgu — source type bazlı
    print("\n6. COT Evidence Sorgusu")
    cot_evidences = repo.get_by_source_type("COT")
    print(f"   COT kanıt sayısı: {len(cot_evidences)}")

    # Test 7: Sayım
    print("\n7. Sayımlar")
    print(f"   Toplam: {repo.count()}")
    print(f"   GC: {repo.count('GC')}")
    print(f"   CL: {repo.count('CL')}")
    print(f"   Asset bazlı: {repo.count_by_asset()}")
    print(f"   Kaynak bazlı: {repo.count_by_source_type()}")

    # Test 8: Sil
    print("\n8. Silme Testi")
    deleted = repo.delete("x_test_001_gc")
    print(f"   Silindi mi? {deleted}")
    print(f"   Toplam kayıt: {repo.count()}")

    # Test 9: save_many
    print("\n9. Toplu Kayıt")
    new_evs = []
    for i in range(3):
        new_evs.append(Evidence(
            evidence_id=f"bulk_{i}_si",
            source_type="X",
            source_name="@test",
            source_document_id=f"bulk_{i}",
            asset_code="SI",
            direction="NEUTRAL",
            claim_text=f"Silver test {i}",
            supporting_text="",
            published_at="2026-09-16T03:00:00+00:00",
            ingested_at=datetime.now(timezone.utc).isoformat(),
            extraction_confidence=0.5,
        ))
    result = repo.save_many(new_evs)
    print(f"   Sonuç: {result}")

    # Temizlik
    if test_db.exists():
        test_db.unlink()
        print(f"\nTest DB silindi: {test_db}")