"""
CTA ERHAN TERMİNALİ — Telegram & Mail Rapor (v3)
==================================================
3 grup: Vadeli+Forex+Emtia | ABD Hisseleri | Asya Hisseleri
State hesabı skor bazlı.
Wayne Enterprise Kılavuzu Operasyonel Hatırlatmaları Entegre Edilmiştir.
"""

import os
import sys
import json
import re
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOT_FILE = DATA_DIR / "snapshots" / "latest.json"

# DENETCI KARARI (2026-10-25): Bu script hem `fetch.yml` (PYTHONPATH=
# github.workspace ayarli) hem de `daily_report.yml` (PYTHONPATH
# AYARLANMAMIS) tarafindan `python scripts/send_report.py` olarak
# dogrudan calistiriliyor -- ikinci durumda `core.*` paketi import
# edilemez. run_weekly_cot.py'deki ayni desenle PROJECT_ROOT'u
# sys.path'e kendimiz ekliyoruz, PYTHONPATH ortam degiskenine bagimli
# kalmiyoruz (minimal, tek-noktali bagimlilik).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.notification_schedule import PARIS_TZ, get_due_slot  # noqa: E402
from core.notification_state import mark_slot_sent, slot_already_sent  # noqa: E402

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
        "📊 <b>CTA ERHAN RAPORU</b> (Wayne Protocol)",
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
    lines.append("")
    lines.append("🛡️ <b>Wayne Protokolü Notu:</b>")
    lines.append("• Çöp CTA Sinyalleri yok sayıldı.")
    lines.append("• Sığ saatlerde işlem açılmaz; Pzt/Salı seans açılışı ve Stop Hunt iğnesi beklenir.")
    lines.append("• Tüm pozisyonlar Cuma kapanışında kapatılır.")
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


def send_email(subject, html_body):
    """SMTP ile mail gonder."""
    smtp_host = os.environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "587"))
    user = os.environ.get("EMAIL_USER", "")
    password = os.environ.get("EMAIL_PASS", "")
    to = os.environ.get("EMAIL_TO", "")
    enabled = os.environ.get("EMAIL_ENABLED", "true").lower()

    if enabled != "true":
        print("[SKIP] EMAIL_ENABLED != true")
        return False

    if not all([user, password, to]):
        print("[FATAL] EMAIL_USER/PASS/TO eksik")
        return False

    plain = re.sub(r"<[^>]+>", "", html_body)
    plain = plain.replace("&nbsp;", " ").replace("&amp;", "&")

    msg = MIMEMultipart("alternative")
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(MIMEText(plain, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as s:
            s.starttls()
            s.login(user, password)
            s.send_message(msg)
        print("[OK] Email gonderildi")
        return True
    except Exception as e:
        print(f"[ERR] Email: {e}")
        return False


def main():
    print("=" * 60)
    print("Telegram & Mail Rapor (v3) — Wayne Protocol Etkin")
    print("=" * 60)

    # DENETCI KARARI (2026-10-25): ZAMANLAMA / HAFTA SONU FILTRESI --
    # bildirim SADECE hafta ici 15:00/18:30/21:30 (Europe/Paris) penceresinde
    # gider. Bu bir hata degil, normal bir "simdi sira degil" durumu
    # oldugu icin sessizce (exit 0) cikilir -- fetch.yml veri toplama/
    # sentez pipeline'i yine de calisir, SADECE bu rapor gonderim adimi
    # atlanir.
    #
    # ACİL DÜZELTME (2026-10-27) -- bkz. core/notification_schedule.py VE
    # core/notification_state.py dosya-basi durustluk notlari: pencere
    # +-7dk'dan +-90dk'ya genisletildi (GERCEK GH Actions run gecikmesi
    # 53-59+ dk olarak olculdu, eski pencere bunu kacirip bildirimleri
    # GUNLERCE SESSIZCE dusuruyordu) VE ayrica "bu slot BUGUN zaten
    # gonderildi mi?" kontrolu eklendi (genisletilmis pencere icinde
    # saatlik cron iki kere ateslerse CIFTE bildirimi onlemek icin).
    now_utc = datetime.now(timezone.utc)
    due_slot = get_due_slot(now_utc)
    if due_slot is None:
        print(
            f"[ZAMANLAMA] Simdi periyodik bildirim penceresinde degil "
            f"(now_utc={now_utc.isoformat()}) -- Telegram ve Email ATLANIYOR."
        )
        return

    today_paris = now_utc.astimezone(PARIS_TZ).date().isoformat()
    if slot_already_sent(due_slot, today_paris):
        print(
            f"[ZAMANLAMA] Slot {due_slot.strftime('%H:%M')} bugun ({today_paris}) "
            f"icin ZATEN gonderilmis -- Telegram ve Email ATLANIYOR (cifte "
            f"bildirim onlendi)."
        )
        return

    snapshot = load_snapshot()

    # Snapshot boş/eksik olsa bile pipeline ve mail akışı asla çökmez, bilgi verir
    if not snapshot:
        print("[WARN] Snapshot bulunamadı veya analiz zaman aşımına uğradı.")
        msg = (
            "⚠️ <b>CTA ERHAN TERMİNAL BİLDİRİMİ</b><br><br>"
            "Bu periyotta yeni snapshot verisi üretilemedi veya analiz adımı zaman aşımına uğradı.<br>"
            "Otomasyon akışı başarıyla tamamlandı. Wayne Protokolü aktif."
        )
    else:
        msg = build_message(snapshot)

    print("--- Mesaj önizleme ---")
    print(msg[:1200])
    print("--- Gönderiliyor ---")

    # Mail gönderimi için HTML şablonu sarmalayıcısı
    subject = f"CTA ERHAN RAPORU (Wayne Protocol) - {datetime.now(timezone.utc).strftime('%d %b %Y %H:%M')}"

    html_msg = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px;">
          <pre style="font-family: 'Courier New', Courier, monospace; font-size: 13px; white-space: pre-wrap; word-wrap: break-word;">{msg}</pre>
        </div>
      </body>
    </html>
    """

    # DENETCI KARARI (2026-10-25): EMAIL GORUNURLUGU -- email ONCE
    # denenir (Telegram'dan once), basarisiz olursa Telegram mesajinin
    # SONUNA bir uyari satiri eklenir. html_msg icerigi (email govdesi)
    # orijinal msg'den uretildigi icin bu uyari EMAIL'IN kendi icine
    # SIZMAZ -- sadece Telegram'a gider.
    email_basarili = send_email(subject, html_msg)

    telegram_msg = msg
    if not email_basarili:
        telegram_msg = telegram_msg + "\n\n⚠️ EMAIL GÖNDERİMİ BAŞARISIZ"

    send_telegram(telegram_msg)

    # ACİL DÜZELTME (2026-10-27) -- gonderim denendikten HEMEN SONRA bu
    # slot'u "bugun gonderildi" olarak isaretle (bkz. core/notification_
    # state.py). Email/Telegram'dan biri basarisiz olsa bile isaretlenir
    # -- amac mukemmel teslimati garanti etmek degil, AYNI slot icin
    # TEKRAR TEKRAR denemeyi (ve basariliysa CIFTE bildirimi) onlemek;
    # kalici bir SMTP/Telegram hatasi zaten her iki fonksiyonun kendi
    # [ERR] loglarinda gorunur.
    mark_slot_sent(due_slot, today_paris)


if __name__ == "__main__":
    main()
