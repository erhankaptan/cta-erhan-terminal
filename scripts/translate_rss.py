"""
CTA ERHAN TERMİNALİ — RSS Çeviri + Yorum
==========================================
İngilizce RSS makalelerini Gemini ile:
- Türkçeye çevirir
- Türkçe yorum üretir
- Varlık analizleri çıkarır (BULLISH/BEARISH/NEUTRAL)
- Tek çağrıda (kota tasarrufu)
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash"
REQUEST_DELAY = 3.0

DATA_DIR = Path("data")
RSS_DIR = DATA_DIR / "rss"
STATE_FILE = DATA_DIR / "translation_state.json"


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


def compute_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_latest_rss_file():
    files = sorted(RSS_DIR.glob("rss_*.json"))
    if not files:
        return None
    return files[-1]


def translate_and_analyze(title_en: str, content_en: str, model) -> dict:
    """Tek çağrıda: çeviri + yorum + varlık analizi."""
    if not title_en and not content_en:
        return {"title_tr": "", "content_tr": "", "yorum": "", "varliklar": [], "genel_yon": "NÖTR"}

    prompt = f"""Sen kıdemli bir CTA (Commodity Trading Advisor) ve vadeli işlemler analistisin.

Aşağıdaki İngilizce finansal makaleyi analiz et:
1. Başlığı Türkçeye çevir
2. İçeriği Türkçeye çevir
3. Makalenin Türkçe YORUMUNU yaz (2-3 cümle, piyasa etkisi)
4. Makalede geçen futures varlıklarını çıkar (BULLISH/BEARISH/NEUTRAL)

BAŞLIK (İngilizce):
{title_en[:500]}

İÇERİK (İngilizce):
{content_en[:2500]}

ÇIKTI FORMATI (sadece JSON, markdown kullanma):
{{
  "title_tr": "Türkçe başlık",
  "content_tr": "Türkçe içerik çevirisi",
  "yorum": "Makalenin Türkçe yorumu (piyasa etkisi, CTA açısından önem)",
  "varliklar": [
    {{
      "sembol": "GC",
      "isim": "Gold",
      "yon": "YUKARI" | "AŞAĞI" | "NÖTR",
      "gerekce": "kısa gerekçe (max 100 karakter)",
      "skor": 0.0-1.0
    }}
  ],
  "genel_yon": "YUKARI" | "AŞAĞI" | "NÖTR" | "KARIŞIK"
}}

KURALLAR:
- 25 futures kontratı tanı: ES, NQ, CL, GC, SI, HG, NG, ZC, ZS, ZW, 6E, 6J, 6B, 6A, 6C, 6S
- Finansal terimleri koru (CTA, COT, S&P 500, Fed, vs.)
- Sadece JSON döndür, markdown kullanma
- Varlık yoksa "varliklar": [] bırak

Şimdi analiz et:"""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Markdown kod bloğu temizle
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return {
            "title_tr": result.get("title_tr", ""),
            "content_tr": result.get("content_tr", ""),
            "yorum": result.get("yorum", ""),
            "varliklar": result.get("varliklar", []),
            "genel_yon": result.get("genel_yon", "NÖTR"),
        }
    except json.JSONDecodeError as e:
        print(f"[ERR] JSON parse hatası: {e}")
        return {
            "title_tr": "", "content_tr": "", "yorum": "",
            "varliklar": [], "genel_yon": "NÖTR",
        }
    except Exception as e:
        print(f"[ERR] Gemini hatası: {type(e).__name__}: {e}")
        return {
            "title_tr": "", "content_tr": "", "yorum": "",
            "varliklar": [], "genel_yon": "NÖTR",
        }


def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — RSS Çeviri + Yorum v2")
    print(f"Zaman: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("[FATAL] GEMINI_API_KEY bulunamadı!")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    rss_file = get_latest_rss_file()
    if not rss_file:
        print("[FATAL] RSS dosyası bulunamadı!")
        return

    print(f"[LOAD] {rss_file}")

    with open(rss_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"[INFO] {len(articles)} makale yüklendi")

    state = load_state()
    processed_count = 0

    for i, article in enumerate(articles, 1):
        title_en = article.get("title_en", "")
        content_en = article.get("content_en", "")

        title_hash = compute_hash(title_en)

        if title_hash in state and state[title_hash].get("yorum"):
            article["title_tr"] = state[title_hash]["title_tr"]
            article["content_tr"] = state[title_hash].get("content_tr", "")
            article["yorum"] = state[title_hash].get("yorum", "")
            article["varliklar"] = state[title_hash].get("varliklar", [])
            article["genel_yon"] = state[title_hash].get("genel_yon", "NÖTR")
            print(f"[{i}/{len(articles)}] Cache: {title_en[:50]}...")
            continue

        print(f"[{i}/{len(articles)}] Analiz: {title_en[:50]}...")

        result = translate_and_analyze(title_en, content_en, model)

        article["title_tr"] = result["title_tr"]
        article["content_tr"] = result["content_tr"]
        article["yorum"] = result["yorum"]
        article["varliklar"] = result["varliklar"]
        article["genel_yon"] = result["genel_yon"]
        article["translation_hash"] = title_hash

        state[title_hash] = {
            "title_en": title_en,
            "title_tr": result["title_tr"],
            "content_tr": result["content_tr"],
            "yorum": result["yorum"],
            "varliklar": result["varliklar"],
            "genel_yon": result["genel_yon"],
            "translated_at": datetime.now(timezone.utc).isoformat(),
        }

        processed_count += 1

        if i < len(articles):
            time.sleep(REQUEST_DELAY)

    save_state(state)

    with open(rss_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"[SAVE] {rss_file}: {processed_count} yeni analiz")
    print("=" * 60)
    print(f"Toplam işlenen: {processed_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
