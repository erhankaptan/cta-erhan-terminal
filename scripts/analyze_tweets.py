"""
CTA ERHAN TERMİNALİ — Gemini Analiz v6 (Genişletilmiş)
========================================================
Öncelikli hesapların tweet'lerini analiz eder.
- Metin + GÖRSEL analizi
- 25 futures + izleme dışı varlıklar (XAUUSD, DXY, BTCUSD vs.)
- Türkçe yön + gerekçe
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
REQUEST_DELAY = 3.0

DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
STATE_FILE = DATA_DIR / "analysis_state.json"

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
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, timeout=20, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            ct = response.headers.get("Content-Type", "").lower()
            # Sadece gerçek görselleri kabul et (html reddet)
            if "image" in ct and "html" not in ct:
                return response.content, ct
            else:
                print(f"    [IMG] Reddedildi (MIME: {ct})")
                return None, None
        else:
            print(f"    [IMG] HTTP {response.status_code}")
    except Exception as e:
        print(f"    [IMG] İndirme hatası: {e}")
    return None, None


# ============================================================
# GEMINI PROMPT (GENİŞLETİLMİŞ)
# ============================================================

PROMPT = """Sen kıdemli bir CTA (Commodity Trading Advisor) ve vadeli işlemler analistisin.

GÖREV: Aşağıdaki tweet metnini ve varsa görselleri analiz et. Tweet'te geçen HER finansal varlığı çıkar.

ÖNEMLİ:
- Görselleri DİKKATLİCE incele. Tablo/grafik/chart varsa her satırı (ürünü) ayrı ayrı oku.
- Tweet piyasa/finans ile ALAKALI DEĞİLSE (siyasi, kişisel, reklam, mizah) → varliklar: []
- Tweet kısa olsa bile içindeki her varlığı yakala.

VARLIK LİSTESİ (bu sembolleri kullan, başka sembol uydurma):

VADELİ KONTRATLAR:
- Endeksler: ES, MES, NQ, MNQ, RTY, YM
- Emtialar: CL, MCL, NG, GC, MGC, SI, HG, PL
- Tahıllar: ZC, ZS, ZW, ZL, ZM
- Dövizler: 6E, 6J, 6B, 6A, 6C, 6S

SPOT / İZLEME DIŞI:
- Değerli Metaller: XAUUSD, XAGUSD
- Forex: EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF
- Kripto: BTCUSD, ETHUSD
- Endeksler/Endeks: SPX500, NAS100, GER40, UK100, JP225, DXY, VIX
- Petrol: USOUSD, UKOIL
- Tahvil: US10Y

EŞLEŞTİRME KURALI:
- "Gold" / "XAUUSD" → GC (futures) veya XAUUSD (spot)
- "S&P 500" / "SPX" → ES (futures) veya SPX500 (spot)
- "Euro" / "EURUSD" → 6E (futures) veya EURUSD (spot)
- "Bitcoin" / "BTC" → BTCUSD
- "Dollar" / "DXY" → DXY
- Hangi formatta geçiyorsa onu kullan.

Tweet metni:
{text}

Kullanıcı: @{username}

ÇIKTI FORMATI (SADECE JSON döndür, markdown/açıklama yok):

{{
  "varliklar": [
    {{
      "sembol": "GC",
      "isim": "Gold",
      "yon": "YUKARI",
      "gerekce": "kısa Türkçe gerekçe (max 150 karakter)",
      "skor": 0.7
    }}
  ],
  "genel_yon": "YUKARI",
  "ozet": "Türkçe 1-2 cümle özet",
  "confidence": 0.8
}}

KURALLAR:
- yon sadece: YUKARI, AŞAĞI, NÖTR
- gerekce Türkçe, max 150 karakter
- skor: 0.0 - 1.0
- varliklar boş olabilir → []

Şimdi analiz et:"""


# ============================================================
# GEMINI ANALİZ
# ============================================================

def analyze_with_gemini(text: str, username: str, image_urls: list):
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = PROMPT.format(text=(text or "")[:1500], username=username)

    contents = [prompt]

    for img_url in image_urls[:3]:
        img_bytes, mime_type = download_image(img_url)
        if img_bytes:
            contents.append({
                "mime_type": mime_type or "image/jpeg",
                "data": img_bytes
            })
            print(f"    [IMG] Görsel eklendi: {img_url[:60]}...")

    response = model.generate_content(contents)
    raw = (response.text or "").strip()

    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
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
# ANA
# ============================================================

def main():
    print("=" * 60)
    print("Gemini Analiz v6 (Genişletilmiş)")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY yok")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    ensure_dirs()

    latest_file = get_latest_tweets_file()
    if not latest_file:
        print("[FATAL] Tweet dosyası yok")
        return

    print(f"[LOAD] {latest_file.name}")
    tweets = load_tweets(latest_file)
    print(f"[INFO] {len(tweets)} tweet")

    priority_tweets = [t for t in tweets if is_priority_tweet(t)]
    print(f"[INFO] {len(priority_tweets)} öncelikli")

    if not priority_tweets:
        print("[DONE] Öncelikli tweet yok")
        return

    state = load_state()
    analyzed_ids = set(state.get("analyzed_ids", []))

    new_tweets = [t for t in priority_tweets if str(t.get("id")) not in analyzed_ids]
    print(f"[INFO] {len(new_tweets)} yeni")

    if not new_tweets:
        print("[DONE] Yeni tweet yok")
        return

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
                vc = len(result["varliklar"])
                print(f"    [OK] {vc} varlık")
            else:
                failed += 1
                print(f"    [FAIL]")
        except Exception as e:
            failed += 1
            print(f"    [ERR] {type(e).__name__}: {str(e)[:120]}")

        if i < len(new_tweets):
            time.sleep(REQUEST_DELAY)

    if results:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = ANALYSIS_DIR / f"analysis_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n[SAVE] {output_file.name}")

    state["analyzed_ids"] = list(analyzed_ids)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    print(f"\n{'=' * 60}")
    print(f"Başarılı: {success}, Başarısız: {failed}")
    print(f"Toplam işlenmiş: {len(analyzed_ids)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()