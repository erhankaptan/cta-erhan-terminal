"""
CTA ERHAN KARAR MOTORU — Signal Engine
=======================================
Faz 2A sinyal uretim motoru.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from core.signals_db import global_signals_db
from sources.trend_loader import get_trend_data
from sources.cot_extremity import get_cot_extremity


# ============================================================
# SABITLER (HIPOTEZ — backtest ile kalibre edilecek)
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"

# DUZELTME (2026-10-28, Reis'in "ZS GUCLU AL diyor ama fiyat gunlerdir
# dusuyor" raporu sonrasi, KAPSAMLI ELDEN GECIRME): bu motor onceden SADECE
# pozisyonlama (COT) + haber sentimenti (Radar) + makale sentimenti
# (Tickmill) kullaniyordu. UCUNDE DE gercek fiyat hareketine bakan tek bir
# bit yoktu. Artik CTA Terminal'in (C:\cta_terminal) zaten canli urettigi,
# gercek fiyattan hesaplanmis EWMAC trend verisi (sources/trend_loader.py)
# 4. bilesen olarak ekleniyor. TREND'in payi bilerek COT ile esit/yakin
# tutuldu -- cunku COT gecmise donuk bir pozisyon fotografi, TREND ise
# "fiyat SU AN ne yapiyor" sorusunun dogrudan cevabi; ikisi de onemli,
# biri digerini bastirmamali.
WEIGHTS_DEFAULT = {"COT": 0.35, "Radar": 0.25, "Tickmill": 0.10, "Trend": 0.30}
WEIGHTS_COT_FRESH = {"COT": 0.40, "Radar": 0.20, "Tickmill": 0.10, "Trend": 0.30}
# TREND verisi o an bayat/yoksa (CTA Terminal calismiyorsa), payi orantili
# olarak digerlerine geri dagitiyoruz -- sistem TREND'siz de calismaya
# devam etsin (eski davranisa yakin, ama artik momentum/celiski kontrolleri
# hala aktif).
WEIGHTS_NO_TREND_DEFAULT = {"COT": 0.50, "Radar": 0.35, "Tickmill": 0.15}
WEIGHTS_NO_TREND_COT_FRESH = {"COT": 0.60, "Radar": 0.25, "Tickmill": 0.15}

THRESHOLD_STRONG = 0.60
THRESHOLD_NORMAL = 0.25
CONFIDENCE_MIN = 55.0
CONFIDENCE_STRONG = 75.0

CONFLICT_ABS_THRESHOLD = 0.45
CONFLICT_PENALTY = 0.70
WEAK_CONFLICT_PENALTY = 0.85

# TREND ile pozisyonlama/sentiment bilesimi (COT+Radar+Tickmill) ters
# dustugunde devreye giren yeni koruma katmani. Reis'in yasadigi somut
# vaka (ZS: COT skoru +1.0 "GUCLU AL" derken EWMAC trend -1 yonlu, 4
# periyottur surmekte ve guclu (0.85) idi) tam olarak bunun icin var.
TREND_DIVERGENCE_STRENGTH_MIN = 0.30   # bu buyuklugun altindaki trend'e guvenilmez
TREND_DIVERGENCE_PERSISTENCE_SOFT = 2  # >=2 periyot: GUCLU AL/SAT yasak, sadece AL/SAT
TREND_DIVERGENCE_PERSISTENCE_HARD = 4  # >=4 periyot + guclu trend: direkt BEKLE
TREND_DIVERGENCE_CONFIDENCE_PENALTY = 0.65  # soft celiskide guven carpani

COT_FRESH_HOURS = 48
RADAR_TTL_HOURS = 4
TICKMILL_TTL_HOURS = 24
TREND_FRESH_HOURS = 36
COT_MAX_DAYS = 7

OFFLIST_CONFIDENCE_CAP = 60.0

# ============================================================
# X HESAPLARI (misterpuertas + juanjesusmontoy) -- 2026-10-28, Reis'in
# "sadece Wayne degil, o uc hesaptan gelen bilgiler de skora dahil olsun"
# talebi uzerine eklendi.
#
# misterpuertas: CTA'larin senaryo bazli beklenen akis TAHMINI (henuz
# gerceklesmemis, projeksiyon) -- bu yuzden Karar Motoru'na ana agirlik
# dagilimina katilan 5. bir "kaynak" olarak degil, hesaplanan skorun
# UZERINE hafif bir harman (blend) olarak ekleniyor. Boylece COT/Radar/
# Tickmill/Trend arasindaki zaten test edilmis denge bozulmuyor.
#
# juanjesusmontoy: SPX gamma rejimi (negatif/pozitif) YONLU bir sinyal
# DEGIL -- "piyasa su an ne kadar oynak/kirilgan" sorusunun cevabi. Bu
# yuzden skor degil, GUVEN CARPANI olarak kullaniliyor. Sadece ES icin
# gecerli (rapor SPX uzerine).
CTA_FLOW_PRODUCT_MAP = {"ES": "SP500", "NQ": "NASDAQ100", "RTY": "RUSSELL2000"}
CTA_FLOW_NORMALIZE_BN = 20.0   # HIPOTEZ: +-20 milyar $ = +-1.0 skor (backtest ile kalibre edilecek)
CTA_FLOW_BLEND_WEIGHT = 0.15   # ana skorun ne kadarinin CTA Flow'a verilecegi
CTA_FLOW_FRESH_HOURS = 7 * 24  # haftalik rapor, 7 gunden eskiyse bayat say

GAMMA_NEGATIVE_CONFIDENCE_MULT = 0.85  # negatif gamma rejimi: guveni kirp
GAMMA_POSITIVE_CONFIDENCE_MULT = 1.0   # pozitif gamma: notr (yapay sisirme yok)
GAMMA_FRESH_HOURS = 7 * 24

MAJOR_PRODUCTS = ["ES", "NQ", "CL", "GC", "6E"]


# ============================================================
# YARDIMCI
# ============================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_float(v, default: float = 0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _load_synthesis_snapshot() -> dict:
    f = SNAPSHOTS_DIR / "latest.json"
    if not f.exists():
        return {}
    try:
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}


# ============================================================
# SKOR TOPLAMA
# ============================================================

def _get_cot_data(product: str) -> Dict[str, Any]:
    """
    COT'un TUM yorumunu doner: skor + momentum + konsensus + non_reportable.
    DUZELTME (2026-10-28, Reis'in "ZS GUCLU AL diyor ama fiyat gunlerdir
    dusuyor" raporu sonrasi, kapsamli elden gecirme): oncesinde bu fonksiyon
    (eski adiyla get_cot_score) SADECE net pozisyon buyuklugunu donduruyordu;
    merkez_cot_loader.py'nin hesapladigi "momentum" (ZAYIFLIYOR/GUCLENIYOR/
    SABIT) ve "non_reportable" (ters indikator) alanlari hic okunmuyordu --
    sadece ekranda gosteriliyor, Karar Motoru'nun kendisine hic girmiyordu.
    Simdi hepsini tek seferde okuyup donduruyoruz ki compute_confidence()
    bunlari kullanabilsin.
    """
    out = {"score": 0.0, "momentum": "SABIT", "consensus": "BILINMIYOR",
           "non_reportable": "YOK"}
    try:
        from sources.evidence_pool import global_evidence_pool
        evs = [e for e in global_evidence_pool.get_evidence_for_product(product)
               if e.get("source_type") == "COT"]
        if not evs:
            return out

        # Kategorili kayitlari bul (MERKEZ), en yeni tarihli olani sec
        candidates = []
        for e in evs:
            meta = e.get("metadata") or {}
            if isinstance(meta, dict) and meta.get("categories"):
                candidates.append(e)

        if not candidates:
            return out

        # En yeni published_at'li kaydi sec
        candidates.sort(key=lambda x: x.get("published_at") or "", reverse=True)
        chosen = candidates[0]
        meta = chosen.get("metadata") or {}

        interp = meta.get("interpreter", {}) or {}
        out["momentum"] = interp.get("momentum", "SABIT")
        out["consensus"] = interp.get("consensus", "BILINMIYOR")
        out["non_reportable"] = interp.get("non_reportable", "YOK")

        # Fallback zinciri
        primary = interp.get("primary_category", "LEVERAGED_FUNDS")
        cats = meta.get("categories", {})

        fallback_order = [primary, "MANAGED_MONEY", "LEVERAGED_FUNDS",
                          "SWAP_DEALER", "OTHER_REPORTABLE", "OTHER_REPORTABLES"]

        net = 0.0
        for cat_name in fallback_order:
            cat = cats.get(cat_name, {})
            long_v = _safe_float(cat.get("long"))
            short_v = _safe_float(cat.get("short"))
            candidate_net = long_v - short_v
            if candidate_net != 0:
                net = candidate_net
                break

        # Hala sifirsa, ilk dolu kategoriyi al
        if net == 0.0:
            for cat_name, cat in cats.items():
                long_v = _safe_float(cat.get("long"))
                short_v = _safe_float(cat.get("short"))
                if long_v + short_v > 0:
                    net = long_v - short_v
                    break

        # DUZELTME (2026-11-12, Reis onayli, "COT: -1.000 her zaman boyle
        # mi cikiyor" sorusu sonrasi): ESKIDEN net sabit /200000.0'a
        # bolunuyordu -- bu TEK bir sayi, TUM urunler icin ayniydi. ES
        # gibi likit urunlerde Leveraged Funds net'i rutin olarak yuz
        # binlerce kontrat oldugu icin bu HER ZAMAN -1.000/+1.000'a
        # yapisiyordu (gercek bir -1..+1 olcek DEGIL, fiilen ikili/binary
        # bir sinyal gibi davraniyordu, urunler arasi KIYASLANAMAZDI).
        # Artik net, o urunun kendi toplam acik pozisyonuna (Open
        # Interest) oraniyla olceklendiriliyor -- urunler arasi adil,
        # dogrudan ve COT analizinde standart bir teknik ("net, OI'nin
        # % kaci" okumasi). OI yoksa/gecersizse (0, None, negatif), eski
        # /200000 formulune SESSIZCE/GUVENLI sekilde dusuyoruz (davranis
        # asla patlamaz, sadece daha kaba bir tahmine doner).
        #
        # BILINCLI SINIR: bu YON/buyukluk skorudur, EKSTREMITE (bugunku
        # pozisyonun urunun KENDI son haftalarina gore ne kadar gergin
        # oldugu) DEGILDIR -- o ayri bir olcum (bkz. sources/cot_extremity.py)
        # ve KARAR MOTORU'nun ana skoruna BILINCLI olarak KARISTIRILMAZ
        # (composite-score yasagi, CTA Terminal'deki LOCKED kuralla ayni
        # disiplin).
        oi = _safe_float(meta.get("open_interest"))
        if oi and oi > 0:
            out["score"] = max(-1.0, min(1.0, net / oi))
        else:
            out["score"] = max(-1.0, min(1.0, net / 200000.0))

        return out
    except Exception:
        return out


def get_cot_score(product: str) -> float:
    """COT skoru -1..+1 (LEVERAGED_FUNDS / MANAGED_MONEY net'inden)."""
    return _get_cot_data(product)["score"]


def get_cot_extremity_info(product: str) -> Dict[str, Any]:
    """COT pozisyonunun kendi gecmisine gore ekstremite bilgisini doner
    (bkz. sources/cot_extremity.py docstring'i) -- KARAR MOTORU skoruna
    KARISMAZ, sadece ekranda ayri baglam/uyari olarak gosterilir. Hicbir
    durumda exception firlatmaz."""
    try:
        return get_cot_extremity(product)
    except Exception:
        return {"extremity_level": None, "weeks_available": 0,
                "status": "YETERSIZ", "current_report_date": None}


def get_cot_momentum(product: str) -> str:
    """COT'un hafta-ustu-hafta momentumu: GUCLENIYOR / ZAYIFLIYOR / SABIT."""
    return _get_cot_data(product)["momentum"]


def get_radar_score(product: str) -> float:
    """Radar skoru -0.75..+0.75 (synthesis snapshot'tan)."""
    snap = _load_synthesis_snapshot()
    results = snap.get("results", {})
    r = results.get(product) or results.get(product.upper())
    if not r:
        return 0.0
    score = _safe_float(r.get("score"))
    return max(-0.75, min(0.75, score))


def get_tickmill_score(product: str) -> float:
    """
    Tickmill RSS'ten sentiment skoru (-1..+1).
    data/rss/*.json dosyalarindan okur (GitHub Actions zaten cekiyor).

    DUZELTME (2026-10-28, Reis'in "Tickmill skorlamasi cok onemli, en saglam
    nasil olur" talebi sonrasi): Rapor icerikleri incelendi, 3 sorun bulundu
    ve duzeltildi:
      1) data/rss/rss_latest.json adinda, icerigi 2 hafta bayat (9-14 Ekim)
         bir dosya "latest" isminden dolayi alfabetik siralamada hep ilk
         sirada geliyordu, "son 10 dosya" penceresinin bir slotunu bosa
         harciyordu -- glob deseni artik bu dosyayi disliyor, sadece
         rss_YYYYMMDD_HHMMSS.json formatindaki gercek tarihli dosyalari aliyor.
      2) Bazi Tickmill makaleleri ("USDCHF H4 | Bearish momentum building" gibi
         teknik setup raporlari) govde metninde ACIK ve GUVENILIR bir
         "Type: Bullish/Bearish ..." alani iceriyor -- bu artik basit kelime
         sayimindan ONCE kontrol ediliyor ve bulunursa AGIRLIKLI/kesin sinyal
         olarak sayiliyor (kelime sayimina girmeden).
      3) "Top 5 Tips for Trading...", "Common Mistakes Traders Make..." gibi
         SAF EGITIM icerigi (yon tasimayan, evergreen makaleler) artik
         basliktan taninip TAMAMEN HARIC TUTULUYOR -- eskiden bunlar da
         kelime sayimina giriyordu, gurultu yaratiyordu.
      4) Basit bir OLUMSUZLAMA kontrolu eklendi -- "not bullish" gibi
         ifadelerde yakalanan kelimenin hemen oncesinde "not/no/despite/n't"
         gibi bir olumsuzlayici varsa oy TERS CEVRILIYOR.
      5) Baslikta gecen yon kelimeleri govdedekinden DAHA AGIRLIKLI sayiliyor
         (basliklar genelde net/kasitli, govde metin daha gurultulu).
    """
    import glob
    import json as _json
    import re as _re

    EGITIM_ICERIK_DESENLERI = [
        "tips for trading", "common mistakes", "how to trade",
        "beginner's guide", "beginners guide", "guide to trading",
    ]
    TYPE_ALANI_RE = _re.compile(r"type:\s*(bullish|bearish)", _re.IGNORECASE)
    OLUMSUZLAYICILAR = ["not ", "no ", "n't ", "despite ", "fails to ", "unable to "]

    def _olumsuzlanmis_mi(text: str, kelime: str, konum: int) -> bool:
        pencere_baslangic = max(0, konum - 25)
        pencere = text[pencere_baslangic:konum]
        return any(o in pencere for o in OLUMSUZLAYICILAR)

    def _agirlikli_say(text: str, kelime_listesi: list, agirlik: float) -> float:
        toplam = 0.0
        for kelime in kelime_listesi:
            for m in _re.finditer(_re.escape(kelime), text):
                oy = -agirlik if _olumsuzlanmis_mi(text, kelime, m.start()) else agirlik
                toplam += oy
        return toplam

    # Ürün → keyword eşlemesi
    PRODUCT_KEYWORDS = {
        "ES": ["s&p 500", "s&p500", "sp500", "spx", "e-mini s&p", "s&p"],
        "NQ": ["nasdaq", "ndx", "nas100"],
        "YM": ["dow", "djia", "us30"],
        "RTY": ["russell", "rut"],
        "NK": ["nikkei", "jp225"],
        "ZT": ["2-year", "2y note", "ust 2y"],
        "ZF": ["5-year", "5y note", "ust 5y"],
        "ZN": ["10-year", "10y note", "ust 10y", "us10y", "treasury"],
        "ZB": ["30-year", "30y bond", "ust bond"],
        "UB": ["ultra bond"],
        "ZQ": ["fed funds"],
        "6E": ["eurusd", "eur/usd", "euro", "eur "],
        "6J": ["usdjpy", "jpy", "yen"],
        "6B": ["gbpusd", "sterling", "cable", "gbp"],
        "6A": ["audusd", "aussie", "aud/usd", "aud "],
        "6C": ["usdcad", "loonie", "cad/usd", "cad "],
        "6N": ["nzdusd", "kiwi", "nzd"],
        "6S": ["usdchf", "swissy", "swiss franc", "chf"],
        "DXY": ["dxy", "dollar index", "us dollar"],
        "CL": ["crude", "wti", "oil"],
        "NG": ["natural gas", "natgas", "nat gas", "gas "],
        "HO": ["heating oil", "ulsd"],
        "RB": ["rbob", "gasoline"],
        "BZ": ["brent"],
        "GC": ["gold", "xauusd", "xau"],
        "SI": ["silver", "xagusd", "xag"],
        "HG": ["copper"],
        "PL": ["platinum"],
        "PA": ["palladium"],
        "ZC": ["corn"],
        "ZS": ["soybean"],
        "ZW": ["wheat"],
        "ZM": ["soybean meal"],
        "ZL": ["soybean oil"],
        "KE": ["kansas wheat", "hrw"],
    }

    BULL = ["bullish", "buy", "long", "upside", "rally", "risk on",
            "constructive", "outperform", "overweight", "higher"]
    BEAR = ["bearish", "sell", "short", "downside", "selloff",
            "risk off", "defensive", "underweight", "caution", "lower"]

    try:
        # En son 10 RSS dosyasini oku (en yeni once). SADECE gercek tarihli
        # anlik-goruntu dosyalarini al (rss_YYYYMMDD_HHMMSS.json) --
        # "rss_latest.json" gibi tarihsiz/bayat arsiv dosyalarini DISLA,
        # cunku adi "latest" oldugu icin alfabetik siralamada hep ilk sirada
        # cikip gercek en-yeni-10 penceresinin bir slotunu bosa harciyordu.
        rss_files = sorted(
            glob.glob(str(DATA_DIR / "rss" / "rss_20*.json")), reverse=True
        )[:10]
        if not rss_files:
            return 0.0

        product_kw = PRODUCT_KEYWORDS.get(product, [])
        if not product_kw:
            return 0.0

        skor_toplam = 0.0
        for rss_file in rss_files:
            try:
                with open(rss_file, "r", encoding="utf-8") as f:
                    items = _json.load(f)
            except Exception:
                continue

            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue
                if item.get("source") != "Tickmill":
                    continue

                title = (item.get("title_en") or item.get("title_tr") or "").lower()
                content = (item.get("content_en") or item.get("content_tr") or "").lower()
                text = title + " " + content

                # Saf egitim/evergreen icerigi (yon tasimiyor) tamamen disla.
                if any(p in title for p in EGITIM_ICERIK_DESENLERI):
                    continue

                if not any(kw in text for kw in product_kw):
                    continue

                # 1. ONCELIK: yapilandirilmis "Type: Bullish/Bearish" alani --
                # en guvenilir sinyal, bulunursa kesin/agirlikli oy olarak say
                # ve bu makale icin kelime sayimina hic girme (cifte sayim
                # onlenir).
                type_eslesme = TYPE_ALANI_RE.search(content)
                if type_eslesme:
                    yon = type_eslesme.group(1).lower()
                    skor_toplam += 3.0 if yon == "bullish" else -3.0
                    continue

                # 2. Baslik kelimeleri govdedekinden daha agirlikli (baslik
                # genelde net/kasitli, govde metin daha gurultulu), basit
                # olumsuzlama kontroluyle birlikte.
                skor_toplam += _agirlikli_say(title, BULL, 2.0)
                skor_toplam -= _agirlikli_say(title, BEAR, 2.0)
                skor_toplam += _agirlikli_say(content, BULL, 1.0)
                skor_toplam -= _agirlikli_say(content, BEAR, 1.0)

        if skor_toplam == 0.0:
            return 0.0

        # -1..+1 araligina normalize et (agirlikli toplam her makalede en
        # fazla birkaç puan katabildigi icin, makul bir bolen ile sikistir).
        score = skor_toplam / (abs(skor_toplam) + 4.0)
        return max(-1.0, min(1.0, score))
    except Exception:
        return 0.0


def _file_age_hours(path: Path) -> float:
    try:
        mtime = path.stat().st_mtime
        return (datetime.now(timezone.utc).timestamp() - mtime) / 3600.0
    except Exception:
        return 999.0


def get_cta_flow_data(product: str) -> Dict[str, Any]:
    """
    misterpuertas'in CTA Flow senaryo tahmininden -1..+1 skor uretir.
    'xw_flat' (1 haftalik, 'duz kalirsa' baz senaryo) kullanilir -- en
    yakin vadeli ve en az spekulatif varsayim. Rapor ES/NQ/RTY disinda
    bir urun icin veri icermiyorsa veya urun bu uc harften biri degilse
    notr/UNAVAILABLE doner. ASLA exception firlatmaz.
    """
    out = {"score": 0.0, "freshness": "UNAVAILABLE", "age_hours": 999.0,
           "raw_flat_bn": None, "report_date": None}
    key = CTA_FLOW_PRODUCT_MAP.get(product.upper().strip())
    if not key:
        return out
    try:
        path = DATA_DIR / "latest_misterpuertas_analysis.json"
        if not path.is_file():
            return out
        age_hours = _file_age_hours(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entry = (data.get("products") or {}).get(key)
        if not entry:
            return out
        flat = entry.get("1w_flat")
        if flat is None:
            return out
        flat = _safe_float(flat)
        score = max(-1.0, min(1.0, flat / CTA_FLOW_NORMALIZE_BN))
        freshness = "OK" if age_hours <= CTA_FLOW_FRESH_HOURS else "STALE"
        out.update({
            "score": score, "freshness": freshness, "age_hours": round(age_hours, 2),
            "raw_flat_bn": flat, "report_date": data.get("report_date"),
        })
        return out
    except Exception:
        return out


def get_gamma_regime_data(product: str) -> Dict[str, Any]:
    """
    juanjesusmontoy'un haftalik SPX gamma raporundan rejim bilgisini
    doner. YONLU DEGIL -- sadece ES icin gecerli (rapor SPX uzerine) ve
    sadece GUVEN CARPANI olarak kullanilir (bkz. calculate_signal).
    ASLA exception firlatmaz.
    """
    out = {"regime": None, "freshness": "UNAVAILABLE", "age_hours": 999.0,
           "confidence_mult": 1.0, "put_wall": None, "call_wall": None,
           "gamma_flip": None, "spx_price": None, "report_date": None}
    if product.upper().strip() != "ES":
        return out
    try:
        path = DATA_DIR / "latest_montoya_analysis.json"
        if not path.is_file():
            return out
        age_hours = _file_age_hours(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        regime = data.get("regime")
        freshness = "OK" if age_hours <= GAMMA_FRESH_HOURS else "STALE"
        mult = 1.0
        if freshness == "OK":
            if regime == "negative":
                mult = GAMMA_NEGATIVE_CONFIDENCE_MULT
            elif regime == "positive":
                mult = GAMMA_POSITIVE_CONFIDENCE_MULT
        out.update({
            "regime": regime, "freshness": freshness, "age_hours": round(age_hours, 2),
            "confidence_mult": mult, "put_wall": data.get("put_wall"),
            "call_wall": data.get("call_wall"), "gamma_flip": data.get("gamma_flip"),
            "spx_price": data.get("spx_price"), "report_date": data.get("report_date"),
        })
        return out
    except Exception:
        return out


# ============================================================
# CELISKI
# ============================================================

def detect_conflict(cot_score: float, radar_score: float) -> tuple:
    if (abs(cot_score) > CONFLICT_ABS_THRESHOLD and
        abs(radar_score) > CONFLICT_ABS_THRESHOLD and
        cot_score * radar_score < 0):
        return True, ["COT", "Radar"], CONFLICT_PENALTY
    if cot_score * radar_score < 0:
        return False, ["COT", "Radar"], WEAK_CONFLICT_PENALTY
    return False, [], 1.0


def detect_trend_divergence(sentiment_composite: float, trend_data: dict) -> tuple:
    """
    YENI (2026-10-28): COT+Radar+Tickmill'in birlesik yonu (pozisyonlama +
    sentiment -- geriye donuk/haber tabanli) ile EWMAC fiyat trendinin
    (su anki gercek fiyat hareketi) ters dustugu durumu yakalar.

    Reis'in yasadigi somut vaka: ZS'de COT skoru +1.0 (GUCLU AL diyordu)
    AMA EWMAC trend yonu -1, 4 periyottur suruyordu ve buyuklugu 0.85
    (guclu). Bu fonksiyon boyle bir durumu "HARD" olarak etiketleyip
    calculate_signal() icinde sinyali BEKLE'ye zorluyor.

    Doner: (seviye, confidence_carpani)
      seviye: "NONE" | "WEAK" | "SOFT" | "HARD"
      NONE  -> trend yok/guvenilmez/ayni yonde, mudahale yok (carpan 1.0)
      WEAK  -> celisik ama trend henuz kisa surmus/zayif, hafif penaltı
      SOFT  -> celisik + trend >=2 periyottur suruyor -> GUCLU AL/SAT yasak
      HARD  -> celisik + trend >=4 periyottur suruyor + guclu -> BEKLE'ye zorla
    """
    direction = trend_data.get("direction", 0)
    strength = trend_data.get("strength", 0.0)
    persistence = trend_data.get("persistence", 0)
    freshness = trend_data.get("freshness", "UNAVAILABLE")

    if freshness != "OK" or direction == 0 or strength < TREND_DIVERGENCE_STRENGTH_MIN:
        return "NONE", 1.0

    sentiment_sign = 1 if sentiment_composite > 0 else (-1 if sentiment_composite < 0 else 0)
    if sentiment_sign == 0 or sentiment_sign == direction:
        return "NONE", 1.0

    if persistence >= TREND_DIVERGENCE_PERSISTENCE_HARD and strength >= 0.5:
        return "HARD", 0.0
    if persistence >= TREND_DIVERGENCE_PERSISTENCE_SOFT:
        return "SOFT", TREND_DIVERGENCE_CONFIDENCE_PENALTY
    return "WEAK", 0.85


# ============================================================
# SKOR
# ============================================================

def compute_weighted_score(cot_score, radar_score, tickmill_score, trend_score,
                           cot_age_hours=999, trend_freshness="UNAVAILABLE"):
    trend_ok = trend_freshness == "OK"
    if trend_ok:
        weights = (WEIGHTS_COT_FRESH if cot_age_hours <= COT_FRESH_HOURS
                   else WEIGHTS_DEFAULT).copy()
        raw = (weights["COT"] * cot_score +
               weights["Radar"] * radar_score +
               weights["Tickmill"] * tickmill_score +
               weights["Trend"] * trend_score)
    else:
        weights = (WEIGHTS_NO_TREND_COT_FRESH if cot_age_hours <= COT_FRESH_HOURS
                   else WEIGHTS_NO_TREND_DEFAULT).copy()
        weights = dict(weights, Trend=0.0)
        raw = (weights["COT"] * cot_score +
               weights["Radar"] * radar_score +
               weights["Tickmill"] * tickmill_score)
    return raw, weights


def compute_confidence(cot_score, radar_score, tickmill_score, is_conflict,
                       cot_age_hours, radar_age_hours, tickmill_age_hours,
                       non_rep_confirms=False, cot_momentum="SABIT",
                       trend_divergence_penalty=1.0):
    signs = [
        1 if cot_score > 0 else (-1 if cot_score < 0 else 0),
        1 if radar_score > 0 else (-1 if radar_score < 0 else 0),
        1 if tickmill_score > 0 else (-1 if tickmill_score < 0 else 0),
    ]
    nonzero = [s for s in signs if s != 0]
    if nonzero:
        dominant = max(set(nonzero), key=nonzero.count)
        uyum = nonzero.count(dominant) / 3.0
    else:
        uyum = 0.0

    kalite = 0.5
    if abs(cot_score) > 0.5:
        kalite += 0.2
    if abs(radar_score) > 0.4:
        kalite += 0.2
    if non_rep_confirms:
        kalite += 0.1
    # YENI: COT'un kendi hafta-ustu-hafta momentumu artik hesaba katiliyor.
    # Onceden bu bilgi sadece ekranda duruyordu -- buyuk ama ZAYIFLAYAN bir
    # pozisyon yuksek "kalite" puani alip gercekte oldugundan daha guvenilir
    # gorunuyordu.
    if cot_momentum == "ZAYIFLIYOR":
        kalite -= 0.15
    elif cot_momentum == "GUCLENIYOR":
        kalite += 0.05
    kalite = max(0.0, min(1.0, kalite))

    tazelik = 1.0
    if cot_age_hours > COT_FRESH_HOURS:
        tazelik -= 0.2
    if radar_age_hours > RADAR_TTL_HOURS:
        tazelik -= 0.3
    if tickmill_age_hours > TICKMILL_TTL_HOURS:
        tazelik -= 0.2
    tazelik = max(0.0, tazelik)

    celiski = 1.0 if is_conflict else 0.0

    conf = (0.40 * uyum + 0.30 * kalite + 0.20 * tazelik + 0.10 * (1 - celiski)) * 100.0
    # YENI: TREND ile sentiment bilesimi celisiyorsa guveni ayrica kirp.
    conf *= trend_divergence_penalty
    return round(conf, 1)


def classify_signal(score: float, confidence: float, trend_divergence: str = "NONE") -> str:
    if confidence < CONFIDENCE_MIN:
        return "BEKLE"
    # YENI: TREND ile celiski HARD ise -- yani fiyat, sentiment'in tam
    # tersine, guclu ve kalici bir trendle gidiyorsa -- hicbir skor/guven
    # kombinasyonu bunu "AL/SAT"a cevirmesin, direkt BEKLE.
    if trend_divergence == "HARD":
        return "BEKLE"
    if score >= THRESHOLD_STRONG and confidence >= CONFIDENCE_STRONG:
        # SOFT celiskide (trend >=2 periyottur ters yonde) "GUCLU" etiketi
        # yasak -- en fazla normal AL/SAT.
        if trend_divergence == "SOFT":
            return "AL"
        return "GÜÇLÜ AL"
    if score >= THRESHOLD_NORMAL:
        return "AL"
    if score <= -THRESHOLD_STRONG and confidence >= CONFIDENCE_STRONG:
        if trend_divergence == "SOFT":
            return "SAT"
        return "GÜÇLÜ SAT"
    if score <= -THRESHOLD_NORMAL:
        return "SAT"
    return "BEKLE"


def classify_signal_type(weights: dict) -> tuple:
    cot_w = weights.get("COT", 0)
    radar_w = weights.get("Radar", 0)
    if cot_w > 0.40 and radar_w <= 0.30:
        return "cot_based", "cot", "until_new_cot"
    if radar_w > 0.30 and cot_w <= 0.45:
        return "radar_based", "radar", "4h"
    return "mixed", "cot", "mixed"


# ============================================================
# ANA FONKSIYON
# ============================================================

def calculate_signal(product, *, is_offlist=False, price_at_signal=None,
                     atr_at_signal=None, cot_age_hours=0.0, radar_age_hours=0.0,
                     tickmill_age_hours=0.0, non_rep_confirms=False):
    product = product.upper().strip()

    cot_score = get_cot_score(product)
    cot_momentum = get_cot_momentum(product)
    radar_score = get_radar_score(product)
    tickmill_score = get_tickmill_score(product)
    trend_data = get_trend_data(product)
    trend_score = trend_data["score"]

    is_conflict, conflict_sources, penalty = detect_conflict(cot_score, radar_score)

    raw_score, weights = compute_weighted_score(
        cot_score, radar_score, tickmill_score, trend_score,
        cot_age_hours=cot_age_hours, trend_freshness=trend_data["freshness"])

    # YENI: TREND, sentiment bilesiminin (COT+Radar+Tickmill, agirliksiz
    # -- sadece YON icin) tam tersini, guclu ve kalici sekilde gosteriyorsa
    # tespit et. Reis'in ZS vakasi tam olarak buydu.
    sentiment_composite = cot_score + radar_score + tickmill_score
    trend_divergence, trend_penalty = detect_trend_divergence(sentiment_composite, trend_data)

    # YENI (2026-10-28): misterpuertas'in CTA Flow senaryo tahmini --
    # sadece ES/NQ/RTY icin ve sadece taze veri varsa, ana skorun uzerine
    # hafif bir harman (blend) olarak ekleniyor. Ana COT/Radar/Tickmill/
    # Trend dengesini bozmamak icin AGIRLIK DAGILIMINA degil, sonuc
    # skora ekleniyor.
    cta_flow_data = get_cta_flow_data(product)
    if cta_flow_data["freshness"] == "OK":
        raw_score = (raw_score * (1 - CTA_FLOW_BLEND_WEIGHT) +
                     cta_flow_data["score"] * CTA_FLOW_BLEND_WEIGHT)
        raw_score = max(-1.0, min(1.0, raw_score))

    if is_conflict:
        raw_score = 0.0
    final_score = raw_score

    confidence = compute_confidence(cot_score, radar_score, tickmill_score,
                                    is_conflict, cot_age_hours, radar_age_hours,
                                    tickmill_age_hours, non_rep_confirms,
                                    cot_momentum=cot_momentum,
                                    trend_divergence_penalty=trend_penalty)
    confidence = confidence * penalty

    # YENI (2026-10-28): juanjesusmontoy'un SPX gamma rejimi -- YONLU
    # DEGIL, sadece ES icin bir guven carpani. Negatif gamma = piyasa daha
    # kirilgan/oynak = sinyale daha az guven.
    gamma_data = get_gamma_regime_data(product)
    if gamma_data["freshness"] == "OK":
        confidence = confidence * gamma_data["confidence_mult"]

    if is_offlist:
        confidence = min(confidence, OFFLIST_CONFIDENCE_CAP)
    confidence = round(confidence, 1)

    signal = classify_signal(final_score, confidence, trend_divergence=trend_divergence)
    signal_type, primary_source, validity_reason = classify_signal_type(weights)

    now = datetime.now(timezone.utc)
    if signal_type == "cot_based":
        expires = now + timedelta(days=COT_MAX_DAYS)
    elif signal_type == "radar_based":
        expires = now + timedelta(hours=RADAR_TTL_HOURS)
    else:
        expires = min(now + timedelta(hours=RADAR_TTL_HOURS),
                      now + timedelta(days=COT_MAX_DAYS))

    return {
        "product": product,
        "signal": signal,
        "raw_score": round(raw_score, 4),
        "final_score": round(final_score, 4),
        "confidence": confidence,
        "cot_score": round(cot_score, 4),
        "cot_momentum": cot_momentum,
        "radar_score": round(radar_score, 4),
        "tickmill_score": round(tickmill_score, 4),
        "trend_score": round(trend_score, 4),
        "trend_direction": trend_data["direction"],
        "trend_persistence": trend_data["persistence"],
        "trend_freshness": trend_data["freshness"],
        "trend_divergence": trend_divergence,
        "cta_flow_score": cta_flow_data["score"] if cta_flow_data["freshness"] == "OK" else None,
        "cta_flow_freshness": cta_flow_data["freshness"],
        "gamma_regime": gamma_data["regime"] if gamma_data["freshness"] == "OK" else None,
        "gamma_confidence_mult": gamma_data["confidence_mult"] if gamma_data["freshness"] == "OK" else 1.0,
        "gamma_levels": {"put_wall": gamma_data["put_wall"], "gamma_flip": gamma_data["gamma_flip"],
                         "call_wall": gamma_data["call_wall"]} if gamma_data["freshness"] == "OK" else None,
        "weights_used": weights,
        "is_conflict": is_conflict,
        "conflict_sources": conflict_sources,
        "signal_type": signal_type,
        "primary_source": primary_source,
        "validity_reason": validity_reason,
        "price_at_signal": price_at_signal,
        "atr_at_signal": atr_at_signal,
        "created_at": now.isoformat(),
        "expires_at": expires.isoformat(),
        "independent_evidence_count": 4 - (1 if is_conflict else 0) - (1 if trend_data["freshness"] != "OK" else 0),
        "source_ages": {"COT": cot_age_hours, "Radar": radar_age_hours,
                        "Tickmill": tickmill_age_hours, "Trend": trend_data["age_hours"]},
    }


def calculate_and_log(product: str, **kwargs) -> Dict[str, Any]:
    sig = calculate_signal(product, **kwargs)
    sig["signal_id"] = global_signals_db.log_signal(sig)
    return sig


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Signal Engine Test")
    print("=" * 60)
    for product in MAJOR_PRODUCTS:
        sig = calculate_signal(product)
        print(f"\n[{product}] {sig['signal']} | Guven %{sig['confidence']}")
        print(f"  Skor: {sig['final_score']:+.4f}")
        print(f"  COT: {sig['cot_score']:+.3f} | Radar: {sig['radar_score']:+.3f} | Tickmill: {sig['tickmill_score']:+.3f}")
        print(f"  Tip: {sig['signal_type']} | Validity: {sig['validity_reason']}")
        print(f"  Celiski: {sig['is_conflict']} {sig['conflict_sources']}")
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
def apply_wayne_handbook_rules(raw_asset_data: dict) -> dict:
    """
    Erhan'ın 'Kurumsal Akış ve Swing Ticaret Başucu El Kitabı' kurallarını uygular.
    """
    ticker = raw_asset_data.get("ticker", "UNKNOWN")
    asset_name = raw_asset_data.get("asset_name", ticker)
    
    raw_flow = raw_asset_data.get("net_flow_1w")
    if raw_flow is None:
        return {
            "ticker": ticker, "asset_name": asset_name, "direction": "INSUFFICIENT", "score": 0.0,
            "net_flow_1w": 0, "return_1w": 0, "oi_change": 0, "oi_corr": 0,
            "status_tags": ["⚠️ YETERSIZ VERI / OKUNAMADI"],
            "protocol_note": "Görselden veri okunamadı, işlem yapılmaz."
        }

    try:
        net_flow_1w = float(raw_flow)
        net_flow_4w = float(raw_asset_data.get("net_flow_4w") or 0.0)
        return_1w = float(raw_asset_data.get("return_1w") or 0.0)
        oi_change = float(raw_asset_data.get("oi_change") or 0.0)
        oi_corr = float(raw_asset_data.get("oi_corr") or 0.0)
    except (ValueError, TypeError):
        return {
            "ticker": ticker, "asset_name": asset_name, "direction": "INSUFFICIENT", "score": 0.0,
            "net_flow_1w": 0, "return_1w": 0, "oi_change": 0, "oi_corr": 0,
            "status_tags": ["⚠️ PARSE HATASI"], "protocol_note": "Hatalı veri formattı."
        }

    # 1. PATRON SÜTUN: 1w Net Flow
    # DUZELTME (2026-10-28, Reis'in onayiyla): esik 0.3 -> 0.5. El Kitabi'nin
    # kendi 1. bolumu -0.5/+0.5 arasini "nötr/zayif akis, kurumsal para henuz
    # kararsiz, acele etme" olarak tanimliyordu; eski 0.3 esigi bu bekleme
    # disiplinini bosa cikariyordu (kararsiz bolgede bile yon karari veriyordu).
    if net_flow_1w >= 0.5:
        direction = "BULLISH"
        score = min(1.0, net_flow_1w / 1.5)
    elif net_flow_1w <= -0.5:
        direction = "BEARISH"
        score = max(-1.0, net_flow_1w / 1.5)
    else:
        direction = "NEUTRAL"
        score = 0.0

    # 2. KURUMSAL BASKI / AŞIRI AKIŞ (|z| >= 1.0)
    is_extreme_flow = abs(net_flow_1w) >= 1.0

    # 3. DİVERJANS / DİP TUZAĞI (Fiyat eksi, Akış artı)
    is_dip_opportunity = (return_1w < 0.0) and (net_flow_1w >= 0.5)
    
    # 4. LİKİDİTE TEMİZLİĞİ / STOP HUNT (OI Change eksi)
    is_stop_hunt_warning = oi_change < 0.0

    # 5. GÜVEN DERECESİ VE MANİPÜLASYON (15/30 Eşikleri)
    abs_corr = abs(oi_corr)
    if abs_corr >= 30:
        confidence = "YÜKSEK (Teknik Seviyelere Saygılı)"
        is_manipulation_risk = False
    elif abs_corr < 15:
        confidence = "DÜŞÜK (Manipülasyon/Stop Avı)"
        is_manipulation_risk = True
    else:
        confidence = "ORTA"
        is_manipulation_risk = False

    # ROZETLER
    status_tags = []
    if is_dip_opportunity: status_tags.append("🔥 DİP TUZAĞI (ALIM FIRSATI)")
    if is_stop_hunt_warning: status_tags.append("⚠️ STOP HUNT / LİKİDİTE İĞNESİ BEKLENİYOR")
    if is_extreme_flow: status_tags.append("🌊 AŞIRI AKIŞ (TREND KARŞITI İŞLEM ALMA)")
    if is_manipulation_risk: status_tags.append("⚡ MANİPÜLASYON BÖLGESİ (GENİŞ STOP BIRAK)")

    return {
        "ticker": ticker, "asset_name": asset_name, "direction": direction, "score": score,
        "net_flow_1w": net_flow_1w, "net_flow_4w": net_flow_4w, "return_1w": return_1w,
        "oi_change": oi_change, "oi_corr": oi_corr, "is_dip_opportunity": is_dip_opportunity,
        "is_stop_hunt_warning": is_stop_hunt_warning, "confidence": confidence,
        "status_tags": status_tags,
        "protocol_note": "Pzt/Salı seans açılışını ve Stop Hunt iğnesini bekle. Bütün pozisyonları Cuma kapanışında kapat."
    }