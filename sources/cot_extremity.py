# sources/cot_extremity.py
"""
COT pozisyonunun KENDI gecmisine gore ne kadar gergin/ekstrem oldugunu
olcer -- CTA Terminal'in (docker_terminals/cta_terminal/cta_cot_measurement.py)
zaten denenmis/denetlenmis "EXTREMITY LEVEL" teknigiyle AYNI matematik
(causal rolling-window min-max), burada CTA ERHAN'in kendi (ayri,
paylasilmayan) kod tabaninda YENIDEN yazildi.

ONEMLI AYRIM (2026-11-12, Reis onayli, "COT -1.000 her zaman boyle mi
cikiyor" tartismasi sonrasi): Bu modul KARAR MOTORU'nun YON/skorunu
DEGISTIRMEZ -- core/signal_engine.py hala YON icin net/open_interest
oranini kullanir. Bu modul SADECE "bugunku pozisyon, bu urunun son N
haftasina gore nerede duruyor" sorusuna ayri, bagimsiz bir cevap verir
(0-100 ekstremite seviyesi). Ikisini TEK bir sayida birlestirmek
(composite score) BILINCLI olarak YAPILMADI -- CTA Terminal'in de LOCKED
kurali budur: yon ve ekstremite ayri epistemik domain'ler, karistirilmaz.
Ornek: ES'in son 4 haftada net'i hep eksi (short) ama en az eksi olan
hafta bugunse, ekstremite ~%97 (kendi penceresinin tavaninda) cikar --
bu "GUCLU YUKARI" demek DEGILDIR, "short pozisyon nispeten hafifliyor"
demektir; yon hala negatiftir ve ayri gosterilir.

DURUSTLUK: yeterli gecmis (min_required_history haftadan az) yoksa
SAHTE bir "notr 50" URETILMEZ, acikca None + status="YETERSIZ" doner.
Tum degerler (gecmis + guncel) AYNIysa 50.0 donmesi bilincli bir
istisnadir -- persentil tanimsizken ortanca kabul etmek fabrikasyon
degil, dejenere-ama-gercek bir durumun dogru ifadesidir.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

from sources.cot_resolver import get_cot_evidence_rows

DEFAULT_MAX_WEEKS = 52
DEFAULT_MIN_REQUIRED_HISTORY = 4


def compute_extremity_level(
    historical_nets: Sequence[float],
    current_net: float,
    min_required_history: int = DEFAULT_MIN_REQUIRED_HISTORY,
) -> Optional[float]:
    """`historical_nets`: SADECE GECMIS (current HARIC) haftalarin net
    pozisyonlari. Yetersiz gecmis -> None (sahte 50 uretilmez)."""
    if len(historical_nets) < min_required_history:
        return None
    full_window = list(historical_nets) + [current_net]
    mn, mx = min(full_window), max(full_window)
    if mx == mn:
        return 50.0
    raw = (current_net - mn) / (mx - mn) * 100
    return max(0.0, min(100.0, raw))


def get_cot_extremity(
    product: str,
    max_weeks: int = DEFAULT_MAX_WEEKS,
    min_required_history: int = DEFAULT_MIN_REQUIRED_HISTORY,
) -> Dict[str, Any]:
    """Urun icin ekstremite bilgisini doner:
      extremity_level  : 0-100 (veya None, yetersiz veri)
      weeks_available   : ekstremite hesaplamasinda kullanilabilen GECMIS
                          hafta sayisi (current haric)
      status            : "OK" / "YETERSIZ"
      current_report_date: en guncel kullanilan rapor tarihi (veya None)

    HICBIR DURUMDA exception firlatmaz -- veri eksik/bozuksa sessizce
    YETERSIZ doner."""
    out: Dict[str, Any] = {
        "extremity_level": None,
        "weeks_available": 0,
        "status": "YETERSIZ",
        "current_report_date": None,
    }
    try:
        rows = get_cot_evidence_rows(product)
        if not rows:
            return out

        current = rows[-1]
        historical = rows[:-1][-max_weeks:] if len(rows) > 1 else []
        out["weeks_available"] = len(historical)
        out["current_report_date"] = current["report_date"]

        level = compute_extremity_level(
            [r["net"] for r in historical],
            current["net"],
            min_required_history=min_required_history,
        )
        if level is not None:
            out["extremity_level"] = round(level, 1)
            out["status"] = "OK"
        return out
    except Exception:
        return {
            "extremity_level": None,
            "weeks_available": 0,
            "status": "YETERSIZ",
            "current_report_date": None,
        }
