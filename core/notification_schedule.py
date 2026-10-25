# -*- coding: utf-8 -*-
"""
CTA ERHAN TERMİNALİ — Bildirim Zamanlama / Hafta Sonu Filtresi
==================================================================
Periyodik rapor bildirimlerinin (Telegram + Email) SADECE hafta içi,
belirli sabit saatlerde gitmesini saglayan ORTAK (merkezi) mantık.

DENETÇİ KARARI (2026-10-25): GitHub Actions cron'u SADECE saatlik
(`0 * * * *`) tetikler -- dakika hassasiyetinde DST-farkindali bir cron
yazmak yerine, GERÇEK gönderim kararı burada, Python içinde
`zoneinfo.ZoneInfo("Europe/Paris")` ile veriliyor. Bu sayede yaz/kış
saati (CEST/CET) geçişi OTOMATIK hesaplanır, cron'u yılda 2 kez elle
değiştirmeye gerek kalmaz (CTA Terminali'ndeki aynı mimari).

Bu modül SADECE "şimdi bildirim gönderilsin mi?" sorusuna cevap verir.
Veri toplama/sentez pipeline'ını (fetch/analyze/synthesis) ETKİLEMEZ --
onlar her saat başı normal çalışır, sadece send_report.py'nin gönderim
adımı bu kontrole tabidir.
"""
from __future__ import annotations

from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo

PARIS_TZ = ZoneInfo("Europe/Paris")

# Reis'in belirledigi 3 sabit saat (Europe/Paris YEREL saati, DST'den
# bagimsiz -- ZoneInfo donusumu otomatik yapar)
SCHEDULED_TIMES = [dtime(15, 0), dtime(18, 30), dtime(21, 30)]

# Saatlik cron (0 * * * *) tam dakikasinda tetiklenmeyebilir / GitHub
# Actions scheduled cron'u gecikebilir (CTA Terminali teşhisinde
# gözlemlendi, bazı tetiklemeler 10+ dk kayabiliyor) -- DENETÇİ onayı:
# ±7 dk tolerans (CTA Terminali ile aynı değer).
WINDOW_TOLERANCE_MINUTES = 7


def is_weekday(now: datetime) -> bool:
    """`now` (herhangi bir timezone-aware datetime) Europe/Paris'e cevrilip
    Pazartesi(0)-Cuma(4) ise True, Cumartesi(5)/Pazar(6) ise False doner."""
    return now.astimezone(PARIS_TZ).weekday() < 5


def is_within_scheduled_window(now: datetime) -> bool:
    """`now`, SCHEDULED_TIMES listesindeki saatlerden EN AZ BIRINE
    +-WINDOW_TOLERANCE_MINUTES icindeyse True doner."""
    now_paris = now.astimezone(PARIS_TZ)
    for hedef in SCHEDULED_TIMES:
        hedef_dt = now_paris.replace(
            hour=hedef.hour, minute=hedef.minute, second=0, microsecond=0,
        )
        fark_dakika = abs((now_paris - hedef_dt).total_seconds()) / 60.0
        if fark_dakika <= WINDOW_TOLERANCE_MINUTES:
            return True
    return False


def is_periodic_notification_due(now: datetime) -> bool:
    """Periyodik rapor bildirimi (Telegram+Email) simdi gitmeli mi?
    Hafta ici VE (3 sabit saatten birine +-7 dk icinde) ise True."""
    return is_weekday(now) and is_within_scheduled_window(now)
