"""
CTA ERHAN TERMİNALİ — Telegram Rapor (v3)
==========================================
3 grup: Vadeli+Forex+Emtia | ABD Hisseleri | Asya Hisseleri
State hesabı skor bazlı.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOT_FILE = DATA_DIR / "snapshots" / "latest.json"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


# ABD hisseleri (bilinen semboller)
US_STOCKS = {
    "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META",
    "NFLX", "AMD", "INTC", "AVGO", "ORCL", "CRM", "ADBE", "QCOM",
    "JPM", "BAC", "GS", "WFC", "C", "MS",
    "XOM", "CVX", "COP", "OXY",
    "DIS", "NKE", "SBUX", "MCD", "KO", "PEP", "WMT", "TGT", "COST",
    "BA", "CAT", "GE", "F", "GM", "RIVN", "LCID",
    "PFE", "JNJ", "MRNA", "UNH", "LLY",
    "PLTR", "COIN", "MSTR", "SQ", "PYPL", "SHOP", "UBER", "LYFT", "ABNB",
    "SPOT", "SNAP", "PINS", "TWLO", "ZM", "DOCU",
}


def categorize(code):
    """Sembolü kategoriye ayır: 'us_stock', 'asia_stock', 'main'."""
    c = code.upper().strip()

    # ABD hisseleri
    if c in US_STOCKS:
        return "us_stock"

    # Asya/HK hisseleri
    if c.endswith(" HK") or c.endswith("HK"):
        return "asia_stock"
    if c.endswith(" JP") or c.endswith("JP"):
        return "asia_stock"
    if c.endswith(" SS") or c.endswith(" SZ"):
        return "asia_stock"
    if c in ("HSTECH", "HSI", "HSCEI", "NIKKEI", "JP225", "KOSPI", "TWII", "SHCOMP"):
        return "asia_stock"

    return "main"


def soften(score, cap=0.75):
    try:
        s = float(score)
    except Exception:
        return 0.0
    return max(-cap, min(cap, s))


def load_snapshot():
    if not SNAPSHOT_FILE.exists():
        return {}
    try:
        with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def compute_state(score, evidence_count, has_conflict=False):
    """
    Skor bazlı state:
    - Hiç kanıt yok → INSUFFICIENT
    - |skor| < 0.10 → NEUTRAL
    - skor >= 0.35 → BULLISH
    - skor <= -0.35 → BEARISH
    - arası (0.10 - 0.35) → CONFLICT (zayıf sinyal)
    """
    if evidence_count == 0:
        return "INSUFFICIENT"

    # Kanıt sayısı 1 ve skor 0 → INSUFFICIENT
    if evidence_count == 1 and abs(score) < 0.05:
        return "INSUFFICIENT"

    if abs(score) < 0.10:
        if has_conflict:
            return "CONFLICT"
        return "NEUTRAL"

    if score >= 0.35:
        return "BULLISH"
    if score <= -0.35:
        return "BEARISH"

    # 0.10 - 0.35 arası → CONFLICT (zayıf, karışık)
    return "CONFLICT"


def format_group(title, items):
    """Bir grup için satırlar üret."""
    if not items:
        return []

    groups = {"BULLISH": [], "BEARISH": [], "CONFLICT": [], "NEUTRAL": [], "INSUFFICIENT": []}
    for code, sc, state in items:
        if state in groups:
            groups[state].append((code, sc))

    for k in groups:
        groups[k].sort(key=lambda x: abs(x[1]), reverse=True)

    lines = [f"═══ <b>{title}</b> ═══", ""]

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

    return lines


def build_message(snapshot):
    results = snapshot.get("results", {})
    if not results:
        return "⚠️ CTA ERHAN RAPORU\n\nSnapshot boş."

    now_tr = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    # Kategorilere ayır
    main_items = []
    us_items = []
    asia_items = []

    for code, r in results.items():
        score = soften(r.get("score", 0.0))
        ev_count = r.get("evidence_count", 0)
        reasons = " ".join(r.get("reasons", []))
        has_conflict = "ÇELİŞKİ" in reasons
        state = compute_state(score, ev_count, has_conflict)

        cat = categorize(code)
        item = (code, score, state)

        if cat == "us_stock":
            us_items.append(item)
        elif cat == "asia_stock":
            asia_items.append(item)
        else:
            main_items.append(item)

    total = len(main_items) + len(us_items) + len(asia_items)

    lines = [
        "📊 <b>CTA ERHAN RAPORU</b>",
        f"🕐 {now_tr}",
        "",
    ]

    # Ana grup
    lines.extend(format_group("VADELİ / FOREX / EMTİA", main_items))

    # ABD hisseleri
    if us_items:
        lines.extend(format_group("ABD HİSSELERİ", us_items))

    # Asya hisseleri
    if asia_items:
        lines.extend(format_group("ASYA / HK HİSSELERİ", asia_items))

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
    print("Telegram Rapor (v3)")
    print("=" * 60)

    snapshot = load_snapshot()
    if not snapshot:
        print("[FATAL] Snapshot bulunamadı")
        return

    msg = build_message(snapshot)
    print("--- Mesaj önizleme ---")
    print(msg[:1200])
    print("--- Gönderiliyor ---")

    send_telegram(msg)


if __name__ == "__main__":
    main()