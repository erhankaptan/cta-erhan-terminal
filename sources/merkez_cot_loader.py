# sources/merkez_cot_loader.py
"""MERKEZ cme_cot_raw_export.json'u okuyup CTA ERHAN evidence.db'sine yazar."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

from sources.evidence_pool import global_evidence_pool
from sources.cot_interpreter import interpret

MERKEZ_EXPORT = Path(r"C:\cta_terminal\cme_cot_raw_export.json")


def _stable_evidence_id(product: str, as_of_date: str) -> str:
    base = f"merkez_cot|{product}|{as_of_date}"
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:24]
    return f"EV_MERKEZ_COT_{digest}"


def _safe_get(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d:
            return d[k]
    return default


def load_merkez_snapshot(path=None) -> int:
    src = Path(path) if path else MERKEZ_EXPORT
    if not src.is_file():
        print(f"[MERKEZ_COT] Dosya yok: {src}")
        return 0

    with src.open("r", encoding="utf-8") as f:
        export = json.load(f)

    symbols = export.get("symbols", {})
    if not symbols:
        print("[MERKEZ_COT] symbols bos.")
        return 0

    added = 0
    total = 0

    for code, entry in symbols.items():
        observations = entry.get("weekly_observations", [])
        if not observations:
            continue
        obs = observations[0]

        as_of = obs.get("as_of_date") or entry.get("as_of_date") or ""
        categories = obs.get("categories", {})
        oi = _safe_get(obs, "open_interest", default=entry.get("open_interest"))
        report_type = entry.get("report_type", "TFF")
        market_name = entry.get("market_and_exchange_names", "")

        interp = interpret(categories, report_type=report_type)

        lines = [f"CFTC {report_type} | {code} | {as_of}"]
        if market_name:
            lines.append(f"Market: {market_name}")
        lines.append(f"Open Interest: {oi}")
        for cat_name, cat in categories.items():
            lines.append(f"  {cat_name}: L={cat.get('long')} S={cat.get('short')} Net={cat.get('net')}")
        lines.append(f"Yon: {interp['cot_yon']} | Momentum: {interp['momentum']} | Konsensus: {interp['consensus']}")
        lines.append(f"Non-Reportable: {interp['non_reportable']}")
        content = "\n".join(lines)

        primary_data = categories.get("LEVERAGED_FUNDS") or categories.get("MANAGED_MONEY") or {}

        metadata = {
            "report_date": as_of,
            "report_type": report_type,
            "market": market_name,
            "open_interest": oi,
            "categories": categories,
            "interpreter": interp,
            "cta_proxy": {
                "long": primary_data.get("long", 0),
                "short": primary_data.get("short", 0),
                "net": interp["net_by_category"].get(interp["primary_category"], 0),
                "change_net": interp["change_by_category"].get(interp["primary_category"], 0),
            },
            "provenance": {
                "publisher": "CFTC",
                "via": "MERKEZ_KAYNAK",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        }
        _write_to_evidences_table(code, as_of, report_type, market_name, categories, interp, content, oi)
        record = {
            "evidence_id": _stable_evidence_id(code, as_of),
            "product": code.upper().strip(),
            "source_id": "SRC_COT_MERKEZ",
            "source_type": "COT",
            "publisher": "CFTC",
            "author": "",
            "published_at": as_of,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "title": f"CFTC COT (MERKEZ) | {code} | {as_of}",
            "content": content,
            "canonical_url": "https://publicreporting.cftc.gov/",
            "metadata": metadata,
        }

        total += 1
        before = global_evidence_pool.count(code)
        global_evidence_pool.add_evidence(record)
        after = global_evidence_pool.count(code)
        if after > before:
            added += 1

    print(f"[MERKEZ_COT] Islendi: {total} urun | Yeni: {added}")
    return added


if __name__ == "__main__":
    load_merkez_snapshot()


def _write_to_evidences_table(code, as_of, report_type, market_name, categories, interp, content, oi):
    """Radar (synthesis) icin evidences tablosuna da yaz."""
    import sqlite3
    db_path = Path(r"C:\Users\erhan\Desktop\CTA ERHAN PYTHON DOSYASI\erhan_proje\erhan\data\evidence.db")
    signal = interp.get("primary_signal", "NEUTRAL")
    if "BULLISH" in signal:
        direction = "BULLISH"
    elif "BEARISH" in signal:
        direction = "BEARISH"
    else:
        direction = "NEUTRAL"

    net = interp.get("net_by_category", {}).get(interp.get("primary_category", ""), 0)
    ev_id = f"merkez_cot_{code}_{as_of}".replace("-", "_")
    claim = f"{report_type} {code}: {interp.get('primary_category')} net={net}"

    conn = sqlite3.connect(str(db_path))
    try:
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
            INSERT OR REPLACE INTO evidences (
                evidence_id, source_type, source_name, source_document_id,
                asset_code, direction, claim_text, supporting_text,
                published_at, ingested_at, extraction_confidence, source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ev_id, "COT", "CFTC COT (MERKEZ)", as_of, code,
            direction, claim, content[:500], as_of,
            datetime.now(timezone.utc).isoformat(), 0.9,
            "https://publicreporting.cftc.gov/",
        ))
        conn.commit()
    finally:
        conn.close()