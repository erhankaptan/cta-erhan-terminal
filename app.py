"""
CTA ERHAN TERMİNALİ — Streamlit UI
====================================
JSON analizlerini ve tweet'leri okur, ekranda gösterir.
Veri kaynağı: data/analysis/ + data/tweets/
"""

import json
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd

# ============================================================
# SAYFA AYARLARI
# ============================================================

st.set_page_config(
    page_title="CTA ERHAN Terminali",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 13px !important;
}
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}
h1, h2, h3, h4 {
    color: #00E5FF !important;
    margin-top: 0.3rem !important;
    margin-bottom: 0.2rem !important;
}
div[data-testid="stMetric"] {
    background-color: #0F2A5C !important;
    border: 1px solid #1E4FA8 !important;
    border-radius: 4px !important;
    padding: 6px 10px !important;
}
div[data-testid="stMetric"] * {
    color: #FFFFFF !important;
}
.bull { color: #00E676 !important; font-weight: 700; }
.bear { color: #FF3B3B !important; font-weight: 700; }
.neutral { color: #FFC107 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# VERİ YÜKLEME
# ============================================================

DATA_DIR = Path("data")
ANALYSIS_DIR = DATA_DIR / "analysis"
TWEETS_DIR = DATA_DIR / "tweets"


@st.cache_data(ttl=300)
def load_latest_analysis():
    """En son analiz dosyasını yükle"""
    if not ANALYSIS_DIR.exists():
        return []
    files = sorted(ANALYSIS_DIR.glob("analysis_*.json"))
    if not files:
        return []
    with open(files[-1], "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(ttl=300)
def load_latest_tweets():
    """En son tweet dosyasını yükle"""
    if not TWEETS_DIR.exists():
        return []
    files = sorted(TWEETS_DIR.glob("tweets_*.json"))
    if not files:
        return []
    with open(files[-1], "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(ttl=300)
def get_last_update():
    """Son güncelleme zamanı"""
    files = sorted(ANALYSIS_DIR.glob("analysis_*.json"))
    if not files:
        return "—"
    timestamp = files[-1].stem.replace("analysis_", "")
    try:
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return timestamp


# ============================================================
# VERİYİ YÜKLE
# ============================================================

analysis_data = load_latest_analysis()
tweets_data = load_latest_tweets()

# ============================================================
# BAŞLIK
# ============================================================

st.markdown('<h1 style="color:#00E5FF;">◉ CTA ERHAN TERMİNALİ</h1>', unsafe_allow_html=True)
st.caption("Vadeli İşlemler / CTA / Piyasa İstihbaratı")

# ============================================================
# SİSTEM DURUMU
# ============================================================

st.subheader("SİSTEM DURUMU")

col1, col2, col3, col4 = st.columns(4)

bull_count = sum(1 for a in analysis_data if a.get("sentiment") == "BULL")
bear_count = sum(1 for a in analysis_data if a.get("sentiment") == "BEAR")
neutral_count = sum(1 for a in analysis_data if a.get("sentiment") == "NEUTRAL")
cta_count = sum(1 for a in analysis_data if a.get("is_cta_signal"))

with col1:
    st.metric("TOPLAM ANALİZ", len(analysis_data))
with col2:
    st.metric("BULL", bull_count)
with col3:
    st.metric("BEAR", bear_count)
with col4:
    st.metric("CTA SİNYALİ", cta_count)

st.caption(f"Son güncelleme: **{get_last_update()}**")
st.divider()

# ============================================================
# SEKMELER
# ============================================================

tab1, tab2, tab3 = st.tabs(["📊 ANALİZLER", "🐦 TWEET'LER", "📈 ÖZET"])

# ============================================================
# TAB 1: ANALİZLER
# ============================================================

with tab1:
    st.subheader("Gemini Analizleri")

    if not analysis_data:
        st.info("Henüz analiz yok. Workflow çalıştığında burada görünecek.")
    else:
        # Filtre
        col1, col2 = st.columns([1, 3])
        with col1:
            sentiment_filter = st.selectbox(
                "Sentiment",
                ["Hepsi", "BULL", "BEAR", "NEUTRAL"]
            )
        with col2:
            username_filter = st.selectbox(
                "Hesap",
                ["Hepsi"] + sorted(set(a.get("username", "") for a in analysis_data))
            )

        # Filtrele
        filtered = analysis_data
        if sentiment_filter != "Hepsi":
            filtered = [a for a in filtered if a.get("sentiment") == sentiment_filter]
        if username_filter != "Hepsi":
            filtered = [a for a in filtered if a.get("username") == username_filter]

        st.caption(f"**{len(filtered)}** analiz gösteriliyor")

        # Her analizi göster
        for i, item in enumerate(filtered, 1):
            sentiment = item.get("sentiment", "NEUTRAL")
            sentiment_class = sentiment.lower()
            username = item.get("username", "")
            text = item.get("text", "")[:200]
            summary = item.get("summary", "")
            confidence = item.get("confidence", 0)
            tickers = item.get("tickers", [])
            is_cta = item.get("is_cta_signal", False)

            with st.expander(
                f"[{sentiment}] @{username} — {text[:80]}...",
                expanded=False
            ):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                        f'<span class="{sentiment_class}">{sentiment}</span>',
                        unsafe_allow_html=True
                    )
                with col2:
                    st.write(f"**Güven:** {confidence}%")
                with col3:
                    st.write(f"**CTA:** {'✅ Evet' if is_cta else '❌ Hayır'}")

                st.write(f"**Ticker'lar:** {', '.join(tickers) if tickers else '—'}")
                st.write(f"**Özet:** {summary}")

                st.markdown("**Orijinal metin:**")
                st.write(text)

# ============================================================
# TAB 2: TWEET'LER
# ============================================================

with tab2:
    st.subheader("Son Tweet'ler")

    if not tweets_data:
        st.info("Henüz tweet yok.")
    else:
        st.caption(f"**{len(tweets_data)}** tweet")

        for item in tweets_data:
            username = item.get("username", "")
            text = item.get("text", "")
            published = item.get("published", "")
            images = item.get("images", [])

            with st.expander(f"@{username} — {text[:80]}...", expanded=False):
                st.write(f"**Tarih:** {published}")
                st.write(text)
                if images:
                    st.write(f"**Görsel:** {len(images)} adet")

# ============================================================
# TAB 3: ÖZET
# ============================================================

with tab3:
    st.subheader("Özet İstatistikler")

    if not analysis_data:
        st.info("Analiz yok.")
    else:
        # Sentiment dağılımı
        st.write("**Sentiment Dağılımı:**")
        df_sentiment = pd.DataFrame({
            "Sentiment": ["BULL", "BEAR", "NEUTRAL"],
            "Adet": [bull_count, bear_count, neutral_count]
        })
        st.bar_chart(df_sentiment.set_index("Sentiment"))

        st.divider()

        # Hesap bazlı
        st.write("**Hesap Bazlı:**")
        df_accounts = pd.DataFrame(analysis_data)
        if "username" in df_accounts.columns:
            counts = df_accounts["username"].value_counts().reset_index()
            counts.columns = ["Hesap", "Adet"]
            st.dataframe(counts, use_container_width=True, hide_index=True)

        st.divider()

        # Ticker bazlı
        st.write("**Ticker Bazlı:**")
        all_tickers = []
        for a in analysis_data:
            all_tickers.extend(a.get("tickers", []))
        if all_tickers:
            df_tickers = pd.Series(all_tickers).value_counts().reset_index()
            df_tickers.columns = ["Ticker", "Adet"]
            st.dataframe(df_tickers, use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("CTA ERHAN Terminali | Kanıt Öncelikli | Salt Okunur İstihbarat")
