# sources/cot_interpreter.py
"""
CFTC COT verisini yorumlar ve UI'ye hazır istihbarat kartı üretir.

- Ana panel için: `summary` (5-6 satır, net, karar verilebilir)
- Detay expander için: `details` (ham veriler, gürültü)

Terminoloji:
- TFF raporu: "Leveraged Funds" = CTA proxy (CTA ağırlıklı ama CTA'ların tamamı değil)
- Disaggregated raporu: "Managed Money" = CTA proxy
"""
from __future__ import annotations

from typing import Any, Dict


def _fmt(value: int) -> str:
    """Sayıyı Türkçe formatla: 134972 → '134.972'"""
    return f"{value:,}".replace(",", ".")


def _fmt_signed(value: int) -> str:
    """İşaretli sayı: +134972 → '+134.972', -1799 → '-1.799'"""
    sign = "+" if value >= 0 else "-"
    return f"{sign}{abs(value):,}".replace(",", ".")


def _direction_label(value: int) -> str:
    if value > 0:
        return "NET LONG"
    if value < 0:
        return "NET SHORT"
    return "NÖTR"


def _momentum_label(change_net: int, cta_net: int) -> str:
    """Haftalık değişimin pozisyona göre yorumu."""
    if change_net == 0:
        return "SABİT"
    # Aynı yönde güçlenme
    if (change_net > 0 and cta_net > 0) or (change_net < 0 and cta_net < 0):
        return "GÜÇLENİYOR"
    # Pozisyon korunuyor ama momentum zayıflıyor
    if (change_net > 0 and cta_net < 0) or (change_net < 0 and cta_net > 0):
        return "ZAYIFLIYOR"
    return "SABİT"


def _consensus_label(cta_net: int, dealer_net: int, inst_net: int) -> str:
    """3 kategori aynı yönde mi?"""
    dirs = []
    for v in (cta_net, dealer_net, inst_net):
        if v > 0:
            dirs.append("LONG")
        elif v < 0:
            dirs.append("SHORT")
        else:
            dirs.append("FLAT")
    unique = set(dirs)
    if len(unique) == 1:
        return "UYUMLU"
    if len(unique) == 2:
        return "KARIŞIK"
    return "ÇELİŞKİLİ"


def _squeeze_risk(cta_net: int, open_interest: int) -> str:
    """
    Aşırı pozisyonlanma / squeeze riski.
    OI'ye göre normalize edilir.
    """
    if open_interest <= 0:
        return "HESAPLANAMADI"
    ratio = cta_net / open_interest  # -1.0 ile +1.0 arası tipik
    pct = abs(ratio) * 100

    if ratio < -0.15:
        return f"YÜKSEK (aşırı short — short squeeze potansiyeli, OI'nin %{pct:.1f}'i)"
    if ratio > 0.15:
        return f"YÜKSEK (aşırı long — kâr satışı riski, OI'nin %{pct:.1f}'i)"
    if pct > 0.08:
        return f"ORTA (OI'nin %{pct:.1f}'i)"
    return f"DÜŞÜK (OI'nin %{pct:.1f}'i)"


def interpret_cot(metadata: Dict[str, Any], product_code: str) -> Dict[str, Any]:
    """
    CFTC COT metadata'sını UI'ye hazır iki katmana ayırır:
    - summary: ana panel (5-6 satır, net)
    - details: detay expander (gürültü, ham veriler)

    Fail-Closed: Eksik veri varsa summary'de "YETERSİZ" gösterilir.
    """
    # --- Fail-Closed: eksik alan kontrolü ---
    required = ["report_date", "market", "open_interest", "cta_proxy", "dealer", "institutional"]
    missing = [k for k in required if k not in metadata]
    if missing:
        return {
            "available": False,
            "summary": {
                "title": "COT Analizi",
                "line1": "Veri eksik",
                "line2": f"Eksik alanlar: {', '.join(missing)}",
                "interpretation": "YETERSİZ",
            },
            "details": {},
        }

    # --- Veri çıkar ---
    report_date = metadata["report_date"]
    report_week = metadata.get("report_week", "")
    market = metadata["market"]
    oi = metadata["open_interest"]

    cta = metadata["cta_proxy"]
    dealer = metadata["dealer"]
    inst = metadata["institutional"]

    cta_long = cta.get("long", 0)
    cta_short = cta.get("short", 0)
    cta_net = cta.get("net", 0)
    cta_change_long = cta.get("change_long", 0)
    cta_change_short = cta.get("change_short", 0)
    cta_change_net = cta.get("change_net", 0)

    dealer_net = dealer.get("net", 0)
    inst_net = inst.get("net", 0)

    # --- Yorum hesapla ---
    cta_dir_label = _direction_label(cta_net)
    momentum = _momentum_label(cta_change_net, cta_net)
    consensus = _consensus_label(cta_net, dealer_net, inst_net)
    squeeze = _squeeze_risk(cta_net, oi)

    # --- Ana panel özet cümleler ---
    cta_label = "Leveraged Funds (CTA Proxy)"
    inst_label = "Asset Manager (Kurumsal)"
    dealer_label = "Dealer (Sell-side)"

    line1 = f"{cta_label}: {cta_dir_label} {_fmt_signed(cta_net)}"
    line2 = f"Haftalık değişim: {_fmt_signed(cta_change_net)} ({momentum})"

    # Yorum cümlesi
    if consensus == "UYUMLU":
        yorum = "Kategoriler aynı yönde — uyumlu sinyal"
    elif consensus == "KARIŞIK":
        yorum = "Kategoriler farklı yönde — karışık sinyal"
    else:
        yorum = "Kategoriler çelişiyor — belirsiz sinyal"

    # --- Details (gürültü) ---
    details = {
        "report_date": report_date,
        "report_week": report_week,
        "market": market,
        "open_interest": oi,
        "cta_proxy": {
            "label": cta_label,
            "long": cta_long,
            "short": cta_short,
            "net": cta_net,
            "change_long": cta_change_long,
            "change_short": cta_change_short,
            "change_net": cta_change_net,
            "direction": cta_dir_label,
            "momentum": momentum,
        },
        "dealer": {
            "label": dealer_label,
            "long": dealer.get("long", 0),
            "short": dealer.get("short", 0),
            "net": dealer_net,
        },
        "institutional": {
            "label": inst_label,
            "long": inst.get("long", 0),
            "short": inst.get("short", 0),
            "net": inst_net,
        },
        "consensus": consensus,
        "squeeze_risk": squeeze,
    }

    return {
        "available": True,
        "summary": {
            "title": f"COT Analizi — {market[:45]}",
            "date_line": f"Rapor: {report_date} | {report_week}",
            "line1": line1,
            "line2": line2,
            "line3": f"{inst_label}: {_direction_label(inst_net)} {_fmt_signed(inst_net)}",
            "interpretation": yorum,
            "consensus": consensus,
        },
        "details": details,
    }