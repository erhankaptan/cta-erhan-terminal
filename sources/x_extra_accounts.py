# sources/x_extra_accounts.py
"""
misterpuertas (Diego Puertas) ve juanjesusmontoy (JJ Montoya) X hesaplarindan
gelen icerigi okuyup yapilandirilmis veriye ceviren modul.

NEDEN BU DOSYA VAR (2026-10-28, Reis'in "sadece Wayne degil, o uc hesaptan
gelen bilgiler de skora dahil olsun" talebi sonrasi):

veri_cekici.py onceden bu iki hesabin son tweet'inde resim olup olmadigini
kontrol edip GECIYORDU -- hicbir icerik cikarilmiyor, hicbir yere
kaydedilmiyordu. Artik ikisi de islenip Karar Motoru'na girdi oluyor.

ICERIK TURLERI (Reis'in gonderdigi ornek gorsellerden):
  - misterpuertas: "Expected CTA Flows by Scenario" bar grafikleri --
    S&P 500 / Nasdaq 100 / Russell 2000 icin senaryo bazli (1W Flat tape,
    1W Up 2SD, 1W Down 2.5SD, 1M varyantlari, Realized last week/month)
    CTA akis TAHMINI ($ milyar, negatif=satis/bearish baski, pozitif=
    alim/bullish baski).
  - juanjesusmontoy: haftalik SPX gamma/opsiyon raporu -- Put Wall,
    Gamma Flip, Call Wall seviyeleri, VIX, gamma rejimi (negatif/pozitif).
    Bu YONLU bir sinyal degil, bir OYNAKLIK REJIMI / seviye haritasi --
    o yuzden Karar Motoru'na dogrudan yon olarak degil, GUVEN CARPANI
    olarak besleniyor (bkz. core/signal_engine.py).

HER IKI HESAP DA bazen gorsel (grafik/rapor fotografi), bazen duz metin
tweet paylasiyor -- bu yuzden her iki yol icin de ayri cikarim fonksiyonu
var (resim varsa Gemini Vision OCR, yoksa Gemini'ye duz metin veriliyor).

GUVENLIK: Bu modul CTA ERHAN TERMINAL.bat uzerinden calisan veri_cekici.py
tarafindan cagrilir. Kendi basina hicbir seyi otomatik calistirmaz.
"""
from __future__ import annotations

import calendar
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
_client: Optional[genai.Client] = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not _GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY tanimli degil (.env kontrol et).")
        _client = genai.Client(api_key=_GEMINI_API_KEY)
    return _client


# ============================================================
# ORTAK YARDIMCILAR
# ============================================================

def pick_latest_entry(entries: List[dict], max_scan: int = 20) -> Optional[dict]:
    """
    nitter RSS girdileri yayin SAATINE gore DEGIL kendi ic sirasina gore
    geliyor (Wayne vakasinda dogrulandi) -- bu yuzden burada da entries[0]'a
    degil, ilk `max_scan` girdiyi tarayip gercekten EN YENI YAYIN TARIHLI
    olani seciyoruz.
    """
    adaylar = []
    for entry in entries[:max_scan]:
        published_struct = entry.get("published_parsed")
        epoch = calendar.timegm(published_struct) if published_struct else 0
        adaylar.append((epoch, entry))
    if not adaylar:
        return None
    adaylar.sort(key=lambda t: t[0], reverse=True)
    return adaylar[0][1]


def _extract_image_url(entry: dict) -> Optional[str]:
    summary = entry.get("summary", "") or ""
    matches = re.findall(r'<img src="([^"]+)"', summary)
    return matches[0] if matches else None


def _download_image(image_url: str) -> bytes:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    if image_url.startswith("/"):
        image_url = "https://nitter.meowing.monster" + image_url
    resp = requests.get(image_url, headers=headers, stream=True, timeout=20)
    resp.raise_for_status()
    return resp.content


def _strip_html(raw_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw_html or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clean_json(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()


def _gemini_vision_json(image_bytes: bytes, prompt: str) -> dict:
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt,
        ],
    )
    return json.loads(_clean_json(response.text))


def _gemini_text_json(text: str, prompt: str) -> dict:
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[f"{prompt}\n\nTWEET METNI:\n{text}"],
    )
    return json.loads(_clean_json(response.text))


# ============================================================
# MISTERPUERTAS -- CTA Flow by Scenario
# ============================================================

MISTERPUERTAS_PROMPT = """
Sen bir finansal grafik OCR uzmanisin. Bu gorsel "Expected CTA Flows by
Scenario" basligi altinda, CTA (trend-takip) fonlarinin senaryo bazli
beklenen alim/satim akis TAHMINLERINI gosteren bar grafikleridir
($ milyar cinsinden; NEGATIF = CTA satisi/bearish baski, POZITIF =
CTA alimi/bullish baski). Panel basliklari genelde "S&P 500",
"Nasdaq 100", "Russell 2000" gibi urun isimleridir. X ekseninde su
senaryo etiketleri olur: "1W Flat tape", "1W Up 2 SD", "1W Down 2.5 SD",
"1M Flat tape", "1M Up 2 SD", "1M Down 2.5 SD", "Realized: last week",
"Realized: last month" (etiketler grafikten grafige hafif degisebilir,
en yakinini esle).

SADECE gecerli bir JSON dondur, ekstra metin/markdown EKLEME:
{
  "report_date": "YYYY-MM-DD veya null (grafikte/baslikta tarih varsa)",
  "products": {
    "SP500": {"1w_flat": -11.6, "1w_up2sd": null, "1w_down25sd": -65.0,
              "1m_flat": null, "1m_up2sd": null, "1m_down25sd": null,
              "realized_last_week": null, "realized_last_month": null},
    "NASDAQ100": { ... ayni alanlar ... },
    "RUSSELL2000": { ... ayni alanlar ... }
  }
}
Okuyamadigin/gormedigin degerler icin null ver, UYDURMA. Grafikte olmayan
bir urun panelini hic ekleme.
"""

