"""
CTA ERHAN TERMİNALİ — RSS Çeviri
====================================
İngilizce RSS makalelerini Gemini ile Türkçeye çevirir.
Orijinal İngilizce içerik korunur.
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"
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


def translate_text(text: str, model) -> str:
    if not text or not text.strip():
        return ""

    prompt = f"""Aşağıdaki İngilizce metni Türkçeye çevir.

KURALLAR:
- Sadece çeviriyi döndür, başka bir şey yazma
- Finansal terimleri koru (CTA, COT, S&P 500, Fed, vs.)
- Kısaltmaları koru (ES, NQ, CL, GC, vs.)
- Doğal Türkçe kullan

İNGİLİZCE METİN:
{text[:3000]}
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERR] Çeviri hatası: {type(e).__name__}")
        return ""


def main():
    print("=" * 60)
    print("CTA ERHAN TERMİNALİ — RSS Çeviri")
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
    translated_count = 0

    for i, article in enumerate(articles, 1):
        title_en = article.get("title_en", "")
        content_en = article.get("content_en", "")

        title_hash = compute_hash(title_en)

        if title_hash in state:
            article["title_tr"] = state[title_hash]["title_tr"]
            article["content_tr"] = state[title_hash].get("content_tr", "")
            print(f"[{i}/{len(articles)}] Cache: {title_en[:50]}...")
            continue

        print(f"[{i}/{len(articles)}] Çeviri: {title_en[:50]}...")

        title_tr = translate_text(title_en, model)
        time.sleep(REQUEST_DELAY)

        content_tr = translate_text(content_en, model)
        time.sleep(REQUEST_DELAY)

        article["title_tr"] = title_tr
        article["content_tr"] = content_tr
        article["translation_hash"] = title_hash

        state[title_hash] = {
            "title_en": title_en,
            "title_tr": title_tr,
            "content_tr": content_tr,
            "translated_at": datetime.now(timezone.utc).isoformat(),
        }

        translated_count += 1

    save_state(state)

    with open(rss_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"[SAVE] {rss_file}: {translated_count} yeni çeviri")
    print("=" * 60)
    print(f"Toplam çevrilen: {translated_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
