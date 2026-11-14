# sources/trend_loader.py
"""
CTA Terminal / Kokboru export'undan EWMAC fiyat-trend verisini okur.

NEDEN BU DOSYA VAR (2026-10-28, Reis'in "ZS'de Karar Motoru GUCLU AL %77.7
diyor ama fiyat gunlerdir dusuyor" raporu sonrasi):

Karar Motoru (core/signal_engine.py) o ana kadar SADECE su ucunu
kullaniyordu: COT (pozisyonlama), Radar (haber sentimenti), Tickmill
(makale sentimenti). UCUNDE DE gercek fiyat hareketine -- "piyasa su an
ne yapiyor" sorusuna -- bakan tek bir bit yoktu. Bu yuzden COT'un
gecmiste (haftalar once) biriktirdigi buyuk bir pozisyon, fiyat o
pozisyonun kurulma nedenini coktan tersine cevirmis olsa bile hala
"GUCLU AL/SAT" diye bagirabiliyordu.

Cozum icin yeni bir fiyat/veri kaynagi ICAT ETMIYORUZ. Ayni makinede
zaten calisan, bagimsiz bir terminal olan CTA Terminal (C:\\cta_terminal)
her dongude Kokboru'ye besledigi export dosyasinin (cta_kokboru_export.json)
icinde her urun icin, gercek fiyattan (CME) hesaplanmis bir "TREND" domain'i
zaten var: EWMAC (fast-slow Exponentially Weighted Moving Average farkinin
isareti + normalize buyuklugu + kac periyottur surdugu "persistence").
Bu modul SADECE o veriyi okur ve Karar Motoru'nun anlayacagi -1..+1'lik
tek bir skora cevirir.

GUVENLIK: Bu dosya hicbir seye YAZMAZ, sadece okur. Dosya yoksa/bozuksa/
urun export'ta yoksa exception FIRLATMAZ -- notr/UNAVAILABLE bir sozluk
doner, Karar Motoru TREND'siz de (eski davranisina yakin sekilde)
calismaya devam eder.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# DUZELTME (2026-11-12, Reis'in "hepsi docker'da calisacak, bilgisayara
# bagimlilik kalmayacak" talimati): ESKIDEN bu yol C:\cta_terminal\
# cta_kokboru_export.json'a SABITTI -- native bir Windows yolu, Linux
# Docker container'i icinde ASLA var olamaz. Bu yuzden get_trend_data()
# hep "dosya yok" dallanip UNAVAILABLE donuyordu, ve KARAR MOTORU'nun
# Trend/EWMAC guvenlik mekanizmasi (2026-10-28'de ZS olayindan sonra
# EKLENMISTI) HICBIR ZAMAN calismiyordu -- "iki gundur piyasa cosuyor ama
# GUCLU SAT" gibi celiskili sinyalleri yakalayamiyordu.
#
# CTA Terminal (ayri bir Docker stack'i, docker_terminals/cta_terminal)
# zaten bu export'u KENDI runtime_state Docker volume'une yaziyor --
# MERKEZ'in COT'u merkez_data volume'une yazdigi gibi. Burada da ayni
# kopru yontemi: docker-compose.yml, o volume'u salt-okunur olarak
# /mnt/cta_terminal_kokboru altina bagliyor, biz de burada sadece env
# var'dan okuyoruz. Env var yoksa (ornegin Docker disinda/testte
# calistirma) eski native yola DUSUYORUZ -- geriye donuk uyumluluk icin,
# davranis degismiyor, sadece Docker'da artik GERCEKTEN calisiyor.
KOKBORU_EXPORT = Path(
    os.environ.get("CTA_ERHAN_KOKBORU_EXPORT_PATH")
    or r"C:\cta_terminal\cta_kokboru_export.json"
)

# EWMAC export'u CTA Terminal'in kendi dongusunde (gunde birkac kez)
# tazeleniyor; bunun cok uzerinde bir yas varsa (ornegin CTA Terminal
# kapaliysa) veriyi "STALE" sayiyoruz, Karar Motoru buna gore agirligini
# geri cekiyor.
TREND_FRESH_HOURS = 36.0

_EMPTY_RESULT: Dict[str, Any] = {
    "direction": 0,
    "strength": 0.0,
    "persistence": 0,
    "score": 0.0,
    "freshness": "UNAVAILABLE",
    "age_hours": 999.0,
    "evaluation_time": None,
}


def _load_export() -> dict:
    if not KOKBORU_EXPORT.is_file():
        return {}
    try:
        with KOKBORU_EXPORT.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _parse_persistence(raw_indicator: str) -> int:
    if not raw_indicator or "persistence=" not in raw_indicator:
        return 0
    try:
        tail = raw_indicator.split("persistence=", 1)[1]
        digits = ""
        for ch in tail:
            if ch.isdigit():
                digits += ch
            else:
                break
        return int(digits) if digits else 0
    except Exception:
        return 0


def get_trend_data(product: str) -> Dict[str, Any]:
    """
    Verilen urun icin EWMAC fiyat-trend verisini dondurur:
      direction      : -1 / 0 / +1 (EWMAC fast-slow farkinin isareti)
      strength        : 0..1 (normalize edilmis EWMAC buyuklugu, clamp'li)
      persistence     : trend kac periyottur ayni yonde (buyuk = daha guvenilir)
      score           : direction * strength -- tek sayi, -1..+1
      freshness       : "OK" / "STALE" / "UNAVAILABLE"
      age_hours       : export'un uretilmesinden bu yana gecen saat
      evaluation_time : CTA Terminal'in kendi hesapladigi ham zaman damgasi

    Veri yoksa/okunamazsa/urun export'ta yoksa: notr + UNAVAILABLE doner.
    HICBIR DURUMDA exception firlatmaz.
    """
    product = product.upper().strip()
    out = dict(_EMPTY_RESULT)
    try:
        export = _load_export()
        if not export:
            return out

        generated_at = export.get("generated_at")
        products = export.get("products", {})
        entry = products.get(product)
        if not entry:
            return out

        domains = entry.get("intelligence_object", {}).get("domains", [])
        trend_domain = next((d for d in domains if d.get("domain") == "TREND"), None)
        if not trend_domain:
            return out

        direction = trend_domain.get("direction")
        if direction not in (-1, 0, 1):
            direction = 0

        try:
            strength = abs(float(trend_domain.get("strength") or 0.0))
        except (TypeError, ValueError):
            strength = 0.0
        strength = min(1.0, strength)

        persistence = _parse_persistence(trend_domain.get("raw_indicator", ""))
        domain_freshness = trend_domain.get("freshness", "UNAVAILABLE")

        age_hours = 999.0
        if generated_at:
            try:
                gen_dt = datetime.fromisoformat(str(generated_at).replace("Z", "+00:00"))
                age_hours = (datetime.now(timezone.utc) - gen_dt).total_seconds() / 3600.0
            except Exception:
                pass

        if domain_freshness == "OK" and age_hours <= TREND_FRESH_HOURS:
            freshness = "OK"
        elif domain_freshness == "UNAVAILABLE":
            freshness = "UNAVAILABLE"
        else:
            freshness = "STALE"

        out.update({
            "direction": direction,
            "strength": strength,
            "persistence": persistence,
            "score": max(-1.0, min(1.0, direction * strength)),
            "freshness": freshness,
            "age_hours": round(age_hours, 2),
            "evaluation_time": entry.get("evaluation_time"),
        })
        return out
    except Exception:
        return dict(_EMPTY_RESULT)


def get_trend_score(product: str) -> float:
    """Kisayol: sadece -1..+1 skoru doner."""
    return get_trend_data(product)["score"]
