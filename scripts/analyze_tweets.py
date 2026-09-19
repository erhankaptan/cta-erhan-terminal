"""
CTA ERHAN TERMİNALİ — Gemini Analiz v5 (Görsel Destekli)
=========================================================
Öncelikli hesapların tweet'lerini analiz eder.
- Metin analizi
- GÖRSEL analizi (tablo, grafik, chart)
- Her varlık ayrı yön (Türkçe)
- Gemini 3.5 Flash (Vision)
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

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash"
REQUEST_DELAY = 3.0

DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
STATE_FILE = DATA_DIR / "analysis_state.json"

# ============================================================
# ÖNCELİKLİ HESAPLAR
# ============================================================

PRIORITY_ACCOUNTS = [
    "wayneterprises",
    "JuanJesusMontoy",
    "misterpuertas",
]

PRIORITY_LOWER = [a.lower() for a in PRIORITY_ACCOUNTS]


def is_priority_tweet(tweet: dict) -> bool:
    username = (tweet.get("username") or "").lower()
    return username in PRIORITY_LOWER


# ============================================================
# YARDIMCI
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
    """Görseli indir, bytes döner."""
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.content, response.headers.get("Content-Type", "image/jpeg")
    except Exception as e:
        print(f"    [IMG] İndirme hatası: {e}")
    return None, None


# ============================================================
# GEMINI PROMPT
# ============================================================

PROMPT = """Sen kıdemli bir CTA (Commodity Trading Advisor) ve vadeli işlemler analistisin.

Aşağıdaki tweet metnini ve varsa görselleri analiz et.

ÖNEMLİ: Görselleri DİKKATLİCE incele. Eğer görsel bir TABLO, GRAFİK veya CHART ise:
- Tablodaki her satırı (ürünü) ayrı ayrı oku
- Her ürün için: yön (Long/Short/Neutral), skor ve gerekçe çıkar
- Örnek tablolar: CTA positioning, Net Flow, OI Change, Return tabloları

Tweet metni:
{text}

Kullanıcı: @{username}

ÇIKTI FORMATI (sadece JSON, başka bir şey yazma):
{{
  "varliklar": [
    {{
      "sembol": "GC",
      "isim": "Gold",
      "yon": "YUKARI" | "AŞAĞI" | "NÖTR",
      "gerekce": "kısa açıklama (max 100 karakter)",
      "skor": 0.0-1.0
    }}
  ],
  "genel_yon": "YUKARI" | "AŞAĞI" | "NÖTR" | "KARIŞIK",
  "ozet": "Türkçe 1-2 cümle özet",
  "confidence": 0.0-1.0
}}

KURALLAR:
- 25 futures kontratı tanı: ES, NQ, CL, GC, SI, HG, NG, ZC, ZS, ZW, 6E, 6J, 6B, 6A, 6C, 6S
- Görselde tablo varsa TÜM ürünleri çıkar
- Yön belirsizse NÖTR yaz
- Gerekçeyi Türkçe yaz
- Sadece JSON döndür, markdown kullanma

Şimdi analiz et:"""


# ============================================================
# GEMINI ANALİZ
# ============================================================

def analyze_with_gemini(text: str, username: str, image_urls: list):
    """Gemini ile metin + görsel analizi."""
    model = genai.GenerativeModel(MODEL_NAME)

    # Prompt hazırla
    prompt = PROMPT.format(text=text[:1500], username=username)

    # İçerik listesi
    contents = [prompt]

    # Görselleri ekle
    for img_url in image_urls[:3]:  # Max 3 görsel
        img_bytes, mime_type = download_image(img_url)
        if img_bytes:
            contents.append({
                "mime_type": mime_type or "image/jpeg",
                "data": img_bytes
            })
            print(f"    [IMG] Görsel eklendi: {img_url[:60]}...")

    # Gemini'ye gönder
    response = model.generate_content(contents)
    raw = response.text.strip()

    # JSON parse
    # Markdown kod bloğu varsa temizle
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"    [ERR] JSON parse hatası: {e}")
        print(f"    [RAW] {raw[:200]}")
        return None


# ============================================================
# ANA FONKSİYON
# ============================================================

def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — Gemini Analiz v5 (Görsel Destekli)")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY bulunamadı")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    ensure_dirs()

    # En son tweet dosyası
    latest_file = get_latest_tweets_file()
    if not latest_file:
        print("[FATAL] Tweet dosyası bulunamadı")
        return

    print(f"[LOAD] {latest_file}")
    tweets = load_tweets(latest_file)
    print(f"[INFO] {len(tweets)} tweet yüklendi")

    # Öncelikli tweet'leri filtrele
    priority_tweets = [t for t in tweets if is_priority_tweet(t)]
    print(f"[INFO] {len(priority_tweets)} öncelikli tweet analiz edilecek")

    if not priority_tweets:
        print("[DONE] Yeni öncelikli tweet yok")
        return

    # State yükle
    state = load_state()
    analyzed_ids = set(state.get("analyzed_ids", []))

    # Yeni tweet'leri bul
    new_tweets = [t for t in priority_tweets if str(t.get("id")) not in analyzed_ids]
    print(f"[INFO] {len(new_tweets)} yeni tweet")

    if not new_tweets:
        print("[DONE] Yeni öncelikli tweet yok")
        return

    # Analiz sonuçları
    results = []
    success = 0
    failed = 0

    for i, tweet in enumerate(new_tweets, 1):
        tweet_id = str(tweet.get("id", ""))
        username = tweet.get("username", "")
        text = tweet.get("text", "")
        images = tweet.get("images", [])

        print(f"\n[{i}/{len(new_tweets)}] @{username} — {text[:60]}...")
        if images:
            print(f"    [IMG] {len(images)} görsel")

        try:
            analysis = analyze_with_gemini(text, username, images)

            if analysis:
                result = {
                    "tweet_id": tweet_id,
                    "username": username,
                    "text": text,
                    "images": images,
                    "analyzed_at": datetime.now(timezone.utc).isoformat(),
                    "varliklar": analysis.get("varliklar", []),
                    "genel_yon": analysis.get("genel_yon", "NÖTR"),
                    "ozet": analysis.get("ozet", ""),
                    "confidence": analysis.get("confidence", 0.0),
                }
                results.append(result)
                analyzed_ids.add(tweet_id)
                success += 1
                print(f"    [OK] {len(result['varliklar'])} varlık çıkarıldı")
            else:
                failed += 1
                print(f"    [FAIL] Analiz başarısız")

        except Exception as e:
            failed += 1
            print(f"    [ERR] {type(e).__name__}: {e}")

        # Rate limit için bekle
        if i < len(new_tweets):
            time.sleep(REQUEST_DELAY)

    # Sonuçları kaydet
    if results:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = ANALYSIS_DIR / f"analysis_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n[SAVE] {output_file}")

    # State güncelle
    state["analyzed_ids"] = list(analyzed_ids)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    print(f"\n{'=' * 60}")
    print(f"Başarılı: {success}, Başarısız: {failed}")
    print(f"Toplam analiz edilen: {len(analyzed_ids)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
