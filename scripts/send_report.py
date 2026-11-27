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
import unicodedata
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOT_FILE = DATA_DIR / "snapshots" / "latest.json"

# DUZELTME (2026-11-18, Reis'in "0.156 gibi rakamlar kafa karistiriyor,
# ne demek belli degil" bulgusu): bir onceki GERCEKTEN GONDERILMIS
# raporun ozet durumunu burada saklıyoruz -- notification_state.py'nin
# "hangi slot bugun gonderildi" kaydiyla AYNI desen (fetch.yml zaten
# `git add data/` yaptigi icin ekstra bir commit adimina gerek yok).
# Amac: her yeni rapor, SADECE hourly pipeline calismasiyla degil,
# SON GONDERILEN raporla kiyaslanip "ne degisti" ozetini uretebilsin.
LAST_REPORTED_FILE = DATA_DIR / "last_reported_snapshot.json"

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


# DUZELTME (2026-11-18): eski compute_state, skor 0.10-0.35 ARASINDA
# kaldiginda -- ger çek bir "iki taraf da güçlü" durumu olmasa bile --
# HER ZAMAN "CONFLICT" donduruyordu. Bu yuzden "-0.349" gibi sirf ESIGE
# YAKIN (ama zayif) skorlar da CONFLICT kovasina dusuyor, "35 CONFLICT"
# gibi kabarik ve anlamsiz bir grup olusturuyordu -- Reis'in "bir sürü
# ondalik rakam, ne demek belli degil" sikayetinin asil kok nedeni
# buydu. Artik GERCEK celiski SADECE core/synthesis_engine.py'deki ile
# AYNI kural ile belirleniyor: her iki tarafta da (bull_weight VE
# bear_weight) guclu kanit var VE birbirine yakinlar. Sirf zayif/sinirda
# kalan skorlar artik BULLISH/BEARISH olarak (dusuk yildizla) gosteriliyor
# -- "CONFLICT" etiketi artik SADECE gercek cekisme anlamina geliyor.
MIN_CONFLICT_WEIGHT = 0.35
CONFLICT_RATIO = 0.70
NEUTRAL_FLOOR = 0.20   # bunun altindaki |skor| artik yildizsiz NEUTRAL


def compute_state(score, evidence_count, bull_weight=0.0, bear_weight=0.0):
    """
    Skor + agirlik bazli state:
    - Hiç kanıt yok → INSUFFICIENT
    - Her iki tarafta da guclu VE birbirine yakin agirlik → CONFLICT (gercek cekisme)
    - |skor| < 0.20 → NEUTRAL (yildizsiz)
    - skor > 0 → BULLISH (yildiz sayisi |skor|'e gore)
    - skor < 0 → BEARISH (yildiz sayisi |skor|'e gore)
    """
    if evidence_count == 0:
        return "INSUFFICIENT"

    if evidence_count == 1 and abs(score) < 0.05:
        return "INSUFFICIENT"

    if bull_weight >= MIN_CONFLICT_WEIGHT and bear_weight >= MIN_CONFLICT_WEIGHT:
        max_w = max(bull_weight, bear_weight)
        min_w = min(bull_weight, bear_weight)
        if max_w > 0 and (min_w / max_w) >= CONFLICT_RATIO:
            return "CONFLICT"

    if abs(score) < NEUTRAL_FLOOR:
        return "NEUTRAL"

    return "BULLISH" if score > 0 else "BEARISH"


def star_rating(score):
    """|skor| -> 1-5 yildiz. %20=1, %40=2, %60=3, %80=4, %100=5 (Reis'in talimati)."""
    a = abs(score)
    if a >= 0.80:
        return 5
    if a >= 0.60:
        return 4
    if a >= 0.40:
        return 3
    if a >= 0.20:
        return 2
    return 1


# ============================================================
# GORSEL GENISLIK DUZELTMESI (Reis'in 2026-11-19 bulgusu: "siralamalar
# biraz kaymis", CTA TERMINAL'deki cta_email_sender.py'de AYNI gun
# yapilan duzeltmeyle PARALEL/AYNI mantik)
# ============================================================
#
# KOK NEDEN: bu dosyada satirlar (orn. "  • USDCAD  🟢⬆️ ⭐⭐⭐  +0.58")
# HICBIR sabit genislik kullanmiyordu -- kod ismi (USDCAD=6 harf, SI=2
# harf) ve yildiz sayisi (1-5) satirdan satira degistigi icin ok+yildiz
# ve skor sutunlari her satirda FARKLI bir yatay konumda basliyordu.
# Ayrica emoji'ler (🟢⬆️⭐) Python'un len()'ine gore 1 kod noktasi ama
# cogu monospace/email fontunda 2 sutun genisliginde render ediliyor --
# bu yuzden duz len()-bazli bir :<N padding'i de tek basina yetmezdi.
_VARYASYON_SECICI = {"️", "︎"}

