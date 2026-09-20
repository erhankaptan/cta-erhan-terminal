# sources/ingestion.py
from datetime import datetime, timezone
import hashlib
from sources.evidence_pool import global_evidence_pool

try:
    from sources.normalization import normalize
except ImportError:
    def normalize(x):
        return x

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

# --- COT adapter ---
try:
    from sources.adapters.cftc_cot import (
        fetch_cftc_cot,
        normalize_cot,
        should_fetch_cot,
    )
    COT_AVAILABLE = True
except ImportError as _e:
    COT_AVAILABLE = False
    _COT_IMPORT_ERROR = str(_e)


# ============================================================
# ÜRÜN LİSTESİ (tüm kaynaklar için ortak)
# ============================================================
TUM_URUNLER = [
    "ES", "MES", "NQ", "MNQ", "RTY", "YM",
    "CL", "MCL", "NG",
    "GC", "MGC", "SI", "HG", "PL",
    "6E", "6J", "6B", "6A", "6C", "6S",
    "ZC", "ZS", "ZW", "ZL", "ZM",
]


SOURCES_REGISTRY = [
    # -------------------- X (API key yok → UNAVAILABLE) --------------------
    {
        "source_id": "SRC_X_001",
        "source_name": "Macro & Futures Feed X",
        "source_type": "X",
        "organization": "Primary Channel",
        "account": "@MacroTerminal_Example",
        "canonical_url": "https://x.com/MacroTerminal_Example",
        "access_method": "X_API_V2_POLL",
        "product_scope": ["ES", "NQ", "CL", "GC"],
        "topic_scope": ["macro", "futures", "liquidity"],
        "priority": 1,
        "poll_interval_minutes": 60,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    # -------------------- RSS / Haber (GERÇEK) --------------------
    {
        "source_id": "SRC_RSS_FED",
        "source_name": "Federal Reserve Press Releases",
        "source_type": "RSS",
        "organization": "Federal Reserve",
        "canonical_url": "https://www.federalreserve.gov/feeds/press_all.xml",
        "access_method": "RSS_ATOM",
        "product_scope": TUM_URUNLER,
        "topic_scope": ["rates", "central_banks", "macro"],
        "priority": 1,
        "poll_interval_minutes": 60,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    {
        "source_id": "SRC_RSS_CME_REFDATA",
        "source_name": "CME Reference Data Notices",
        "source_type": "RSS",
        "organization": "CME Group",
        "canonical_url": "https://www.cmegroup.com/rss/cme-reference-data-feed.rss",
        "access_method": "RSS_ATOM",
        "product_scope": TUM_URUNLER,
        "topic_scope": ["reference_data", "futures", "markets"],
        "priority": 1,
        "poll_interval_minutes": 60,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    {
        "source_id": "SRC_RSS_CME_GLOBEX",
        "source_name": "CME Globex Advisories",
        "source_type": "RSS",
        "organization": "CME Group",
        "canonical_url": "https://feeds.feedburner.com/GlobexAdvisories",
        "access_method": "RSS_ATOM",
        "product_scope": TUM_URUNLER,
        "topic_scope": ["globex", "operations", "markets"],
        "priority": 1,
        "poll_interval_minutes": 60,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    {
        "source_id": "SRC_RSS_CME_CLEARING",
        "source_name": "CME Clearing Advisories",
        "source_type": "RSS",
        "organization": "CME Group",
        "canonical_url": "https://feeds.feedburner.com/ClearingAdvisories",
        "access_method": "RSS_ATOM",
        "product_scope": TUM_URUNLER,
        "topic_scope": ["clearing", "operations", "markets"],
        "priority": 1,
        "poll_interval_minutes": 60,
        "enabled": True,
        "verification_status": "VERIFIED",
    },
    # -------------------- CFTC COT / TFF (GERÇEK) --------------------
    {
        "source_id": "SRC_COT_CFTC",
        "source_name": "CFTC Commitments of Traders (TFF)",
        "source_type": "COT",
        "organization": "CFTC",
        "canonical_url": "https://publicreporting.cftc.gov/resource/gpe5-46if.json",
        "access_method": "SOCRATA_API",
        "product_scope": TUM_URUNLER,
        "topic_scope": ["cot", "positioning", "cta_proxy"],
        "priority": 1,
        "poll_interval_minutes": 10080,  # haftada 1
        "enabled": True,
        "verification_status": "VERIFIED",
    },
]


def make_stable_evidence_id(source_id: str, content: str, url: str | None = None) -> str:
    base = f"{source_id}|{(url or '').strip()}|{content.strip()[:800]}"
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:24]
    return f"EV_{digest}"


def fetch_rss_entries(source: dict) -> list[dict]:
    """Gerçek RSS çekimi. Başarısız olursa boş liste döner."""
    if not FEEDPARSER_AVAILABLE:
        return []

    url = source.get("canonical_url")
    if not url:
        return []

    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            return []

        results = []
        for entry in feed.entries[:15]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            published = entry.get("published", entry.get("updated", ""))

            content = f"{title}\n\n{summary}".strip()
            if not content:
                continue

            results.append({
                "title": title,
                "content": content,
                "canonical_url": link or url,
                "published_at": published,
                "source_id": source.get("source_id"),
                "source_type": "RSS",
                "publisher": source.get("organization") or source.get("source_name"),
                "author": entry.get("author", ""),
            })
        return results
    except Exception:
        return []


def fetch_raw_data_from_source(source: dict, product_code: str) -> list[dict] | None:
    source_type = source.get("source_type", "").upper()

    if source_type == "RSS":
        entries = fetch_rss_entries(source)
        if not entries:
            return None
        return entries

    if source_type == "COT":
        if not COT_AVAILABLE:
            print(f"[COT] adapter yüklenemedi: {_COT_IMPORT_ERROR}")
            return None
        raw = fetch_cftc_cot(product_code)
        if not raw:
            return None
        return [normalize_cot(item, product_code) for item in raw]

    # X, Institutional, PDF → henüz gerçek erişim yok
    return None


def run_ingestion_pipelineForProduct(product_code: str) -> dict:
    product_code = product_code.upper().strip()
    added = 0
    skipped = 0
    unavailable = 0

    for source in SOURCES_REGISTRY:
        if not source.get("enabled", True):
            continue

        scopes = source.get("product_scope", [])
        if product_code not in scopes and scopes:
            continue

        if source.get("source_type", "").upper() == "COT":
            if COT_AVAILABLE and not should_fetch_cot(product_code, global_evidence_pool):
                continue

        raw_items = fetch_raw_data_from_source(source, product_code)

        if raw_items is None:
            unavailable += 1
            continue

        if not isinstance(raw_items, list):
            raw_items = [raw_items]

        for raw_data in raw_items:
            if source.get("source_type", "").upper() == "COT":
                normalized_record = dict(raw_data)
            else:
                try:
                    normalized_record = normalize(raw_data)
                except Exception:
                    normalized_record = None

                if not isinstance(normalized_record, dict):
                    normalized_record = dict(raw_data)

            normalized_record["product"] = product_code
            normalized_record["source_id"] = (
                normalized_record.get("source_id")
                or source.get("source_id")
            )
            normalized_record["source_type"] = source.get("source_type")
            normalized_record["publisher"] = (
                normalized_record.get("publisher")
                or source.get("organization")
                or source.get("source_name")
            )
            normalized_record["canonical_url"] = (
                normalized_record.get("canonical_url")
                or source.get("canonical_url")
            )
            normalized_record["ingested_at"] = datetime.now(timezone.utc).isoformat()

            content = normalized_record.get("content") or ""
            url = normalized_record.get("canonical_url")

            if not normalized_record.get("evidence_id"):
                evidence_id = make_stable_evidence_id(
                    source_id=source.get("source_id", "UNKNOWN"),
                    content=f"{product_code}|{content}",   # ← product_code prefix
                    url=url,
                )
                normalized_record["evidence_id"] = evidence_id

            before = global_evidence_pool.count(product_code)
            global_evidence_pool.add_evidence(normalized_record)
            after = global_evidence_pool.count(product_code)

            if after > before:
                added += 1
            else:
                skipped += 1

    return {
        "product": product_code,
        "added": added,
        "skipped_duplicates": skipped,
        "unavailable_sources": unavailable,
        "total_in_pool": global_evidence_pool.count(product_code),
    }