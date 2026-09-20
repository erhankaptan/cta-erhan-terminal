"""
CTA ERHAN TERMİNALİ — Asset Catalog
====================================
25 futures kontratının kanonik tanımı.
Alias'lar, Türkçe isimler, varlık sınıfları ve CFTC eşleştirmeleri.

Bu dosya SADECE VERİ içerir. Kod çalıştırmaz.
"""

from typing import Dict, List, Optional


# ============================================================
# 25 FUTURES KONTRATI — KANONİK TANIM
# ============================================================

ASSET_CATALOG: Dict[str, Dict] = {

    # --------------------------------------------------------
    # HİSSE ENDEKSLERİ (6)
    # --------------------------------------------------------
    "ES": {
        "name_tr": "S&P 500 E-mini",
        "name_en": "S&P 500 E-mini",
        "asset_class": "Hisse Endeksi",
        "root_symbol": "ES",
        "aliases": [
            "s&p 500", "sp500", "s&p500", "spx", "es",
            "s&p", "sp 500", "s&p500 e-mini",
        ],
        "cftc_market": "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "MES": {
        "name_tr": "Micro S&P 500",
        "name_en": "Micro S&P 500",
        "asset_class": "Hisse Endeksi",
        "root_symbol": "ES",
        "aliases": ["micro s&p", "mes", "micro sp500"],
        "cftc_market": "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "NQ": {
        "name_tr": "Nasdaq 100 E-mini",
        "name_en": "Nasdaq 100 E-mini",
        "asset_class": "Hisse Endeksi",
        "root_symbol": "NQ",
        "aliases": [
            "nasdaq", "nasdaq 100", "ndx", "nq", "tech",
            "nasdaq 100 e-mini",
        ],
        "cftc_market": "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "MNQ": {
        "name_tr": "Micro Nasdaq 100",
        "name_en": "Micro Nasdaq 100",
        "asset_class": "Hisse Endeksi",
        "root_symbol": "NQ",
        "aliases": ["micro nasdaq", "mnq"],
        "cftc_market": "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "RTY": {
        "name_tr": "Russell 2000 E-mini",
        "name_en": "Russell 2000 E-mini",
        "asset_class": "Hisse Endeksi",
        "root_symbol": "RTY",
        "aliases": ["russell", "russell 2000", "rty", "small caps"],
        "cftc_market": "RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "YM": {
        "name_tr": "Dow E-mini",
        "name_en": "Dow E-mini",
        "asset_class": "Hisse Endeksi",
        "root_symbol": "YM",
        "aliases": ["dow", "dow jones", "djia", "ym"],
        "cftc_market": "DJIA x $5 - CHICAGO BOARD OF TRADE",
        "cftc_report": "TFF",
    },

    # --------------------------------------------------------
    # ENERJİ (3)
    # --------------------------------------------------------
    "CL": {
        "name_tr": "Ham Petrol",
        "name_en": "Crude Oil WTI",
        "asset_class": "Enerji",
        "root_symbol": "CL",
        "aliases": [
            "crude", "crude oil", "wti", "oil", "west texas",
            "nymex crude", "ham petrol",
        ],
        "cftc_market": "WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE",
        "cftc_report": "DISAGG",
    },
    "MCL": {
        "name_tr": "Micro Ham Petrol",
        "name_en": "Micro Crude Oil",
        "asset_class": "Enerji",
        "root_symbol": "CL",
        "aliases": ["micro crude", "mcl"],
        "cftc_market": "WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE",
        "cftc_report": "DISAGG",
    },
    "NG": {
        "name_tr": "Doğal Gaz",
        "name_en": "Natural Gas",
        "asset_class": "Enerji",
        "root_symbol": "NG",
        "aliases": [
            "natural gas", "nat gas", "natgas", "henry hub",
            "doğal gaz", "gas",
        ],
        "cftc_market": "HENRY HUB LAST DAY FIN - NEW YORK MERCANTILE EXCHANGE",
        "cftc_report": "DISAGG",
    },

    # --------------------------------------------------------
    # METALLER (5)
    # --------------------------------------------------------
    "GC": {
        "name_tr": "Altın",
        "name_en": "Gold",
        "asset_class": "Kıymetli Metal",
        "root_symbol": "GC",
        "aliases": [
            "gold", "xau", "altın", "comex gold", "gold futures",
            "xauusd",
        ],
        "cftc_market": "GOLD - COMMODITY EXCHANGE INC.",
        "cftc_report": "DISAGG",
    },
    "MGC": {
        "name_tr": "Micro Altın",
        "name_en": "Micro Gold",
        "asset_class": "Kıymetli Metal",
        "root_symbol": "GC",
        "aliases": ["micro gold", "mgc"],
        "cftc_market": "GOLD - COMMODITY EXCHANGE INC.",
        "cftc_report": "DISAGG",
    },
    "SI": {
        "name_tr": "Gümüş",
        "name_en": "Silver",
        "asset_class": "Kıymetli Metal",
        "root_symbol": "SI",
        "aliases": ["silver", "xag", "gümüş", "comex silver"],
        "cftc_market": "SILVER - COMMODITY EXCHANGE INC.",
        "cftc_report": "DISAGG",
    },
    "HG": {
        "name_tr": "Bakır",
        "name_en": "Copper",
        "asset_class": "Baz Metal",
        "root_symbol": "HG",
        "aliases": ["copper", "bakır", "comex copper"],
        "cftc_market": "COPPER- #1 - COMMODITY EXCHANGE INC.",
        "cftc_report": "DISAGG",
    },
    "PL": {
        "name_tr": "Platin",
        "name_en": "Platinum",
        "asset_class": "Kıymetli Metal",
        "root_symbol": "PL",
        "aliases": ["platinum", "platin"],
        "cftc_market": "PLATINUM - NEW YORK MERCANTILE EXCHANGE",
        "cftc_report": "DISAGG",
    },

    # --------------------------------------------------------
    # DÖVİZ (6)
    # --------------------------------------------------------
    "6E": {
        "name_tr": "Euro FX",
        "name_en": "Euro FX",
        "asset_class": "Döviz",
        "root_symbol": "6E",
        "aliases": ["euro", "eur", "eurusd", "6e"],
        "cftc_market": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "6J": {
        "name_tr": "Japon Yeni",
        "name_en": "Japanese Yen",
        "asset_class": "Döviz",
        "root_symbol": "6J",
        "aliases": ["yen", "jpy", "usdjpy", "6j", "japon yeni"],
        "cftc_market": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "6B": {
        "name_tr": "İngiliz Sterlini",
        "name_en": "British Pound",
        "asset_class": "Döviz",
        "root_symbol": "6B",
        "aliases": ["pound", "gbp", "gbpusd", "6b", "sterlin"],
        "cftc_market": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "6A": {
        "name_tr": "Avustralya Doları",
        "name_en": "Australian Dollar",
        "asset_class": "Döviz",
        "root_symbol": "6A",
        "aliases": ["aussie", "aud", "audusd", "6a"],
        "cftc_market": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "6C": {
        "name_tr": "Kanada Doları",
        "name_en": "Canadian Dollar",
        "asset_class": "Döviz",
        "root_symbol": "6C",
        "aliases": ["loonie", "cad", "usdcad", "6c"],
        "cftc_market": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },
    "6S": {
        "name_tr": "İsviçre Frangı",
        "name_en": "Swiss Franc",
        "asset_class": "Döviz",
        "root_symbol": "6S",
        "aliases": ["franc", "chf", "usdchf", "6s", "swissy"],
        "cftc_market": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
        "cftc_report": "TFF",
    },

    # --------------------------------------------------------
    # TARIM (5)
    # --------------------------------------------------------
    "ZC": {
        "name_tr": "Mısır",
        "name_en": "Corn",
        "asset_class": "Tarım",
        "root_symbol": "ZC",
        "aliases": ["corn", "mısır", "cbot corn"],
        "cftc_market": "CORN - CHICAGO BOARD OF TRADE",
        "cftc_report": "DISAGG",
    },
    "ZS": {
        "name_tr": "Soya Fasulyesi",
        "name_en": "Soybean",
        "asset_class": "Tarım",
        "root_symbol": "ZS",
        "aliases": ["soybean", "soy", "soya", "soybeans"],
        "cftc_market": "SOYBEANS - CHICAGO BOARD OF TRADE",
        "cftc_report": "DISAGG",
    },
    "ZW": {
        "name_tr": "Buğday",
        "name_en": "Wheat",
        "asset_class": "Tarım",
        "root_symbol": "ZW",
        "aliases": ["wheat", "buğday", "cbot wheat"],
        "cftc_market": "WHEAT-SRW - CHICAGO BOARD OF TRADE",
        "cftc_report": "DISAGG",
    },
    "ZL": {
        "name_tr": "Soya Yağı",
        "name_en": "Soybean Oil",
        "asset_class": "Tarım",
        "root_symbol": "ZL",
        "aliases": ["soybean oil", "soy oil", "soya yağı"],
        "cftc_market": "SOYBEAN OIL - CHICAGO BOARD OF TRADE",
        "cftc_report": "DISAGG",
    },
    "ZM": {
        "name_tr": "Soya Küspesi",
        "name_en": "Soybean Meal",
        "asset_class": "Tarım",
        "root_symbol": "ZM",
        "aliases": ["soybean meal", "soy meal", "soya küspesi"],
        "cftc_market": "SOYBEAN MEAL - CHICAGO BOARD OF TRADE",
        "cftc_report": "DISAGG",
    },
}


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def get_asset(asset_code: str) -> Optional[Dict]:
    """Kontrat kodundan tanım döner."""
    return ASSET_CATALOG.get(asset_code.upper().strip())


def get_all_codes() -> List[str]:
    """Tüm kontrat kodlarını döner."""
    return list(ASSET_CATALOG.keys())


def get_root_symbol(asset_code: str) -> Optional[str]:
    """Micro → ana ürün kök sembolünü döner."""
    asset = get_asset(asset_code)
    return asset.get("root_symbol") if asset else None


def get_cftc_market(asset_code: str) -> Optional[str]:
    """CFTC market adını döner."""
    asset = get_asset(asset_code)
    return asset.get("cftc_market") if asset else None


def get_asset_class(asset_code: str) -> Optional[str]:
    """Varlık sınıfını döner."""
    asset = get_asset(asset_code)
    return asset.get("asset_class") if asset else None


# ============================================================
# KONTROL — 25 KONTRAT VAR MI?
# ============================================================

if __name__ == "__main__":
    total = len(ASSET_CATALOG)
    print(f"Toplam kontrat: {total}")

    if total != 25:
        print(f"UYARI: BEKLENEN 25, BULUNAN: {total}")
    else:
        print("OK: 25 kontrat tam")

    from collections import Counter
    classes = Counter(a["asset_class"] for a in ASSET_CATALOG.values())
    print("\nVarlik siniflari:")
    for cls, count in classes.items():
        print(f"  {cls}: {count}")