# ============================================================
# ORTA-DUZEY VURGU + RENK (Reis'in 2026-11-19 ikinci istegi: "urun
# isimlerini az buyult kalinlastir", "yukari/asagi yazilarinin yanina
# ok birak, yazilari az buyult kalinlastir", "yuzdelik artis/azalisi
# yesil/kirmizi yazabilir misin")
#
# Telegram HTML'i SADECE b/i/u/s/code/pre/a/tg-spoiler/blockquote
# destekliyor -- OZEL renk/font-size YOK. Bu yuzden bu 3 yeni vurgu
# da (orta-boy-kalin, yesil, kirmizi) gorunmez sentinel karakterlerle
# isaretlenir: Telegram'a giden metinden TAMAMEN silinir (bkz.
# _telegram_icin_temizle), email HTML'inde ise <span>'e cevrilir
# (bkz. email_msg insaati). Baslik vurgusu (<b>...</b>, zaten
# Telegram-safe) ile KARISTIRILMAMALI -- o ayri ve degismedi.
# ============================================================
_VURGU2_BASLA = "\x01"
_VURGU2_BITIR = "\x02"
_YESIL_BASLA = "\x03"
_YESIL_BITIR = "\x04"
_KIRMIZI_BASLA = "\x05"
_KIRMIZI_BITIR = "\x06"
_SENTINEL_KARAKTERLERI = {
    _VURGU2_BASLA, _VURGU2_BITIR, _YESIL_BASLA, _YESIL_BITIR,
    _KIRMIZI_BASLA, _KIRMIZI_BITIR,
}


def _vurgu2(s):
    """Orta-duzey vurgu: urun kodlari, 'Yukarı'/'Aşağı' kelimeleri.
    Baslik vurgusundan (16px/900) kucuk tutuluyor (14px/700) ki her
    satirin HER YERI baslik gibi gorunmesin."""
    return f"{_VURGU2_BASLA}{s}{_VURGU2_BITIR}"


def _yesil(s):
    return f"{_YESIL_BASLA}{s}{_YESIL_BITIR}"


def _kirmizi(s):
    return f"{_KIRMIZI_BASLA}{s}{_KIRMIZI_BITIR}"


def _telegram_icin_temizle(s):
    """Email-only sentinel'leri Telegram'a giden metinden siler --
    Telegram'in HTML parser'i bu karakterleri TANIMAZ, birakilirsa
    mesaj reddedilebilir veya cop karakter olarak gorunur."""
    for ch in _SENTINEL_KARAKTERLERI:
        s = s.replace(ch, "")
    return s


def _karakter_genislik(ch):
    if ch in _VARYASYON_SECICI or ch in _SENTINEL_KARAKTERLERI:
        return 0
    cp = ord(ch)
    if (
        0x1F300 <= cp <= 0x1FAFF
        or 0x2600 <= cp <= 0x27BF
        or 0x2190 <= cp <= 0x21FF
        or 0x2B00 <= cp <= 0x2BFF  # Misc Symbols & Arrows (⭐⬆⬇ vb.)
    ):
        return 2
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("W", "F"):
        return 2
    return 1


def _gorsel_genislik(s):
    return sum(_karakter_genislik(ch) for ch in s)


def _pad(s, width):
    """len()-bazli :<N yerine GORSEL genislige gore sola-hizali doldurma."""
    eksik = width - _gorsel_genislik(s)
    return s + (" " * eksik if eksik > 0 else "")


# Sabit sutun genislikleri -- kod ismi ve ok+yildiz blogu artik HER
# satirda AYNI yatay konumda basliyor, skor da onlarin ardindan hep ayni
# yerden.
_KOD_GENISLIK = 8
_TAG_GENISLIK = 16  # "🟢⬆️ " (gorsel ~5) + 5 yildiz (gorsel 10) + pay


