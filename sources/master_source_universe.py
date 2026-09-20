# ============================================================


from __future__ import annotations


from typing import Dict, List


from .access_channel import AccessChannel
from .master_source import MasterSource
from .source_identity_status import SourceIdentityStatus
from .source_type import SourceType


MASTER_X_HANDLES = (
    "@CTAIntelligence",
    "@nilssonhedge",
    "@iasgcta",
    "@rcmAlts",
    "@MikeWShell",
    "@ShellCapital",
    "@JaffrayW",
    "@rjparkerjr09",
    "@rjpjr12",
    "@VicNiederhoffer",
    "@mmelissinos",
    "@TrendFollower9",
    "@TyphonCapital",
    "@LindaRaschke",
    "@PeterLBrandt",
    "@MebFaber",
    "@JohnFMauldin",
    "@mark_dow",
    "@David_Stendahl",
    "@MissTrade",
    "@EmanuelDerman",
    "@CFTC",
    "@CMEGroup",
    "@LME_news",
    "@NFA_News",
    "@theniba",
    "@CAIAAssociation",
    "@CQGInc",
    "@Trading_Tech",
    "@iBroker",
    "@jameskoutoulas",
    "@opalesque",
    "@DailyAlts",
    "@JohnLothian",
    "@MarketsWiki",
    "@gate39media",
    "@HedgeWorld",
    "@Open_Markets",
    "@researchpuzzler",
    "@AlephBlog",
    "@cfromhertz",
    "@kiantrades",
    "@misterpuertas",
    "@MacroOps",
    "@CovenantCap",
    "@LJMPartners",
    "@AuspiceCapital",
    "@QbasisInvest",
    "@Bluenose_CTA",
    "@stengercap",
    "@QuantumPeakCap",
    "@AGManagedFut",
    "@ManagedFutureUK",
    "@AttainCap2",
    "@AnthonyCrudele",
    "@CommodMkt",
    "@FuturesTrader71",
    "@Covel",
    "@JBoorman",
    "@nntaleb",
    "@jackschwager",
    "@JezLiberty",
    "@ScottChantigny",
    "@AlpineAdvisor",
    "@MarkMelin",
    "@CBOE",
    "@ICE_Markets",
    "@JohnLRoe",
    "@DubaiMercantile",
)


HIGH_VALUE_HUMANS_25 = (
    "@rjparkerjr09",
    "@rjpjr12",
    "@PeterLBrandt",
    "@LindaRaschke",
    "@AnthonyCrudele",
    "@FuturesTrader71",
    "@CommodMkt",
    "@misterpuertas",
    "@TheStalwart",
    "@MacroOps",
    "@Covel",
    "@JBoorman",
    "@nntaleb",
    "@jackschwager",
    "@MebFaber",
    "@JohnFMauldin",
    "@mark_dow",
    "@David_Stendahl",
    "@EmanuelDerman",
    "@mmelissinos",
    "@TrendFollower9",
    "@AuspiceCapital",
    "@TyphonCapital",
    "@QuantumPeakCap",
    "@AttainCap2",
)


INSTITUTIONAL_CTAS = (
    (
        "master.institution.crabel",
        "Crabel",
        "crabel.com",
    ),
    (
        "master.institution.dynamic_beta",
        "Dynamic Beta",
        "dbi.co",
    ),
    (
        "master.institution.qim",
        "QIM",
        "quantitative.com",
    ),
    (
        "master.institution.qbasis",
        "Qbasis",
        "en.qbasisinvest.com",
    ),
    (
        "master.institution.typhon_capital",
        "Typhon Capital",
        "typhoncap.com",
    ),
)


def build_master_sources() -> List[MasterSource]:
    sources: List[MasterSource] = []


    for handle in MASTER_X_HANDLES:
        sources.append(
            MasterSource(
                master_source_id=f"master.x.{handle.lstrip('@')}",
                name=handle,
                source_type=SourceType.X_ACCOUNT,
                source_identity_status=SourceIdentityStatus.UNRESOLVED,
                access_channels=(AccessChannel.X,),
                source_roles=(),
            )
        )


    for source_id, name, domain in INSTITUTIONAL_CTAS:
        sources.append(
            MasterSource(
                master_source_id=source_id,
                name=name,
                source_type=SourceType.INSTITUTION,
                source_identity_status=SourceIdentityStatus.UNRESOLVED,
                access_channels=(),
                source_roles=(),
                metadata={"domain": domain},
            )
        )


    sources.append(
        MasterSource(
            master_source_id="master.tick_bill",
            name="Tick Bill",
            source_type=SourceType.PERSON,
            source_identity_status=SourceIdentityStatus.UNRESOLVED,
            access_channels=(),
            source_roles=(),
        )
    )


    return sources


MASTER_SOURCES = build_master_sources()


MASTER_SOURCE_REGISTRY: Dict[str, MasterSource] = {
    source.master_source_id: source
    for source in MASTER_SOURCES
}


# ============================================================
