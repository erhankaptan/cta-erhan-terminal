"""
CTA ERHAN TERMİNALİ — Build Evidence Pool (v2)
================================================
X analizleri + RSS (varliklar) + COT → evidence havuzu.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from core.evidence_models import (
    Evidence,
    create_evidence_id,
    now_utc_iso,
)
from core.evidence_repository import EvidenceRepository


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
RSS_DIR = DATA_DIR / "rss"
COT_DB = DATA_DIR / "evidence.db"
NEW_DB = DATA_DIR / "evidence_pool.db"


# ============================================================
# YÖN DÖNÜŞTÜRME
# ============================================================

def normalize_direction(raw: str) -> str:
    if not raw:
        return "UNKNOWN"
    r = str(raw).upper().strip()
    if r in ("YUKARI", "YÜKSELİŞ", "BULLISH", "LONG", "AL", "ALIM"):
        return "BULLISH"
    if r in ("AŞAĞI", "DÜŞÜŞ", "BEARISH", "SHORT", "SAT", "SATIM"):
        return "BEARISH"
    if r in ("NÖTR", "NOTR", "NEUTRAL", "YATAY"):
        return "NEUTRAL"
    return "UNKNOWN"


# ============================================================
# X TWEET → EVIDENCE
# ============================================================

def analysis_to_evidences(analysis_data: Dict) -> List[Evidence]:
    tweet_id = (
        analysis_data.get("tweet_id")
        or analysis_data.get("id")
        or analysis_data.get("tweet_url", "").split("/")[-1]
        or ""
    )
    username = analysis_data.get("username", "")
    text = analysis_data.get("text", "")
    analyzed_at = analysis_data.get("analyzed_at", now_utc_iso())
    ozet = analysis_data.get("ozet", "")
    varliklar = analysis_data.get("varliklar", []) or []

    if not varliklar:
        return []

    evidences = []
    for idx, v in enumerate(varliklar):
        sembol = (v.get("sembol") or "").upper().strip()
        if not sembol:
            continue

        direction = normalize_direction(v.get("yon", ""))
        if direction == "UNKNOWN":
            continue

        # tweet_id boşsa idx ile ayır
        doc_id = tweet_id if tweet_id else f"{username}_{analyzed_at}_{idx}"
        ev_id = create_evidence_id("X", doc_id, sembol)

        source_url = ""
        if tweet_id and username:
            source_url = f"https://x.com/{username}/status/{tweet_id}"

        isim = v.get("isim", sembol)
        gerekce = v.get("gerekce", "")
        claim = f"{isim} ({sembol}) — {direction}"
        supporting = gerekce or ozet or text[:200]

        try:
            conf = float(v.get("skor", 0.75))
            if conf > 1:
                conf = conf / 100.0
        except Exception:
            conf = 0.75

        evidences.append(Evidence(
            evidence_id=ev_id,
            source_type="X",
            source_name=f"@{username}" if username else "X",
            source_document_id=doc_id,
            asset_code=sembol,
            direction=direction,
            claim_text=claim,
            supporting_text=supporting,
            published_at=analyzed_at,
            ingested_at=now_utc_iso(),
            extraction_confidence=conf,
            source_url=source_url or None,
        ))

    return evidences


# ============================================================
# RSS MAKALE → EVIDENCE (varliklar'dan)
# ============================================================

def rss_to_evidences(rss_data: Dict) -> List[Evidence]:
    rss_id = rss_data.get("id") or rss_data.get("guid") or ""
    title_tr = (rss_data.get("title_tr") or "").strip()
    title_en = (rss_data.get("title_en") or rss_data.get("title") or "").strip()
    content_tr = (rss_data.get("content_tr") or "").strip()
    content_en = (rss_data.get("content_en") or rss_data.get("content") or "").strip()
    published_at = rss_data.get("published_at", "") or now_utc_iso()
    url = rss_data.get("url", "")
    varliklar = rss_data.get("varliklar", []) or []

    if not rss_id:
        rss_id = f"rss_{hash(title_tr or title_en)}"

    display_title = title_tr or title_en or rss_id
    evidences = []

    # varliklar varsa → yönlü evidence
    if varliklar:
        for idx, v in enumerate(varliklar):
            sembol = (v.get("sembol") or "").upper().strip()
            if not sembol:
                continue
            direction = normalize_direction(v.get("yon", ""))
            if direction == "UNKNOWN":
                continue

            ev_id = create_evidence_id("RSS", f"{rss_id}_{idx}", sembol)

            isim = v.get("isim", sembol)
            gerekce = v.get("gerekce", "")
            claim = f"{isim} ({sembol}) — Tickmill: {direction}"
            supporting = gerekce or (content_tr or content_en)[:300]

            try:
                conf = float(v.get("skor", 0.7))
                if conf > 1:
                    conf = conf / 100.0
            except Exception:
                conf = 0.7

            evidences.append(Evidence(
                evidence_id=ev_id,
                source_type="RSS",
                source_name="Tickmill",
                source_document_id=rss_id,
                asset_code=sembol,
                direction=direction,
                claim_text=claim,
                supporting_text=supporting,
                published_at=published_at,
                ingested_at=now_utc_iso(),
                extraction_confidence=conf,
                source_url=url or None,
            ))

    return evidences


# ============================================================
# COT → EVIDENCE
# ============================================================

def cot_to_evidences(cot_db_path: Path) -> List[Evidence]:
    if not cot_db_path.exists():
        print(f"  [SKIP] COT DB yok: {cot_db_path}")
        return []

    evidences = []
    try:
        with sqlite3.connect(str(cot_db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM evidence WHERE source_type = 'COT' OR source_type IS NULL"
            ).fetchall()

            for row in rows:
                d = dict(row)
                product = (d.get("product") or "").upper().strip()
                if not product:
                    continue

                metadata = {}
                try:
                    if d.get("metadata_json"):
                        metadata = json.loads(d["metadata_json"])
                except Exception:
                    metadata = {}

                direction = "NEUTRAL"
                cta_proxy = metadata.get("cta_proxy", {}) or {}
                cta_net = cta_proxy.get("net", 0) or 0
                if cta_net > 0:
                    direction = "BULLISH"
                elif cta_net < 0:
                    direction = "BEARISH"

                source_id = d.get("source_id", "")
                evidence_id_orig = d.get("evidence_id", "")
                ev_id = create_evidence_id("COT", evidence_id_orig or product, product)

                evidences.append(Evidence(
                    evidence_id=ev_id,
                    source_type="COT",
                    source_name=d.get("publisher", "CFTC COT"),
                    source_document_id=evidence_id_orig or source_id or product,
                    asset_code=product,
                    direction=direction,
                    claim_text=d.get("title", "") or f"COT {product}",
                    supporting_text=(d.get("content", "") or "")[:500],
                    published_at=d.get("published_at", "") or now_utc_iso(),
                    ingested_at=now_utc_iso(),
                    extraction_confidence=0.98,
                    source_url=d.get("canonical_url"),
                ))
    except Exception as e:
        print(f"  [ERR] COT DB okunamadı: {e}")

    return evidences


# ============================================================
# JSON OKU
# ============================================================

def load_json_files(folder: Path, pattern: str) -> List[Dict]:
    if not folder.exists():
        return []
    all_items = []
    for fp in sorted(folder.glob(pattern)):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                all_items.extend(data)
            elif isinstance(data, dict):
                all_items.append(data)
        except Exception:
            continue
    return all_items


# ============================================================
# ANA
# ============================================================

def main():
    print("=" * 60)
    print("Build Evidence Pool (v2)")
    print(f"Zaman: {now_utc_iso()}")
    print("=" * 60)

    if NEW_DB.exists():
        NEW_DB.unlink()
        print(f"[CLEAN] Eski havuz silindi")

    repo = EvidenceRepository(str(NEW_DB))
    print(f"[DB] {NEW_DB}")

    print("\n[1/4] X analiz edilenler...")
    analyses = load_json_files(ANALYSIS_DIR, "analysis_*.json")
    print(f"      {len(analyses)} analiz yüklendi")
    x_evidences = []
    for a in analyses:
        x_evidences.extend(analysis_to_evidences(a))
    print(f"      {len(x_evidences)} X evidence")

    print("\n[2/4] RSS makaleleri...")
    rss_items = load_json_files(RSS_DIR, "rss_*.json")
    print(f"      {len(rss_items)} makale yüklendi")
    rss_evidences = []
    for r in rss_items:
        rss_evidences.extend(rss_to_evidences(r))
    print(f"      {len(rss_evidences)} RSS evidence")

    print("\n[3/4] COT verisi...")
    cot_evidences = cot_to_evidences(COT_DB)
    print(f"      {len(cot_evidences)} COT evidence")

    print("\n[4/4] Kaydediliyor...")
    all_evidences = x_evidences + rss_evidences + cot_evidences
    print(f"      Toplam: {len(all_evidences)}")
    result = repo.save_many(all_evidences)
    print(f"      Yeni: {result['new']}, Dup: {result['skipped']}, Hata: {result['errors']}")

    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"Toplam kanıt: {repo.count()}")
    print("Kaynak bazlı:")
    for src, cnt in repo.count_by_source_type().items():
        print(f"  {src}: {cnt}")
    print("\nAsset bazlı (ilk 15):")
    for asset, cnt in list(repo.count_by_asset().items())[:15]:
        print(f"  {asset}: {cnt}")
    print("=" * 60)


if __name__ == "__main__":
    main()