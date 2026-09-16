"""
CTA ERHAN TERMİNALİ — RSS Fetcher
====================================
Tickmill blog RSS feed'ini okur.
Ham veriyi (İngilizce) JSON'a kaydeder.
Çeviri ayrı adımda yapılır (translate_rss.py).
"""

import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from html import unescape
import re

import feedparser

# ============================================================
# AYARLAR
# ============================================================

RSS_FEEDS = [
    {
        "name": "Tickmill",
        "url": "https://www.tickmill.com/blog/rss/feed.xml",
        "language": "en",
    },
]

DATA_DIR = Path("data")
RSS_DIR = DATA_DIR / "rss"
STATE_FILE = DATA_DIR / "rss_state.json"


# ============================================================
# YARDIMCI
# ============================================================

def ensure_dirs():
    RSS_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================================================
# RSS ÇEKME
# ============================================================

def fetch_feed(feed_info: dict) -> list:
    url = feed_info["url"]
    name = feed_info["name"]
    lang = feed_info["language"]

    print(f"[FETCH] {name} → {url}")

    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            article_id = entry.get("id") or entry.get("link", "")
            if not article_id:
                continue

            # Tarih
            published = entry.get("published", "")

            article = {
                "id": article_id,
                "source": name,
                "source_type": "RSS",
                "language_original": lang,
                "language_display": "tr",
                "title_en": clean_text(entry.get("title", "")),
                "title_tr": "",  # Çeviri sonra eklenecek
                "content_en": clean_text(entry.get("summary", "")),
                "content_tr": "",  # Çeviri sonra eklenecek
                "url": entry.get("link", ""),
                "published_at": published,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "translation_hash": "",  # Cache için
            }
            articles.append(article)

        print(f"[OK] {name}: {len(articles)} makale")
        return articles

    except Exception as e:
        print(f"[ERR] {name}: {type(e).__name__}: {e}")
        return []


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — RSS Fetcher")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    ensure_dirs()
    state = load_state()

    all_articles = []
    total_new = 0

    for feed_info in RSS_FEEDS:
        articles = fetch_feed(feed_info)

        # Daha önce işlenmiş ID'leri al
        feed_key = feed_info["name"]
        processed = set(state.get(feed_key, {}).get("processed_ids", []))

        # Yeni olanları filtrele
        new_articles = [a for a in articles if a["id"] not in processed]

        if new_articles:
            all_articles.extend(new_articles)
            new_ids = [a["id"] for a in new_articles]
            state.setdefault(feed_key, {})["processed_ids"] = list(
                processed | set(new_ids)
            )[-1000:]
            state[feed_key]["last_update"] = datetime.now(timezone.utc).isoformat()
            total_new += len(new_articles)
            print(f"[NEW] {feed_key}: {len(new_articles)} yeni makale")
        else:
            print(f"[SAME] {feed_key}: yeni makale yok")

    # State kaydet
    save_state(state)

    # Yeni makale varsa JSON'a kaydet
    if all_articles:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = RSS_DIR / f"rss_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)

        print(f"[SAVE] {output_file}: {len(all_articles)} makale")

    # Özet
    print("=" * 60)
    print(f"Toplam yeni: {total_new}")
    print("=" * 60)


if __name__ == "__main__":
    main()
