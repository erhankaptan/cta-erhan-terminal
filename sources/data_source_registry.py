# ============================================================


from __future__ import annotations


from typing import Dict, Tuple


from .data_source import (
    AccessMethod,
    AccessMode,
    DataSource,
    InformationContentType,
    MultimodalContent,
    SourceAccess,
)
from .master_source import MasterSource
from .source_identity_status import SourceIdentityStatus
from .source_type import SourceType


DATA_API_SOURCE_DEFINITIONS = (
    ("master.data.yfinance", "yfinance"),
    ("master.data.fred_api", "FRED API"),
    ("master.data.nasdaq_data_link", "Nasdaq Data Link"),
    ("master.data.openbb", "OpenBB"),
    ("master.data.eulerpool_api", "Eulerpool API"),
    ("master.data.alpha_vantage", "Alpha Vantage"),
    ("master.data.trading_economics", "Trading Economics"),
    ("master.data.convextrade", "ConvexTrade"),
    ("master.data.cboe_historical_data", "CBOE Historical Data"),
    ("master.data.vixcentral", "VIXCentral"),
    ("master.data.tradier", "Tradier"),
    ("master.data.flashalpha", "FlashAlpha"),
    ("master.data.pineify_gex_chart", "Pineify GEX Chart"),
    ("master.data.barchart", "Barchart"),
    ("master.data.finra", "FINRA"),
)


ETF_FUND_SOURCE_DEFINITIONS = (
    ("master.etf.dbmf", "DBMF"),
    ("master.etf.kmlm", "KMLM"),
    ("master.etf.tfpn", "TFPN"),
    ("master.etf.cta", "CTA"),
    ("master.etf.asmf", "ASMF"),
    ("master.etf.imgp", "iMGP / iM Global Partner"),
    ("master.etf.kfa_funds", "KFA Funds"),
    ("master.etf.blueprint", "Blueprint"),
    ("master.etf.simplify", "Simplify"),
    ("master.etf.etf_com", "ETF.com"),
    ("master.etf.etfdb_com", "ETFdb.com"),
    ("master.etf.dbmfwatch_com", "dbmfwatch.com"),
)


OPTIONS_VOLATILITY_SOURCE_DEFINITIONS = (
    ("master.options.cboe", "CBOE"),
    ("master.options.cboe_historical", "CBOE Historical"),
    ("master.options.vix", "VIX"),
    ("master.options.vixcentral", "VIXCentral"),
    ("master.options.convextrade", "ConvexTrade"),
    ("master.options.flashalpha", "FlashAlpha"),
    ("master.options.pineify_gex_chart", "Pineify GEX Chart"),
    ("master.options.tradier", "Tradier"),
    ("master.options.gex_metrix", "GEX-Metrix"),
)


MACRO_SOURCE_DEFINITIONS = (
    ("master.macro.cpi", "CPI"),
    ("master.macro.pce", "PCE"),
    ("master.macro.nfp", "NFP"),
    ("master.macro.pmi", "PMI"),
    ("master.macro.treasury_auction", "Treasury Auction"),
    ("master.macro.opex", "OPEX"),
    ("master.macro.fred", "FRED"),
    ("master.macro.trading_economics", "Trading Economics"),
    ("master.macro.alpha_vantage", "Alpha Vantage"),
    ("master.macro.fed", "Fed"),
    ("master.macro.ecb", "ECB"),
    ("master.macro.boj", "BOJ"),
    ("master.macro.economic_surprise", "Economic Surprise"),
)


FUTURES_POSITIONING_SOURCE_DEFINITIONS = (
    ("master.futures.cme_daily_bulletin", "CME Daily Bulletin"),
    ("master.futures.cftc_cot", "CFTC COT"),
    ("master.futures.nasdaq_data_link", "Nasdaq Data Link"),
    ("master.futures.yfinance", "yfinance"),
    ("master.futures.openbb", "OpenBB"),
    ("master.futures.barchart", "Barchart"),
)


SG_UNAVAILABLE_SOURCE_DEFINITIONS = (
    ("master.sg.trend_index", "SG Trend Index"),
    ("master.sg.paid_cta_data", "paid SG CTA data"),
    ("master.sg.bloomberg_cta_data", "Bloomberg SG CTA data"),
)


