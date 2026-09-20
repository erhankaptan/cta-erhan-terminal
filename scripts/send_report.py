"""
CTA ERHAN TERMİNALİ — Telegram Rapor
======================================
Snapshot'ı okur, Telegram botuna özet rapor atar.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SNAPSHOT_FILE = PROJECT_ROOT / "data" / "snapshots" / "latest.json"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def soften(score, cap=0.75):
    try:
        s = float(score)
    except Exception:
        return 0.0
    return max(-cap, min(cap, s))


def load_snapshot():
    if not SNAPSHOT_FILE.exists():
        return None
    try:
        with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_message(snapshot):
    results = snapshot.get("results", {})
    if not results:
        return "⚠️ CTA ERHAN RAPORU\n\nSnapshot boş."

    now_tr = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    groups = {
        "BULLISH": [], "BEARISH": [], "CONFLICT": [],
        "NEUTRAL": [], "INSUFFICIENT": [],
    }

    for code, r in results.items():
        state = r.get("state", "INSUFFICIENT")
        score = soften(r.get("score", 0.0))
        if state in groups:
            groups[state].append((code, score))

    for k in groups:
        groups[k].sort(key=lambda x: abs(x[1]), reverse=True)

    lines = [
        "📊 <b>CTA ERHAN RAPORU</b>",
        f"🕐 {now_tr}",
        "",
    ]

    if groups["BULLISH"]:
        lines.append(f"🟢 <b>BULLISH</b> ({len(groups['BULLISH'])})")
        for code, sc in groups["BULLISH"][:8]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["BEARISH"]:
        lines.append(f"🔴 <b>BEARISH</b> ({len(groups['BEARISH'])})")
        for code, sc in groups["BEARISH"][:8]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["CONFLICT"]:
        lines.append(f"🟠 <b>CONFLICT</b> ({len(groups['CONFLICT'])})")
        for code, sc in groups["CONFLICT"][:8]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["NEUTRAL"]:
        lines.append(f"⚪ <b>NEUTRAL</b> ({len(groups['NEUTRAL'])})")
        for code, sc in groups["NEUTRAL"][:8]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["INSUFFICIENT"]:
        codes = ", ".join([c for c, _ in groups["INSUFFICIENT"]])
        lines.append(f"⚫ <b>INSUFFICIENT</b> ({len(groups['INSUFFICIENT'])})")
        lines.append(f"  {codes}")
        lines.append("")

    total = sum(len(v) for v in groups.values())
    lines.append(f"📈 Toplam: <b>{total}</b> varlık")
    lines.append(f"🔗 {snapshot.get('generated_at', '—')[:16]}")

    return "\n".join(lines)


def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[FATAL] TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID yok")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            print("[OK] Telegram mesajı gönderildi")
            return True
        else:
            print(f"[ERR] HTTP {r.status_code}: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"[ERR] {e}")
        return False


def main():
    print("=" * 60)
    print("Telegram Rapor")
    print("=" * 60)

    snapshot = load_snapshot()
    if not snapshot:
        print("[FATAL] Snapshot bulunamadı")
        return

    msg = build_message(snapshot)
    print("--- Mesaj önizleme ---")
    print(msg[:500])
    print("--- Gönderiliyor ---")

    send_telegram(msg)


if __name__ == "__main__":
    main()