def _kod_satirlari(kodlar, basina=8):
    """Reis'in 2026-11-19 istegi: NOTR/YETERSIZ gibi uzun kod listeleri
    (40+ kod) tek bir paragrafta ust uste binmesin diye sabit sayida
    kod iceren satirlara bolunur."""
    satirlar = []
    for i in range(0, len(kodlar), basina):
        satirlar.append("  " + ", ".join(kodlar[i:i + basina]))
    return satirlar


def intensity_tag(score):
    """Yon oku (renkli emoji, hem Telegram hem email'de HTML'siz calisir)
    + sari yildizlar. Reis'in talimati: yildizlar sari, yukari ok yesil,
    asagi ok (dogal olarak) kirmizi -- emoji rengi zaten sabit oldugu
    icin HTML <span style> gerekmiyor, Telegram'in sinirli HTML seti de
    bu sekilde bozulmuyor."""
    arrow = "🟢⬆️" if score > 0 else "🔴⬇️"
    stars = "⭐" * star_rating(score)
    return f"{arrow} {stars}"


def format_group(title, items):
    """Bir grup için satırlar üret.

    items: (code, score, state, bull_weight, bear_weight) tuple listesi.
    """
    if not items:
        return []

    groups = {"BULLISH": [], "BEARISH": [], "CONFLICT": [], "NEUTRAL": [], "INSUFFICIENT": []}
    for code, sc, state, bw, brw in items:
        if state in groups:
            groups[state].append((code, sc, bw, brw))

    for k in groups:
        groups[k].sort(key=lambda x: abs(x[1]), reverse=True)

    lines = [f"═══ <b>{title}</b> ═══", ""]

    if groups["BULLISH"]:
        lines.append(f"🟢 <b>BULLISH</b> ({len(groups['BULLISH'])})")
        for code, sc, bw, brw in groups["BULLISH"][:12]:
            lines.append(f"  • {_vurgu2(_pad(code,_KOD_GENISLIK))} {_pad(intensity_tag(sc),_TAG_GENISLIK)} <code>{sc:+.2f}</code>")
        lines.append("")

    if groups["BEARISH"]:
        lines.append(f"🔴 <b>BEARISH</b> ({len(groups['BEARISH'])})")
        for code, sc, bw, brw in groups["BEARISH"][:12]:
            lines.append(f"  • {_vurgu2(_pad(code,_KOD_GENISLIK))} {_pad(intensity_tag(sc),_TAG_GENISLIK)} <code>{sc:+.2f}</code>")
        lines.append("")

    if groups["CONFLICT"]:
        # DUZELTME (2026-11-18): artik burada TEK skor degil, iki tarafin
        # agirligi gosteriliyor -- "CONFLICT" artik gercekten "iki taraf
        # da guclu" anlamina geldigi icin hangi tarafin ne kadar guclu
        # oldugunu gormek, tek bir yaniltici sayidan daha anlamli.
        lines.append(f"⚡ <b>ÇELİŞKİ</b> ({len(groups['CONFLICT'])})  — iki taraf da güçlü, net yön yok")
        for code, sc, bw, brw in groups["CONFLICT"][:12]:
            # DUZELTME (2026-11-18, Reis'in "BULLISH duzeldi ama altinda
            # yine anlamsiz rakamlar var" bulgusu): ham agirlik toplamlari
            # (orn. "5.77 / 4.68") kanit sayisi arttikca sinirsiz
            # buyuyebildigi icin tek basina HICBIR SEY ifade etmiyordu.
            # Artik iki tarafin TOPLAM icindeki PAYI (yuzde) gosteriliyor
            # -- "%55 / %45" gibi -- hem sezgisel hem de ne kadar
            # kiyasiya oldugunu (50/50'ye ne kadar yakin) dogrudan anlatiyor.
            total = bw + brw
            pct_up = round(bw / total * 100) if total > 0 else 50
            pct_down = 100 - pct_up
            # Reis'in 2026-11-19 ikinci istegi: "Yukarı"/"Aşağı" yanina ok
            # birak, yazilari az buyult-kalinlastir, yuzdeyi yesil/kirmizi
            # yap (sadece email'de renk gorunur, Telegram'da sentinel'ler
            # silinir -- bkz. _telegram_icin_temizle).
            lines.append(
                f"  • {_vurgu2(_pad(code,_KOD_GENISLIK))} "
                f"🟢⬆️ {_vurgu2('Yukarı')}: <code>{_yesil(f'%{pct_up}')}</code> / "
                f"🔴⬇️ {_vurgu2('Aşağı')}: <code>{_kirmizi(f'%{pct_down}')}</code>"
            )
        lines.append("")

    if groups["NEUTRAL"]:
        lines.append(f"⚪ <b>NÖTR</b> ({len(groups['NEUTRAL'])})")
        lines.extend(_kod_satirlari([c for c, _, _, _ in groups["NEUTRAL"]]))
        lines.append("")

    if groups["INSUFFICIENT"]:
        lines.append(f"⚫ <b>YETERSİZ VERİ</b> ({len(groups['INSUFFICIENT'])})")
        lines.extend(_kod_satirlari([c for c, _, _, _ in groups["INSUFFICIENT"]]))
        lines.append("")

    return lines


