"""
CTA ERHAN KARAR MOTORU — Signals DB
====================================
Faz 2A sinyal log altyapisi.

- signals_audit tablosu (SQLite)
- log_signal() : yeni sinyal kaydet
- get_active_signal() : urun icin aktif sinyal
- get_signal_history() : gecmis sinyaller
- update_signal_outcome() : T+1h/T+4h/T+1d fiyat guncelle
- get_hit_rate() : isabet orani

Konum: core/signals_db.py
DB: data/signals.db
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# SABITLER
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DB = DATA_DIR / "signals.db"


# ============================================================
# SIGNALS DB CLASS
# ============================================================

class SignalsDB:
    """Karar motoru sinyal log altyapisi."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = Path(db_path or DEFAULT_DB).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    # --------------------------------------------------------
    # BAGLANTI
    # --------------------------------------------------------
    def _connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=30.0,
            check_same_thread=False,
        )
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.row_factory = sqlite3.Row
        return conn

    # --------------------------------------------------------
    # TABLO OLUSTUR
    # --------------------------------------------------------
    def _init_db(self) -> None:
        with self._connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS signals_audit (
                    signal_id TEXT PRIMARY KEY,
                    product TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT,

                    -- Skorlar
                    raw_score REAL,
                    final_score REAL,
                    confidence REAL,
                    signal TEXT,

                    -- Kaynak skorlari
                    cot_score REAL,
                    radar_score REAL,
                    tickmill_score REAL,

                    -- Agirliklar
                    weights_used TEXT,

                    -- Celiski
                    is_conflict INTEGER,
                    conflict_sources TEXT,

                    -- Bagimsizlik
                    independent_evidence_count INTEGER,
                    source_ages TEXT,

                    -- Sinyal tipi
                    signal_type TEXT,
                    primary_source TEXT,
                    validity_reason TEXT,

                    -- Degisim
                    previous_signal_id TEXT,
                    change_reason TEXT,

                    -- Fiyat snapshot (KRITIK)
                    price_at_signal REAL,
                    atr_at_signal REAL,

                    -- Arka plan doldurulacak
                    price_t1h REAL,
                    price_t4h REAL,
                    price_t1d REAL,
                    hit_t4h INTEGER,
                    hit_t1d INTEGER
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_product
                ON signals_audit(product)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_created
                ON signals_audit(created_at DESC)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_product_created
                ON signals_audit(product, created_at DESC)
            """)
            conn.commit()

    # --------------------------------------------------------
    # YENI SINYAL LOG
    # --------------------------------------------------------
    def log_signal(self, signal_dict: Dict[str, Any]) -> str:
        """Yeni sinyal kaydet. signal_id dondurur."""
        signal_id = signal_dict.get("signal_id") or f"sig_{uuid.uuid4().hex[:12]}"
        created_at = signal_dict.get("created_at") or datetime.now(timezone.utc).isoformat()

        # JSON alanlarini serialize et
        weights_json = json.dumps(signal_dict.get("weights_used", {}), ensure_ascii=False)
        conflict_json = json.dumps(signal_dict.get("conflict_sources", []), ensure_ascii=False)
        source_ages_json = json.dumps(signal_dict.get("source_ages", {}), ensure_ascii=False)

        with self._connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO signals_audit (
                    signal_id, product, created_at, expires_at,
                    raw_score, final_score, confidence, signal,
                    cot_score, radar_score, tickmill_score,
                    weights_used,
                    is_conflict, conflict_sources,
                    independent_evidence_count, source_ages,
                    signal_type, primary_source, validity_reason,
                    previous_signal_id, change_reason,
                    price_at_signal, atr_at_signal
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                signal_id,
                signal_dict.get("product"),
                created_at,
                signal_dict.get("expires_at"),
                signal_dict.get("raw_score"),
                signal_dict.get("final_score"),
                signal_dict.get("confidence"),
                signal_dict.get("signal"),
                signal_dict.get("cot_score"),
                signal_dict.get("radar_score"),
                signal_dict.get("tickmill_score"),
                weights_json,
                1 if signal_dict.get("is_conflict") else 0,
                conflict_json,
                signal_dict.get("independent_evidence_count"),
                source_ages_json,
                signal_dict.get("signal_type"),
                signal_dict.get("primary_source"),
                signal_dict.get("validity_reason"),
                signal_dict.get("previous_signal_id"),
                signal_dict.get("change_reason"),
                signal_dict.get("price_at_signal"),
                signal_dict.get("atr_at_signal"),
            ))
            conn.commit()
        return signal_id

    # --------------------------------------------------------
    # AKTIF SINYAL
    # --------------------------------------------------------
    def get_active_signal(self, product: str) -> Optional[Dict[str, Any]]:
        """Urun icin en son sinyali getir."""
        product = product.upper().strip()
        with self._connection() as conn:
            row = conn.execute("""
                SELECT * FROM signals_audit
                WHERE product = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (product,)).fetchone()
            if not row:
                return None
            return self._row_to_dict(row)

    # --------------------------------------------------------
    # GECMIS SINYALLER
    # --------------------------------------------------------
    def get_signal_history(self, product: str, limit: int = 30) -> List[Dict[str, Any]]:
        """Urun icin gecmis sinyalleri getir (en yeni once)."""
        product = product.upper().strip()
        with self._connection() as conn:
            rows = conn.execute("""
                SELECT * FROM signals_audit
                WHERE product = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (product, limit)).fetchall()
            return [self._row_to_dict(r) for r in rows]

    # --------------------------------------------------------
    # ISABET ORANI
    # --------------------------------------------------------
    def get_hit_rate(self, product: str, window: int = 30) -> Dict[str, Any]:
        """Son X sinyalin isabet orani."""
        product = product.upper().strip()
        with self._connection() as conn:
            rows = conn.execute("""
                SELECT hit_t4h, hit_t1d
                FROM signals_audit
                WHERE product = ? AND (hit_t4h IS NOT NULL OR hit_t1d IS NOT NULL)
                ORDER BY created_at DESC
                LIMIT ?
            """, (product, window)).fetchall()

        if not rows:
            return {"count": 0, "hit_rate_4h": None, "hit_rate_1d": None}

        hits_4h = [r["hit_t4h"] for r in rows if r["hit_t4h"] is not None]
        hits_1d = [r["hit_t1d"] for r in rows if r["hit_t1d"] is not None]

        return {
            "count": len(rows),
            "hit_rate_4h": (sum(hits_4h) / len(hits_4h) * 100) if hits_4h else None,
            "hit_rate_1d": (sum(hits_1d) / len(hits_1d) * 100) if hits_1d else None,
        }

    # --------------------------------------------------------
    # ARKA PLAN: FIYAT GUNCELLE
    # --------------------------------------------------------
    def update_signal_outcome(
        self,
        signal_id: str,
        price_t1h: Optional[float] = None,
        price_t4h: Optional[float] = None,
        price_t1d: Optional[float] = None,
    ) -> bool:
        """T+1h/T+4h/T+1d fiyatlarini guncelle ve hit hesapla."""
        with self._connection() as conn:
            # Mevcut kaydi al
            row = conn.execute("""
                SELECT product, signal, price_at_signal, atr_at_signal
                FROM signals_audit WHERE signal_id = ?
            """, (signal_id,)).fetchone()

            if not row:
                return False

            entry = row["price_at_signal"]
            atr = row["atr_at_signal"]
            signal = row["signal"]

            # Hit hesapla (0.4 ATR esik)
            hit_4h = None
            hit_1d = None

            if entry is not None and atr is not None and atr > 0:
                threshold = atr * 0.4

                if price_t4h is not None:
                    move = price_t4h - entry
                    if signal in ("GÜÇLÜ AL", "AL"):
                        hit_4h = 1 if move >= threshold else 0
                    elif signal in ("GÜÇLÜ SAT", "SAT"):
                        hit_4h = 1 if move <= -threshold else 0
                    else:
                        hit_4h = 0

                if price_t1d is not None:
                    move = price_t1d - entry
                    if signal in ("GÜÇLÜ AL", "AL"):
                        hit_1d = 1 if move >= threshold else 0
                    elif signal in ("GÜÇLÜ SAT", "SAT"):
                        hit_1d = 1 if move <= -threshold else 0
                    else:
                        hit_1d = 0

            # Guncelle
            updates = []
            params = []
            if price_t1h is not None:
                updates.append("price_t1h = ?")
                params.append(price_t1h)
            if price_t4h is not None:
                updates.append("price_t4h = ?")
                params.append(price_t4h)
            if price_t1d is not None:
                updates.append("price_t1d = ?")
                params.append(price_t1d)
            if hit_4h is not None:
                updates.append("hit_t4h = ?")
                params.append(hit_4h)
            if hit_1d is not None:
                updates.append("hit_t1d = ?")
                params.append(hit_1d)

            if not updates:
                return False

            params.append(signal_id)
            conn.execute(f"""
                UPDATE signals_audit
                SET {", ".join(updates)}
                WHERE signal_id = ?
            """, tuple(params))
            conn.commit()
            return True

    # --------------------------------------------------------
    # YARDIMCI
    # --------------------------------------------------------
    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """SQLite row -> dict (JSON alanlari parse et)."""
        d = dict(row)
        # JSON alanlari parse
        for key in ("weights_used", "conflict_sources", "source_ages"):
            if d.get(key):
                try:
                    d[key] = json.loads(d[key])
                except Exception:
                    d[key] = {}
        # is_conflict boolean
        if "is_conflict" in d:
            d["is_conflict"] = bool(d["is_conflict"])
        return d

    # --------------------------------------------------------
    # TOPLU ISTATISTIK
    # --------------------------------------------------------
    def get_stats(self) -> Dict[str, Any]:
        """Genel istatistikler."""
        with self._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM signals_audit").fetchone()[0]
            products = conn.execute("""
                SELECT product, COUNT(*) as cnt
                FROM signals_audit
                GROUP BY product
                ORDER BY cnt DESC
            """).fetchall()
            return {
                "total_signals": total,
                "by_product": {r["product"]: r["cnt"] for r in products},
            }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

global_signals_db = SignalsDB()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SignalsDB Test")
    print("=" * 60)

    db = SignalsDB()

    # Test 1: Ornek sinyal log
    sample_signal = {
        "product": "ES",
        "signal": "AL",
        "raw_score": 0.28,
        "final_score": 0.28,
        "confidence": 68.8,
        "cot_score": -0.80,
        "radar_score": 0.70,
        "tickmill_score": 0.50,
        "weights_used": {"COT": 0.50, "Radar": 0.35, "Tickmill": 0.15},
        "is_conflict": True,
        "conflict_sources": ["COT", "Radar"],
        "signal_type": "mixed",
        "primary_source": "cot",
        "validity_reason": "mixed",
        "price_at_signal": 4520.5,
        "atr_at_signal": 30.2,
        "independent_evidence_count": 2,
        "source_ages": {"COT": 12, "Radar": 2, "Tickmill": 4},
    }

    sig_id = db.log_signal(sample_signal)
    print(f"\n[1] Sinyal kaydedildi: {sig_id}")

    # Test 2: Aktif sinyal
    active = db.get_active_signal("ES")
    print(f"\n[2] Aktif sinyal: {active['signal']} | Guven %{active['confidence']}")
    print(f"    Conflict: {active['is_conflict']} | Kaynaklar: {active['conflict_sources']}")

    # Test 3: Gecmis
    history = db.get_signal_history("ES", limit=5)
    print(f"\n[3] Gecmis sinyal sayisi: {len(history)}")

    # Test 4: Outcome guncelle
    db.update_signal_outcome(sig_id, price_t4h=4540.0, price_t1d=4550.0)
    print(f"\n[4] Outcome guncellendi")

    # Test 5: Hit rate
    hit = db.get_hit_rate("ES", window=30)
    print(f"\n[5] Isabet orani: {hit}")

    # Test 6: Stats
    stats = db.get_stats()
    print(f"\n[6] Toplam sinyal: {stats['total_signals']}")
    print(f"    Urun dagilimi: {stats['by_product']}")

    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)