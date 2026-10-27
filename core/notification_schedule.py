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

ACİL DÜZELTME (2026-10-27, Reis'in "bildirimler gelmiyor" şikayeti sonrası)
===========================================================================
KÖK NEDEN (gerçek GitHub Actions run geçmişiyle DOĞRULANDI, UYDURMA DEĞİL):
`gh run list` ile bu reponun `fetch.yml` ("CTA Terminal - Auto Pipeline")
çalıştırmalarının SON birkaç günü incelendi. Saatlik cron (`0 * * * *`)
HER saat dakika :00'da ateşlemesi gerekirken, GERÇEK çalışma zamanları
şöyle (örnekler): 01:16, 21:27, 16:37, 09:53, 03:48, 23:03, 20:31, 17:28,
13:01, 07:22 UTC -- yani +-10 ila +-60 dakika (bazı günler daha da fazla)
kayan, GitHub Actions'ın kendi scheduled-workflow kuyruğundan kaynaklanan
bir gecikme (Anthropic/Claude'un bir hatası değil, GitHub'ın belgelenmiş,
özellikle ücretsiz/az-kullanımlı repolarda gözlenen davranışı). Hedef
saatlere (14:00/17:30/20:30 UTC, kış saatinde) en yakın örneklerin
sapması bile 53-59 dakikaydı -- eski ±7 dakikalık tolerans bunların
NEREDEYSE HİÇBİRİNİ yakalayamıyordu. Sonuç: kod MANTIK OLARAK doğru
çalışıyordu ama pencere sistematik olarak kaçırıldığı için bildirimler
günler boyu SESSİZCE gitmiyordu.

DÜZELTME: WINDOW_TOLERANCE_MINUTES 7 -> 90 dakikaya çıkarıldı (gözlenen
gecikmeyi büyük marjla karşılar). SCHEDULED_TIMES arasındaki EN KISA
mesafe 3.5 saat (210 dakika) olduğu için ±90 dakikalık pencere ASLA iki
hedefi birden kapsamaz (2*90=180 < 210) -- çapraz-tetikleme riski YOK.
Saatlik cron zaten geniş bir pencerede birden fazla kez ateşleyebileceği
için (GOZLEM'deki AYNI riskle BİREBİR aynı sınıf), send_report.py'de
AYRICA core/notification_state.py ile GÜN+SLOT bazlı "zaten gönderildi"
kaydı eklendi -- çifte bildirim riski o katmanda engelleniyor.
"""
from __future__ import annotations

from datetime import datetime, time as dtime
from typing import Optional
from zoneinfo import ZoneInfo

PARIS_TZ = ZoneInfo("Europe/Paris")

# Reis'in belirledigi 3 sabit saat (Europe/Paris YEREL saati, DST'den
# bagimsiz -- ZoneInfo donusumu otomatik yapar)
SCHEDULED_TIMES = [dtime(15, 0), dtime(18, 30), dtime(21, 30)]

# ACİL DÜZELTME (2026-10-27): 7 -> 90. Bkz. modül başı dürüstlük notu --
# gerçek GH Actions run geçmişinde gözlenen kayma (53-59+ dk) eski 7
# dakikalık toleransı aşıyordu. SCHEDULED_TIMES arasındaki en kısa mesafe
# (3.5 saat = 210 dk) sayesinde 90 dakikalık pencere çapraz-tetikleme
# riski taşımaz (2*90=180 < 210).
WINDOW_TOLERANCE_MINUTES = 90


def is_weekday(now: datetime) -> bool:
    """`now` (herhangi bir timezone-aware datetime) Europe/Paris'e cevrilip
    Pazartesi(0)-Cuma(4) ise True, Cumartesi(5)/Pazar(6) ise False doner."""
    return now.astimezone(PARIS_TZ).weekday() < 5


def get_due_slot(now: datetime) -> Optional[dtime]:
    """now (Paris saatine cevrilince) SCHEDULED_TIMES'tan EN YAKIN olanina
    +-WINDOW_TOLERANCE_MINUTES icindeyse o hedef saati (dtime) dondurur;
    hafta sonuysa veya hicbir hedefe yeterince yakin degilse None doner.
    ACİL DÜZELTME (2026-10-27) -- GOZLEM (kurumsal-makro-gozlem-terminali)
    icin uygulanan AYNI desen: artik HANGI slot'un (15:00/18:30/21:30)
    due oldugu da biliniyor, boylece core/notification_state.py GUN+SLOT
    bazli "zaten gonderildi" kaydi tutabiliyor."""
    if not is_weekday(now):
        return None
    now_paris = now.astimezone(PARIS_TZ)
    best: Optional[dtime] = None
    best_fark: Optional[float] = None
    for hedef in SCHEDULED_TIMES:
        hedef_dt = now_paris.replace(
            hour=hedef.hour, minute=hedef.minute, second=0, microsecond=0,
        )
        fark_dakika = abs((now_paris - hedef_dt).total_seconds()) / 60.0
        if fark_dakika <= WINDOW_TOLERANCE_MINUTES:
            if best_fark is None or fark_dakika < best_fark:
                best, best_fark = hedef, fark_dakika
    return best


def is_within_scheduled_window(now: datetime) -> bool:
    """`now`, SCHEDULED_TIMES listesindeki saatlerden EN AZ BIRINE
    +-WINDOW_TOLERANCE_MINUTES icindeyse True doner. (Geriye donuk
    uyumluluk icin korundu -- get_due_slot()'un uzerine ince bir
    sarmalayici.)"""
    return get_due_slot(now) is not None


def is_periodic_notification_due(now: datetime) -> bool:
    """Periyodik rapor bildirimi (Telegram+Email) simdi gitmeli mi?
    Hafta ici VE (3 sabit saatten birine +-90 dk icinde) ise True.
    NOT: bu fonksiyon SADECE zaman penceresini kontrol eder, "bu slot
    BUGUN zaten gonderildi mi" sorusunu BILMEZ -- send_report.py o
    kontrolu core/notification_state.py ile AYRICA yapar."""
    return get_due_slot(now) is not None
