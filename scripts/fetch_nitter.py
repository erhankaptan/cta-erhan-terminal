"""
CTA ERHAN TERMİNALİ — Nitter Fetch Script v2
==========================================
Nitter RSS üzerinden X (Twitter) hesaplarından tweet çeker.
- 10 instance fallback
- XML parse (feedparser yerine xml.etree)
- Tweet ID deduplication (last_run.json)
- 0 TL — tamamen ücretsiz
"""

import os
import json
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from html import unescape

import requests
import xml.etree.ElementTree as ET

# ============================================================
# AYARLAR
# ============================================================

TARGET_ACCOUNTS = [
    # Kişisel (7)
    "wayneterprises",
    "stenodata",
    "LynAldenContact",
    "MacroAlf",
    "biancoresearch",
    "CrossBorderCap",
    "MikeZaccardi",   
    "JuanJesusMontoy",
    # Kurumsal (1)
    "Nomura",
    # Haber (5)
    "zerohedge",
    "MacroCompass",
    "TheTerminal",
    "Hedgeye",
    "Tickmill",
    # Chart (3)
    "jam_croissant",
    "topdowncharts",
    "MacroRiskAdvisory",
    # CTA Uzman (13)
    "rcmAlts",
    "MacroOps",
    "rjpjr12",
    "PeterLBrandt",
    "LindaRaschke",
    "AnthonyCrudele",
    "FuturesTrader71",
    "CommodMkt",
    "tracyalloway",
    "misterpuertas",
    "TheStalwart",
    "AttainCap2",
    "JPokoTrades",
]

NITTER_INSTANCES = [
    "https://nitter.meowing.monster",
    "https://nitter.kareem.one",
    "https://nitter.miningtcup.me",
    "https://shitter.thepixora.com",
    "https://nitter.xitter.cc",
    "https://nitter.jaydenha.uk",
    "https://nitter.click",
    "https://x.n0g.xyz",
    "https://tw.eir-nya.gay",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
]

DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
STATE_FILE = DATA_DIR / "last_run.json"

# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def ensure_dirs():
    TWEETS_DIR.mkdir(parents=True, exist_ok=True)


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


def get_working_instance() -> str:
    for instance in NITTER_INSTANCES:
        try:
            url = f"{instance}/wayneterprises/rss"
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0 (CTA-Erhan-Terminal)"},
            )
            if response.status_code == 200 and b"<rss" in response.content[:500]:
                try:
                    root = ET.fromstring(response.content)
                    items = root.findall(".//item")
                    if len(items) > 0:
                        print(f"[OK] Çalışan instance: {instance} ({len(items)} item)")
                        return instance
                    else:
                        print(f"[SKIP] {instance} çalışıyor ama 0 tweet")
                except ET.ParseError:
                    print(f"[SKIP] {instance} XML parse edilemedi")
        except Exception as e:
            print(f"[SKIP] {instance} hata: {type(e).__name__}")
            continue
    raise Exception("Hiçbir Nitter instance çalışmıyor!")


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_images(description: str) -> list:
    if not description:
        return []
    urls = re.findall(r'<img\s+src="([^"]+)"', description)
    return [url for url in urls if url]


def fetch_rss(instance: str, username: str) -> list:
    url = f"{instance}/{username}/rss"
    print(f"[FETCH] {url}")

    try:
        response = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0 (CTA-Erhan-Terminal)"},
        )

        if response.status_code != 200:
            print(f"[FAIL] HTTP {response.status_code}")
            return []

        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        tweets = []
        for item in items:
            title_elem = item.find("title")
            title = title_elem.text if title_elem is not None else ""

            guid_elem = item.find("guid")
            guid = guid_elem.text if guid_elem is not None else ""

            pubdate_elem = item.find("pubDate")
            pub_date = pubdate_elem.text if pubdate_elem is not None else ""

            link_elem = item.find("link")
            link = link_elem.text if link_elem is not None else ""

            desc_elem = item.find("description")
            description = desc_elem.text if desc_elem is not None else ""

            images = extract_images(description)

            tweet = {
                "id": guid,
                "username": username,
                "text": clean_text(title),
                "url": link,
                "published": pub_date,
                "images": images,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
            tweets.append(tweet)

        print(f"[OK] {username}: {len(tweets)} tweet")
        return tweets

    except ET.ParseError as e:
        print(f"[ERR] {username} XML parse: {e}")
        return []
    except Exception as e:
        print(f"[ERR] {username}: {type(e).__name__}: {e}")
        return []


def get_processed_ids(username: str, state: dict) -> set:
    return set(state.get(username, {}).get("processed_ids", []))


def update_state(username: str, new_ids: list, state: dict):
    if username not in state:
        state[username] = {"processed_ids": []}

    existing = set(state[username]["processed_ids"])
    existing.update(new_ids)

    state[username]["processed_ids"] = list(existing)[-500:]
    state[username]["last_update"] = datetime.now(timezone.utc).isoformat()


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — Nitter Fetch v2")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    ensure_dirs()
    state = load_state()

    try:
        instance = get_working_instance()
    except Exception as e:
        print(f"[FATAL] {e}")
        return

    all_new_tweets = []
    total_fetched = 0
    total_new = 0

    for username in TARGET_ACCOUNTS:
        tweets = fetch_rss(instance, username)
        total_fetched += len(tweets)

        if not tweets:
            time.sleep(1)
            continue

        processed_ids = get_processed_ids(username, state)
        new_tweets = [t for t in tweets if t["id"] and t["id"] not in processed_ids]

        if new_tweets:
            all_new_tweets.extend(new_tweets)
            update_state(username, [t["id"] for t in new_tweets], state)
            total_new += len(new_tweets)
            print(f"[NEW] {username}: {len(new_tweets)} yeni tweet")
        else:
            print(f"[SAME] {username}: yeni tweet yok")

        time.sleep(1)

    save_state(state)

    if all_new_tweets:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = TWEETS_DIR / f"tweets_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_new_tweets, f, ensure_ascii=False, indent=2)

        print(f"[SAVE] {output_file}: {len(all_new_tweets)} tweet")

    print("=" * 60)
    print(f"Toplam çekilen: {total_fetched}")
    print(f"Yeni: {total_new}")
    print(f"Instance: {instance}")
    print("=" * 60)


if __name__ == "__main__":
    main()
