"""
CTA ERHAN TERMİNALİ — app.py (v22 - KARAR MOTORU + LOG + KOYU TEMA)
"""

import streamlit as st
import json
import sqlite3
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CTA ERHAN Terminali",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- HARICI CSS YÜKLE ----------
_css_path = Path(__file__).parent / "styles.css"
if _css_path.exists():
    with open(_css_path, "r", encoding="utf-8") as _f:
        st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)

# ============================================================
# YOLLAR
# ============================================================
PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
TWEETS_DIR = DATA_DIR / "tweets"
ANALYSIS_DIR = DATA_DIR / "analysis"
RSS_DIR = DATA_DIR / "rss"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
COT_DB = DATA_DIR / "evidence.db"


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


def load_synthesis_snapshot():
    f = SNAPSHOTS_DIR / "latest.json"
    if not f.exists():
        return {}
    try:
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}


def load_cot_for_product(product):
    if not COT_DB.exists():
        return []
    try:
        with sqlite3.connect(str(COT_DB)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM evidence WHERE source_type = 'COT' AND product = ?",
                (product.upper().strip(),)
            ).fetchall()
            results = []
            for row in rows:
                d = dict(row)
                if d.get("metadata_json"):
                    try:
                        d["metadata"] = json.loads(d["metadata_json"])
                    except Exception:
                        d["metadata"] = {}
                results.append(d)
            return results
    except Exception:
        return []


# ============================================================
# ÜRÜN KATEGORİLERİ
# ============================================================
product_categories = {
    "Endeksler":  ["ES", "NQ", "YM", "RTY", "NK", "MSCI_EM", "MSCI_EAFE"],
    "Faizler":    ["ZT", "ZF", "ZN", "ZB", "UB", "UWB", "SR1", "SR3", "ZQ"],
    "Dövizler":   ["DXY", "6E", "6J", "6B", "6A", "6C", "6N", "6S"],
    "Enerji":     ["CL", "NG", "HO", "RB", "BZ"],
    "Metaller":   ["GC", "SI", "HG", "PL", "PA"],
    "Tahıllar":   ["ZC", "ZS", "ZL", "ZM", "ZW", "KE"],
}

product_names = {
    "ES": "S&P 500 E-mini", "MES": "Micro S&P 500",
    "NQ": "Nasdaq 100 E-mini", "MNQ": "Micro Nasdaq 100",
    "RTY": "Russell 2000 E-mini", "YM": "Dow E-mini",
    "CL": "Ham Petrol", "MCL": "Micro Ham Petrol", "NG": "Doğal Gaz",
    "GC": "Altın", "MGC": "Micro Altın", "SI": "Gümüş", "HG": "Bakır", "PL": "Platin",
    "6E": "Euro FX", "6J": "Japon Yeni", "6B": "İngiliz Sterlini",
    "6A": "Avustralya Doları", "6C": "Kanada Doları", "6S": "İsviçre Frangı",
    "ZC": "Mısır", "ZS": "Soya Fasulyesi", "ZW": "Buğday", "ZL": "Soya Yağı", "ZM": "Soya Küspesi",
    "NK": "Nikkei 225",
    "MSCI_EM": "MSCI Emerging Markets",
    "MSCI_EAFE": "MSCI EAFE",
    "ZT": "2Y Note", "ZF": "5Y Note", "ZN": "10Y Note", "ZB": "30Y Bond",
    "UB": "Ultra Bond", "UWB": "Ultra 10Y", "SR1": "SOFR 1M", "SR3": "SOFR 3M",
    "ZQ": "Fed Funds",
    "6N": "Yeni Zelanda Doları",
    "DXY": "US Dollar Index",
    "HO": "Kalorifer Yakıtı", "RB": "Benzin RBOB", "BZ": "Brent Petrol",
    "PA": "Paladyum",
    "KE": "Buğday (HRW)",
}

TRACKED_CODES = set()
for _cat_list in product_categories.values():
    TRACKED_CODES.update(_cat_list)

