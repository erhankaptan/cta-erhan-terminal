import streamlit as st

st.set_page_config(
    page_title="CTA ERHAN Terminali",
    page_icon="â—ˆ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ÃœRÃœNLER
# ============================================================

products = [
    "ES", "MES", "NQ", "MNQ", "RTY", "YM",
    "CL", "MCL", "NG",
    "GC", "MGC", "SI", "HG", "PL",
    "6E", "6J", "6B", "6A", "6C", "6S",
    "ZC", "ZS", "ZW", "ZL", "ZM"
]

product_names = {
    "ES": "S&P 500 E-mini",
    "MES": "Micro S&P 500",
    "NQ": "Nasdaq 100 E-mini",
    "MNQ": "Micro Nasdaq 100",
    "RTY": "Russell 2000 E-mini",
    "YM": "Dow E-mini",
    "CL": "Ham Petrol",
    "MCL": "Micro Ham Petrol",
    "NG": "DoÄŸal Gaz",
    "GC": "AltÄ±n",
    "MGC": "Micro AltÄ±n",
    "SI": "GÃ¼mÃ¼ÅŸ",
    "HG": "BakÄ±r",
    "PL": "Platin",
    "6E": "Euro FX",
    "6J": "Japon Yeni",
    "6B": "Ä°ngiliz Sterlini",
    "6A": "Avustralya DolarÄ±",
    "6C": "Kanada DolarÄ±",
    "6S": "Ä°sviÃ§re FrangÄ±",
    "ZC": "MÄ±sÄ±r",
    "ZS": "Soya Fasulyesi",
    "ZW": "BuÄŸday",
    "ZL": "Soya YaÄŸÄ±",
    "ZM": "Soya KÃ¼spesi",
}

# ============================================================
# TEMA
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       ANA ARKA PLAN
       ====================================================== */

    .stApp {
        background-color: #15181B;
        color: #F4F6F8;
    }

    [data-testid="stHeader"] {
        background-color: #15181B;
    }

    [data-testid="stSidebar"] {
        background-color: #191C20;
    }

    [data-testid="stSidebar"] * {
        color: #F4F6F8;
    }

    /* ======================================================
       GENEL BOYUTLAR
       ====================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 0.65rem;
        padding-bottom: 1rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
    }

    h1 {
        font-size: 1.65rem !important;
        margin-bottom: 0.15rem !important;
    }

    h2 {
        font-size: 1.15rem !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.35rem !important;
    }

    h3 {
        font-size: 0.98rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.25rem !important;
    }

    p {
        font-size: 0.84rem !important;
        line-height: 1.25 !important;
    }

    /* ======================================================
       ANA BAÅžLIKLAR
       ====================================================== */

   h1,
h2,
h3 {
    color: #164A68 !important;
}

.cta-main-title {
    color: #FFFFFF !important;
    display: block !important;
        width: 100% !important;
        max-width: none !important;
        overflow: visible !important;
        white-space: nowrap !important;
        line-height: 1.35 !important;
        padding: 8px 0 14px 0 !important;
        margin: 0 !important;
    }

    /* ======================================================
       DÄ°KDÃ–RTGEN / BANT PANELLERÄ°
       PARLAMENT MAVÄ°SÄ° + PARLAK BEYAZ
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #164A68 !important;
        border: 1px solid #2B7097 !important;
        border-radius: 7px;
        padding: 7px 9px;
    }

    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
    }

    /* ======================================================
       EXPANDER BANTLARI
       ====================================================== */

    [data-testid="stExpander"] {
        background-color: #164A68 !important;
        border: 1px solid #2B7097 !important;
        border-radius: 6px;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] p {
        color: #FFFFFF !important;
    }

    [data-testid="stExpander"] p {
        font-size: 0.78rem !important;
    }

    /* ======================================================
       STREAMLIT UYARI / DURUM BANTLARI
       ====================================================== */

    [data-testid="stAlert"] {
        background-color: #164A68 !important;
        border: 1px solid #2B7097 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stAlert"] * {
        color: #FFFFFF !important;
    }

    /* ======================================================
       BUTONLAR
       ====================================================== */

    .stButton button {
        background-color: #164A68 !important;
        color: #FFFFFF !important;
        border: 1px solid #2B7097 !important;
        font-size: 0.78rem !important;
    }

    /* ======================================================
       SIDEBAR BAÅžLIKLARI
       ====================================================== */

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] h1 {
        font-size: 1.3rem !important;
    }

    [data-testid="stSidebar"] h2 {
        font-size: 0.95rem !important;
    }

    [data-testid="stSidebar"] .stSelectbox label {
        font-size: 0.75rem !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #164A68 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* ======================================================
       AKTÄ°F ÃœRÃœN
       ====================================================== */

    .active-product {
        font-size: 1.18rem;
        font-weight: 800;
        color: #FF3030 !important;
    }

    .active-product-name {
        font-size: 1.12rem;
        font-weight: 800;
        color: #39FF14 !important;
    }

    /* ======================================================
       GENEL METÄ°N
       ====================================================== */

    .stCaption {
        color: #D7DDE2 !important;
    }

    hr {
        margin: 0.45rem 0 !important;
        border-color: #31515F !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SOL MENÃœ
# ============================================================

with st.sidebar:

    st.markdown(
        '<h1 class="cta-main-title">â—ˆ CTA ERHAN</h1>',
        unsafe_allow_html=True,
    )

    st.caption("Vadeli Ä°ÅŸlemler / CTA / Piyasa Ä°stihbaratÄ±")

    st.divider()

    st.subheader("ÃœRÃœN SEÃ‡Ä°MÄ°")

    selected_product = st.selectbox(
        "Aktif Ã¼rÃ¼n",
        products,
        index=0,
    )

    st.markdown(
        f'<div class="active-product-name">{selected_product}</div>',
        unsafe_allow_html=True,
    )

    st.caption(product_names[selected_product])

    st.divider()

    st.subheader("TERMÄ°NAL")

    st.write("â—ˆ CTA RadarÄ±")
    st.write("â—ˆ Vadeli Ä°ÅŸlemler Panosu")
    st.write("â—ˆ COT Analizi")
    st.write("â—ˆ Kaynak Ä°stihbaratÄ±")
    st.write("â—ˆ KanÄ±t Havuzu")
    st.write("â—ˆ Analiz")
    st.write("â—ˆ Sentez")

    st.divider()

    st.subheader("SÄ°STEM SINIRI")

    st.success("SALT OKUNUR Ä°STÄ°HBARAT")

    st.write("Karar Ã¼retmez.")
    st.write("Emir gÃ¶ndermez.")
    st.write("Otomatik iÅŸlem yapmaz.")

# ============================================================
# ANA BAÅžLIK
# ============================================================

st.markdown(
    '<h1 class="cta-main-title">â—ˆ CTA ERHAN TERMÄ°NALÄ°</h1>',
    unsafe_allow_html=True,
)

st.caption("Vadeli Ä°ÅŸlemler / CTA / Piyasa Ä°stihbaratÄ±")

st.markdown(
    f'''
    <div style="
        background:#164A68;
        border:1px solid #2B7097;
        border-radius:7px;
        padding:11px 15px;
        margin:6px 0 10px 0;
    ">
        <span style="
            color:#FF3030;
            font-size:1.18rem;
            font-weight:800;
        ">Aktif Ã¼rÃ¼n: </span>
        <span style="
            color:#39FF14;
            font-size:1.18rem;
            font-weight:800;
        ">{selected_product}</span>
        <span style="
            color:#FFFFFF;
            font-size:1.02rem;
            font-weight:600;
        "> â€” {product_names[selected_product]}</span>
    </div>
    ''',
    unsafe_allow_html=True,
)

st.divider()

# ============================================================
# SÄ°STEM DURUMU
# ============================================================

st.subheader("SÄ°STEM DURUMU")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("CTA YÃ–NÃœ", "NÃ–TR")

with col2:
    st.metric("GÃœVEN", "â€”")

with col3:
    st.metric("REJÄ°M", "BÄ°LÄ°NMÄ°YOR")

with col4:
    st.metric("KAYNAK DURUMU", "HAZIR")

with col5:
    st.metric("KANIT", "0")

st.divider()

# ============================================================
# ANA PANELLER
# ============================================================

left, middle, right = st.columns(3)

# ============================================================
# SOL
# ============================================================

with left:

    st.header("CTA RADARI")

    st.write(f"ÃœrÃ¼n: **{selected_product}**")
    st.write("YÃ¶n: **YETERSÄ°Z**")
    st.write("GÃ¼Ã§: **YETERSÄ°Z**")
    st.write("Belirsizlik: **YÃœKSEK**")
    st.write("Ã‡atÄ±ÅŸma: **YOK**")
    st.write("Nihai YÃ¶n: **YETERSÄ°Z**")

    st.divider()

    st.header("VADELÄ° Ä°ÅžLEMLER PANOSU")

    st.write(f"Kontrat: **{selected_product}**")
    st.write(f"EnstrÃ¼man: **{product_names[selected_product]}**")
    st.write("Fiyat: â€”")
    st.write("Hacim: â€”")
    st.write("AÃ§Ä±k Pozisyon: â€”")
    st.write("Volatilite: â€”")

    st.info("GerÃ§ek piyasa verisi bu aÅŸamada baÄŸlÄ± deÄŸil.")

    with st.expander("Vadeli Ä°ÅŸlemler DetaylarÄ±"):
        st.write("Veri kaynaÄŸÄ±: â€”")
        st.write("Zaman damgasÄ±: â€”")
        st.write("Seans: â€”")

    st.divider()

    st.header("COT ANALÄ°ZÄ°")

    st.write("CFTC COT: **YALNIZCA VEKÄ°L VERÄ°**")
    st.write("YÃ¶netilen Para: â€”")
    st.write("Ticari Pozisyonlar: â€”")
    st.write("Ticari Olmayan Pozisyonlar: â€”")

    with st.expander("COT AÃ§Ä±klamasÄ±"):
        st.write("COT verisi doÄŸrudan CTA pozisyonu deÄŸildir.")
        st.write(
            "YalnÄ±zca vekil veri ve araÅŸtÄ±rma kanÄ±tÄ± olarak kullanÄ±lÄ±r."
        )

# ============================================================
# ORTA
# ============================================================

with middle:

    st.header("KAYNAK Ä°STÄ°HBARATI")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "X / BÄ°RÄ°NCÄ°L",
            "RSS / HABER",
            "KURUMSAL",
            "PDF RAPORLAR",
        ]
    )

    with tab1:

        st.subheader("X / Birincil Kaynak")
        st.info("X gÃ¶nderileri birincil kaynak katmanÄ±dÄ±r.")
        st.metric("GÃ¶nderiler", "0")
        st.write("DoÄŸrulanmÄ±ÅŸ: 0")
        st.write("DoÄŸrulanmamÄ±ÅŸ: 0")

        with st.expander("X Kaynak Durumu"):
            st.write("Kaynak alma: HAZIR")
            st.write("AyrÄ±ÅŸtÄ±rma: HAZIR")
            st.write("KanÄ±t Ã§Ä±karÄ±mÄ±: HAZIR")

    with tab2:

        st.subheader("RSS / Haber")
        st.info("RSS haber ve araÅŸtÄ±rma akÄ±ÅŸlarÄ±.")
        st.write("AkÄ±ÅŸlar: 0")
        st.write("Ã–geler: 0")
        st.write("GÃ¼ncel: 0")

    with tab3:

        st.subheader("Kurumsal Kaynaklar")
        st.info("KurumlarÄ±n aÃ§Ä±k web ve araÅŸtÄ±rma yayÄ±nlarÄ±.")
        st.write("Kurumlar: 0")
        st.write("Belgeler: 0")
        st.write("DoÄŸrulanmÄ±ÅŸ: 0")

    with tab4:

        st.subheader("PDF RaporlarÄ±")
        st.info("Kurumsal PDF raporlarÄ±.")
        st.write("PDF dosyalarÄ±: 0")
        st.write("Taranan sayfalar: 0")
        st.write("Ã‡Ä±karÄ±lan kanÄ±t: 0")

    st.divider()

    st.header("KANIT HAVUZU")

    evidence = {
        "Kaynak": ["â€”"],
        "TÃ¼r": ["â€”"],
        "ÃœrÃ¼n": [selected_product],
        "Durum": ["KANIT YOK"],
        "Zaman": ["â€”"],
    }

    st.dataframe(
        evidence,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Kaynak â†’ Kaynak GeÃ§miÅŸi â†’ KanÄ±t â†’ Ä°stihbarat"
    )

