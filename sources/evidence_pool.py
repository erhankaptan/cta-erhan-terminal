# sources/evidence_pool.py
from __future__ import annotations
import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

class EvidencePool:
    _instance: Optional["EvidencePool"] = None

    def __new__(cls, db_path: str | Path | None = None) -> "EvidencePool":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: str | Path | None = None) -> None:
        if getattr(self, "_initialized", False):
            return
        
        # Doğrudan senin masaüstündeki tam mutlak yolunu sabitliyoruz
        PROJECT_ROOT = Path(r"C:\Users\erhan\Desktop\CTA ERHAN PYTHON DOSYASI\erhan_proje\erhan")
        DATA_DIR = PROJECT_ROOT / "data"
        default_db = DATA_DIR / "evidence.db"
        
        self.db_path = Path(db_path or default_db).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._initialize_database()
        self._initialized = True

    def _connection(self):
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=30.0,
            check_same_thread=False,
        )
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _initialize_database(self) -> None:
        with self._connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evidence (
                    evidence_id TEXT PRIMARY KEY,
                    product TEXT,
                    source_id TEXT,
                    source_type TEXT,
                    publisher TEXT,
                    author TEXT,
                    published_at TEXT,
                    ingested_at TEXT,
                    title TEXT,
                    content TEXT NOT NULL,
                    canonical_url TEXT,
                    metadata_json TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_evidence_product
                ON evidence(product)
            """)
            conn.commit()

    def add_evidence(self, record: Dict[str, Any]) -> None:
        evidence_id = record.get("evidence_id") or f"REC_{datetime.now(timezone.utc).timestamp()}"
        product = record.get("product", "UNKNOWN").upper().strip()
        
        if "ingested_at" not in record:
            record["ingested_at"] = datetime.now(timezone.utc).isoformat()

        with self._connection() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO evidence (
                    evidence_id, product, source_id, source_type, publisher,
                    author, published_at, ingested_at, title, content,
                    canonical_url, metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                evidence_id,
                product,
                record.get("source_id"),
                record.get("source_type"),
                record.get("publisher"),
                record.get("author"),
                record.get("published_at"),
                record.get("ingested_at"),
                record.get("title"),
                record.get("content", ""),
                record.get("canonical_url"),
                json.dumps(record.get("metadata", {}), ensure_ascii=False),
            ))
            conn.commit()

    def get_evidence_for_product(self, product: str) -> List[Dict[str, Any]]:
        product = product.upper().strip()
        with self._connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT *
                FROM evidence
                WHERE product = ?
                ORDER BY published_at DESC
            """, (product,)).fetchall()

        results = []
        for row in rows:
            d = dict(row)
            if d.get("metadata_json"):
                try:
                    d["metadata"] = json.loads(d["metadata_json"])
                except Exception:
                    d["metadata"] = {}
            results.append(d)
        return results

    def get_all(self, product: str) -> List[Dict[str, Any]]:
        return self.get_evidence_for_product(product)

    def count(self, product: str | None = None) -> int:
        with self._connection() as connection:
            if product is None:
                row = connection.execute("SELECT COUNT(*) FROM evidence").fetchone()
            else:
                row = connection.execute(
                    "SELECT COUNT(*) FROM evidence WHERE product = ?",
                    (product.upper().strip(),),
                ).fetchone()
        return int(row[0])

global_evidence_pool = EvidencePool()