MISTERPUERTAS_TEXT_PROMPT = """
Asagidaki tweet metni CTA (trend-takip) fon akislariyla ilgili. Eger
spesifik bir $ rakami veya senaryo (1 haftalik/1 aylik beklenen akis gibi)
geciyorsa SADECE asagidaki JSON semasina gore cikar, gecmiyorsa tum
degerleri null birak:
{
  "report_date": null,
  "products": {
    "SP500": {"1w_flat": null, "1w_up2sd": null, "1w_down25sd": null,
              "1m_flat": null, "1m_up2sd": null, "1m_down25sd": null,
              "realized_last_week": null, "realized_last_month": null}
  },
  "free_text_summary": "varsa tweetin 1 cumlelik ozeti, yoksa null"
}
SADECE JSON dondur.
"""


def process_misterpuertas_entry(entry: dict) -> Optional[dict]:
    """Tek bir misterpuertas tweet girdisini isler, yapilandirilmis veri doner."""
    image_url = _extract_image_url(entry)
    try:
        if image_url:
            image_bytes = _download_image(image_url)
            data = _gemini_vision_json(image_bytes, MISTERPUERTAS_PROMPT)
        else:
            text = _strip_html(entry.get("summary", ""))
            if not text:
                return None
            data = _gemini_text_json(text, MISTERPUERTAS_TEXT_PROMPT)
        data["source_tweet_title"] = entry.get("title", "")
        data["source_published"] = entry.get("published", "")
        data["had_image"] = bool(image_url)
        return data
    except Exception as e:
        print(f"HATA: misterpuertas isleme basarisiz -> {e}")
        return None


# ============================================================
# JUANJESUSMONTOY -- Haftalik SPX Gamma Raporu
# ============================================================

MONTOYA_PROMPT = """
Sen bir finansal opsiyon/gamma raporu analistisin. Bu gorsel SPX ile
ilgili haftalik bir gamma/volatilite raporudur (JJ Montoya tarzinda).
Rapordan su alanlari cikar:

SADECE gecerli bir JSON dondur, ekstra metin/markdown EKLEME:
{
  "report_date": "YYYY-MM-DD veya null",
  "spx_price": sayi veya null,
  "vix": sayi veya null,
  "gamma_flip": sayi veya null (Gamma Flip seviyesi),
  "put_wall": sayi veya null (Put Wall seviyesi),
  "call_wall": sayi veya null (Call Wall seviyesi),
  "regime": "negative" veya "positive" veya null (metinde "gamma negatif"/
            "negative gamma"/"gamma negativa" geciyorsa negative, "gamma
            pozitif"/"positive gamma"/"gamma positiva" geciyorsa positive),
  "summary_tr": "raporun 1-2 cumlelik Turkce ozeti"
}
Okuyamadigin alanlar icin null ver, UYDURMA.
"""

MONTOYA_TEXT_PROMPT = """
Asagidaki tweet metni SPX gamma/opsiyon piyasasiyla ilgili olabilir.
Metinden su alanlari cikarmaya calis, metinde yoksa null birak:
{
  "report_date": null,
  "spx_price": null,
  "vix": null,
  "gamma_flip": null,
  "put_wall": null,
  "call_wall": null,
  "regime": null,
  "summary_tr": "metnin 1-2 cumlelik Turkce ozeti, alakasizsa null"
}
SADECE JSON dondur.
"""


def process_montoya_entry(entry: dict) -> Optional[dict]:
    """Tek bir juanjesusmontoy tweet girdisini isler, yapilandirilmis veri doner."""
    image_url = _extract_image_url(entry)
    try:
        if image_url:
            image_bytes = _download_image(image_url)
            data = _gemini_vision_json(image_bytes, MONTOYA_PROMPT)
        else:
            text = _strip_html(entry.get("summary", ""))
            if not text:
                return None
            data = _gemini_text_json(text, MONTOYA_TEXT_PROMPT)
        data["source_tweet_title"] = entry.get("title", "")
        data["source_published"] = entry.get("published", "")
        data["had_image"] = bool(image_url)
        return data
    except Exception as e:
        print(f"HATA: juanjesusmontoy isleme basarisiz -> {e}")
        return None


# ============================================================
# KAYIT
# ============================================================

def save_misterpuertas_analysis(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / "latest_misterpuertas_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ misterpuertas analizi kaydedildi (data/latest_misterpuertas_analysis.json)")


def save_montoya_analysis(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / "latest_montoya_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ juanjesusmontoy analizi kaydedildi (data/latest_montoya_analysis.json)")