TRACKED_CODES.update({"MES", "MNQ", "MCL", "MGC", "M2K", "MYM"})

COT_ALIASES = {
    "SPX500", "NAS100", "US10Y", "XAUUSD", "XAGUSD", "UKOIL",
    "EURUSD", "GBPUSD", "USDJPY", "NZDUSD",
    "MES", "MNQ", "MCL", "MGC", "M2K", "MYM",
}

EGZOTIK = {
    "TZT1", "QS1", "XB1", "HO1", "LA1", "LN1", "MXCN",
    "CSI1000", "SH000905", "SHSN300", "XIN9I", "HSBIO",
    "VVIX", "CIBR", "CNXT", "AGI", "OPEN", "NBIS",
    "SAP", "HUBS", "WDAY", "TEAM", "MRVL",
    "CRM", "CSCO", "NOW", "LULU", "CRWD",
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<h1 style="color:#00E5FF;">◉ CTA ERHAN</h1>', unsafe_allow_html=True)
    st.caption("Vadeli İşlemler / CTA / Piyasa İstihbaratı")
    st.divider()
    st.subheader("ÜRÜN SEÇİMİ")
    selected_category = st.selectbox("Kategori", list(product_categories.keys()), index=0)
    selected_product = st.selectbox("Ürün", product_categories[selected_category], index=0)
    st.markdown(f'<h2 style="color:#00E5FF;">{selected_product}</h2>', unsafe_allow_html=True)
    st.caption(product_names.get(selected_product, ""))
    st.divider()
    st.subheader("SİSTEM SINIRI")
    st.success("SALT OKUNUR İSTİHBARAT")

# ============================================================
# VERİLER
# ============================================================
all_tweets = load_json_files(TWEETS_DIR, "tweets_*.json")
all_analysis = load_json_files(ANALYSIS_DIR, "analysis_*.json")
all_rss = load_json_files(RSS_DIR, "rss_*.json")
synthesis_snapshot = load_synthesis_snapshot()

x_with_assets = [a for a in all_analysis if a.get("varliklar") and len(a.get("varliklar", [])) > 0]
x_analyzed = len(x_with_assets)
x_total = len(all_analysis)
rss_total = len(all_rss)


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def soften_score(score, cap=0.75):
    try:
        s = float(score)
    except Exception:
        return 0.0
    if s > cap:
        return cap
    if s < -cap:
        return -cap
    return s


def build_segments_for(code):
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


def state_color(state, score=0.0):
    if state == "BULLISH":
        return "#00E676"
    if state == "BEARISH":
        return "#FF3B3B"
    if state == "CONFLICT":
        return "#FF8C00"
    if state == "NEUTRAL":
        return "#FFC107"
    return "#333333"


def offlist_products():
    offlist = {}
    for item in all_analysis:
        username = (item.get("username") or "").strip()
        for v in (item.get("varliklar") or []):
            sembol = (v.get("sembol") or "").upper().strip()
            if sembol and sembol not in TRACKED_CODES:
                e = offlist.setdefault(sembol, {"isim": v.get("isim", ""), "kaynaklar": set(), "yonler": set()})
                if username:
                    e["kaynaklar"].add("@" + username)
                e["yonler"].add(str(v.get("yon", "?")))
    for item in all_rss:
        for v in (item.get("varliklar") or []):
            sembol = (v.get("sembol") or "").upper().strip()
            if sembol and sembol not in TRACKED_CODES:
                e = offlist.setdefault(sembol, {"isim": v.get("isim", ""), "kaynaklar": set(), "yonler": set()})
                e["kaynaklar"].add("tickmill")
                e["yonler"].add(str(v.get("yon", "?")))
    return offlist


def categorize_offlist(code):
    c = code.upper().strip()
    abd_endeks = {"SPX500", "NAS100", "DXY", "VIX", "US10Y", "GER40", "UK100", "JP225"}
    if c in abd_endeks:
        return "ABD_ENDEKS"
    abd_etf = {"TLT", "SPY", "QQQ", "KWEB", "FXI", "EWJ", "EWT", "EWY", "KSTR", "HSI", "HSTECH", "HSCEI"}
    if c in abd_etf:
        return "ABD_ETF"
    emtia = {"XAUUSD", "XAGUSD", "UKOIL", "USOUSD", "BTCUSD", "SOL",
             "EURUSD", "GBPUSD", "NZDUSD", "USDJPY", "USDCAD", "USDCHF", "AUDUSD"}
    if c in emtia:
        return "EMTIA"
    us_stocks = {"AAPL", "AMD", "AMZN", "AVGO", "GOOGL", "META", "MSFT", "NVDA", "TSLA", "BABA"}
    if c in us_stocks:
        return "ABD_HISSE"
    return "ASYA"


# ============================================================
# BAŞLIK
# ============================================================
st.markdown('<h1 style="color:#00E5FF;">◉ CTA ERHAN TERMİNALİ</h1>', unsafe_allow_html=True)
st.markdown(
    f'<div class="aktif-urun-kutu">'
    f'<span class="aktif-urun-baslik">AKTİF ÜRÜN: </span>'
    f'<span class="aktif-urun-deger">{selected_product} — {product_names.get(selected_product, "")}</span>'
    f'</div>',
    unsafe_allow_html=True,
)


def make_bar_html(yon, skor):
    yon_str = str(yon).upper().strip()
    try:
        skor_val = float(skor)
    except Exception:
        skor_val = 0.0

    if "YUKARI" in yon_str or "BULL" in yon_str:
        color = "#00E676"; emoji = "🟢"
        score = abs(skor_val) if skor_val != 0 else 0.5
    elif "AŞAĞI" in yon_str or "BEAR" in yon_str:
        color = "#FF3B3B"; emoji = "🔴"
        score = -abs(skor_val) if skor_val != 0 else -0.5
    else:
        color = "#FFC107"; emoji = "🟡"
        score = 0.0

    pct = min(100, abs(score) * 100)
    return f'''<div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
        <span style="font-size:13px;font-weight:700;color:#FFF;min-width:70px;">{emoji} {yon}</span>
        <div style="flex:1;background:#1a1a1a;height:14px;border-radius:3px;overflow:hidden;border:1px solid #1E4FA8;">
            <div style="width:{pct:.0f}%;height:100%;background:{color};"></div>
        </div>
        <span style="color:{color};font-weight:800;font-size:13px;min-width:45px;text-align:right;">{score:+.2f}</span>
    </div>'''


# ============================================================
# SEKMELER
# ============================================================
tab_pano, tab_x = st.tabs(["📊 PANO", f"📱 X ANALİZLERİ ({x_analyzed} / {x_total})"])


# ============================================================
# SEKME 1 — PANO
# ============================================================
with tab_pano:
    col_left, col_mid, col_right = st.columns(3)

    # ---------- SOL: CTA RADARI ----------
    with col_left:
        st.markdown("### 🔴 CTA RADARI")

        if synthesis_snapshot:
            results = synthesis_snapshot.get("results", {})

            if results:
                STATE_ICONS = {
                    "BULLISH": "🟢", "BEARISH": "🔴", "NEUTRAL": "⚪",
                    "CONFLICT": "🟠", "INSUFFICIENT": "⚫",
                }

                html_rows = ""
                for code, r in sorted(results.items()):
                    if code.upper() not in TRACKED_CODES:
                        continue

                    raw_score = r.get("score", 0.0)
                    score = soften_score(raw_score, cap=0.75)
                    segments = build_segments_for(code)
                    state = compute_state_from_segments(segments, r.get("state", "INSUFFICIENT"))
                    emoji = STATE_ICONS.get(state, "⚫")

                    kaynak_set = []
                    seen_k = set()
                    for _, kaynak in segments:
                        if kaynak not in seen_k:
                            seen_k.add(kaynak)
                            kaynak_set.append(kaynak)
                    kanit = len(kaynak_set)
                    kaynak_str = ", ".join(kaynak_set) if kaynak_set else "—"

                    color = state_color(state, score)
                    pct = min(100, abs(score) * 100) if state != "INSUFFICIENT" else 0

                    if state == "INSUFFICIENT":
                        durum_html = (
                            '<div style="display:flex;align-items:center;gap:10px;">'
                            f'<span style="font-size:14px;color:#666;min-width:110px;">{emoji} —</span>'
                            '<div style="flex:1;background:#0a0a0a;height:16px;border-radius:3px;'
                            'border:1px solid #333;"></div>'
                            '<span style="color:#666;font-weight:800;font-size:13px;min-width:60px;text-align:right;">—</span>'
                            '</div>'
                        )
                    else:
                        durum_html = (
                            '<div style="display:flex;align-items:center;gap:10px;">'
                            f'<span style="font-size:14px;font-weight:700;color:#FFF;min-width:110px;">{emoji} {state}</span>'
                            f'<div style="flex:1;background:#1a1a1a;height:16px;border-radius:3px;overflow:hidden;border:1px solid #1E4FA8;">'
                            f'<div style="width:{pct:.0f}%;height:100%;background:{color};"></div>'
                            '</div>'
                            f'<span style="color:#FFF;font-weight:800;font-size:13px;min-width:60px;text-align:right;">{score:+.3f}</span>'
                            '</div>'
                        )

                    html_rows += f"""
                    <tr>
                        <td style="color:#00E5FF;font-size:16px;font-weight:800;padding:6px 8px;border-bottom:1px solid #1E4FA8;width:52px;">{code}</td>
                        <td style="padding:6px 8px;border-bottom:1px solid #1E4FA8;">{durum_html}</td>
                        <td style="color:#FFF;font-size:14px;font-weight:800;padding:6px 4px;border-bottom:1px solid #1E4FA8;text-align:center;width:45px;">{kanit}</td>
                        <td style="color:#B8D4FF;font-size:12px;font-weight:600;padding:6px 6px;border-bottom:1px solid #1E4FA8;width:130px;word-break:break-word;">{kaynak_str}</td>
                    </tr>
                    """

                html_table = f"""
                <div style="overflow-x:auto;">
                <table style="width:100%;border-collapse:collapse;background:#0a0a0a;border:1px solid #1E4FA8;border-radius:6px;">
                    <thead>
                        <tr style="background:#0F2A5C;">
                            <th style="color:#FFF;font-size:14px;font-weight:800;padding:8px 8px;text-align:left;border-bottom:2px solid #00E5FF;">KOD</th>
                            <th style="color:#FFF;font-size:14px;font-weight:800;padding:8px 8px;text-align:left;border-bottom:2px solid #00E5FF;">DURUM</th>
                            <th style="color:#FFF;font-size:14px;font-weight:800;padding:8px 4px;text-align:center;border-bottom:2px solid #00E5FF;">KANIT</th>
                            <th style="color:#FFF;font-size:14px;font-weight:800;padding:8px 6px;text-align:left;border-bottom:2px solid #00E5FF;">KAYNAK</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_rows}
                    </tbody>
                </table>
                </div>
                """
                tracked_count = sum(1 for c in results if c.upper() in TRACKED_CODES)
                iframe_height = 50 + tracked_count * 44
                components.html(html_table, height=iframe_height, scrolling=False)

                gen = synthesis_snapshot.get("generated_at", "—")
                st.caption(f"Snapshot: {gen} | Skor üst sınırı: ±0.75")
        else:
            st.info("Snapshot bulunamadı.")

    # ---------- ORTA: TICKMILL ----------
    with col_mid:
        st.markdown("### 📰 TICKMILL YORUMLARI")
        st.caption(f"Toplam: {rss_total} makale")

        if not all_rss:
            st.caption("Henüz RSS makalesi yok.")
        else:
            rss_html = ""
            for article in all_rss[-15:][::-1]:
                title_tr = article.get("title_tr", "").strip()
                title_en = article.get("title_en", "").strip()
                display_title = title_tr or title_en
                content_tr = article.get("content_tr", "").strip()
                content_en = article.get("content_en", "").strip()
                yorum = article.get("yorum", "").strip()
                varliklar = article.get("varliklar", [])
                published = article.get("published_at", "")

                varlik_html = ""
                for v in varliklar:
                    sembol = v.get("sembol", "?")
                    isim = v.get("isim", "")
                    vyon = v.get("yon", "NÖTR")
                    skor = v.get("skor", 0.5)
                    gerekce = v.get("gerekce", "")
                    bar = make_bar_html(vyon, skor)
                    varlik_html += (
                        f'<div style="background:#0a0a0a;border:1px solid #1E4FA8;border-radius:4px;padding:8px 12px;margin:6px 0;">'
                        f'<div style="color:#FFFFFF;font-size:16px;font-weight:800;margin-bottom:4px;">{sembol} — {isim}</div>'
                        f'{bar}'
                        f'<div style="color:#DDDDDD;font-size:14px;margin-top:4px;line-height:1.5;">{gerekce}</div>'
                        f'</div>'
                    )

                yorum_html = ""
                if yorum:
                    yorum_html = (
                        f'<div style="background:#0F2A5C;padding:10px 14px;border-radius:6px;margin:8px 0;border-left:4px solid #00E5FF;">'
                        f'<div style="color:#FFFFFF;font-size:14px;font-weight:800;margin-bottom:5px;">💬 YORUM</div>'
                        f'<div style="color:#FFFFFF;font-size:15px;font-weight:700;line-height:1.6;">{yorum}</div>'
                        f'</div>'
                    )

                original_html = ""
                if content_en:
                    original_html += f'<div style="color:#FFFFFF;font-size:14px;font-weight:800;margin:8px 0 4px;">🇬🇧 İngilizce:</div><div style="color:#DDDDDD;font-size:14px;line-height:1.6;">{content_en[:1500]}</div>'
                if content_tr:
                    original_html += f'<div style="color:#FFFFFF;font-size:14px;font-weight:800;margin:8px 0 4px;">🇹🇷 Türkçe:</div><div style="color:#DDDDDD;font-size:14px;line-height:1.6;">{content_tr[:1500]}</div>'

                rss_html += f'''
                <details style="margin:6px 0;border:1px solid #1E4FA8;border-radius:6px;background:#0a0a0a;">
                    <summary style="color:#FFFFFF;font-size:16px;font-weight:700;padding:10px 12px;cursor:pointer;list-style:none;">
                        📝 {display_title[:70]}
                    </summary>
                    <div style="padding:10px 12px;">
                        {yorum_html}
                        {varlik_html}
                        <details style="margin:8px 0;border:1px solid #333;border-radius:4px;background:#050505;">
                            <summary style="color:#FFFFFF;font-size:15px;font-weight:700;padding:8px 10px;cursor:pointer;list-style:none;">📄 Orijinal + Çeviri</summary>
                            <div style="padding:8px 10px;">{original_html}</div>
                        </details>
                        <div style="color:#999;font-size:12px;margin-top:6px;">🕐 {published}</div>
                    </div>
                </details>
                '''

            components.html(rss_html, height=700, scrolling=True)

    # ---------- SAĞ: KARAR MOTORU + COT RAPORU ----------
    with col_right:
        st.markdown(f"### 🎯 KARAR MOTORU: {selected_product}")

        try:
            from core.signal_engine import calculate_signal, MAJOR_PRODUCTS
            _sig = calculate_signal(selected_product)

            # LOG
            try:
                from core.signals_db import global_signals_db as _gdb
                from datetime import datetime as _dt, timezone as _tz
                _today = _dt.now(_tz.utc).strftime("%Y-%m-%d")
                _ex = _gdb.get_active_signal(selected_product)
                _log_it = True
                if _ex:
                    if ((_ex.get("created_at") or "")[:10] == _today and
                        _ex.get("signal") == _sig.get("signal")):
                        _log_it = False
                if _log_it:
                    _sig["signal_id"] = _gdb.log_signal(_sig)
            except Exception:
                pass

            _conf = _sig.get("confidence", 0)
            _signal = _sig.get("signal", "BEKLE")
            _skor = _sig.get("final_score", 0)
            _cot_s = _sig.get("cot_score", 0)
            _radar_s = _sig.get("radar_score", 0)
            _tm_s = _sig.get("tickmill_score", 0)
            _is_conflict = _sig.get("is_conflict", False)
            _conflict_src = _sig.get("conflict_sources", [])
            _signal_type = _sig.get("signal_type", "mixed")
            _validity = _sig.get("validity_reason", "mixed")
            _created = _sig.get("created_at", "")

            if "GÜÇLÜ AL" in _signal or _signal == "AL":
                _color = "#00E676"
            elif "GÜÇLÜ SAT" in _signal or _signal == "SAT":
                _color = "#FF3B3B"
            else:
                _color = "#999"

            st.markdown(f"""
            <div style="background:#0a0a0a;border:2px solid {_color};border-radius:6px;padding:12px;margin-bottom:8px;">
                <div style="font-size:24px;font-weight:900;color:{_color};margin-bottom:8px;">
                    {_signal}  <span style="font-size:16px;color:#FFF;">|</span>  <span style="font-size:16px;color:#00E5FF;">Güven %{_conf:.1f}</span>
                </div>
                <div style="font-size:11px;color:#AAA;">
                    {_created[:19].replace('T', ' ')} UTC | {_signal_type} sinyal | Validity: {_validity}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("COT", f"{_cot_s:+.3f}")
            with col_s2:
                st.metric("Radar", f"{_radar_s:+.3f}")
            with col_s3:
                st.metric("Tickmill", f"{_tm_s:+.3f}")

            if _is_conflict:
                st.warning(f"⚠️ ÇELİŞKİLİ SİNYAL — {' + '.join(_conflict_src)} ters yönde")

            st.caption(f"Skor: {_skor:+.4f} | Sinyal Tipi: {_signal_type}")

            if selected_product not in MAJOR_PRODUCTS:
                st.caption(f"ℹ️ Bu ürün Faz 2A kapsamı dışında. Sadece {', '.join(MAJOR_PRODUCTS)} için tam analiz var.")

        except Exception as _e:
            st.caption(f"⚠️ Karar motoru hatası: {_e}")

        st.divider()

        st.markdown(f"### 📊 COT RAPORU: {selected_product}")

        try:
            from sources.merkez_cot_loader import load_merkez_snapshot
            load_merkez_snapshot()
        except Exception as _e:
            st.caption(f"⚠️ MERKEZ tazeleme uyarısı: {_e}")

        cot_records = load_cot_for_product(selected_product)

        if not cot_records:
            st.caption(f"{selected_product} için COT kaydı bulunamadı.")
        else:
            cot = next((c for c in cot_records if c.get("metadata", {}).get("categories")), cot_records[0])
            metadata = cot.get("metadata", {}) if isinstance(cot.get("metadata"), dict) else {}
            categories = metadata.get("categories", {})
            interp = metadata.get("interpreter", {})
            report_type = metadata.get("report_type", "TFF")
            report_date = metadata.get("report_date", "")
            oi = metadata.get("open_interest", 0)

            st.caption(f"📅 {report_date} | CFTC {report_type} Raporu")

            yon = interp.get("cot_yon", "?")
            momentum = interp.get("momentum", "?")
            consensus = interp.get("consensus", "?")
            non_rep = interp.get("non_reportable", "YOK")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Yön", yon)
            with col_b:
                st.metric("Momentum", momentum)
            with col_c:
                st.metric("Konsensüs", consensus)

            if "TERS_INDIKATOR" in non_rep:
                st.warning(f"⚠️ TERS İNDİKATÖR: {non_rep}")
            elif non_rep == "NOTR":
                st.info("ℹ️ Non-Reportable: Nötr")
            elif non_rep == "YOK":
                st.caption("ℹ️ Non-Reportable verisi yok.")

            st.markdown("##### Kategori Detayları")
            if report_type == "TFF":
                cat_order = ["DEALER_INTERMEDIARY", "ASSET_MANAGER", "LEVERAGED_FUNDS", "OTHER_REPORTABLES", "NON_REPORTABLE"]
            else:
                cat_order = ["PRODUCER_MERCHANT", "SWAP_DEALER", "MANAGED_MONEY", "OTHER_REPORTABLE", "NON_REPORTABLE"]

            cat_labels = {
                "DEALER_INTERMEDIARY": "🏦 Dealer/Interm.",
                "ASSET_MANAGER": "💼 Asset Manager",
                "LEVERAGED_FUNDS": "🎯 Leveraged Funds",
                "OTHER_REPORTABLES": "👥 Other Reportables",
                "PRODUCER_MERCHANT": "🌾 Producer/Merchant",
                "SWAP_DEALER": "🔄 Swap Dealer",
                "MANAGED_MONEY": "💰 Managed Money",
                "OTHER_REPORTABLE": "👥 Other Reportable",
                "NON_REPORTABLE": "⚠️ Non-Reportable",
            }

            rows_html = []
            for cat in cat_order:
                c = categories.get(cat) or {}
                long_v = c.get("long", 0) or 0
                short_v = c.get("short", 0) or 0
                net_v = c.get("net")
                if net_v is None:
                    net_v = long_v - short_v
                net_color = "#00E676" if net_v > 0 else ("#FF3B3B" if net_v < 0 else "#999")
                rows_html.append(
                    f'<tr>'
                    f'<td style="padding:4px 4px;color:#DDD;font-size:11px;">{cat_labels.get(cat, cat)}</td>'
                    f'<td style="padding:4px 4px;text-align:right;color:#00E676;font-size:11px;">{long_v:,}</td>'
                    f'<td style="padding:4px 4px;text-align:right;color:#FF3B3B;font-size:11px;">{short_v:,}</td>'
                    f'<td style="padding:4px 4px;text-align:right;color:{net_color};font-weight:700;font-size:11px;">{net_v:+,}</td>'
                    f'</tr>'
                )

            table_html = f'''
            <div style="background:#0a0a0a;border:1px solid #1E4FA8;border-radius:4px;padding:6px;margin:8px 0;overflow-x:auto;">
              <table style="width:100%;border-collapse:collapse;font-size:11px;table-layout:fixed;">
                <colgroup>
                  <col style="width:38%;">
                  <col style="width:20%;">
                  <col style="width:20%;">
                  <col style="width:22%;">
                </colgroup>
                <thead>
                  <tr style="background:#111;color:#00E5FF;">
                    <th style="padding:4px 4px;text-align:left;font-size:11px;">Kategori</th>
                    <th style="padding:4px 4px;text-align:right;font-size:11px;">Long</th>
                    <th style="padding:4px 4px;text-align:right;font-size:11px;">Short</th>
                    <th style="padding:4px 4px;text-align:right;font-size:11px;">Net</th>
                  </tr>
                </thead>
                <tbody>
                  {''.join(rows_html)}
                </tbody>
              </table>
            </div>
            '''
            components.html(table_html, height=260, scrolling=False)

            st.metric("Açık Pozisyon (OI)", f"{oi:,}" if isinstance(oi, (int, float)) else str(oi))
            st.caption("⚠️ COT doğrudan CTA pozisyonu değildir. Non-Reportable ters indikatör olarak değerlendirilir.")

        st.divider()
        with st.expander("📋 İZLEME LİSTESİNDE OLMAYAN ÜRÜNLER", expanded=False):
            offlist = offlist_products()
            offlist = {k: v for k, v in offlist.items() if k.upper() not in EGZOTIK and k.upper() not in COT_ALIASES}

            if not offlist:
                st.caption(f"Şu an {len(TRACKED_CODES)} ürün dışında konuşulan bir varlık yok.")
            else:
                groups = {"ABD_ENDEKS": [], "ABD_ETF": [], "EMTIA": [], "ABD_HISSE": [], "ASYA": []}
                for sembol, data in sorted(offlist.items()):
                    grp = categorize_offlist(sembol)
                    groups[grp].append((sembol, data))

                GROUP_TITLES = {
                    "ABD_ENDEKS": "🇺🇸 ABD ENDEKSLERİ",
                    "ABD_ETF": "📊 ABD ETF'LERİ",
                    "EMTIA": "🛢️ EMTİA / KRİPTO / FOREX",
                    "ABD_HISSE": "💼 ABD HİSSELERİ",
                    "ASYA": "🇭🇰 ASYA / HK",
                }

                for grp_key in ["ABD_ENDEKS", "ABD_ETF", "EMTIA", "ABD_HISSE", "ASYA"]:
                    items = groups[grp_key]
                    if not items:
                        continue
                    st.markdown(f"**{GROUP_TITLES[grp_key]}** ({len(items)})")
                    for sembol, data in items:
                        isim = data.get("isim", "") or ""
                        yonler = ", ".join(sorted(data["yonler"])) if data["yonler"] else "—"
                        kaynaklar = ", ".join(sorted(data["kaynaklar"])) if data["kaynaklar"] else "—"
                        st.markdown(
                            f'<div style="background:#0a0a0a;border:1px solid #333;border-radius:4px;padding:6px 10px;margin:4px 0;">'
                            f'<div style="color:#FFC107;font-size:14px;font-weight:800;">{sembol} — {isim}</div>'
                            f'<div style="color:#B8D4FF;font-size:12px;margin-top:3px;">Yön: {yonler}</div>'
                            f'<div style="color:#888;font-size:11px;margin-top:2px;">Kaynak: {kaynaklar}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )


# ============================================================
# SEKME 2 — X ANALİZLERİ
# ============================================================
with tab_x:
    st.markdown(f"### 📱 X ANALİZLERİ")
    st.caption(f"Varlık içeren: {x_analyzed} / Toplam: {x_total} analiz")

    if not x_with_assets:
        st.warning("Henüz varlık içeren X analizi yok.")
    else:
        for item in x_with_assets[-50:][::-1]:
            username = item.get("username", "")
            text = item.get("text", "")
            ozet = item.get("ozet", "")
            varliklar = item.get("varliklar", [])
            analyzed_at = item.get("analyzed_at", "")[:16]

            with st.expander(f"@{username} — {text[:80]}...", expanded=False):
                st.markdown(f"**@{username}** — *{analyzed_at}*")
                st.write(text)

                if ozet and not ozet.startswith("Hata"):
                    st.markdown(
                        f'<div style="background:#0F2A5C;padding:10px 12px;border-radius:6px;margin:6px 0;border-left:4px solid #00E5FF;">'
                        f'<div style="color:#00E5FF;font-size:13px;font-weight:800;margin-bottom:4px;">📝 ÖZET</div>'
                        f'<div style="color:#FFF;font-size:14px;font-weight:700;line-height:1.5;">{ozet}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                for v in varliklar:
                    sembol = v.get("sembol", "?")
                    isim = v.get("isim", "")
                    vyon = v.get("yon", "NÖTR")
                    skor = v.get("skor", 0.5)
                    gerekce = v.get("gerekce", "")
                    bar = make_bar_html(vyon, skor)
                    st.markdown(
                        f'<div style="background:#0a0a0a;border:1px solid #1E4FA8;border-radius:4px;padding:6px 10px;margin:4px 0;">'
                        f'<div style="color:#00E5FF;font-size:14px;font-weight:800;margin-bottom:3px;">{sembol} — {isim}</div>'
                        f'{bar}'
                        f'<div style="color:#CCC;font-size:12px;margin-top:3px;line-height:1.4;">{gerekce}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

st.divider()
st.caption("CTA ERHAN Terminali | Kanıt Öncelikli | Salt Okunur İstihbarat")