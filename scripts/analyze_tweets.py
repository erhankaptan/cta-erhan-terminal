"""
CTA ERHAN TERMİNALİ — Gemini Analiz
=====================================
Tweet metinlerini ve görsellerini Gemini API ile analiz eder.
- BULL/BEAR/NEUTRAL sentiment çıkarır
- CTA sinyallerini tespit eder
- Confidence skoru verir
- Türkçe özet çıkarır
- 0 TL — Gemini free tier
"""

import os
import json
import time
import base64
from datetime import datetime, timezone
from pathlib import Path

import requests
import google.generativeai as genai

# ============================================================
# AYARLAR
# ============================================================

# API Key (GitHub Actions'ta secret'tan gelir)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini model
MODEL_NAME = "gemini-flash-latest"

# Rate limit (60 istek/dakika = 1 istek/saniye)
REQUEST_DELAY = 1.5

# Klasörler
DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
STATE_FILE = DATA_DIR / "analysis_state.json"

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


def get_latest_tweets_file() -> Path:
    """En son tweet dosyasını bul"""
    files = sorted(TWEETS_DIR.glob("tweets_*.json"))
    if not files:
        return None
    return files[-1]


def load_tweets(filepath: Path) -> list:
    """Tweet dosyasını yükle"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def download_image(url: str) -> bytes:
    """Görseli indir"""
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

Aşağıdaki tweet metnini ve ekli görseli (varsa) analiz et:

TWEET METNİ:
{text}

GÖRSEL ANALİZİ:
{image_note}

Görevler:
1. Metnin piyasa yönünü belirle (BULL / BEAR / NEUTRAL)
2. İlgili varlıkları tespit et (ES, NQ, CL, GC, BTC, veya GENERAL)
3. CTA sinyali içeriyor mu? (evet/hayır)
4. Güven skoru ver (0-100)
5. Kısa Türkçe özet yaz (max 150 karakter)

SADECE aşağıdaki JSON formatında cevap ver, başka bir şey yazma:

{{
  "sentiment": "BULL|BEAR|NEUTRAL",
  "tickers": ["ES", "NQ"],
  "is_cta_signal": true,
  "confidence": 75,
  "summary": "Kısa Türkçe özet"
}}
"""


def analyze_tweet(text: str, images: list) -> dict:
    """Bir tweet'i analiz et"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)

        # Görsel notu
        image_note = f"{len(images)} görsel eklendi" if images else "Görsel yok"

        # Prompt
        prompt = PROMPT.format(text=text[:2000], image_note=image_note)

        # İçerik listesi
        contents = [prompt]

        # Görselleri ekle (max 2 tane)
        for img_url in images[:2]:
            img_bytes = download_image(img_url)
            if img_bytes:
                contents.append({
                    "mime_type": "image/jpeg",
                    "data": img_bytes
                })

        # Gemini'ye gönder
        response = model.generate_content(contents)

        # JSON parse
        raw = response.text.strip()

        # JSON bloğunu çıkar
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        return {
            "sentiment": "NEUTRAL",
            "tickers": [],
            "is_cta_signal": False,
            "confidence": 0,
            "summary": f"JSON parse hatası: {str(e)[:80]}",
        }
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
    print("CTA ERHAN TERMİNALİ — Gemini Analiz")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # API key kontrolü
    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY bulunamadı!")
        return

    # Gemini'yi başlat
    genai.configure(api_key=GEMINI_API_KEY)

    ensure_dirs()
    state = load_state()

    # En son tweet dosyasını bul
    tweets_file = get_latest_tweets_file()
    if not tweets_file:
        print("[FATAL] Tweet dosyası bulunamadı!")
        return

    print(f"[LOAD] {tweets_file}")

    tweets = load_tweets(tweets_file)
    print(f"[INFO] {len(tweets)} tweet yüklendi")

    # İşlenmiş tweet'leri atla
    processed_ids = set(state.get("processed_ids", []))

    # Analiz edilecek tweet'ler
    to_analyze = [t for t in tweets if t.get("id") and t["id"] not in processed_ids]
    print(f"[INFO] {len(to_analyze)} tweet analiz edilecek")

    if not to_analyze:
        print("[DONE] Yeni tweet yok, çıkılıyor")
        return

    # Her tweet'i analiz et
    results = []
    new_processed = []

    for i, tweet in enumerate(to_analyze, 1):
        tweet_id = tweet.get("id", "")
        username = tweet.get("username", "")
        text = tweet.get("text", "")
        images = tweet.get("images", [])

        print(f"[{i}/{len(to_analyze)}] @{username}: {text[:60]}...")

        # Analiz
        analysis = analyze_tweet(text, images)

        # Sonuç
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

        # Rate limit için bekle
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
    print(f"Toplam analiz: {len(results)}")

    # Sentiment dağılımı
    bull = sum(1 for r in results if r.get("sentiment") == "BULL")
    bear = sum(1 for r in results if r.get("sentiment") == "BEAR")
    neutral = sum(1 for r in results if r.get("sentiment") == "NEUTRAL")
    cta_signals = sum(1 for r in results if r.get("is_cta_signal"))

    print(f"BULL: {bull}")
    print(f"BEAR: {bear}")
    print(f"NEUTRAL: {neutral}")
    print(f"CTA sinyali: {cta_signals}")
    print("=" * 60)


if __name__ == "__main__":
    main()