# ============================================================
# SAÄž
# ============================================================

with right:

    st.header("ANALÄ°Z")

    st.write("YÃ¶n")
    st.warning("YETERSÄ°Z")

    st.write("GÃ¼Ã§")
    st.warning("YETERSÄ°Z")

    st.write("Belirsizlik")
    st.warning("YÃœKSEK")

    st.write("Ã‡atÄ±ÅŸma")
    st.success("YOK")

    st.write("Rejim")
    st.warning("BÄ°LÄ°NMÄ°YOR")

    st.divider()

    st.header("SENTEZ")

    st.error("YETERSÄ°Z KANIT")

    st.write(
        "Mevcut kanÄ±tlarla doÄŸrulanmÄ±ÅŸ yÃ¶nsel sonuÃ§ Ã¼retilemiyor."
    )

    st.write("Nihai YÃ¶n: **YETERSÄ°Z**")

    with st.expander("Sentez AyrÄ±ntÄ±larÄ±"):
        st.write("TÃœMÃœ UYUMLU: HayÄ±r")
        st.write("NÃ–TR: HayÄ±r")
        st.write("BÃ–LÃœNMÃœÅž: HayÄ±r")
        st.write("YETERSÄ°Z: Evet")

    st.divider()

    st.header("KAYNAK DURUMU")

    st.write("X / Birincil: **HAZIR**")
    st.write("RSS: **HAZIR**")
    st.write("Kurumsal: **HAZIR**")
    st.write("PDF: **HAZIR**")
    st.write("COT: **HAZIR**")
    st.write("IBKR / TWS: **Ä°STEÄžE BAÄžLI**")

