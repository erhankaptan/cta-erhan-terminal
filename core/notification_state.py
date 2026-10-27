# -*- coding: utf-8 -*-
"""GUN+SLOT bazli "bu bildirim zaten gonderildi mi?" kaydi.

ACİL DÜZELTME (2026-10-27) -- bkz. core/notification_schedule.py modül
başı dürüstlük notu: WINDOW_TOLERANCE_MINUTES 7'den 90'a çıkarıldıktan
sonra, saatlik cron (`0 * * * *`) AYNI slot'un 90 dakikalık penceresi
içinde İKİ KERE (örn. hedefin 70 dk öncesinde bir kere, 40 dk sonrasında
bir kere) ateşlerse eski mantık İKİSİNDE DE bildirim gönderirdi -- ÇİFTE
bildirim. Bu modül, data/last_notification_state.json dosyasina
{"date": "YYYY-MM-DD", "slots_sent": ["15:00", "18:30", "21:30"]} seklinde
(Paris YEREL tarihi + saat:dakika etiketiyle) kayit tutarak bunu engeller.

Bu dosya fetch.yml'nin SONUNDAKİ "Commit and push" adımıyla (zaten
`git add data/` yapıyor -- YENİ bir adım EKLENMEDİ) otomatik olarak
repoya kaydedilip bir sonraki run'un checkout'unda hazır bulunur --
GOZLEM reposundaki (actions/cache tabanlı) karşılığından DAHA BASİT,
çünkü bu repo zaten data/'yı commit ediyor.
"""
from __future__ import annotations

import json
from datetime import time as dtime
from pathlib import Path

STATE_PATH = Path(__file__).parent.parent / "data" / "last_notification_state.json"


def _slot_label(slot: dtime) -> str:
    return slot.strftime("%H:%M")


def load_state() -> dict:
    """Durum dosyasini okur. Yok/bozuksa (ilk calisma, bozuk JSON) BOS bir
    durum doner -- asla exception firlatmaz (fail-open: emin olunamiyorsa
    "henuz gonderilmedi" varsayilir, bildirim KACIRILMAZ)."""
    if not STATE_PATH.exists():
        return {"date": None, "slots_sent": []}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"date": None, "slots_sent": []}
        return {
            "date": data.get("date"),
            "slots_sent": list(data.get("slots_sent") or []),
        }
    except (OSError, json.JSONDecodeError):
        return {"date": None, "slots_sent": []}


def slot_already_sent(slot: dtime, today_paris_date: str) -> bool:
    """Bugun (Paris yerel tarihi) bu slot icin bildirim ZATEN gonderildi mi?"""
    state = load_state()
    if state.get("date") != today_paris_date:
        return False
    return _slot_label(slot) in state.get("slots_sent", [])


def mark_slot_sent(slot: dtime, today_paris_date: str) -> None:
    """Bu slot'u bugun icin "gonderildi" olarak isaretler. Tarih degismisse
    (yeni gun) eski slots_sent listesi SIFIRLANIR -- her gun temiz baslar."""
    state = load_state()
    if state.get("date") != today_paris_date:
        state = {"date": today_paris_date, "slots_sent": []}
    slots = set(state.get("slots_sent", []))
    slots.add(_slot_label(slot))
    state["date"] = today_paris_date
    state["slots_sent"] = sorted(slots)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
