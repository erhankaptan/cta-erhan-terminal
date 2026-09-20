"""
CTA ERHAN TERMİNALİ — app.py (v18 - FİLTRELİ + YUMUŞATILMIŞ SKOR)
"""

import streamlit as st
import json
import sqlite3
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CTA ERHAN Terminali",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
    .block-container {
        padding-top: 0 !important; padding-bottom: 0 !important;
        padding-left: 0.3rem !important; padding-right: 0.3rem !important;
        margin-top: 0 !important; max-width: 100% !important;
    }
    html, body, [class*="css"] { font-size: 13px !important; }
    h1 { font-size: 22px !important; margin: 0 !important; padding: 0 !important; line-height: 1.2 !important; }
    h2 { font-size: 19px !important; margin: 0.1rem 0 !important; }
    h3 { font-size: 18px !important; margin: 0.2rem 0 !important; font-weight: 800 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #00E5FF !important; }

    div[data-testid="stMetric"] {
        background-color: #0F2A5C !important;
        border: 1px solid #1E4FA8 !important;
        border-radius: 4px !important;
        padding: 4px 8px !important;
    }
    div[data-testid="stMetric"] label {
        font-size: 16px !important; font-weight: 700 !important; color: #B8D4FF !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 20px !important; font-weight: 800 !important; color: #FFFFFF !important;
    }
    div[data-testid="stMetric"] * { color: #FFFFFF !important; }

    .aktif-urun-kutu {
        padding: 4px 10px; border: 1px solid #333;
        border-radius: 4px; background: #0a0a0a; margin-bottom: 4px;
    }
    .aktif-urun-baslik { color: #FFFFFF; font-weight: 700; font-size: 13px; }
    .aktif-urun-deger { color: #00E676; font-weight: 700; font-size: 16px; }
    hr { margin: 0.3rem 0 !important; padding: 0 !important; }

    section[data-testid="stSidebar"] * { font-size: 16px !important; }
    section[data-testid="stSidebar"] label { font-size: 16px !important; font-weight: 700 !important; }
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { font-size: 16px !important; }
    section[data-testid="stSidebar"] h1 { font-size: 24px !important; }
    section[data-testid="stSidebar"] h2 { font-size: 22px !important; }
    section[data-testid="stSidebar"] h3 { font-size: 18px !important; }

    details { font-size: 15px !important; margin-bottom: 2px !important; }
    details summary {
        font-size: 15px !important; font-weight: 700 !important;
        color: #00E5FF !important; padding: 4px 4px !important;
    }
    details p, details span, details li, details div {
        font-size: 14px !important; line-height: 1.4 !important;
    }
    details p { margin: 0.2rem 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    "Borsalar": ["ES", "MES", "NQ", "MNQ", "RTY", "YM"],
    "Emtialar": ["CL", "MCL", "NG", "GC", "MGC", "SI", "HG", "PL"],
    "Tahıllar": ["ZC", "ZS", "ZW", "ZL", "ZM"],
    "Dövizler": ["6E", "6J", "6B", "6A", "6C", "6S"],
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
}

TRACKED_CODES = set()
for _cat_list in product_categories.values():
    TRACKED_CODES.update(_cat_list)

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

# Sadece VARLIK içeren X analizleri
x_with_assets = [a for a in all_analysis if a.get("varliklar") and len(a.get("varliklar", [])) > 0]
x_analyzed = len(x_with_assets)
x_total = len(all_analysis)

rss_total = len(all_rss)


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def soften_score(score, cap=0.75):
    """±cap üstünü kırp. Tek kaynak uçmasın."""
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

                    # SKOR YUMUŞATMA
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

    # ---------- SAĞ: COT + İZLEME LİSTESİ ----------
    with col_right:
        st.markdown(f"### 📊 COT RAPORU: {selected_product}")
        st.caption("CFTC COT — Vekil Veri")

        cot_records = load_cot_for_product(selected_product)

        if not cot_records:
            st.caption(f"{selected_product} için COT kaydı bulunamadı.")
        else:
            for cot in cot_records[:3]:
                title = cot.get("title", f"COT {selected_product}")
                published = cot.get("published_at", "")
                publisher = cot.get("publisher", "CFTC")
                metadata = cot.get("metadata", {})

                st.markdown(f"**{title}**")
                st.caption(f"📅 {published} | 📡 {publisher}")

                cta_proxy = metadata.get("cta_proxy", {}) if isinstance(metadata, dict) else {}
                if cta_proxy:
                    long_pos = cta_proxy.get("long", 0)
                    short_pos = cta_proxy.get("short", 0)
                    net = cta_proxy.get("net", 0)
                    change = cta_proxy.get("change_net", 0)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Long", f"{long_pos:,}")
                    with col2:
                        st.metric("Short", f"{short_pos:,}")

                    st.metric("Net", f"{net:+,}")
                    st.metric("Değişim", f"{change:+,}")

                    total = long_pos + short_pos
                    if total > 0:
                        long_pct = (long_pos / total) * 100
                        short_pct = (short_pos / total) * 100
                    else:
                        long_pct = short_pct = 0.0

                    bars_html = f'''
                    <div style="background:#0a0a0a;border:1px solid #1E4FA8;border-radius:4px;padding:10px;margin:8px 0;">
                        <div style="color:#00E5FF;font-size:15px;font-weight:800;margin-bottom:6px;">LONG</div>
                        <div style="background:#1a1a1a;height:20px;border-radius:3px;overflow:hidden;border:1px solid #1E4FA8;">
                            <div style="width:{long_pct:.2f}%;height:100%;background:#00E676;"></div>
                        </div>
                        <div style="color:#FFFFFF;font-weight:800;margin-top:4px;text-align:right;font-size:16px;">{long_pos:,} — %{long_pct:.0f}</div>
                        <div style="color:#00E5FF;font-size:15px;font-weight:800;margin-top:10px;margin-bottom:6px;">SHORT</div>
                        <div style="background:#1a1a1a;height:20px;border-radius:3px;overflow:hidden;border:1px solid #1E4FA8;">
                            <div style="width:{short_pct:.2f}%;height:100%;background:#FF3B3B;"></div>
                        </div>
                        <div style="color:#FFFFFF;font-weight:800;margin-top:4px;text-align:right;font-size:16px;">{short_pos:,} — %{short_pct:.0f}</div>
                    </div>
                    '''
                    components.html(bars_html, height=200, scrolling=False)

                st.caption("⚠️ COT doğrudan CTA pozisyonu değildir.")

        st.divider()
        with st.expander("📋 İZLEME LİSTESİNDE OLMAYAN ÜRÜNLER", expanded=False):
            offlist = offlist_products()
            if not offlist:
                st.caption("Şu an 25 ürün dışında konuşulan bir varlık yok.")
            else:
                for sembol, data in sorted(offlist.items()):
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
# SEKME 2 — X ANALİZLERİ (SADECE VARLIK İÇERENLER)
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