def _source(
    source_id: str,
    name: str,
    source_type: SourceType = SourceType.INSTITUTION,
) -> MasterSource:
    return MasterSource(
        master_source_id=source_id,
        name=name,
        source_type=source_type,
        source_identity_status=SourceIdentityStatus.UNRESOLVED,
        access_channels=(),
        source_roles=(),
    )


def _data_source(
    source_id: str,
    name: str,
    scope: Tuple[str, ...] = (),
    content_types: Tuple[InformationContentType, ...] = (
        InformationContentType.TEXT,
        InformationContentType.NUMERIC,
        InformationContentType.TABLE,
        InformationContentType.CHART,
        InformationContentType.SCREENSHOT,
        InformationContentType.PHOTO,
        InformationContentType.INFOGRAPHIC,
        InformationContentType.DIAGRAM,
        InformationContentType.MAP,
        InformationContentType.VISUAL_PANEL,
    ),
) -> DataSource:
    return DataSource(
        master_source=_source(source_id, name),
        access_methods=(),
        access_modes=(),
        scope=scope,
        content_types=content_types,
        accesses=(),
        multimodal=MultimodalContent(
            content_types=content_types,
            source_id=source_id,
            provenance_preserved=True,
        ),
    )


def build_data_api_sources() -> Tuple[DataSource, ...]:
    return tuple(
        _data_source(source_id, name)
        for source_id, name in DATA_API_SOURCE_DEFINITIONS
    )


def build_etf_fund_sources() -> Tuple[DataSource, ...]:
    return tuple(
        _data_source(
            source_id,
            name,
            scope=(
                "product identity",
                "strategy",
                "performance",
                "holdings",
                "factsheet",
                "benchmark",
            ),
        )
        for source_id, name in ETF_FUND_SOURCE_DEFINITIONS
    )


def build_options_volatility_sources() -> Tuple[DataSource, ...]:
    return tuple(
        _data_source(
            source_id,
            name,
            scope=(
                "options",
                "volatility",
                "dealer-positioning",
            ),
        )
        for source_id, name in OPTIONS_VOLATILITY_SOURCE_DEFINITIONS
    )


def build_macro_sources() -> Tuple[DataSource, ...]:
    return tuple(
        _data_source(
            source_id,
            name,
            scope=("macro",),
        )
        for source_id, name in MACRO_SOURCE_DEFINITIONS
    )


def build_futures_positioning_sources() -> Tuple[DataSource, ...]:
    return tuple(
        _data_source(
            source_id,
            name,
            scope=(
                "futures",
                "positioning",
                "seasonality",
            ),
        )
        for source_id, name in FUTURES_POSITIONING_SOURCE_DEFINITIONS
    )


def build_sg_unavailable_sources() -> Tuple[DataSource, ...]:
    return tuple(
        DataSource(
            master_source=_source(source_id, name),
            access_methods=(),
            access_modes=(AccessMode.NON_OPERATIONAL,),
            scope=("UNAVAILABLE",),
            content_types=(),
            accesses=(),
            multimodal=None,
        )
        for source_id, name in SG_UNAVAILABLE_SOURCE_DEFINITIONS
    )


DATA_API_SOURCES = build_data_api_sources()
ETF_FUND_SOURCES = build_etf_fund_sources()
OPTIONS_VOLATILITY_SOURCES = build_options_volatility_sources()
MACRO_SOURCES = build_macro_sources()
FUTURES_POSITIONING_SOURCES = build_futures_positioning_sources()
SG_UNAVAILABLE_SOURCES = build_sg_unavailable_sources()


ALL_43_SOURCES = (
    DATA_API_SOURCES
    + ETF_FUND_SOURCES
    + OPTIONS_VOLATILITY_SOURCES
    + MACRO_SOURCES
    + FUTURES_POSITIONING_SOURCES
    + SG_UNAVAILABLE_SOURCES
)


DATA_SOURCE_REGISTRY: Dict[str, DataSource] = {
    source.master_source.master_source_id: source
    for source in ALL_43_SOURCES
}


# ============================================================
