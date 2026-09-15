"""
CTA ERHAN TERMİNALİ — Nitter Fetch Script
==========================================
Nitter RSS üzerinden X (Twitter) hesaplarından tweet çeker.
- 29 hesap için fallback instance listesi
- Tweet ID deduplication (last_run.json)
- JSON commit formatı
- 0 TL — tamamen ücretsiz
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

# ============================================================
# AYARLAR
# ============================================================

# Başlangıç için 3 hesap (test)
# İleride 29 hesaba çıkaracağız
TARGET_ACCOUNTS = [
    "wayneterprises",
    "PeterLBrandt",
    "MacroAlf",
]

# Nitter instance'ları (fallback için)
# Biri çalışmazsa sırayla diğerlerini dener
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://shitter.thepixora.com",
    "https://nitter.kareem.one",
    "https://nitter.miningtcup.me",
    "https://nitter.meowing.monster",
    "https://nitter.xitter.cc",
    "https://nitter.jaydenha.uk",
    "https://nitter.click",
    "https://x.n0g.xyz",
    "https://tw.eir-nya.gay",
]

# Veri klasörleri
DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
RAW_DIR = DATA_DIR / "raw"
STATE_FILE = DATA_DIR / "last_run.json"

# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def ensure_dirs():
    """Klasörleri oluştur"""
    TWEETS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    """Son çekim bilgisini yükle"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    """Son çekim bilgisini kaydet"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_working_instance() -> str:
    """Çalışan Nitter instance'ını bul"""
    for instance in NITTER_INSTANCES:
        try:
            response = requests.get(
                f"{instance}/wayneterprises/rss",
                timeout=8,
                headers={"User-Agent": "Mozilla/5.0 (CTA-Erhan-Terminal)"},
            )
            if response.status_code == 200 and len(response.content) > 500:
                print(f"[OK] Çalışan instance: {instance}")
                return instance
        except Exception as e:
            print(f"[SKIP] {instance} çalışmıyor: {e}")
            continue
    raise Exception("Hiçbir Nitter instance çalışmıyor!")


def fetch_rss(instance: str, username: str) -> list:
    """Bir hesabın RSS'ini çek"""
    url = f"{instance}/{username}/rss"
    print(f"[FETCH] {url}")

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (CTA-Erhan-Terminal)"},
        )
        if response.status_code != 200:
            print(f"[FAIL] HTTP {response.status_code}")
            return []

        feed = feedparser.parse(response.content)
        tweets = []

        for entry in feed.entries:
            tweet = {
                "id": extract_tweet_id(entry.get("id", "")),
                "username": username,
                "text": entry.get("title", ""),
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
            tweets.append(tweet)

        print(f"[OK] {username}: {len(tweets)} tweet")
        return tweets

    except Exception as e:
        print(f"[ERR] {username}: {e}")
        return []


def extract_tweet_id(url_or_id: str) -> str:
    """Tweet URL'sinden ID çıkar"""
    if not url_or_id:
        return ""
    # Nitter URL formatı: https://nitter.net/user/status/123456789
    if "/status/" in url_or_id:
        parts = url_or_id.split("/status/")
        if len(parts) > 1:
            return parts[1].split("#")[0].split("?")[0]
    return url_or_id


def get_processed_ids(username: str, state: dict) -> set:
    """Daha önce işlenmiş tweet ID'lerini al"""
    return set(state.get(username, {}).get("processed_ids", []))


def update_state(username: str, new_ids: list, state: dict):
    """State'i güncelle"""
    if username not in state:
        state[username] = {"processed_ids": []}

    existing = set(state[username]["processed_ids"])
    existing.update(new_ids)

    # Son 500 ID'yi tut (sınırsız büyümesin)
    state[username]["processed_ids"] = list(existing)[-500:]
    state[username]["last_update"] = datetime.now(timezone.utc).isoformat()


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — Nitter Fetch")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    ensure_dirs()
    state = load_state()

    # Çalışan instance bul
    try:
        instance = get_working_instance()
    except Exception as e:
        print(f"[FATAL] {e}")
        return

    all_new_tweets = []
    total_fetched = 0
    total_new = 0

    # Her hesabı çek
    for username in TARGET_ACCOUNTS:
        tweets = fetch_rss(instance, username)
        total_fetched += len(tweets)

        processed_ids = get_processed_ids(username, state)
        new_tweets = [t for t in tweets if t["id"] and t["id"] not in processed_ids]

        if new_tweets:
            all_new_tweets.extend(new_tweets)
            update_state(username, [t["id"] for t in new_tweets], state)
            total_new += len(new_tweets)
            print(f"[NEW] {username}: {len(new_tweets)} yeni tweet")
        else:
            print(f"[SAME] {username}: yeni tweet yok")

        time.sleep(1)  # Rate limit için bekle

    # State kaydet
    save_state(state)

    # Yeni tweet varsa JSON'a yaz
    if all_new_tweets:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = TWEETS_DIR / f"tweets_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_new_tweets, f, ensure_ascii=False, indent=2)

        print(f"[SAVE] {output_file}: {len(all_new_tweets)} tweet")

    # Özet
    print("=" * 60)
    print(f"Toplam çekilen: {total_fetched}")
    print(f"Yeni: {total_new}")
    print(f"Instance: {instance}")
    print("=" * 60)


if __name__ == "__main__":
    main()
