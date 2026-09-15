"""
CTA ERHAN TERMİNALİ — Gemini Analiz v3
=========================================
Sadece 10 ÖNCELİKLİ hesabı analiz eder.
Diğerleri: raw kayıt, analiz yok.
"""

import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import google.generativeai as genai

# ============================================================
# AYARLAR
# ============================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"
REQUEST_DELAY = 2.0

DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
STATE_FILE = DATA_DIR / "analysis_state.json"

# ============================================================
# ÖNCELİKLİ HESAPLAR (Sadece bunlar analiz edilir)
# ============================================================

PRIORITY_ACCOUNTS = [
    "wayneterprises",
    "PeterLBrandt",
    "LindaRaschke",
    "AnthonyCrudele",
    "FuturesTrader71",
    "CommodMkt",
    "rcmAlts",
    "MacroOps",
    "AttainCap2",
    "JPokoTrades",
]

PRIORITY_LOWER = [a.lower() for a in PRIORITY_ACCOUNTS]


def is_priority_tweet(tweet: dict) -> bool:
    """Tweet öncelikli hesaptan mı?"""
    username = (tweet.get("username") or "").lower()
    return username in PRIORITY_LOWER

# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def ensure_dirs():
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


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


def get_latest_tweets_file():
    files = sorted(TWEETS_DIR.glob("tweets_*.json"))
    if not files:
        return None
    return files[-1]


def load_tweets(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def download_image(url: str):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None

# ============================================================
# GEMINI ANALİZ
# ============================================================

PROMPT = """Sen kıdemli bir CTA (Commodity Trading Advisor) ve vadeli işlemler analistisin.

Tweet metnini ve varsa görseli analiz et:

TWEET:
{text}

Görev: Piyasa yönünü BULL/BEAR/NEUTRAL olarak sınıflandır.
CTA sinyali içeriyor mu? (evet/hayır)
Güven skoru (0-100).
Türkçe kısa özet (max 150 karakter).

SADECE JSON döndür:
{{
  "sentiment": "BULL|BEAR|NEUTRAL",
  "tickers": ["ES", "NQ"],
  "is_cta_signal": true,
  "confidence": 75,
  "summary": "Kısa Türkçe özet"
}}
"""


def analyze_tweet(text: str, images: list) -> dict:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = PROMPT.format(text=text[:2000])
        contents = [prompt]

        for img_url in images[:1]:
            img_bytes = download_image(img_url)
            if img_bytes:
                contents.append({
                    "mime_type": "image/jpeg",
                    "data": img_bytes
                })

        response = model.generate_content(contents)
        raw = response.text.strip()

        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        return json.loads(raw)

    except Exception as e:
        return {
            "sentiment": "NEUTRAL",
            "tickers": [],
            "is_cta_signal": False,
            "confidence": 0,
            "summary": f"Hata: {type(e).__name__}",
        }

# ============================================================
# ANA FONKSİYON
# ============================================================

def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — Gemini Analiz v3 (10 Hesap)")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY bulunamadı!")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    ensure_dirs()
    state = load_state()

    tweets_file = get_latest_tweets_file()
    if not tweets_file:
        print("[FATAL] Tweet dosyası bulunamadı!")
        return

    print(f"[LOAD] {tweets_file}")
    tweets = load_tweets(tweets_file)
    print(f"[INFO] {len(tweets)} tweet yüklendi")

    processed_ids = set(state.get("processed_ids", []))

    # SADECE ÖNCELİKLİ HESAPLAR
    priority_tweets = [
        t for t in tweets
        if t.get("id")
        and t["id"] not in processed_ids
        and is_priority_tweet(t)
    ]

    print(f"[INFO] {len(priority_tweets)} öncelikli tweet analiz edilecek")

    if not priority_tweets:
        print("[DONE] Yeni öncelikli tweet yok")
        return

    results = []
    new_processed = []

    for i, tweet in enumerate(priority_tweets, 1):
        tweet_id = tweet.get("id", "")
        username = tweet.get("username", "")
        text = tweet.get("text", "")
        images = tweet.get("images", [])

        print(f"[{i}/{len(priority_tweets)}] @{username}: {text[:60]}...")

        analysis = analyze_tweet(text, images)

        result = {
            "tweet_id": tweet_id,
            "username": username,
            "text": text[:500],
            "images": images,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            **analysis,
        }
        results.append(result)
        new_processed.append(tweet_id)

        time.sleep(REQUEST_DELAY)

    # State güncelle
    state["processed_ids"] = list(set(processed_ids) | set(new_processed))[-2000:]
    state["last_update"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    # Sonuçları kaydet
    if results:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = ANALYSIS_DIR / f"analysis_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"[SAVE] {output_file}: {len(results)} analiz")

    # Özet
    print("=" * 60)
    print(f"Toplam: {len(results)}")
    bull = sum(1 for r in results if r.get("sentiment") == "BULL")
    bear = sum(1 for r in results if r.get("sentiment") == "BEAR")
    neutral = sum(1 for r in results if r.get("sentiment") == "NEUTRAL")
    cta = sum(1 for r in results if r.get("is_cta_signal"))
    print(f"BULL: {bull}, BEAR: {bear}, NEUTRAL: {neutral}")
    print(f"CTA Sinyali: {cta}")
    print("=" * 60)


if __name__ == "__main__":
    main()