def load_last_reported():
    """Son GERCEKTEN GONDERILMIS raporun ozet durumunu okur (yoksa bos)."""
    if not LAST_REPORTED_FILE.exists():
        return {}
    try:
        data = json.loads(LAST_REPORTED_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        return data
    except (OSError, json.JSONDecodeError):
        return {}


def save_last_reported(assets_summary, generated_at):
    """Bu raporu 'son gonderilen' olarak kaydeder -- bir sonraki rapor
    bununla kiyaslanacak."""
    LAST_REPORTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {"generated_at": generated_at, "assets": assets_summary}
    LAST_REPORTED_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def build_changes_box(prev, current_assets, now_label):
    """Reis'in talimati (2026-11-18): raporun EN BASINDA, bir onceki
    GONDERILEN rapora gore ne degisti -- durum degisikligi, yildiz
    sayisi degisikligi veya CONFLICT'e girip-cikma. Ayni kalanlar
    gosterilmez (yoksa yine kalabalik/anlamsiz olur)."""
    if not prev or not prev.get("assets"):
        return []  # ilk rapor -- kiyaslanacak onceki veri yok

    prev_assets = prev["assets"]
    prev_label = (prev.get("generated_at") or "—")[:16]

    change_lines = []
    for code, cur in current_assets.items():
        old = prev_assets.get(code)
        if old is None:
            continue  # yeni varlik, "degisim" sayilmaz

        old_state, new_state = old.get("state"), cur.get("state")
        old_stars, new_stars = old.get("stars", 0), cur.get("stars", 0)

        if old_state == new_state and old_stars == new_stars:
            continue  # gercek bir degisim yok, atla

        if new_state == "CONFLICT" and old_state != "CONFLICT":
            change_lines.append((abs(cur.get("score", 0)), f"  • {code}: yön belirsizleşti → ⚡ ÇELİŞKİ"))
        elif old_state == "CONFLICT" and new_state != "CONFLICT":
            tag = intensity_tag(cur.get("score", 0))
            change_lines.append((abs(cur.get("score", 0)), f"  • {code}: ÇELİŞKİ çözüldü → {tag}"))
        elif old_state != new_state:
            change_lines.append((abs(cur.get("score", 0)), f"  • {code}: {old_state} → {new_state}  {intensity_tag(cur.get('score', 0))}"))
        elif new_stars > old_stars:
            change_lines.append((abs(cur.get("score", 0)), f"  • {code}: güçlendi, {'⭐' * old_stars} → {intensity_tag(cur.get('score', 0))}"))
        elif new_stars < old_stars:
            change_lines.append((abs(cur.get("score", 0)), f"  • {code}: zayıfladı, {'⭐' * old_stars} → {intensity_tag(cur.get('score', 0))}"))

    if not change_lines:
        return []

    change_lines.sort(key=lambda x: x[0], reverse=True)
    top = [line for _, line in change_lines[:8]]

    box = [
        f"📊 <b>SON RAPORDAN BU YANA DEĞİŞENLER</b> ({prev_label} → {now_label})",
    ]
    box.extend(top)
    if len(change_lines) > 8:
        box.append(f"  … ve {len(change_lines) - 8} değişiklik daha")
    box.append("")
    return box


def build_message(snapshot):
    results = snapshot.get("results", {})
    if not results:
        return "⚠️ CTA ERHAN RAPORU\n\nSnapshot boş."

    now_tr = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    now_label = snapshot.get("generated_at", "—")[:16]

    main_items = []
    us_items = []
    asia_items = []
    current_assets = {}

    for code, r in results.items():
        score = soften(r.get("score", 0.0))
        ev_count = r.get("evidence_count", 0)
        bull_weight = r.get("bull_weight", 0.0) or 0.0
        bear_weight = r.get("bear_weight", 0.0) or 0.0
        state = compute_state(score, ev_count, bull_weight, bear_weight)

        current_assets[code] = {
            "state": state,
            "score": score,
            "stars": star_rating(score) if state in ("BULLISH", "BEARISH") else 0,
        }

        cat = categorize(code)
        item = (code, score, state, bull_weight, bear_weight)

        if cat == "us_stock":
            us_items.append(item)
        elif cat == "asia_stock":
            asia_items.append(item)
        else:
            main_items.append(item)

    total = len(main_items) + len(us_items) + len(asia_items)

    # DEGISENLER KUTUSU -- onceki GONDERILEN raporla kiyasla, raporun
    # EN BASINA koy (Reis'in talimati).
    prev_reported = load_last_reported()
    lines = build_changes_box(prev_reported, current_assets, now_label)

    lines.extend([
        "📊 <b>CTA ERHAN RAPORU</b> (Wayne Protocol)",
        f"🕐 {now_tr}",
        "",
    ])

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

    # Bu raporu "son gonderilen" olarak kaydet -- bir sonraki rapor
    # bununla kiyaslanacak. mark_slot_sent() ile AYNI felsefe: gonderim
    # (email/telegram) basarisiz olsa bile kaydedilir, amac mukemmel
    # teslimat degil, bir sonraki kiyasin DOGRU referans noktasina
    # sahip olmasi.
    save_last_reported(current_assets, now_label)

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
    # DUZELTME (2026-11-19, Reis'in "kalin harfler yok, hizalama da yok"
    # bulgusu): multipart/alternative'de e-posta istemcisi SON eklenen
    # parcayi tercih eder/gosterir (RFC 2046 -- parcalar en basitten en
    # "zengin"e siralanmali). HTML once eklenmisti, duz metin SONRA --
    # yani Gmail HTML'i degil duz metni gosteriyordu, bu da hem kalin
    # basliklarin hem de monospace hizalamanin KAYBOLMASINA sebep
    # oluyordu. CTA TERMINAL ve GOZLEM'de siralama zaten dogruydu
    # (plain once, html sonra) -- burada da AYNI siraya getirildi.
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

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
    #
    # AYRICA bu turda EKLENDI: workflow_dispatch (Reis'in elle "Run
    # workflow" ile tetiklemesi, GitHub Actions bunu GITHUB_EVENT_NAME
    # ortam degiskenine yazar) HER ZAMAN pencereyi VE "zaten gonderildi"
    # kontrolunu ATLAR -- boylece Reis istedigi an, zamanlama penceresi
    # disinda bile, "test bildirimi" gonderip SMTP/Telegram kimlik
    # bilgilerinin hala gecerli oldugunu dogrulayabilir (GOZLEM'deki
    # (kurumsal-makro-gozlem-terminali) check_schedule.py'de ZATEN
    # kullanilan AYNI desen).
    #
    # DUZELTME (2026-11-27, Reis'in "CTA ERHAN RAPORU saatte bir geliyor,
    # 3 sabit saatte gelmesi gerekiyordu" bulgusu uzerine -- KOK SEBEP):
    # Reis'in Docker'inda 7/24 calisan otomatik dongu (scripts/
    # trigger_github_pipeline.py, saatlik), GitHub'in "schedule" tetikleyi-
    # cisinin bazen gec/kacirmasina karsi, fetch.yml'yi DOGRUDAN
    # workflow_dispatch API'siyle tetikliyordu -- ama bu GITHUB_EVENT_NAME'i
    # workflow_dispatch'e esitledigi icin YUKARIDAKI is_manual=True oluyor
    # ve her saat, GUN/SAAT FARKETMEKSIZIN, GERCEK bir rapor maili/Telegram
    # mesaji KOSULSUZ gonderiliyordu -- 3-slot/gun kurali fiilen hic
    # calismiyordu. Artik trigger_github_pipeline.py cagrisina
    # "trigger_source=docker_auto" input'u eklendi (fetch.yml'den
    # TRIGGER_SOURCE ortam degiskenine aktariliyor) -- Reis'in GERCEKTEN
    # GitHub arayuzunden elle "Run workflow"a basmasi bu alani BOS
    # birakir (varsayilan ""), SADECE o durumda kosulsuz/aninda gonderim
    # eskisi gibi calisir. Otomatik Docker dongusunden gelen cagrilar
    # artik is_manual=False sayilir, yani normal pencere + "zaten
    # gonderildi mi" kontrolune TABI olur.
    is_manual = (
        os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
        and not os.environ.get("TRIGGER_SOURCE", "").strip()
    )
    now_utc = datetime.now(timezone.utc)
    today_paris = now_utc.astimezone(PARIS_TZ).date().isoformat()

    if is_manual:
        due_slot = get_due_slot(now_utc)
        print(
            f"[ZAMANLAMA] Manuel tetikleme (workflow_dispatch) -- pencere VE "
            f"'zaten gonderildi' kontrolu ATLANIYOR, bildirim HER HALUKARDA "
            f"gonderiliyor (now_utc={now_utc.isoformat()})."
        )
    else:
        due_slot = get_due_slot(now_utc)
        if due_slot is None:
            print(
                f"[ZAMANLAMA] Simdi periyodik bildirim penceresinde degil "
                f"(now_utc={now_utc.isoformat()}) -- Telegram ve Email ATLANIYOR."
            )
            return

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

    # DUZELTME (2026-11-19, Reis'in "basliklar daha kalin/belirgin olsun"
    # istegi): Telegram sadece <b> (KALIN) destekliyor, BUYUK font-size
    # DESTEKLEMIYOR (bilinen platform siniri) -- bu yuzden msg (Telegram'a
    # giden) <b> ile ayniyla kaliyor, SADECE email'in HTML govdesinde
    # <b>...</b> daha buyuk+kalin bir span'a yukseltiliyor. Bu rapordaki
    # TUM <b> kullanimlari zaten birer baslik/etiket oldugu icin (skor gibi
    # veri degerleri <code> ile isaretleniyor, <b> ile DEGIL) kapsamli bir
    # degisim guvenli.
    email_msg = re.sub(
        r"<b>(.*?)</b>",
        r'<span style="font-size:16px;font-weight:900">\1</span>',
        msg,
    )
    # Reis'in 2026-11-19 ikinci istegi: urun kodlari + "Yukarı"/"Aşağı"
    # orta-buyuklukte kalin, yukselis/dusus yuzdeleri yesil/kirmizi --
    # SADECE email HTML'inde (Telegram'da bu sentinel'ler silinir, bkz.
    # asagidaki _telegram_icin_temizle cagrisi).
    email_msg = (
        email_msg.replace(_VURGU2_BASLA, '<span style="font-size:14px;font-weight:700">')
        .replace(_VURGU2_BITIR, "</span>")
        .replace(_YESIL_BASLA, '<span style="color:#2e7d32;font-weight:700">')
        .replace(_YESIL_BITIR, "</span>")
        .replace(_KIRMIZI_BASLA, '<span style="color:#c62828;font-weight:700">')
        .replace(_KIRMIZI_BITIR, "</span>")
    )
    html_msg = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px;">
          <pre style="font-family: 'Courier New', Courier, monospace; font-size: 13px; white-space: pre-wrap; word-wrap: break-word;">{email_msg}</pre>
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

    # Telegram'a giden metin bu yeni sentinel'leri TANIMIYOR -- orta-boy-
    # kalin/yesil/kirmizi SADECE email'e ozel, Telegram'dan tamamen silinir.
    telegram_msg = _telegram_icin_temizle(msg)
    if not email_basarili:
        telegram_msg = telegram_msg + "\n\n⚠️ EMAIL GÖNDERİMİ BAŞARISIZ"

    send_telegram(telegram_msg)

    # ACİL DÜZELTME (2026-10-27) -- gonderim denendikten HEMEN SONRA bu
    # slot'u "bugun gonderildi" olarak isaretle (bkz. core/notification_
    # state.py). Email/Telegram'dan biri basarisiz olsa bile isaretlenir
    # -- amac mukemmel teslimati garanti etmek degil, AYNI slot icin
    # TEKRAR TEKRAR denemeyi (ve basariliysa CIFTE bildirimi) onlemek;
    # kalici bir SMTP/Telegram hatasi zaten her iki fonksiyonun kendi
    # [ERR] loglarinda gorunur. Manuel (workflow_dispatch) test gonderimleri
    # GUN+SLOT kaydini KIRLETMEMELI -- due_slot gercek bir zamanlanmis
    # slot DEGILSE (manuel calistirma pencere disindaysa None olabilir)
    # de isaretleme atlanir.
    if not is_manual and due_slot is not None:
        mark_slot_sent(due_slot, today_paris)


if __name__ == "__main__":
    main()
