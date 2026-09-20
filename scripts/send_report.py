"""
CTA ERHAN TERMİNALİ — Telegram Rapor (v2)
==========================================
app.py ile aynı mantık: segment bazlı state hesabı.
X + RSS dosyalarından canlı okur.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
RSS_DIR = DATA_DIR / "rss"
SNAPSHOT_FILE = DATA_DIR / "snapshots" / "latest.json"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def load_json_files(folder, pattern):
    if not folder.exists():
        return []
    items = []
    seen = set()
    for fp in sorted(folder.glob(pattern)):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    tid = item.get("id") or item.get("tweet_id") or item.get("guid") or str(hash(str(item)))
                    if tid not in seen:
                        seen.add(tid)
                        items.append(item)
        except Exception:
            continue
    return items


def load_snapshot():
    if not SNAPSHOT_FILE.exists():
        return {}
    try:
        with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def build_segments_for(code, all_analysis, all_rss):
    segments = []
    code_u = code.upper().strip()
    for item in all_analysis:
        username = (item.get("username") or "").strip()
        for v in (item.get("varliklar") or []):
            sembol = (v.get("sembol") or "").upper().strip()
            if sembol == code_u:
                segments.append((v.get("yon", "NÖTR"), "@" + username if username else "X"))
    for item in all_rss:
        for v in (item.get("varliklar") or []):
            sembol = (v.get("sembol") or "").upper().strip()
            if sembol == code_u:
                segments.append((v.get("yon", "NÖTR"), "tickmill"))
    return segments


def compute_state_from_segments(segments, fallback="INSUFFICIENT"):
    if not segments:
        return fallback
    bull = bear = 0
    for y, _ in segments:
        yu = str(y).upper()
        if "YUKARI" in yu or "BULL" in yu or "LONG" in yu:
            bull += 1
        elif "AŞAĞI" in yu or "BEAR" in yu or "SHORT" in yu:
            bear += 1
    if bull > 0 and bear > 0:
        return "CONFLICT"
    if bull > 0:
        return "BULLISH"
    if bear > 0:
        return "BEARISH"
    return "NEUTRAL"


def soften(score, cap=0.75):
    try:
        s = float(score)
    except Exception:
        return 0.0
    return max(-cap, min(cap, s))


def build_message(snapshot, all_analysis, all_rss):
    results = snapshot.get("results", {})
    if not results:
        return "⚠️ CTA ERHAN RAPORU\n\nSnapshot boş."

    now_tr = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    groups = {
        "BULLISH": [], "BEARISH": [], "CONFLICT": [],
        "NEUTRAL": [], "INSUFFICIENT": [],
    }

    for code, r in results.items():
        score = soften(r.get("score", 0.0))
        segments = build_segments_for(code, all_analysis, all_rss)
        state = compute_state_from_segments(segments, r.get("state", "INSUFFICIENT"))
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
        for code, sc in groups["BULLISH"][:12]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["BEARISH"]:
        lines.append(f"🔴 <b>BEARISH</b> ({len(groups['BEARISH'])})")
        for code, sc in groups["BEARISH"][:12]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["CONFLICT"]:
        lines.append(f"🟠 <b>CONFLICT</b> ({len(groups['CONFLICT'])})")
        for code, sc in groups["CONFLICT"][:12]:
            lines.append(f"  • {code}  <code>{sc:+.3f}</code>")
        lines.append("")

    if groups["NEUTRAL"]:
        lines.append(f"⚪ <b>NEUTRAL</b> ({len(groups['NEUTRAL'])})")
        for code, sc in groups["NEUTRAL"][:12]:
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
    print("Telegram Rapor (v2)")
    print("=" * 60)

    snapshot = load_snapshot()
    if not snapshot:
        print("[FATAL] Snapshot bulunamadı")
        return

    all_analysis = load_json_files(ANALYSIS_DIR, "analysis_*.json")
    all_rss = load_json_files(RSS_DIR, "rss_*.json")

    print(f"[INFO] {len(all_analysis)} X analizi, {len(all_rss)} RSS makalesi")

    msg = build_message(snapshot, all_analysis, all_rss)
    print("--- Mesaj önizleme ---")
    print(msg[:800])
    print("--- Gönderiliyor ---")

    send_telegram(msg)


if __name__ == "__main__":
    main()