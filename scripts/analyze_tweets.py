"""
CTA ERHAN TERMİNALİ — Gemini Analiz v9 (google-genai)
======================================================
Yeni SDK: google-genai (eski google-generativeai değil)
"""

import os
import json
import time
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"
REQUEST_DELAY = 3.0

DATA_DIR = Path("data")
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
STATE_FILE = DATA_DIR / "analysis_state.json"

PRIORITY_ACCOUNTS = ["wayneterprises", "JuanJesusMontoy", "misterpuertas"]
PRIORITY_LOWER = [a.lower() for a in PRIORITY_ACCOUNTS]


def is_priority_tweet(tweet: dict) -> bool:
    username = (tweet.get("username") or "").lower()
    return username in PRIORITY_LOWER


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


def get_all_tweets_files():
    return sorted(TWEETS_DIR.glob("tweets_*.json"))


def load_tweets(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def download_image(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, timeout=20, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            ct = response.headers.get("Content-Type", "").lower()
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


PROMPT = """Sen kıdemli bir CTA (Commodity Trading Advisor) ve vadeli işlemler analistisin.

GÖREV: Aşağıdaki tweet metnini ve varsa görselleri analiz et. Tweet'te geçen HER finansal varlığı ÇIKAR.

ÇOK ÖNEMLİ — AGRESİF OL:
- Tweet kısa olsa bile, ima etse bile, dolaylı konuşsa bile varlık çıkar.
- Hashtag (#gold, #SPX, #BTC) ve kısaltma ($ES, $GC, $SPX) varsa mutlaka yakala.
- Tweet'te şirket adı geçiyorsa (Nvidia, Tesla, Apple) → hisse sembolü olarak al (NVDA, TSLA, AAPL).
- Tweet İspanyolca/İngilizce/Türkçe olabilir, hepsini işle.
- Tweet "FED faiz kararı" diyorsa → DXY, US10Y, XAUUSD çıkar.
- Tweet "Çin ekonomisi" diyorsa → HG, ES, SPX500 çıkar.
- Tweet "petrol" diyorsa → CL, MCL, USOUSD çıkar.
- HK hisseleri (700 HK, 9988 HK vs.) da geçerli — onları da çıkar.
- Eğer tweet tamamen alakasız (siyasi, kişisel, reklam, mizah) → varliklar: []

GÖRSEL: Varsa tablo/grafik oku. Her satırı (ürünü) ayrı ayrı çıkar.

VARLIK LİSTESİ:

VADELİ:
- Endeks: ES, MES, NQ, MNQ, RTY, YM
- Emtia: CL, MCL, NG, GC, MGC, SI, HG, PL
- Tahıl: ZC, ZS, ZW, ZL, ZM
- Döviz: 6E, 6J, 6B, 6A, 6C, 6S

SPOT / İZLEME DIŞI:
- Değerli: XAUUSD, XAGUSD
- Forex: EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF
- Kripto: BTCUSD, ETHUSD, SOL
- Endeks: SPX500, NAS100, GER40, UK100, JP225, DXY, VIX
- Petrol: USOUSD, UKOIL
- Tahvil: US10Y
- Hisse: NVDA, TSLA, AAPL, MSFT, AMZN, GOOGL, META
- HK: 700 HK, 9988 HK, 1299 HK, 1810 HK, HSTECH, HSI

Tweet metni:
{text}

Kullanıcı: @{username}

ÇIKTI (SADECE JSON):

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
- yon: YUKARI, AŞAĞI, NÖTR
- gerekce: Türkçe, max 150 karakter
- skor: 0.0 - 1.0
- varliklar boş olabilir → []

Şimdi analiz et:"""


def analyze_with_gemini(text: str, username: str, image_urls: list, client):
    prompt = PROMPT.format(text=(text or "")[:1500], username=username)

    contents = [prompt]
    for img_url in image_urls[:3]:
        img_bytes, mime_type = download_image(img_url)
        if img_bytes:
            contents.append(
                types.Part.from_bytes(data=img_bytes, mime_type=mime_type or "image/jpeg")
            )
            print(f"    [IMG] Görsel eklendi")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=8192,
        ),
    )
    raw = (response.text or "").strip()

    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
            if raw.startswith("json"):
                raw = raw[4:]
    raw = raw.strip()

    if not raw.startswith("{"):
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            raw = m.group(0)

    # 1. Normal dene
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 2. Trailing virgülleri temizle
    cleaned = re.sub(r',\s*([}\]])', r'\1', raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 3. Kesik JSON'u tamamla
    try:
        if '"varliklar"' in raw:
            idx = raw.rfind('}')
            if idx > 0:
                truncated = raw[:idx+1]
                opens = truncated.count('[') - truncated.count(']')
                trunc2 = truncated + (']' * opens)
                opens2 = trunc2.count('{') - trunc2.count('}')
                trunc3 = trunc2 + ('}' * opens2)
                return json.loads(trunc3)
    except Exception:
        pass

    print(f"    [ERR] JSON parse başarısız")
    print(f"    [RAW] {raw[:200]}")
    return None


def analyze_with_retry(text, username, images, client, max_retries=2):
    for attempt in range(max_retries):
        try:
            result = analyze_with_gemini(text, username, images, client)
            if result is not None:
                return result
        except Exception as e:
            print(f"    [RETRY {attempt+1}] {type(e).__name__}: {str(e)[:100]}")
            time.sleep(2)
    return None


def main():
    print("=" * 60)
    print("Gemini Analiz v9 (google-genai)")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY yok")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)
    ensure_dirs()

    files = get_all_tweets_files()
    if not files:
        print("[FATAL] Tweet dosyası yok")
        return

    print(f"[INFO] {len(files)} tweet dosyası bulundu")

    all_tweets = []
    for fp in files:
        try:
            tweets = load_tweets(fp)
            all_tweets.extend(tweets)
        except Exception as e:
            print(f"  [ERR] {fp.name}: {e}")

    print(f"[INFO] Toplam {len(all_tweets)} tweet")

    priority_tweets = [t for t in all_tweets if is_priority_tweet(t)]

    seen_ids = set()
    unique_tweets = []
    for t in priority_tweets:
        tid = str(t.get("id", ""))
        if tid and tid not in seen_ids:
            seen_ids.add(tid)
            unique_tweets.append(t)

    print(f"[INFO] {len(unique_tweets)} öncelikli (unique)")

    if not unique_tweets:
        print("[DONE] Öncelikli tweet yok")
        return

    state = load_state()
    analyzed_ids = set(state.get("analyzed_ids", []))

    new_tweets = [t for t in unique_tweets if str(t.get("id")) not in analyzed_ids]
    print(f"[INFO] {len(new_tweets)} yeni")

    if not new_tweets:
        print("[DONE] Yeni tweet yok")
        return

    results = []
    success = 0
    failed = 0
    total_assets = 0

    for i, tweet in enumerate(new_tweets, 1):
        tweet_id = str(tweet.get("id", ""))
        username = tweet.get("username", "")
        text = tweet.get("text", "")
        images = tweet.get("images", [])

        print(f"\n[{i}/{len(new_tweets)}] @{username} — {text[:60]}...")

        analysis = analyze_with_retry(text, username, images, client)

        if analysis:
            varliklar = analysis.get("varliklar", [])
            result = {
                "tweet_id": tweet_id,
                "username": username,
                "text": text,
                "images": images,
                "analyzed_at": datetime.now(timezone.utc).isoformat(),
                "varliklar": varliklar,
                "genel_yon": analysis.get("genel_yon", "NÖTR"),
                "ozet": analysis.get("ozet", ""),
                "confidence": analysis.get("confidence", 0.0),
            }
            results.append(result)
            analyzed_ids.add(tweet_id)
            success += 1
            total_assets += len(varliklar)
            print(f"    [OK] {len(varliklar)} varlık")
        else:
            failed += 1
            print(f"    [FAIL]")

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
    print(f"Toplam varlık çıkarıldı: {total_assets}")
    print(f"Toplam işlenmiş ID: {len(analyzed_ids)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()