# ============================================================
# Ä°STÄ°HBARAT AKIÅžI
# ============================================================

st.divider()

st.header("Ä°STÄ°HBARAT AKIÅžI")

p1, p2, p3, p4, p5, p6, p7 = st.columns(7)

with p1:
    st.write("1")
    st.caption("KAYNAK")

with p2:
    st.write("2")
    st.caption("KAYNAK ALMA")

with p3:
    st.write("3")
    st.caption("NORMALÄ°ZASYON")

with p4:
    st.write("4")
    st.caption("KAYNAK GEÃ‡MÄ°ÅžÄ°")

with p5:
    st.write("5")
    st.caption("KANIT")

with p6:
    st.write("6")
    st.caption("Ä°STÄ°HBARAT")

with p7:
    st.write("7")
    st.caption("SENTEZ")

# ============================================================
# ALT BÃ–LÃœM
# ============================================================

st.divider()

v1, v2 = st.columns(2)

with v1:

    st.subheader("DOÄžRULAMA")

    st.write("Kaynak doÄŸrulamasÄ±: â€”")
    st.write("GÃ¼ncellik doÄŸrulamasÄ±: â€”")
    st.write("KanÄ±t doÄŸrulamasÄ±: â€”")
    st.write("Ã‡atÄ±ÅŸma doÄŸrulamasÄ±: â€”")
    st.write("Ã‡Ã¼rÃ¼tme testi: â€”")

with v2:

    st.subheader("OPERASYONEL DURUM")

    st.write("Terminal: **HAZIR**")
    st.write("Kaynak Motoru: **HAZIR**")
    st.write("KanÄ±t Motoru: **HAZIR**")
    st.write("Analiz Motoru: **HAZIR**")
    st.write("Ä°ÅŸlem: **DEVRE DIÅžI**")

st.divider()

st.caption(
    "CTA ERHAN Terminali | KanÄ±t Ã–ncelikli | Salt Okunur Ä°stihbarat"
)
