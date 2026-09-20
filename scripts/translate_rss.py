"""
CTA ERHAN TERMİNALİ — Translate RSS (v3)
=========================================
Tickmill RSS makalelerini Gemini ile:
  - Türkçeye çevirir
  - Kısa yorum yazar
  - Varlık analizi yapar (sembol, yon, skor, gerekce)
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone

try:
    import google.generativeai as genai
except ImportError:
    print("HATA: pip install google-generativeai")
    raise


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
RSS_DIR = DATA_DIR / "rss"
STATE_FILE = DATA_DIR / "translation_state.json"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
WAIT_SECONDS = 3


PRODUCT_LIST = """ES, MES, NQ, MNQ, RTY, YM (Endeksler)
CL, MCL, NG, GC, MGC, SI, HG, PL (Emtialar)
ZC, ZS, ZW, ZL, ZM (Tahıllar)
6E, 6J, 6B, 6A, 6C, 6S (Dövizler)

İZLEME DIŞI (bunları da sembol olarak kullan, çevirme):
XAUUSD, XAGUSD, EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF,
BTCUSD, ETHUSD, USOUSD, UKOIL, SPX500, NAS100, GER40, UK100, JP225,
DXY, VIX, US10Y, TSLA, AAPL, NVDA, MSFT, AMZN, GOOGL"""


PROMPT = """Aşağıdaki İngilizce finans makalesini Türkçe analiz et.

VARLIK LİSTESİ (sadece bu kodları kullan):
{product_list}

GÖREVLER:
1. Başlığı Türkçeye çevir → title_tr
2. İçeriği Türkçeye çevir (max 1500 karakter) → content_tr
3. Kısa Türkçe yorum (2-3 cümle) → yorum
4. Makalede geçen her varlık için analiz → varliklar
5. Genel yön (YUKARI/AŞAĞI/NÖTR) → genel_yon

ÇIKTI: SADECE JSON, başka metin yok:

{{
  "title_tr": "...",
  "content_tr": "...",
  "yorum": "...",
  "genel_yon": "YUKARI",
  "varliklar": [
    {{
      "sembol": "GC",
      "isim": "Altın",
      "yon": "YUKARI",
      "gerekce": "kısa gerekçe",
      "skor": 0.7
    }}
  ]
}}

KURALLAR:
- sembol listeden olmalı (GC, ES, 6E gibi)
- yon: YUKARI, AŞAĞI, NÖTR (büyük harf)
- skor: 0.0-1.0 arası ondalık (0.7 gibi)
- Makalede futures yoksa → "varliklar": []

BAŞLIK: {title}
İÇERİK: {content}
"""


def load_state():
    if not STATE_FILE.exists():
        return {"processed_ids": []}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"processed_ids": []}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def call_gemini(title, content):
    if not GEMINI_API_KEY:
        return {"hata": "GEMINI_API_KEY yok"}
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = PROMPT.format(
            product_list=PRODUCT_LIST,
            title=(title or "")[:500],
            content=(content or "")[:3000],
        )
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        if text.startswith("```"):
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
        text = text.strip()
        return json.loads(text)
    except Exception as e:
        return {"hata": str(e)}


def process_rss_files():
    state = load_state()
    processed = set(state.get("processed_ids", []))

    if not RSS_DIR.exists():
        print(f"RSS klasörü yok: {RSS_DIR}")
        return

    files = sorted(RSS_DIR.glob("rss_*.json"))
    print(f"Toplam {len(files)} dosya")

    new_count = 0
    skip_count = 0
    err_count = 0

    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [ERR] {fp.name}: {e}")
            continue

        is_list = isinstance(data, list)
        items = data if is_list else [data]
        updated = False

        for item in items:
            rss_id = item.get("id") or item.get("guid") or ""
            if not rss_id:
                continue

            if rss_id in processed and item.get("title_tr"):
                skip_count += 1
                continue

            title = item.get("title") or item.get("title_en") or ""
            content = item.get("content") or item.get("content_en") or item.get("summary") or ""

            if not title or not content:
                continue

            print(f"  -> {(title or '')[:60]}...")
            result = call_gemini(title, content)

            if "hata" in result:
                print(f"     [HATA] {result['hata'][:100]}")
                err_count += 1
                continue

            item["title_tr"] = result.get("title_tr", "") or ""
            item["content_tr"] = result.get("content_tr", "") or ""
            item["yorum"] = result.get("yorum", "") or ""
            item["genel_yon"] = result.get("genel_yon", "NÖTR")
            item["varliklar"] = result.get("varliklar", []) or []
            item["translated_at"] = datetime.now(timezone.utc).isoformat()

            processed.add(rss_id)
            new_count += 1
            updated = True
            time.sleep(WAIT_SECONDS)

        if updated:
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(items if is_list else items[0], f, ensure_ascii=False, indent=2)

    state["processed_ids"] = list(processed)
    save_state(state)
    print(f"\nOK. Yeni: {new_count}, Atlandi: {skip_count}, Hata: {err_count}")


if __name__ == "__main__":
    print("=" * 60)
    print("Translate RSS (v3)")
    print("=" * 60)
    process_rss_files()