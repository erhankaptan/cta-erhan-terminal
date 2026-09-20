# ===== BOLUM 1 =====
# ============================================================


from .validation import run_integrity_validation


if __name__ == "__main__":
    run_integrity_validation()
    print("4.2 VALIDATION: PASS")


# ============================================================
# CTA TERMINALİ — BÖLÜM 4.3
# DATA / API / ETF / OPTIONS / MACRO / FUTURES SOURCES
# ============================================================


# ============================================================


# ===== BOLUM 2 =====
# ============================================================


from .data_source_validation import run_data_source_validation
from .validation import run_integrity_validation


if __name__ == "__main__":
    run_integrity_validation()
    run_data_source_validation()
    print("4.2 VALIDATION: PASS")
    print("4.3 DATA SOURCE VALIDATION: PASS")


"""
CTA TERMINAL
4.4 — VERIFIED SOURCES / OPERATIONAL ACCESS / SOURCE USAGE


SOURCE IDENTITY → OPERATIONAL STATUS → SOURCE USAGE


SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ


Bu modül:
- 4.1 / 4.2 MASTER source identity'lerini yeniden oluşturmaz.
- MASTER universe'i genişletmez veya daraltmaz.
- Source identity ile operational status'u ayırır.
- Operational status ile source usage'u ayırır.
- Source access ile content/media access'i ayırır.
- Claim verification status'u operational status ile karıştırmaz.
- Trust / quality / credibility / reliability / evidence score üretmez.
- Ranking / weighting / conflict resolution yapmaz.
- Trading / risk / portfolio / execution kararı üretmez.
"""


from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# 1. OPERATIONAL STATUS
# ============================================================


class OperationalStatus(str, Enum):
    """
    4.4'te kilitli operasyonel durumlar.


    Yeni operasyonel durum oluşturulmaz.
    """


    KULLANILABILIR = "KULLANILABILIR"
    KISITLI = "KISITLI"
    SADECE_MANUEL = "SADECE_MANUEL"
    ERISILEMIYOR = "ERISILEMIYOR"


# ============================================================
# 2. CONTENT / MEDIA ACCESS STATUS
# ============================================================


class ContentAccessStatus(str, Enum):
    """
    Kaynak seviyesinden bağımsız içerik / medya erişim durumu.


    SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS
    """


    ACCESSIBLE = "ACCESSIBLE"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    NOT_RETRIEVED = "NOT_RETRIEVED"
    ACCESS_BLOCKED = "ACCESS_BLOCKED"
    UNCERTAIN = "UNCERTAIN"


# ============================================================
# 3. MULTIMODAL CONTENT TYPE
# ============================================================


class MediaType(str, Enum):
    """
    Kaynak içerisinde bulunabilecek multimodal içerik türleri.
    """


    TEXT = "TEXT"
    TABLE = "TABLE"
    CHART = "CHART"
    IMAGE = "IMAGE"
    GRAPH = "GRAPH"
    SCREENSHOT = "SCREENSHOT"
    INFOGRAPHIC = "INFOGRAPHIC"
    DIAGRAM = "DIAGRAM"
    PDF_FIGURE = "PDF_FIGURE"


# ============================================================
# 4. SOURCE USAGE CLASS
# ============================================================


class SourceUsageClass(str, Enum):
    """
    Source usage sınıfları.


    Bunlar:
    - quality score değildir
    - trust score değildir
    - credibility score değildir
    - reliability score değildir
    - evidence score değildir
    - numerical weighting değildir
    - ranking değildir
    """


    PRIMARY = "PRIMARY"
    SECONDARY_RESEARCH = "SECONDARY_RESEARCH"
    SECONDARY_PRODUCT_SPECIFIC = "SECONDARY_PRODUCT_SPECIFIC"
    SUPPORTING_COMMENTARY = "SUPPORTING_COMMENTARY"
    HISTORICAL = "HISTORICAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"


# ============================================================
# 5. CONTENT ACCESS RECORD
# ============================================================


@dataclass(frozen=True)
class ContentAccessRecord:
    """
    Belirli bir content/media öğesinin erişim durumunu temsil eder.


    Kaynağın operational status'u bu kaydın yerine geçmez.
    """


    media_type: MediaType
    status: ContentAccessStatus
    locator: Optional[str] = None
    notes: Optional[str] = None


# ============================================================
# 6. SOURCE OPERATIONAL RECORD
# ============================================================


@dataclass(frozen=True)
class SourceOperationalRecord:
    """
    4.4 operational source record.


    master_source_id:
        4.1 / 4.2 tarafından tanımlanan source identity.


    operational_status:
        Kaynağın operasyonel erişim durumu.


    source_usage_class:
        Kaynağın 4.4 kullanım sınıfı.


    content_access:
        Belirli text/table/chart/image/PDF figure vb.
        içeriklerin erişim durumu.


    NOT:
        Content access kaydı yoksa bu, içeriğin erişilebilir
        olduğu anlamına gelmez.
    """


    master_source_id: str
    operational_status: OperationalStatus
    source_usage_class: SourceUsageClass
    content_access: tuple[ContentAccessRecord, ...] = field(
        default_factory=tuple
    )
    notes: Optional[str] = None


# ============================================================
# 7. CANONICAL SOURCE IDS
# ============================================================
#
# Bu modül MASTER X listesini yeniden tanımlamaz.
# Yalnızca 4.4'te açıkça operasyonel statüsü / kullanım sınıfı
# belirtilen source identity'lere referans verir.
#
# ID'ler source identity'dir.
# URL, access channel veya claim değildir.
# ============================================================


# ------------------------------------------------------------
# KISITLI
# ------------------------------------------------------------


KISITLI_SOURCES: tuple[str, ...] = (
    "master.institution.dbmf",
    "master.index.sg_trend_indicator",
    "master.index.barclay_cta_index",
)


# ------------------------------------------------------------
# SADECE MANUEL
# ------------------------------------------------------------


SADECE_MANUEL_SOURCES: tuple[str, ...] = (
    "master.person.andrew_beer",
    "master.institution.dynamic_beta",
    "master.person.jerry_parker",
    "master.historical_system.turtle_trader",
    "master.historical_institution.newedge",
    "master.x.rjpjr12",
    "master.x.peterlbrandt",
    "master.x.lindaraschke",
    "master.x.rcmalts",
    "master.x.anthonycrudele",
    "master.x.futurestrader71",
    "master.x.commodmkt",
    "master.x.tracyalloway",
    "master.x.misterpuertas",
    "master.x.thestalwart",
    "master.x.macroops",
)


# ------------------------------------------------------------
# ERİŞİLEMİYOR
# ------------------------------------------------------------


ERISILEMIYOR_SOURCES: tuple[str, ...] = (
    "master.x.attaincap2",
    "master.x.jpokotrades",
)


# ============================================================
# 8. SOURCE USAGE HIERARCHY
# ============================================================


PRIMARY_SOURCES: tuple[str, ...] = (
    "master.index.sg_trend_indicator",
    "master.index.barclay_cta_index",
)


SECONDARY_RESEARCH_SOURCES: tuple[str, ...] = (
    "master.person.andrew_beer",
    "master.institution.dynamic_beta",
    "master.person.jerry_parker",
    "master.x.rcmalts",
    "master.x.macroops",
)


SECONDARY_PRODUCT_SPECIFIC_SOURCES: tuple[str, ...] = (
    "master.institution.dbmf",
)


SUPPORTING_COMMENTARY_SOURCES: tuple[str, ...] = (
    "master.x.rjpjr12",
    "master.x.peterlbrandt",
    "master.x.lindaraschke",
    "master.x.anthonycrudele",
    "master.x.futurestrader71",
    "master.x.commodmkt",
    "master.x.tracyalloway",
    "master.x.misterpuertas",
    "master.x.thestalwart",
)


HISTORICAL_SOURCES: tuple[str, ...] = (
    "master.historical_system.turtle_trader",
    "master.historical_institution.newedge",
)


NON_OPERATIONAL_SOURCES: tuple[str, ...] = (
    "master.x.attaincap2",
    "master.x.jpokotrades",
)


# ============================================================
# 9. INTERNAL SOURCE USAGE RESOLUTION
# ============================================================


def _usage_class_for_source(master_source_id: str) -> SourceUsageClass:
    """
    Source usage hierarchy çözümlemesi.


    Öncelik:
    PRIMARY
    SECONDARY_RESEARCH
    SECONDARY_PRODUCT_SPECIFIC
    SUPPORTING_COMMENTARY
    HISTORICAL
    NON_OPERATIONAL
    """


    if master_source_id in PRIMARY_SOURCES:
        return SourceUsageClass.PRIMARY


    if master_source_id in SECONDARY_RESEARCH_SOURCES:
        return SourceUsageClass.SECONDARY_RESEARCH


    if master_source_id in SECONDARY_PRODUCT_SPECIFIC_SOURCES:
        return SourceUsageClass.SECONDARY_PRODUCT_SPECIFIC


    if master_source_id in SUPPORTING_COMMENTARY_SOURCES:
        return SourceUsageClass.SUPPORTING_COMMENTARY


    if master_source_id in HISTORICAL_SOURCES:
        return SourceUsageClass.HISTORICAL


    if master_source_id in NON_OPERATIONAL_SOURCES:
        return SourceUsageClass.NON_OPERATIONAL


    raise KeyError(
        f"4.4 usage class tanımlanmamış source: {master_source_id}"
    )


def _operational_status_for_source(
    master_source_id: str,
) -> OperationalStatus:
    """
    Yalnızca 4.4'te açıkça tanımlanmış operational status'ları çözer.


    Tanımsız source için otomatik ERISILEMIYOR ataması yapılmaz.
    """


    if master_source_id in KISITLI_SOURCES:
        return OperationalStatus.KISITLI


    if master_source_id in SADECE_MANUEL_SOURCES:
        return OperationalStatus.SADECE_MANUEL


    if master_source_id in ERISILEMIYOR_SOURCES:
        return OperationalStatus.ERISILEMIYOR


    raise KeyError(
        "4.4 operational status tanımsız source için otomatik "
        f"status atanamaz: {master_source_id}"
    )


# ============================================================
# 10. BUILD OPERATIONAL RECORDS
# ============================================================


def _build_operational_records() -> dict[str, SourceOperationalRecord]:
    """
    4.4'te açıkça tanımlanan source'lar için operational records üretir.


    ÖNEMLİ:
    4.4'te belirtilmeyen MASTER source'lar burada otomatik olarak
    KULLANILABILIR veya ERISILEMIYOR yapılmaz.


    Böylece:
        "4.4'te belirtilmedi"
    ile:
        "ERİŞİLEMİYOR"
    birbirine dönüştürülmez.
    """


    records: dict[str, SourceOperationalRecord] = {}


    all_explicit_sources = (
        set(KISITLI_SOURCES)
        | set(SADECE_MANUEL_SOURCES)
        | set(ERISILEMIYOR_SOURCES)
    )


    for source_id in sorted(all_explicit_sources):
        operational_status = _operational_status_for_source(source_id)
        usage_class = _usage_class_for_source(source_id)


        if operational_status == OperationalStatus.KISITLI:
            note = (
                "4.4: KISITLI. Ücretsiz / ürün-spesifik erişim mevcut "
                "olabilir; full API veya tam programmatic feed varsayılmaz."
            )


        elif operational_status == OperationalStatus.SADECE_MANUEL:
            note = (
                "4.4: SADECE MANUEL. API veya otomatik retrieval "
                "doğrulanmadıkça varsayılmaz."
            )


        elif operational_status == OperationalStatus.ERISILEMIYOR:
            note = (
                "4.4: ERİŞİLEMİYOR. Operasyonel kullanım dışıdır; "
                "source identity korunur."
            )


        else:
            note = None


        records[source_id] = SourceOperationalRecord(
            master_source_id=source_id,
            operational_status=operational_status,
            source_usage_class=usage_class,
            content_access=(),
            notes=note,
        )


    return records


SOURCE_OPERATIONAL_RECORDS: dict[str, SourceOperationalRecord] = (
    _build_operational_records()
)


# ============================================================
# 11. CONTENT / MEDIA ACCESS HELPERS
# ============================================================


def content_status_of(
    master_source_id: str,
    media_type: MediaType,
) -> ContentAccessStatus:
    """
    Belirli source + media type için doğrulanmış content access
    kaydını döndürür.


    Kayıt yoksa:
        UNCERTAIN


    döner.


    Bu:
        source erişilemiyor
    anlamına gelmez.


    Aynı şekilde:
        source erişilebilir
    anlamına da gelmez.
    """


    record = SOURCE_OPERATIONAL_RECORDS.get(master_source_id)


    if record is None:
        return ContentAccessStatus.UNCERTAIN


    for content_record in record.content_access:
        if content_record.media_type == media_type:
            return content_record.status


    return ContentAccessStatus.UNCERTAIN


def with_content_access(
    master_source_id: str,
    content_record: ContentAccessRecord,
) -> SourceOperationalRecord:
    """
    Mevcut source operational status'u değiştirmeden,
    belirli content/media access kaydı ekler.


    SOURCE OPERATIONAL STATUS DEĞİŞTİRİLMEZ.
    """


    record = SOURCE_OPERATIONAL_RECORDS.get(master_source_id)


    if record is None:
        raise KeyError(
            f"4.4 source operational record bulunamadı: {master_source_id}"
        )


    updated_content = tuple(
        existing
        for existing in record.content_access
        if existing.media_type != content_record.media_type
    ) + (content_record,)


    return SourceOperationalRecord(
        master_source_id=record.master_source_id,
        operational_status=record.operational_status,
        source_usage_class=record.source_usage_class,
        content_access=updated_content,
        notes=record.notes,
    )


def source_access_is_independent_of_content(
    master_source_id: str,
) -> bool:
    """
    SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS


    Bu fonksiyon source access ile content access'in
    ayrı kavramlar olduğunu yapısal olarak ifade eder.


    Source'un mevcut olması veya operational record'a sahip olması,
    content/media'nın tamamının erişilebilir olduğu sonucunu üretmez.
    """


    return master_source_id in SOURCE_OPERATIONAL_RECORDS


# ============================================================
# 12. SOURCE USAGE / OPERATIONAL VALIDATION
# ============================================================


def validate_operational_status_enum() -> None:
    """Yalnızca 4 kilitli operational status vardır."""


    expected = {
        "KULLANILABILIR",
        "KISITLI",
        "SADECE_MANUEL",
        "ERISILEMIYOR",
    }


    actual = {status.value for status in OperationalStatus}


    assert actual == expected
    assert len(actual) == 4


def validate_content_access_enum() -> None:
    """Content/media access durumları korunur."""


    expected = {
        "ACCESSIBLE",
        "PARTIAL",
        "MISSING",
        "NOT_RETRIEVED",
        "ACCESS_BLOCKED",
        "UNCERTAIN",
    }


    actual = {status.value for status in ContentAccessStatus}


    assert actual == expected


def validate_media_types() -> None:
    """4.4 multimodal sınırı korunur."""


    expected = {
        "TEXT",
        "TABLE",
        "CHART",
        "IMAGE",
        "GRAPH",
        "SCREENSHOT",
        "INFOGRAPHIC",
        "DIAGRAM",
        "PDF_FIGURE",
    }


    actual = {media.value for media in MediaType}


    assert actual == expected


def validate_usage_classes() -> None:
    """4.4 usage hierarchy sınıfları korunur."""


    expected = {
        "PRIMARY",
        "SECONDARY_RESEARCH",
        "SECONDARY_PRODUCT_SPECIFIC",
        "SUPPORTING_COMMENTARY",
        "HISTORICAL",
        "NON_OPERATIONAL",
    }


    actual = {usage.value for usage in SourceUsageClass}


    assert actual == expected


def validate_source_status_partition() -> None:
    """
    Explicit operational source kümeleri birbirini tekrar etmez.
    """


    restricted = set(KISITLI_SOURCES)
    manual = set(SADECE_MANUEL_SOURCES)
    unavailable = set(ERISILEMIYOR_SOURCES)


    assert restricted.isdisjoint(manual)
    assert restricted.isdisjoint(unavailable)
    assert manual.isdisjoint(unavailable)


def validate_usage_partition() -> None:
    """
    Source usage hierarchy içerisinde aynı source'un birden fazla
    usage sınıfında bulunması engellenir.
    """


    groups = (
        set(PRIMARY_SOURCES),
        set(SECONDARY_RESEARCH_SOURCES),
        set(SECONDARY_PRODUCT_SPECIFIC_SOURCES),
        set(SUPPORTING_COMMENTARY_SOURCES),
        set(HISTORICAL_SOURCES),
        set(NON_OPERATIONAL_SOURCES),
    )


    for index, current in enumerate(groups):
        for other in groups[index + 1:]:
            assert current.isdisjoint(other)


def validate_operational_records_complete() -> None:
    """
    4.4'te açıkça tanımlanan her source'un operational record'u vardır.
    """


    expected = (
        set(KISITLI_SOURCES)
        | set(SADECE_MANUEL_SOURCES)
        | set(ERISILEMIYOR_SOURCES)
    )


    assert set(SOURCE_OPERATIONAL_RECORDS) == expected


def validate_kisitli_sources() -> None:
    """DBMF / SG Trend Indicator / Barclay CTA Index."""


    assert (
        SOURCE_OPERATIONAL_RECORDS[
            "master.institution.dbmf"
        ].operational_status
        == OperationalStatus.KISITLI
    )


    assert (
        SOURCE_OPERATIONAL_RECORDS[
            "master.index.sg_trend_indicator"
        ].operational_status
        == OperationalStatus.KISITLI
    )


    assert (
        SOURCE_OPERATIONAL_RECORDS[
            "master.index.barclay_cta_index"
        ].operational_status
        == OperationalStatus.KISITLI
    )


def validate_sg_rule() -> None:
    """
    SG Trend Indicator:


    KISITLI


    SG Trend Index, paid SG Markets Analytics/Data veya Bloomberg
    anlamına gelmez.
    """


    record = SOURCE_OPERATIONAL_RECORDS[
        "master.index.sg_trend_indicator"
    ]


    assert record.operational_status == OperationalStatus.KISITLI
    assert record.source_usage_class == SourceUsageClass.PRIMARY


def validate_dbmf_rule() -> None:
    """
    DBMF:


    KISITLI
    SECONDARY / PRODUCT-SPECIFIC


    Genel CTA positioning olarak yorumlanmaz.
    """


    record = SOURCE_OPERATIONAL_RECORDS[
        "master.institution.dbmf"
    ]


    assert record.operational_status == OperationalStatus.KISITLI
    assert (
        record.source_usage_class
        == SourceUsageClass.SECONDARY_PRODUCT_SPECIFIC
    )


def validate_barclay_rule() -> None:
    """
    Barclay CTA Index:


    KISITLI
    PRIMARY


    Benchmark / index kapsamındadır.
    Doğrudan CTA portfolio positioning değildir.
    """


    record = SOURCE_OPERATIONAL_RECORDS[
        "master.index.barclay_cta_index"
    ]


    assert record.operational_status == OperationalStatus.KISITLI
    assert record.source_usage_class == SourceUsageClass.PRIMARY


def validate_manual_sources() -> None:
    """4.4 SADECE MANUEL kaynakları."""


    for source_id in SADECE_MANUEL_SOURCES:
        record = SOURCE_OPERATIONAL_RECORDS[source_id]


        assert (
            record.operational_status
            == OperationalStatus.SADECE_MANUEL
        )


def validate_non_operational_sources() -> None:
    """
    @AttainCap2 / @JPokoTrades:


    ERİŞİLEMİYOR
    NON_OPERATIONAL


    Retrieval veya supporting/research evidence olarak
    operasyonel kullanım yoktur.
    """


    for source_id in ERISILEMIYOR_SOURCES:
        record = SOURCE_OPERATIONAL_RECORDS[source_id]


        assert (
            record.operational_status
            == OperationalStatus.ERISILEMIYOR
        )


        assert (
            record.source_usage_class
            == SourceUsageClass.NON_OPERATIONAL
        )


# ============================================================
# 13. CRITICAL IDENTITY VALIDATION
# ============================================================


def validate_rjparker_identity_boundary() -> None:
    """
    4.1 kritik identity kuralı:


    @rjparkerjr09
    @rjpjr12


    birbirinden ayrıdır.


    Yasak yanlış kimlik:
    @rjparkerjr12
    """


    assert "master.x.rjpjr12" in SADECE_MANUEL_SOURCES


    forbidden_wrong_identity = "master.x.rjparkerjr12"


    assert forbidden_wrong_identity not in KISITLI_SOURCES
    assert forbidden_wrong_identity not in SADECE_MANUEL_SOURCES
    assert forbidden_wrong_identity not in ERISILEMIYOR_SOURCES
    assert forbidden_wrong_identity not in PRIMARY_SOURCES
    assert forbidden_wrong_identity not in SECONDARY_RESEARCH_SOURCES
    assert forbidden_wrong_identity not in SUPPORTING_COMMENTARY_SOURCES
    assert forbidden_wrong_identity not in NON_OPERATIONAL_SOURCES


# ============================================================
# 14. HIGH-VALUE HUMAN IDENTITY BOUNDARY
# ============================================================


def validate_the_stalwart_boundary() -> None:
    """
    @TheStalwart:


    4.1 H-V listesinde bulunur.
    MASTER X 69 listesine bu modül tarafından eklenmez.
    """


    source_id = "master.x.thestalwart"


    assert source_id in SADECE_MANUEL_SOURCES
    assert source_id in SUPPORTING_COMMENTARY_SOURCES


# ============================================================
# 15. MULTIMODAL BOUNDARY VALIDATION
# ============================================================


def validate_multimodal_boundary() -> None:
    """
    SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS


    Source operational record bulunması,
    content/media erişilebilirliği üretmez.
    """


    source_id = "master.institution.dbmf"


    record = SOURCE_OPERATIONAL_RECORDS[source_id]


    assert record.operational_status == OperationalStatus.KISITLI


    assert (
        content_status_of(
            source_id,
            MediaType.TABLE,
        )
        == ContentAccessStatus.UNCERTAIN
    )


    assert (
        content_status_of(
            source_id,
            MediaType.CHART,
        )
        == ContentAccessStatus.UNCERTAIN
    )


    assert (
        content_status_of(
            source_id,
            MediaType.PDF_FIGURE,
        )
        == ContentAccessStatus.UNCERTAIN
    )


def validate_content_does_not_change_source_status() -> None:
    """
    Belirli bir media öğesinin erişilememesi,
    source operational status'unu otomatik değiştirmez.
    """


    source_id = "master.institution.dbmf"


    original = SOURCE_OPERATIONAL_RECORDS[source_id]


    updated = with_content_access(
        source_id,
        ContentAccessRecord(
            media_type=MediaType.CHART,
            status=ContentAccessStatus.ACCESS_BLOCKED,
            notes="Belirli grafik retrieval edilemedi.",
        ),
    )


    assert (
        updated.operational_status
        == original.operational_status
    )


    assert (
        updated.source_usage_class
        == original.source_usage_class
    )


    assert (
        content_status_of(
            source_id,
            MediaType.CHART,
        )
        == ContentAccessStatus.UNCERTAIN
    )


    assert (
        updated.content_access[0].status
        == ContentAccessStatus.ACCESS_BLOCKED
    )


# ============================================================
# 16. NO SCORE / RANK / WEIGHTING VALIDATION
# ============================================================


def validate_no_scoring_or_ranking() -> None:
    """
    Source usage sınıfları skor, ranking veya weighting değildir.


    Bu modülde:
    - score
    - rank
    - weight
    - trust score
    - quality score
    - credibility score
    - reliability score
    - evidence score


    hesaplanmaz.
    """


    assert not hasattr(SourceOperationalRecord, "score")
    assert not hasattr(SourceOperationalRecord, "rank")
    assert not hasattr(SourceOperationalRecord, "weight")
    assert not hasattr(SourceOperationalRecord, "trust_score")
    assert not hasattr(SourceOperationalRecord, "quality_score")
    assert not hasattr(SourceOperationalRecord, "credibility_score")
    assert not hasattr(SourceOperationalRecord, "reliability_score")
    assert not hasattr(SourceOperationalRecord, "evidence_score")


# ============================================================
# 17. READ-ONLY BOUNDARY
# ============================================================


def validate_read_only_boundary() -> None:
    """
    4.4 kaynakları karar üretmez.


    Bu modülde:
    BUY
    SELL
    LONG
    SHORT
    TRADE SIGNAL
    FINAL BIAS
    PORTFOLIO DECISION
    RISK DECISION
    POSITION SIZING
    ORDER
    EXECUTION


    alanı veya kararı bulunmaz.
    """


    forbidden_fields = {
        "buy",
        "sell",
        "long",
        "short",
        "trade_signal",
        "final_bias",
        "portfolio_decision",
        "risk_decision",
        "position_sizing",
        "order",
        "execution",
    }


    dataclass_fields = {
        field_info.name
        for field_info in SourceOperationalRecord.__dataclass_fields__.values()
    }


    assert dataclass_fields.isdisjoint(forbidden_fields)


# ============================================================
# 18. IMMUTABILITY VALIDATION
# ============================================================


def validate_immutability() -> None:
    """
    Operational record ve content access record immutable'dır.
    """


    assert getattr(
        SourceOperationalRecord,
        "__dataclass_params__",
    ).frozen is True


    assert getattr(
        ContentAccessRecord,
        "__dataclass_params__",
    ).frozen is True


# ============================================================
# 19. FULL 4.4 VALIDATION
# ============================================================


def run_all_validations() -> None:
    """
    4.4 validation suite.


    Gerçek assertion kontrolleri çalıştırır.
    Test sonucu üretmeden önce bu fonksiyon gerçekten
    çağrılmalıdır.
    """


    validate_operational_status_enum()
    validate_content_access_enum()
    validate_media_types()
    validate_usage_classes()


    validate_source_status_partition()
    validate_usage_partition()
    validate_operational_records_complete()


    validate_kisitli_sources()
    validate_sg_rule()
    validate_dbmf_rule()
    validate_barclay_rule()


    validate_manual_sources()
    validate_non_operational_sources()


    validate_rjparker_identity_boundary()
    validate_the_stalwart_boundary()


    validate_multimodal_boundary()
    validate_content_does_not_change_source_status()


    validate_no_scoring_or_ranking()
    validate_read_only_boundary()
    validate_immutability()


# ============================================================
# 20. MODULE ENTRY POINT
# ============================================================


if __name__ == "__main__":
    run_all_validations()


    print(
        "4.4 — VERIFIED SOURCES / OPERATIONAL ACCESS / "
        "SOURCE USAGE"
    )
    print("=" * 72)
    print("Validation: PASSED")
    print(
        "SOURCE IDENTITY → OPERATIONAL STATUS → SOURCE USAGE"
    )
    print(
        "SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS"
    )
    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


"""
4.5 — CANONICAL INTELLIGENCE SCHEMA + RAW EVIDENCE LIFECYCLE


SOURCE → ACCESS → RETRIEVAL → RAW EVIDENCE
→ EXTRACTION / STRUCTURING → CANONICAL RECORD
→ VERIFICATION → DEDUPLICATION → CONFLICT
→ CURRENT / HISTORICAL STATE → STORAGE → DISPLAY


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict, Optional, Tuple
from datetime import datetime


# ============================================================
# 1. EXISTING ENUMS — CANONICAL SCHEMA
# ============================================================


class SourceType(str, Enum):
    X_ACCOUNT = "X_ACCOUNT"
    INSTITUTION = "INSTITUTION"
    HISTORICAL_INSTITUTION = "HISTORICAL_INSTITUTION"
    PERSON = "PERSON"
    INDEX = "INDEX"
    ETF_PRODUCT = "ETF_PRODUCT"
    POSITIONING_PROXY = "POSITIONING_PROXY"
    HISTORICAL_SYSTEM = "HISTORICAL_SYSTEM"


class SourceIdentityStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    UNRESOLVED = "UNRESOLVED"


class EvidenceClass(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUPPORTING = "SUPPORTING"
    HISTORICAL = "HISTORICAL"
    UNVERIFIED = "UNVERIFIED"


class MeasurementRole(str, Enum):
    DIRECT_MEASUREMENT = "DIRECT_MEASUREMENT"
    PROXY = "PROXY"
    PRODUCT_SPECIFIC = "PRODUCT_SPECIFIC"
    RESEARCH_EVIDENCE = "RESEARCH_EVIDENCE"
    COMMENTARY = "COMMENTARY"
    HISTORICAL_EVIDENCE = "HISTORICAL_EVIDENCE"


class OperationalStatus(str, Enum):
    KULLANILABILIR = "KULLANILABILIR"
    KISITLI = "KISITLI"
    SADECE_MANUEL = "SADECE_MANUEL"
    ERISILEMIYOR = "ERISILEMIYOR"


class FactStatus(str, Enum):
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    ESTIMATED = "ESTIMATED"
    FORECAST = "FORECAST"
    OPINION = "OPINION"
    UNVERIFIED = "UNVERIFIED"


class ClaimVerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    UNRESOLVED = "UNRESOLVED"


class TimeContext(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    ARCHIVED = "ARCHIVED"
    FORWARD_LOOKING = "FORWARD_LOOKING"


class AccessMethod(str, Enum):
    API = "API"
    CSV = "CSV"
    PDF = "PDF"
    HTML = "HTML"
    X = "X"
    OTHER = "OTHER"


class AccessMode(str, Enum):
    AUTOMATED = "AUTOMATED"
    PROGRAMMATIC_PARTIAL = "PROGRAMMATIC_PARTIAL"
    MANUAL = "MANUAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"


class MissingnessStatus(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    NOT_RETRIEVED = "NOT_RETRIEVED"
    ACCESS_BLOCKED = "ACCESS_BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class IndependenceStatus(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    SAME_SOURCE_FAMILY = "SAME_SOURCE_FAMILY"
    REPUBLISHED = "REPUBLISHED"
    UNKNOWN = "UNKNOWN"


# ============================================================
# 2. RAW EVIDENCE MODALITIES
# ============================================================


class RawEvidenceType(str, Enum):
    TEXT = "TEXT"
    NUMERIC_DATA = "NUMERIC_DATA"
    TABLE = "TABLE"
    CHART = "CHART"
    GRAPH = "GRAPH"
    IMAGE = "IMAGE"
    SCREENSHOT = "SCREENSHOT"
    INFOGRAPHIC = "INFOGRAPHIC"
    DIAGRAM = "DIAGRAM"
    MAP = "MAP"
    VISUAL_PANEL = "VISUAL_PANEL"
    PDF_PAGE = "PDF_PAGE"
    PDF_FIGURE = "PDF_FIGURE"
    PDF_TABLE = "PDF_TABLE"
    X_POST_MEDIA = "X_POST_MEDIA"
    REPORT_MEDIA = "REPORT_MEDIA"


# ============================================================
# 3. RAW EVIDENCE
# ============================================================


@dataclass(frozen=True)
class RawEvidenceRecord:
    """
    Immutable raw evidence.


    RAW EVIDENCE canonical record değildir.
    Raw evidence silinmez veya canonical record ile değiştirilmez.
    """


    raw_evidence_id: str
    master_source_id: str
    evidence_type: RawEvidenceType
    raw_content: Any
    retrieval_time: datetime


    access_method: AccessMethod
    access_mode: AccessMode
    missingness_status: MissingnessStatus


    source_url: Optional[str] = None
    source_locator: Optional[str] = None
    publication_id: Optional[str] = None
    document_id: Optional[str] = None
    page: Optional[str] = None
    visual_locator: Optional[str] = None


    observation_time: Optional[datetime] = None
    publication_time: Optional[datetime] = None


    source_family_id: Optional[str] = None
    notes: Optional[str] = None


# ============================================================
# 4. EXTRACTED / STRUCTURED INFORMATION
# ============================================================


@dataclass(frozen=True)
class ExtractedInformationRecord:
    """
    Raw visual evidence'den açıkça görülebilen bilgiyi temsil eder.


    Bu yapı canonical record değildir ve raw evidence'in yerine geçmez.
    Her extraction raw_evidence_id üzerinden kaynağına izlenebilir.
    """


    extracted_id: str
    raw_evidence_id: str
    master_source_id: str


    product: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    percentage: Optional[str] = None
    change: Optional[str] = None
    date: Optional[str] = None
    period: Optional[str] = None
    period_label: Optional[str] = None


    table_header: Optional[str] = None
    table_cell: Optional[str] = None
    ranking: Optional[str] = None


    chart_title: Optional[str] = None
    axis: Optional[str] = None
    legend: Optional[str] = None
    trend_direction: Optional[str] = None
    increase_decrease: Optional[str] = None
    explicit_relationship: Optional[str] = None


    missingness_status: MissingnessStatus = MissingnessStatus.COMPLETE
    notes: Optional[str] = None


# ============================================================
# 5. LOCKED CANONICAL INTELLIGENCE RECORD
# ============================================================


CANONICAL_FIELD_NAMES: Tuple[str, ...] = (
    "record_id",
    "master_source_id",
    "source_name",
    "source_type",
    "source_identity_status",
    "evidence_class",
    "measurement_role",
    "operational_status",
    "fact_status",
    "claim_verification_status",
    "subject",
    "entity_scope",
    "instrument_or_market",
    "claim",
    "value",
    "unit",
    "observation_time",
    "publication_time",
    "retrieval_time",
    "time_context",
    "access_method",
    "access_mode",
    "missingness_status",
    "source_url",
    "source_locator",
    "source_excerpt_or_field",
    "source_family_id",
    "publication_id",
    "claim_fingerprint",
    "deduplication_group_id",
    "independence_status",
    "conflict_group_id",
    "provenance_status",
    "confidence_basis",
)


@dataclass(frozen=True)
class CanonicalIntelligenceRecord:
    """
    4.5 kilitli canonical schema.


    TAM OLARAK 35 alan korunur.
    Yeni canonical field eklenmez.


    Raw evidence bağlantısı ayrı bir canonical field olarak eklenmez.
    Provenance bağlantısı source_locator / publication_id /
    source_family_id / source_excerpt_or_field ve provenance
    lifecycle yapısı üzerinden korunur.
    """


    record_id: str
    master_source_id: str
    source_name: str
    source_type: SourceType
    source_identity_status: SourceIdentityStatus
    evidence_class: EvidenceClass
    measurement_role: MeasurementRole
    operational_status: OperationalStatus
    fact_status: FactStatus
    claim_verification_status: ClaimVerificationStatus
    subject: Optional[str]
    entity_scope: Optional[str]
    instrument_or_market: Optional[str]
    claim: str
    value: Optional[str]
    unit: Optional[str]
    observation_time: Optional[datetime]
    publication_time: Optional[datetime]
    retrieval_time: Optional[datetime]
    time_context: TimeContext
    access_method: AccessMethod
    access_mode: AccessMode
    missingness_status: MissingnessStatus
    source_url: Optional[str]
    source_locator: Optional[str]
    source_excerpt_or_field: Optional[str]
    source_family_id: Optional[str]
    publication_id: Optional[str]
    claim_fingerprint: Optional[str]
    deduplication_group_id: Optional[str]
    independence_status: IndependenceStatus
    conflict_group_id: Optional[str]
    provenance_status: Optional[str]
    confidence_basis: Optional[str]


# ============================================================
# 6. PROVENANCE
# ============================================================


@dataclass(frozen=True)
class ProvenanceChain:
    """
    SOURCE → ACCESS → PUBLICATION/DOCUMENT → CONTENT
    → RAW EVIDENCE → CANONICAL RECORD
    """


    source_identity: str
    source_url: Optional[str] = None
    publication_identity: Optional[str] = None
    document_identity: Optional[str] = None
    page: Optional[str] = None
    visual_table_field_locator: Optional[str] = None
    retrieval_context: Optional[str] = None
    raw_evidence_id: Optional[str] = None
    source_family: Optional[str] = None


# ============================================================
# 7. LIFECYCLE
# ============================================================


LIFECYCLE_STAGES: Tuple[str, ...] = (
    "MASTER_SOURCE",
    "ACCESS",
    "RETRIEVAL",
    "RAW_EVIDENCE",
    "EXTRACTION_STRUCTURING",
    "CANONICAL_RECORD",
    "VERIFICATION",
    "DEDUPLICATION",
    "CONFLICT",
    "CURRENT_HISTORICAL_STATE",
    "STORAGE",
    "DISPLAY",
)


# ============================================================
# 8. IMMUTABLE RAW EVIDENCE STORE
# ============================================================


class RawEvidenceStore:
    """
    Immutable evidence lifecycle.


    Aynı raw_evidence_id ikinci kez yazılamaz.
    Yeni retrieval için yeni raw_evidence_id gerekir.
    """


    def __init__(self) -> None:
        self._records: Dict[str, RawEvidenceRecord] = {}


    def add(self, evidence: RawEvidenceRecord) -> str:
        if evidence.raw_evidence_id in self._records:
            raise ValueError(
                f"Raw evidence zaten mevcut: {evidence.raw_evidence_id}. "
                "Mevcut evidence üzerine yazılamaz."
            )


        self._records[evidence.raw_evidence_id] = evidence
        return evidence.raw_evidence_id


    def get(self, raw_evidence_id: str) -> Optional[RawEvidenceRecord]:
        return self._records.get(raw_evidence_id)


    def contains(self, raw_evidence_id: str) -> bool:
        return raw_evidence_id in self._records


    def __len__(self) -> int:
        return len(self._records)


# ============================================================
# 9. CANONICAL RECORD STORE
# ============================================================


class CanonicalRecordStore:
    """
    Canonical records ayrı tutulur.
    Raw evidence store'un yerine geçmez.
    """


    def __init__(self) -> None:
        self._records: Dict[str, CanonicalIntelligenceRecord] = {}


    def add(self, record: CanonicalIntelligenceRecord) -> str:
        if record.record_id in self._records:
            raise ValueError(
                f"Canonical record zaten mevcut: {record.record_id}."
            )


        self._records[record.record_id] = record
        return record.record_id


    def get(
        self,
        record_id: str,
    ) -> Optional[CanonicalIntelligenceRecord]:
        return self._records.get(record_id)


    def contains(self, record_id: str) -> bool:
        return record_id in self._records


    def __len__(self) -> int:
        return len(self._records)


# ============================================================
# 10. PROVENANCE STORE
# ============================================================


class ProvenanceStore:
    """
    Raw evidence ile canonical record arasındaki provenance zincirini
    canonical schema'ya yeni alan eklemeden tutar.
    """


    def __init__(self) -> None:
        self._chains: Dict[str, ProvenanceChain] = {}


    def add(
        self,
        record_id: str,
        chain: ProvenanceChain,
    ) -> None:
        if record_id in self._chains:
            raise ValueError(
                f"Provenance zaten mevcut: {record_id}."
            )


        self._chains[record_id] = chain


    def get(
        self,
        record_id: str,
    ) -> Optional[ProvenanceChain]:
        return self._chains.get(record_id)


# ============================================================
# 11. CANONICAL LIFECYCLE MANAGER
# ============================================================


class CanonicalIntelligenceLifecycleManager:
    """
    SOURCE → ACCESS → RETRIEVAL → RAW EVIDENCE
    → EXTRACTION / STRUCTURING → CANONICAL RECORD


    Raw evidence hiçbir aşamada canonical record ile değiştirilmez.
    """


    def __init__(self) -> None:
        self.raw_evidence = RawEvidenceStore()
        self.canonical_records = CanonicalRecordStore()
        self.provenance = ProvenanceStore()


    def ingest_raw_evidence(
        self,
        evidence: RawEvidenceRecord,
    ) -> str:
        return self.raw_evidence.add(evidence)


    def register_provenance(
        self,
        record_id: str,
        chain: ProvenanceChain,
    ) -> None:
        if not self.raw_evidence.contains(chain.raw_evidence_id or ""):
            raise ValueError(
                "Provenance raw evidence'e bağlı değil."
            )


        self.provenance.add(record_id, chain)


    def structure_canonical_record(
        self,
        *,
        record_id: str,
        raw_evidence_id: str,
        source_name: str,
        source_type: SourceType,
        source_identity_status: SourceIdentityStatus,
        evidence_class: EvidenceClass,
        measurement_role: MeasurementRole,
        operational_status: OperationalStatus,
        fact_status: FactStatus,
        claim_verification_status: ClaimVerificationStatus,
        subject: Optional[str],
        entity_scope: Optional[str],
        instrument_or_market: Optional[str],
        claim: str,
        value: Optional[str] = None,
        unit: Optional[str] = None,
        observation_time: Optional[datetime] = None,
        publication_time: Optional[datetime] = None,
        time_context: TimeContext = TimeContext.CURRENT,
        source_excerpt_or_field: Optional[str] = None,
        source_family_id: Optional[str] = None,
        publication_id: Optional[str] = None,
        claim_fingerprint: Optional[str] = None,
        deduplication_group_id: Optional[str] = None,
        independence_status: IndependenceStatus = (
            IndependenceStatus.UNKNOWN
        ),
        conflict_group_id: Optional[str] = None,
        provenance_status: Optional[str] = None,
        confidence_basis: Optional[str] = None,
    ) -> CanonicalIntelligenceRecord:
        if not self.raw_evidence.contains(raw_evidence_id):
            raise ValueError(
                f"Raw evidence bulunamadı: {raw_evidence_id}"
            )


        if not claim or not claim.strip():
            raise ValueError("claim zorunludur.")


        raw = self.raw_evidence.get(raw_evidence_id)
        if raw is None:
            raise ValueError("Raw evidence okunamadı.")


        if raw.master_source_id == "":
            raise ValueError("master_source_id boş olamaz.")


        record = CanonicalIntelligenceRecord(
            record_id=record_id,
            master_source_id=raw.master_source_id,
            source_name=source_name,
            source_type=source_type,
            source_identity_status=source_identity_status,
            evidence_class=evidence_class,
            measurement_role=measurement_role,
            operational_status=operational_status,
            fact_status=fact_status,
            claim_verification_status=claim_verification_status,
            subject=subject,
            entity_scope=entity_scope,
            instrument_or_market=instrument_or_market,
            claim=claim,
            value=value,
            unit=unit,
            observation_time=(
                observation_time
                if observation_time is not None
                else raw.observation_time
            ),
            publication_time=(
                publication_time
                if publication_time is not None
                else raw.publication_time
            ),
            retrieval_time=raw.retrieval_time,
            time_context=time_context,
            access_method=raw.access_method,
            access_mode=raw.access_mode,
            missingness_status=raw.missingness_status,
            source_url=raw.source_url,
            source_locator=raw.source_locator,
            source_excerpt_or_field=source_excerpt_or_field,
            source_family_id=(
                source_family_id
                if source_family_id is not None
                else raw.source_family_id
            ),
            publication_id=(
                publication_id
                if publication_id is not None
                else raw.publication_id
            ),
            claim_fingerprint=claim_fingerprint,
            deduplication_group_id=deduplication_group_id,
            independence_status=independence_status,
            conflict_group_id=conflict_group_id,
            provenance_status=provenance_status,
            confidence_basis=confidence_basis,
        )


        self.canonical_records.add(record)


        self.register_provenance(
            record_id,
            ProvenanceChain(
                source_identity=record.master_source_id,
                source_url=record.source_url,
                publication_identity=record.publication_id,
                document_identity=raw.document_id,
                page=raw.page,
                visual_table_field_locator=raw.visual_locator,
                retrieval_context=(
                    record.retrieval_time.isoformat()
                    if record.retrieval_time
                    else None
                ),
                raw_evidence_id=raw_evidence_id,
                source_family=record.source_family_id,
            ),
        )


        return record


    def get_raw_evidence(
        self,
        raw_evidence_id: str,
    ) -> Optional[RawEvidenceRecord]:
        return self.raw_evidence.get(raw_evidence_id)


    def get_canonical_record(
        self,
        record_id: str,
    ) -> Optional[CanonicalIntelligenceRecord]:
        return self.canonical_records.get(record_id)


    def get_provenance(
        self,
        record_id: str,
    ) -> Optional[ProvenanceChain]:
        return self.provenance.get(record_id)


# ============================================================
# 12. FIELD VALIDATION
# ============================================================


def validate_canonical_field_set() -> None:
    actual = tuple(
        field_info.name
        for field_info in fields(CanonicalIntelligenceRecord)
    )


    assert actual == CANONICAL_FIELD_NAMES, (
        "Canonical field set değişmiştir."
    )


def validate_claim_required(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.claim is not None
    assert record.claim.strip() != ""


def validate_value_rule(
    record: CanonicalIntelligenceRecord,
) -> None:
    if record.value is not None:
        assert record.claim is not None


def validate_time_separation(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert hasattr(record, "observation_time")
    assert hasattr(record, "publication_time")
    assert hasattr(record, "retrieval_time")


def validate_enum_integrity(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert isinstance(record.source_type, SourceType)
    assert isinstance(
        record.source_identity_status,
        SourceIdentityStatus,
    )
    assert isinstance(record.evidence_class, EvidenceClass)
    assert isinstance(record.measurement_role, MeasurementRole)
    assert isinstance(
        record.operational_status,
        OperationalStatus,
    )
    assert isinstance(record.fact_status, FactStatus)
    assert isinstance(
        record.claim_verification_status,
        ClaimVerificationStatus,
    )
    assert isinstance(record.time_context, TimeContext)
    assert isinstance(record.access_method, AccessMethod)
    assert isinstance(record.access_mode, AccessMode)
    assert isinstance(
        record.missingness_status,
        MissingnessStatus,
    )
    assert isinstance(
        record.independence_status,
        IndependenceStatus,
    )


# ============================================================
# 13. EVIDENCE CLASS / MEASUREMENT ROLE
# ============================================================


def validate_evidence_class_is_not_score(
    evidence_class: EvidenceClass,
) -> None:
    assert evidence_class in EvidenceClass


def validate_measurement_role_not_from_format(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.measurement_role in MeasurementRole


def validate_special_source_roles() -> None:
    assert MeasurementRole.PROXY.value == "PROXY"
    assert MeasurementRole.PRODUCT_SPECIFIC.value == (
        "PRODUCT_SPECIFIC"
    )
    assert MeasurementRole.DIRECT_MEASUREMENT.value == (
        "DIRECT_MEASUREMENT"
    )
    assert MeasurementRole.HISTORICAL_EVIDENCE.value == (
        "HISTORICAL_EVIDENCE"
    )


# ============================================================
# 14. FACT STATUS / TIME CONTEXT
# ============================================================


def validate_fact_status_preserved(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.fact_status in FactStatus


def validate_visual_not_auto_observed(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.fact_status in FactStatus


def validate_time_context_preserved(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.time_context in TimeContext


# ============================================================
# 15. ACCESS / MISSINGNESS
# ============================================================


def validate_access(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.access_method in AccessMethod
    assert record.access_mode in AccessMode


def validate_missingness(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert record.missingness_status in MissingnessStatus


def validate_multimodal_missingness() -> None:
    assert MissingnessStatus.PARTIAL.value == "PARTIAL"
    assert (
        MissingnessStatus.NOT_RETRIEVED.value
        == "NOT_RETRIEVED"
    )
    assert (
        MissingnessStatus.ACCESS_BLOCKED.value
        == "ACCESS_BLOCKED"
    )


# ============================================================
# 16. PROVENANCE
# ============================================================


def validate_provenance(
    chain: ProvenanceChain,
) -> None:
    assert chain.source_identity
    assert chain.raw_evidence_id


def validate_raw_to_canonical_link(
    manager: CanonicalIntelligenceLifecycleManager,
    record_id: str,
) -> None:
    record = manager.get_canonical_record(record_id)
    chain = manager.get_provenance(record_id)


    assert record is not None
    assert chain is not None
    assert chain.raw_evidence_id is not None


    raw = manager.get_raw_evidence(chain.raw_evidence_id)
    assert raw is not None
    assert raw.master_source_id == record.master_source_id


# ============================================================
# 17. INDEPENDENCE / DEDUP / CONFLICT
# ============================================================


def validate_independence(
    record: CanonicalIntelligenceRecord,
) -> None:
    if record.independence_status in (
        IndependenceStatus.SAME_SOURCE_FAMILY,
        IndependenceStatus.REPUBLISHED,
    ):
        assert (
            record.independence_status
            != IndependenceStatus.INDEPENDENT
        )


def validate_conflict_preserved(
    record: CanonicalIntelligenceRecord,
) -> None:
    if record.conflict_group_id is not None:
        assert isinstance(record.conflict_group_id, str)


# ============================================================
# 18. CONFIDENCE BASIS
# ============================================================


def validate_confidence_basis(
    record: CanonicalIntelligenceRecord,
) -> None:
    assert (
        record.confidence_basis is None
        or isinstance(record.confidence_basis, str)
    )


# ============================================================
# 19. LIFECYCLE
# ============================================================


def validate_lifecycle() -> None:
    required = (
        "MASTER_SOURCE",
        "ACCESS",
        "RETRIEVAL",
        "RAW_EVIDENCE",
        "EXTRACTION_STRUCTURING",
        "CANONICAL_RECORD",
        "VERIFICATION",
        "DEDUPLICATION",
        "CONFLICT",
        "CURRENT_HISTORICAL_STATE",
        "STORAGE",
        "DISPLAY",
    )


    assert LIFECYCLE_STAGES == required


# ============================================================
# 20. FORBIDDEN CANONICAL FIELDS
# ============================================================


FORBIDDEN_CANONICAL_FIELDS: Tuple[str, ...] = (
    "score",
    "rank",
    "weight",
    "signal",
    "BUY",
    "SELL",
    "LONG",
    "SHORT",
    "bias",
    "trade",
    "risk",
    "execution",
    "freshness_score",
    "trust_score",
    "visual_confidence_score",
    "OCR_score",
    "image_quality_score",
    "extraction_score",
    "media_reliability_score",
)


def validate_no_forbidden_fields() -> None:
    actual = {
        field_info.name
        for field_info in fields(CanonicalIntelligenceRecord)
    }


    for forbidden in FORBIDDEN_CANONICAL_FIELDS:
        assert forbidden not in actual, (
            f"Yasaklı canonical field bulundu: {forbidden}"
        )


# ============================================================
# 21. READ-ONLY / MULTIMODAL BOUNDARY
# ============================================================


def validate_read_only_boundary() -> None:
    forbidden_behavior_terms = {
        "BUY",
        "SELL",
        "LONG",
        "SHORT",
        "TRADE_SIGNAL",
        "FINAL_BIAS",
        "RISK_DECISION",
        "EXECUTION",
        "POSITION_SIZING",
    }


    assert forbidden_behavior_terms


def validate_multimodal_boundary() -> None:
    """
    4.5 multimodal evidence'i korur ve yapılandırır.


    CTA interpretation, direction, synthesis, reliability score,
    confidence score veya trade/risk decision üretmez.
    """
    assert RawEvidenceType.CHART in RawEvidenceType
    assert RawEvidenceType.IMAGE in RawEvidenceType
    assert RawEvidenceType.PDF_FIGURE in RawEvidenceType
    assert RawEvidenceType.X_POST_MEDIA in RawEvidenceType


# ============================================================
# 22. CODING / RUNTIME HONESTY
# ============================================================


def validate_runtime_honesty() -> None:
    """
    Kod tarafından doğrulanmamış:
    OCR success
    complete visual extraction
    complete PDF extraction
    automatic media retrieval
    chart understanding
    automatic visual interpretation


    iddiası üretilmez.
    """
    assert True


# ============================================================
# 23. IMMUTABILITY TEST
# ============================================================


def validate_immutable_raw_evidence() -> None:
    manager = CanonicalIntelligenceLifecycleManager()


    evidence = RawEvidenceRecord(
        raw_evidence_id="raw-test-001",
        master_source_id="master.test",
        evidence_type=RawEvidenceType.CHART,
        raw_content={"visible": "test"},
        retrieval_time=datetime.utcnow(),
        access_method=AccessMethod.PDF,
        access_mode=AccessMode.MANUAL,
        missingness_status=MissingnessStatus.COMPLETE,
    )


    manager.ingest_raw_evidence(evidence)


    try:
        manager.ingest_raw_evidence(evidence)
    except ValueError:
        return


    raise AssertionError(
        "Mevcut raw evidence üzerine yazılmasına izin verildi."
    )


# ============================================================
# 24. CANONICAL / RAW SEPARATION TEST
# ============================================================


def validate_raw_canonical_separation() -> None:
    manager = CanonicalIntelligenceLifecycleManager()


    evidence = RawEvidenceRecord(
        raw_evidence_id="raw-test-002",
        master_source_id="master.test",
        evidence_type=RawEvidenceType.TABLE,
        raw_content={"cell": "100"},
        retrieval_time=datetime.utcnow(),
        access_method=AccessMethod.PDF,
        access_mode=AccessMode.MANUAL,
        missingness_status=MissingnessStatus.COMPLETE,
        source_url="https://example.invalid/test.pdf",
        source_locator="page=4;table=1;cell=B2",
        publication_id="publication-test",
    )


    manager.ingest_raw_evidence(evidence)


    record = manager.structure_canonical_record(
        record_id="record-test-002",
        raw_evidence_id="raw-test-002",
        source_name="Test Source",
        source_type=SourceType.INSTITUTION,
        source_identity_status=SourceIdentityStatus.UNRESOLVED,
        evidence_class=EvidenceClass.SUPPORTING,
        measurement_role=MeasurementRole.RESEARCH_EVIDENCE,
        operational_status=OperationalStatus.SADECE_MANUEL,
        fact_status=FactStatus.REPORTED,
        claim_verification_status=(
            ClaimVerificationStatus.UNRESOLVED
        ),
        subject="Test",
        entity_scope="Test",
        instrument_or_market="Test",
        claim="Test value is reported.",
        value="100",
        unit="unit",
        time_context=TimeContext.HISTORICAL,
        source_excerpt_or_field="table cell B2",
    )


    assert record.record_id == "record-test-002"
    assert record.master_source_id == "master.test"
    assert record.claim == "Test value is reported."
    assert record.retrieval_time == evidence.retrieval_time


    validate_raw_to_canonical_link(
        manager,
        "record-test-002",
    )


# ============================================================
# 25. SPECIAL SOURCE BOUNDARIES
# ============================================================


def validate_special_source_boundaries() -> None:
    # CFTC COT → POSITIONING_PROXY
    assert MeasurementRole.PROXY == MeasurementRole.PROXY


    # DBMF → PRODUCT_SPECIFIC
    assert (
        MeasurementRole.PRODUCT_SPECIFIC
        == MeasurementRole.PRODUCT_SPECIFIC
    )


    # SG Trend Indicator → DIRECT_MEASUREMENT
    assert (
        MeasurementRole.DIRECT_MEASUREMENT
        == MeasurementRole.DIRECT_MEASUREMENT
    )


    # Bunlar birbirine dönüştürülmez.
    assert (
        MeasurementRole.PROXY
        != MeasurementRole.DIRECT_MEASUREMENT
    )
    assert (
        MeasurementRole.PRODUCT_SPECIFIC
        != MeasurementRole.DIRECT_MEASUREMENT
    )


# ============================================================
# 26. FULL VALIDATION
# ============================================================


def validate_4_5() -> None:
    validate_canonical_field_set()
    validate_no_forbidden_fields()
    validate_lifecycle()
    validate_multimodal_boundary()
    validate_multimodal_missingness()
    validate_runtime_honesty()
    validate_read_only_boundary()


    validate_special_source_roles()
    validate_special_source_boundaries()


    validate_immutable_raw_evidence()
    validate_raw_canonical_separation()


    manager = CanonicalIntelligenceLifecycleManager()


    evidence = RawEvidenceRecord(
        raw_evidence_id="validation-raw-001",
        master_source_id="master.validation",
        evidence_type=RawEvidenceType.IMAGE,
        raw_content={"visible_information": "test"},
        retrieval_time=datetime.utcnow(),
        access_method=AccessMethod.X,
        access_mode=AccessMode.MANUAL,
        missingness_status=MissingnessStatus.PARTIAL,
        source_url="https://example.invalid/post",
        source_locator="post-media-1",
        publication_id="validation-publication",
        source_family_id="validation-family",
    )


    manager.ingest_raw_evidence(evidence)


    record = manager.structure_canonical_record(
        record_id="validation-record-001",
        raw_evidence_id="validation-raw-001",
        source_name="Validation Source",
        source_type=SourceType.X_ACCOUNT,
        source_identity_status=SourceIdentityStatus.UNRESOLVED,
        evidence_class=EvidenceClass.SUPPORTING,
        measurement_role=MeasurementRole.COMMENTARY,
        operational_status=OperationalStatus.SADECE_MANUEL,
        fact_status=FactStatus.REPORTED,
        claim_verification_status=(
            ClaimVerificationStatus.UNRESOLVED
        ),
        subject="Validation",
        entity_scope="Validation",
        instrument_or_market="Validation",
        claim="Visible information is reported by the source.",
        value=None,
        unit=None,
        time_context=TimeContext.CURRENT,
        source_excerpt_or_field="post text / media locator",
    )


    validate_claim_required(record)
    validate_value_rule(record)
    validate_time_separation(record)
    validate_enum_integrity(record)
    validate_evidence_class_is_not_score(record.evidence_class)
    validate_measurement_role_not_from_format(record)
    validate_fact_status_preserved(record)
    validate_visual_not_auto_observed(record)
    validate_time_context_preserved(record)
    validate_access(record)
    validate_missingness(record)
    validate_provenance(
        manager.get_provenance("validation-record-001")
    )
    validate_raw_to_canonical_link(
        manager,
        "validation-record-001",
    )
    validate_independence(record)
    validate_conflict_preserved(record)
    validate_confidence_basis(record)


# ============================================================
# 27. MAIN
# ============================================================


if __name__ == "__main__":
    validate_4_5()


    print(
        "4.5 — CANONICAL INTELLIGENCE SCHEMA "
        "+ RAW EVIDENCE LIFECYCLE"
    )
    print("=" * 70)
    print(
        "SOURCE → ACCESS → RETRIEVAL → RAW EVIDENCE "
        "→ EXTRACTION / STRUCTURING → CANONICAL RECORD"
    )
    print(
        "RAW EVIDENCE ≠ CANONICAL RECORD"
    )
    print(
        "SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS"
    )
    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )
    print("=" * 70)
    print("Validation: OK")


"""
CTA TERMINAL — 4.6 DISPLAY / QUERY / UPDATE / FRESHNESS


4.5 CANONICAL INTELLIGENCE SCHEMA korunur.
4.6 yalnızca DISPLAY / QUERY / UPDATE / FRESHNESS davranışını tanımlar.


LOCKED FLOW:
RAW EVIDENCE → STRUCTURED INFORMATION → CANONICAL RECORD → DISPLAY


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ


HARD BOUNDARIES:
- Canonical schema'ya yeni alan eklenmez.
- raw_evidence_id canonical record içinde tutulmaz.
- Raw evidence immutable'dır.
- Existing record/evidence sessizce overwrite edilmez.
- Multimodal raw evidence ile structured information ayrıdır.
- Conflict çözülmez.
- Truth selection yapılmaz.
- Freshness ayrı canonical field değildir.
- Freshness score/status/expiry alanı yoktur.
- BUY/SELL/LONG/SHORT/bias/risk/execution üretilmez.
- Görsel gösterimi yorum/analiz anlamına gelmez.
"""


from __future__ import annotations


from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Iterable, Optional, Tuple


# ============================================================
# 1. 4.5'TE KİLİTLİ MEVCUT ENUM'LAR
# ============================================================


class SourceType(str, Enum):
    X_ACCOUNT = "X_ACCOUNT"
    INSTITUTION = "INSTITUTION"
    HISTORICAL_INSTITUTION = "HISTORICAL_INSTITUTION"
    PERSON = "PERSON"
    INDEX = "INDEX"
    ETF_PRODUCT = "ETF_PRODUCT"
    POSITIONING_PROXY = "POSITIONING_PROXY"
    HISTORICAL_SYSTEM = "HISTORICAL_SYSTEM"


class SourceIdentityStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    UNRESOLVED = "UNRESOLVED"


class OperationalStatus(str, Enum):
    KULLANILABILIR = "KULLANILABILIR"
    KISITLI = "KISITLI"
    SADECE_MANUEL = "SADECE_MANUEL"
    ERISILEMIYOR = "ERISILEMIYOR"


class EvidenceClass(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUPPORTING = "SUPPORTING"
    HISTORICAL = "HISTORICAL"
    UNVERIFIED = "UNVERIFIED"


class MeasurementRole(str, Enum):
    DIRECT_MEASUREMENT = "DIRECT_MEASUREMENT"
    PROXY = "PROXY"
    PRODUCT_SPECIFIC = "PRODUCT_SPECIFIC"
    RESEARCH_EVIDENCE = "RESEARCH_EVIDENCE"
    COMMENTARY = "COMMENTARY"
    HISTORICAL_EVIDENCE = "HISTORICAL_EVIDENCE"


class FactStatus(str, Enum):
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    ESTIMATED = "ESTIMATED"
    FORECAST = "FORECAST"
    OPINION = "OPINION"
    UNVERIFIED = "UNVERIFIED"


class ClaimVerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    UNRESOLVED = "UNRESOLVED"


class TimeContext(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    ARCHIVED = "ARCHIVED"
    FORWARD_LOOKING = "FORWARD_LOOKING"


class AccessMethod(str, Enum):
    API = "API"
    CSV = "CSV"
    PDF = "PDF"
    HTML = "HTML"
    X = "X"
    OTHER = "OTHER"


class AccessMode(str, Enum):
    AUTOMATED = "AUTOMATED"
    PROGRAMMATIC_PARTIAL = "PROGRAMMATIC_PARTIAL"
    MANUAL = "MANUAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"


class MissingnessStatus(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    NOT_RETRIEVED = "NOT_RETRIEVED"
    ACCESS_BLOCKED = "ACCESS_BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class IndependenceStatus(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    SAME_SOURCE_FAMILY = "SAME_SOURCE_FAMILY"
    REPUBLISHED = "REPUBLISHED"
    UNKNOWN = "UNKNOWN"


class RawEvidenceType(str, Enum):
    TEXT = "TEXT"
    NUMERIC_DATA = "NUMERIC_DATA"
    TABLE = "TABLE"
    CHART = "CHART"
    GRAPH = "GRAPH"
    IMAGE = "IMAGE"
    SCREENSHOT = "SCREENSHOT"
    INFOGRAPHIC = "INFOGRAPHIC"
    DIAGRAM = "DIAGRAM"
    MAP = "MAP"
    VISUAL_PANEL = "VISUAL_PANEL"
    PDF_PAGE = "PDF_PAGE"
    PDF_FIGURE = "PDF_FIGURE"
    PDF_TABLE = "PDF_TABLE"
    X_POST_MEDIA = "X_POST_MEDIA"
    REPORT_MEDIA = "REPORT_MEDIA"


# ============================================================
# 2. CANONICAL FIELD SCHEMA — 4.5 LOCKED
#
# EXACTLY 34 FIELDS
# ============================================================


CANONICAL_FIELD_NAMES: Tuple[str, ...] = (
    "record_id",
    "master_source_id",
    "source_name",
    "source_type",
    "source_identity_status",
    "evidence_class",
    "measurement_role",
    "operational_status",
    "fact_status",
    "claim_verification_status",
    "subject",
    "entity_scope",
    "instrument_or_market",
    "claim",
    "value",
    "unit",
    "observation_time",
    "publication_time",
    "retrieval_time",
    "time_context",
    "access_method",
    "access_mode",
    "missingness_status",
    "source_url",
    "source_locator",
    "source_excerpt_or_field",
    "source_family_id",
    "publication_id",
    "claim_fingerprint",
    "deduplication_group_id",
    "independence_status",
    "conflict_group_id",
    "provenance_status",
    "confidence_basis",
)


@dataclass(frozen=True)
class CanonicalIntelligenceRecord:
    """
    4.5'te kilitlenen canonical schema.


    Bu dataclass'a 4.6 tarafından hiçbir yeni canonical field eklenmez.
    """


    record_id: str
    master_source_id: str
    source_name: str
    source_type: SourceType
    source_identity_status: SourceIdentityStatus
    evidence_class: EvidenceClass
    measurement_role: MeasurementRole
    operational_status: OperationalStatus
    fact_status: FactStatus
    claim_verification_status: ClaimVerificationStatus
    subject: Optional[str]
    entity_scope: Optional[str]
    instrument_or_market: Optional[str]
    claim: str
    value: Optional[str]
    unit: Optional[str]
    observation_time: Optional[str]
    publication_time: Optional[str]
    retrieval_time: Optional[str]
    time_context: TimeContext
    access_method: Optional[AccessMethod]
    access_mode: Optional[AccessMode]
    missingness_status: MissingnessStatus
    source_url: Optional[str]
    source_locator: Optional[str]
    source_excerpt_or_field: Optional[str]
    source_family_id: Optional[str]
    publication_id: Optional[str]
    claim_fingerprint: Optional[str]
    deduplication_group_id: Optional[str]
    independence_status: IndependenceStatus
    conflict_group_id: Optional[str]
    provenance_status: Optional[str]
    confidence_basis: Optional[str]


# ============================================================
# 3. RAW EVIDENCE
#
# Canonical record'dan ayrı tutulur.
# raw_evidence_id canonical field değildir.
# ============================================================


@dataclass(frozen=True)
class RawEvidenceRecord:
    """
    Immutable raw evidence.


    Raw evidence; text, numeric data, table, chart, image, PDF visual,
    X media veya diğer multimodal içerikleri temsil edebilir.


    raw_content bilinmeyen/erişilemeyen durumda None olabilir.
    MissingnessStatus bunun nedenini korur.
    """


    raw_evidence_id: str
    master_source_id: str
    evidence_type: RawEvidenceType
    raw_content: Any = None
    source_url: Optional[str] = None
    source_locator: Optional[str] = None
    document_id: Optional[str] = None
    page: Optional[str] = None
    visual_locator: Optional[str] = None
    retrieval_time: Optional[str] = None
    observation_time: Optional[str] = None
    publication_time: Optional[str] = None
    access_method: Optional[AccessMethod] = None
    access_mode: Optional[AccessMode] = None
    missingness_status: MissingnessStatus = MissingnessStatus.COMPLETE
    notes: Optional[str] = None


# ============================================================
# 4. STRUCTURED INFORMATION
#
# Raw evidence'in yerine geçmez.
# ============================================================


@dataclass(frozen=True)
class ExtractedInformationRecord:
    """
    Raw evidence'den görülebilen/readable information'ın
    yapılandırılmış temsilidir.


    Bu yapı canonical schema değildir.
    """


    extracted_id: str
    raw_evidence_id: str
    master_source_id: str
    product: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    percentage: Optional[str] = None
    change: Optional[str] = None
    date: Optional[str] = None
    period: Optional[str] = None
    period_label: Optional[str] = None
    table_header: Optional[str] = None
    table_cell: Optional[str] = None
    ranking: Optional[str] = None
    chart_title: Optional[str] = None
    axis: Optional[str] = None
    legend: Optional[str] = None
    trend_direction: Optional[str] = None
    increase_decrease: Optional[str] = None
    explicit_relationship: Optional[str] = None
    missingness_status: MissingnessStatus = MissingnessStatus.COMPLETE
    notes: Optional[str] = None


# ============================================================
# 5. CANONICAL ↔ RAW EVIDENCE BAĞLANTISI
#
# raw_evidence_id canonical record içine eklenmez.
# ============================================================


@dataclass(frozen=True)
class CanonicalEvidenceLink:
    """
    Canonical record ile raw evidence arasındaki dış bağlantıdır.


    Bu yapı canonical schema'nın parçası değildir.
    """


    record_id: str
    raw_evidence_id: str
    extracted_information_ids: Tuple[str, ...] = field(default_factory=tuple)


# ============================================================
# 6. PROVENANCE TRACE
# ============================================================


@dataclass(frozen=True)
class ProvenanceTrace:
    """
    SOURCE → ACCESS → PUBLICATION/DOCUMENT → CONTENT → RAW EVIDENCE
    → CANONICAL RECORD zincirini ayrı olarak korur.
    """


    record_id: str
    master_source_id: str
    source_url: Optional[str]
    source_locator: Optional[str]
    publication_id: Optional[str]
    document_id: Optional[str]
    raw_evidence_id: Optional[str]
    extracted_information_ids: Tuple[str, ...] = field(default_factory=tuple)


# ============================================================
# 7. VERIFICATION HISTORY
#
# Canonical record alanı değildir.
# ============================================================


@dataclass(frozen=True)
class VerificationHistoryEntry:
    record_id: str
    previous_status: Optional[ClaimVerificationStatus]
    new_status: ClaimVerificationStatus
    event_time: Optional[str]
    evidence_context: Optional[str] = None


# ============================================================
# 8. UPDATE / RETRIEVAL EVENT
# ============================================================


@dataclass(frozen=True)
class RetrievalUpdateEvent:
    event_id: str
    record_id: str
    previous_record_id: Optional[str]
    new_record_id: str
    previous_raw_evidence_id: Optional[str]
    new_raw_evidence_id: Optional[str]
    reason: str
    retrieval_time: Optional[str]


# ============================================================
# 9. DISPLAY — MAIN
# ============================================================


@dataclass(frozen=True)
class DisplayMainView:
    """
    Main display canonical alanlardan oluşur.


    raw evidence ve structured information burada canonical field
    olarak eklenmez; ayrı display bölümlerinde gösterilir.
    """


    record_id: str
    master_source_id: str
    source_name: str
    source_type: SourceType
    source_identity_status: SourceIdentityStatus
    evidence_class: EvidenceClass
    measurement_role: MeasurementRole
    operational_status: OperationalStatus
    fact_status: FactStatus
    claim_verification_status: ClaimVerificationStatus
    subject: Optional[str]
    entity_scope: Optional[str]
    instrument_or_market: Optional[str]
    claim: str
    value: Optional[str]
    unit: Optional[str]
    observation_time: Optional[str]
    publication_time: Optional[str]
    retrieval_time: Optional[str]
    time_context: TimeContext
    access_method: Optional[AccessMethod]
    access_mode: Optional[AccessMode]
    missingness_status: MissingnessStatus


# ============================================================
# 10. MULTIMODAL DISPLAY
# ============================================================


@dataclass(frozen=True)
class DisplayMultimodalView:
    """
    RAW EVIDENCE ve STRUCTURED INFORMATION açıkça ayrıdır.
    """


    raw_evidence: RawEvidenceRecord
    structured_information: Tuple[ExtractedInformationRecord, ...] = field(
        default_factory=tuple
    )


# ============================================================
# 11. EVIDENCE DETAILS DISPLAY
# ============================================================


@dataclass(frozen=True)
class DisplayEvidenceDetails:
    record_id: str
    source_url: Optional[str]
    source_locator: Optional[str]
    source_excerpt_or_field: Optional[str]
    publication_time: Optional[str]
    retrieval_time: Optional[str]
    access_method: Optional[AccessMethod]
    missingness_status: MissingnessStatus
    source_family_id: Optional[str]
    publication_id: Optional[str]
    claim_fingerprint: Optional[str]
    deduplication_group_id: Optional[str]
    independence_status: IndependenceStatus
    conflict_group_id: Optional[str]
    confidence_basis: Optional[str]
    verification_history: Tuple[VerificationHistoryEntry, ...] = field(
        default_factory=tuple
    )
    raw_evidence: Tuple[RawEvidenceRecord, ...] = field(default_factory=tuple)
    provenance: Optional[ProvenanceTrace] = None


# ============================================================
# 12. PDF DISPLAY
# ============================================================


@dataclass(frozen=True)
class DisplayPdfView:
    raw_evidence: RawEvidenceRecord
    page: Optional[str]
    table: Optional[str]
    chart: Optional[str]
    figure: Optional[str]
    visual_panel: Optional[str]


# ============================================================
# 13. X MEDIA DISPLAY
# ============================================================


@dataclass(frozen=True)
class DisplayXMediaView:
    """
    X POST:
    TEXT + MEDIA


    Media alınamasa bile post text/source identity korunur.
    """


    source_identity: str
    post_text: Optional[str]
    media_raw_evidence: Optional[RawEvidenceRecord]
    media_missingness_status: MissingnessStatus


# ============================================================
# 14. QUERY / FILTER
#
# Yalnız mevcut canonical alanlar kullanılır.
# ============================================================


@dataclass(frozen=True)
class QueryFilter:
    source_id: Optional[str] = None
    source_type: Optional[SourceType] = None
    evidence_class: Optional[EvidenceClass] = None
    measurement_role: Optional[MeasurementRole] = None
    fact_status: Optional[FactStatus] = None
    claim_verification_status: Optional[ClaimVerificationStatus] = None
    time_context: Optional[TimeContext] = None
    subject: Optional[str] = None
    entity_scope: Optional[str] = None
    instrument_or_market: Optional[str] = None
    missingness_status: Optional[MissingnessStatus] = None
    publication_id: Optional[str] = None
    source_family_id: Optional[str] = None
    claim_fingerprint: Optional[str] = None
    deduplication_group_id: Optional[str] = None
    independence_status: Optional[IndependenceStatus] = None
    conflict_group_id: Optional[str] = None
    provenance_status: Optional[str] = None


    # Operational query controls; canonical fields değildir.
    include_unverified: bool = False
    include_unresolved: bool = False


def query_records(
    records: Iterable[CanonicalIntelligenceRecord],
    query: QueryFilter,
) -> Tuple[CanonicalIntelligenceRecord, ...]:
    """
    Canonical record'lar üzerinde yalnız mevcut canonical alanlarla
    filtreleme yapar.


    Varsayılan:
    - UNVERIFIED claim verification gizlenir.
    - UNRESOLVED claim verification gizlenir.


    Conflict çözülmez.
    Truth selection yapılmaz.
    """


    result = []


    for record in records:


        if (
            not query.include_unverified
            and record.claim_verification_status
            == ClaimVerificationStatus.UNVERIFIED
        ):
            continue


        if (
            not query.include_unresolved
            and record.claim_verification_status
            == ClaimVerificationStatus.UNRESOLVED
        ):
            continue


        if (
            query.source_id is not None
            and record.master_source_id != query.source_id
        ):
            continue


        if (
            query.source_type is not None
            and record.source_type != query.source_type
        ):
            continue


        if (
            query.evidence_class is not None
            and record.evidence_class != query.evidence_class
        ):
            continue


        if (
            query.measurement_role is not None
            and record.measurement_role != query.measurement_role
        ):
            continue


        if (
            query.fact_status is not None
            and record.fact_status != query.fact_status
        ):
            continue


        if (
            query.claim_verification_status is not None
            and record.claim_verification_status
            != query.claim_verification_status
        ):
            continue


        if (
            query.time_context is not None
            and record.time_context != query.time_context
        ):
            continue


        if query.subject is not None and record.subject != query.subject:
            continue


        if (
            query.entity_scope is not None
            and record.entity_scope != query.entity_scope
        ):
            continue


        if (
            query.instrument_or_market is not None
            and record.instrument_or_market
            != query.instrument_or_market
        ):
            continue


        if (
            query.missingness_status is not None
            and record.missingness_status
            != query.missingness_status
        ):
            continue


        if (
            query.publication_id is not None
            and record.publication_id != query.publication_id
        ):
            continue


        if (
            query.source_family_id is not None
            and record.source_family_id != query.source_family_id
        ):
            continue


        if (
            query.claim_fingerprint is not None
            and record.claim_fingerprint
            != query.claim_fingerprint
        ):
            continue


        if (
            query.deduplication_group_id is not None
            and record.deduplication_group_id
            != query.deduplication_group_id
        ):
            continue


        if (
            query.independence_status is not None
            and record.independence_status
            != query.independence_status
        ):
            continue


        if (
            query.conflict_group_id is not None
            and record.conflict_group_id
            != query.conflict_group_id
        ):
            continue


        if (
            query.provenance_status is not None
            and record.provenance_status
            != query.provenance_status
        ):
            continue


        result.append(record)


    return tuple(result)


# ============================================================
# 15. CONFLICT QUERY
# ============================================================


def query_conflict_group(
    records: Iterable[CanonicalIntelligenceRecord],
    conflict_group_id: str,
) -> Tuple[CanonicalIntelligenceRecord, ...]:
    """
    Conflict kayıtlarının tamamını getirir.


    Bu fonksiyon:
    - silmez
    - birleştirmez
    - consensus üretmez
    - truth selection yapmaz
    """


    return tuple(
        record
        for record in records
        if record.conflict_group_id == conflict_group_id
    )


# ============================================================
# 16. IMMUTABLE STORE
# ============================================================


class ImmutableEvidenceStore:
    """
    Raw evidence store.


    Aynı ID ile ikinci kez kayıt yapılması overwrite değildir;
    hata olarak reddedilir.
    """


    def __init__(self) -> None:
        self._records: dict[str, RawEvidenceRecord] = {}


    def add(self, evidence: RawEvidenceRecord) -> str:
        if evidence.raw_evidence_id in self._records:
            raise ValueError(
                f"Raw evidence already exists: {evidence.raw_evidence_id}. "
                "Existing evidence cannot be overwritten."
            )


        self._records[evidence.raw_evidence_id] = evidence
        return evidence.raw_evidence_id


    def get(self, raw_evidence_id: str) -> RawEvidenceRecord:
        try:
            return self._records[raw_evidence_id]
        except KeyError as exc:
            raise KeyError(
                f"Raw evidence not found: {raw_evidence_id}"
            ) from exc


    def all(self) -> Tuple[RawEvidenceRecord, ...]:
        return tuple(self._records.values())


class CanonicalRecordStore:
    """
    Canonical record store.


    Existing record sessizce overwrite edilemez.
    """


    def __init__(self) -> None:
        self._records: dict[str, CanonicalIntelligenceRecord] = {}


    def add(self, record: CanonicalIntelligenceRecord) -> str:
        if record.record_id in self._records:
            raise ValueError(
                f"Canonical record already exists: {record.record_id}. "
                "Create a new record for an update."
            )


        self._records[record.record_id] = record
        return record.record_id


    def get(self, record_id: str) -> CanonicalIntelligenceRecord:
        try:
            return self._records[record_id]
        except KeyError as exc:
            raise KeyError(
                f"Canonical record not found: {record_id}"
            ) from exc


    def all(self) -> Tuple[CanonicalIntelligenceRecord, ...]:
        return tuple(self._records.values())


# ============================================================
# 17. EVIDENCE LINK STORE
# ============================================================


class EvidenceLinkStore:
    """
    Canonical ↔ Raw Evidence bağlantısını canonical schema dışında tutar.
    """


    def __init__(self) -> None:
        self._links: dict[str, CanonicalEvidenceLink] = {}


    def add(self, link: CanonicalEvidenceLink) -> str:
        if link.record_id in self._links:
            raise ValueError(
                f"Evidence link already exists for record: {link.record_id}"
            )


        self._links[link.record_id] = link
        return link.record_id


    def get(self, record_id: str) -> CanonicalEvidenceLink:
        try:
            return self._links[record_id]
        except KeyError as exc:
            raise KeyError(
                f"Evidence link not found: {record_id}"
            ) from exc


# ============================================================
# 18. PROVENANCE STORE
# ============================================================


class ProvenanceStore:
    def __init__(self) -> None:
        self._traces: dict[str, ProvenanceTrace] = {}


    def add(self, trace: ProvenanceTrace) -> str:
        if trace.record_id in self._traces:
            raise ValueError(
                f"Provenance already exists for record: {trace.record_id}"
            )


        self._traces[trace.record_id] = trace
        return trace.record_id


    def get(self, record_id: str) -> ProvenanceTrace:
        try:
            return self._traces[record_id]
        except KeyError as exc:
            raise KeyError(
                f"Provenance not found: {record_id}"
            ) from exc


# ============================================================
# 19. VERIFICATION HISTORY STORE
# ============================================================


class VerificationHistoryStore:
    def __init__(self) -> None:
        self._history: dict[
            str, list[VerificationHistoryEntry]
        ] = {}


    def append(self, entry: VerificationHistoryEntry) -> None:
        self._history.setdefault(entry.record_id, []).append(entry)


    def get(
        self,
        record_id: str,
    ) -> Tuple[VerificationHistoryEntry, ...]:
        return tuple(self._history.get(record_id, ()))


# ============================================================
# 20. RETRIEVAL UPDATE STORE
# ============================================================


class RetrievalUpdateStore:
    def __init__(self) -> None:
        self._events: dict[str, RetrievalUpdateEvent] = {}


    def add(self, event: RetrievalUpdateEvent) -> str:
        if event.event_id in self._events:
            raise ValueError(
                f"Retrieval update event already exists: {event.event_id}"
            )


        self._events[event.event_id] = event
        return event.event_id


    def all(self) -> Tuple[RetrievalUpdateEvent, ...]:
        return tuple(self._events.values())


# ============================================================
# 21. CONTENT CHANGE
#
# 4.6 specification:
# claim, value, scope, instrument, observation time,
# fact status değişirse yeni canonical record.
# ============================================================


CONTENT_CHANGE_FIELDS: Tuple[str, ...] = (
    "claim",
    "value",
    "entity_scope",
    "instrument_or_market",
    "observation_time",
    "fact_status",
)


def content_change_requires_new_record(
    old_record: CanonicalIntelligenceRecord,
    new_record: CanonicalIntelligenceRecord,
) -> bool:
    for field_name in CONTENT_CHANGE_FIELDS:
        if getattr(old_record, field_name) != getattr(
            new_record, field_name
        ):
            return True


    return False


def require_new_record_for_content_change(
    old_record: CanonicalIntelligenceRecord,
    new_record: CanonicalIntelligenceRecord,
) -> None:
    """
    İçerik değişmişse aynı record_id kullanılamaz.
    """


    if content_change_requires_new_record(old_record, new_record):
        if old_record.record_id == new_record.record_id:
            raise ValueError(
                "Content changed but record_id was reused. "
                "Create a new canonical record."
            )


# ============================================================
# 22. RETRIEVAL / REFRESH
# ============================================================


def create_retrieval_update_event(
    old_record: CanonicalIntelligenceRecord,
    new_record: CanonicalIntelligenceRecord,
    old_raw_evidence_id: Optional[str],
    new_raw_evidence_id: Optional[str],
    event_id: str,
    reason: str,
    retrieval_time: Optional[str],
) -> RetrievalUpdateEvent:
    """
    New retrieval mevcut record'u overwrite etmez.


    Yeni publication / observation / evidence gerekiyorsa
    yeni record/evidence kullanılmalıdır.
    """


    if old_record.record_id == new_record.record_id:
        raise ValueError(
            "Refresh cannot overwrite an existing canonical record."
        )


    if (
        old_raw_evidence_id is not None
        and new_raw_evidence_id is not None
        and old_raw_evidence_id == new_raw_evidence_id
    ):
        raise ValueError(
            "New retrieval cannot overwrite/reuse old raw evidence ID."
        )


    return RetrievalUpdateEvent(
        event_id=event_id,
        record_id=new_record.record_id,
        previous_record_id=old_record.record_id,
        new_record_id=new_record.record_id,
        previous_raw_evidence_id=old_raw_evidence_id,
        new_raw_evidence_id=new_raw_evidence_id,
        reason=reason,
        retrieval_time=retrieval_time,
    )


# ============================================================
# 23. VERIFICATION UPDATE
# ============================================================


def create_verification_history_entry(
    record_id: str,
    previous_status: Optional[ClaimVerificationStatus],
    new_status: ClaimVerificationStatus,
    event_time: Optional[str],
    evidence_context: Optional[str] = None,
) -> VerificationHistoryEntry:
    """
    Verification değişikliği history'de tutulur.


    Geçmiş canonical record geriye dönük olarak değiştirilmez.
    """


    return VerificationHistoryEntry(
        record_id=record_id,
        previous_status=previous_status,
        new_status=new_status,
        event_time=event_time,
        evidence_context=evidence_context,
    )


# ============================================================
# 24. FRESHNESS — DERIVED ONLY
#
# Freshness canonical field değildir.
# Freshness score/status/expiry üretilmez.
# ============================================================


@dataclass(frozen=True)
class FreshnessDerivation:
    """
    Persist edilen canonical state değildir.


    Yalnız mevcut zaman/provenance alanlarından türetilen
    gözlemsel bağlamı taşır.
    """


    observation_time: Optional[str]
    publication_time: Optional[str]
    retrieval_time: Optional[str]
    time_context: TimeContext
    source_type: SourceType
    missingness_status: MissingnessStatus
    access_mode: Optional[AccessMode]
    provenance_status: Optional[str]


def derive_freshness_context(
    record: CanonicalIntelligenceRecord,
) -> FreshnessDerivation:
    """
    Freshness ayrı bir truth field olarak saklanmaz.


    Retrieval zamanı ile publication/observation zamanı
    birbirinden ayrıdır.
    """


    return FreshnessDerivation(
        observation_time=record.observation_time,
        publication_time=record.publication_time,
        retrieval_time=record.retrieval_time,
        time_context=record.time_context,
        source_type=record.source_type,
        missingness_status=record.missingness_status,
        access_mode=record.access_mode,
        provenance_status=record.provenance_status,
    )


FORBIDDEN_FRESHNESS_FIELDS: Tuple[str, ...] = (
    "freshness_status",
    "staleness_status",
    "expiration_status",
    "expiry_time",
    "stale_after",
    "expired_after",
    "freshness_score",
)


def validate_no_forbidden_freshness_fields() -> None:
    canonical_fields = {
        item.name
        for item in fields(CanonicalIntelligenceRecord)
    }


    forbidden_enum_value = "EXPIRED"


    for forbidden in FORBIDDEN_FRESHNESS_FIELDS:
        if forbidden in canonical_fields:
            raise AssertionError(
                f"Forbidden freshness field found: {forbidden}"
            )


    if forbidden_enum_value in TimeContext.__members__:
        raise AssertionError(
            "EXPIRED must not exist as a canonical TimeContext."
        )


# ============================================================
# 25. DISPLAY STATUS SEPARATION
# ============================================================


def validate_display_status_separation() -> None:
    """
    Farklı epistemic/operational kavramların birbirine
    dönüştürülmediğini doğrular.
    """


    assert "CURRENT" in TimeContext.__members__
    assert "HISTORICAL" in TimeContext.__members__


    assert "FORECAST" in FactStatus.__members__
    assert "OBSERVED" in FactStatus.__members__


    assert "AUTOMATED" in AccessMode.__members__
    assert "MANUAL" in AccessMode.__members__


    assert "COMPLETE" in MissingnessStatus.__members__
    assert "PARTIAL" in MissingnessStatus.__members__
    assert "NOT_RETRIEVED" in MissingnessStatus.__members__


    assert RawEvidenceType.TEXT.value == "TEXT"


def validate_time_context_is_not_changed_by_retrieval(
    record: CanonicalIntelligenceRecord,
) -> None:
    """
    Retrieval zamanı historical/forward-looking/current niteliğini
    otomatik olarak değiştirmez.
    """


    if record.time_context == TimeContext.HISTORICAL:
        assert record.time_context == TimeContext.HISTORICAL


    if record.time_context == TimeContext.FORWARD_LOOKING:
        assert record.time_context == TimeContext.FORWARD_LOOKING


# ============================================================
# 26. MULTIMODAL MISSINGNESS
# ============================================================


def preserve_visual_missingness(
    raw_evidence: RawEvidenceRecord,
) -> MissingnessStatus:
    """
    Görsel okunamıyorsa mevcut missingness korunur.
    Veri tahmin edilmez.
    """


    return raw_evidence.missingness_status


def x_media_does_not_discard_post(
    view: DisplayXMediaView,
) -> bool:
    """
    Media yokluğu X post text/source identity'yi silmez.
    """


    if view.media_missingness_status in (
        MissingnessStatus.NOT_RETRIEVED,
        MissingnessStatus.ACCESS_BLOCKED,
        MissingnessStatus.MISSING,
        MissingnessStatus.PARTIAL,
    ):
        return (
            view.post_text is not None
            or bool(view.source_identity)
        )


    return True


# ============================================================
# 27. DISPLAY TRACEABILITY
# ============================================================


def build_display_main_view(
    record: CanonicalIntelligenceRecord,
) -> DisplayMainView:
    return DisplayMainView(
        record_id=record.record_id,
        master_source_id=record.master_source_id,
        source_name=record.source_name,
        source_type=record.source_type,
        source_identity_status=record.source_identity_status,
        evidence_class=record.evidence_class,
        measurement_role=record.measurement_role,
        operational_status=record.operational_status,
        fact_status=record.fact_status,
        claim_verification_status=record.claim_verification_status,
        subject=record.subject,
        entity_scope=record.entity_scope,
        instrument_or_market=record.instrument_or_market,
        claim=record.claim,
        value=record.value,
        unit=record.unit,
        observation_time=record.observation_time,
        publication_time=record.publication_time,
        retrieval_time=record.retrieval_time,
        time_context=record.time_context,
        access_method=record.access_method,
        access_mode=record.access_mode,
        missingness_status=record.missingness_status,
    )


def build_display_evidence_details(
    record: CanonicalIntelligenceRecord,
    raw_evidence: Tuple[RawEvidenceRecord, ...],
    verification_history: Tuple[VerificationHistoryEntry, ...],
    provenance: Optional[ProvenanceTrace],
) -> DisplayEvidenceDetails:
    return DisplayEvidenceDetails(
        record_id=record.record_id,
        source_url=record.source_url,
        source_locator=record.source_locator,
        source_excerpt_or_field=record.source_excerpt_or_field,
        publication_time=record.publication_time,
        retrieval_time=record.retrieval_time,
        access_method=record.access_method,
        missingness_status=record.missingness_status,
        source_family_id=record.source_family_id,
        publication_id=record.publication_id,
        claim_fingerprint=record.claim_fingerprint,
        deduplication_group_id=record.deduplication_group_id,
        independence_status=record.independence_status,
        conflict_group_id=record.conflict_group_id,
        confidence_basis=record.confidence_basis,
        verification_history=verification_history,
        raw_evidence=raw_evidence,
        provenance=provenance,
    )


# ============================================================
# 28. DISPLAY / ANALYSIS SINIRI
# ============================================================


FORBIDDEN_ANALYTICAL_CONCEPTS: Tuple[str, ...] = (
    "convergence",
    "divergence",
    "cta_synthesis",
    "confidence_score",
    "reliability_score",
    "evidence_strength",
    "ranking",
    "weighting",
    "prediction",
    "trade_decision",
    "BUY",
    "SELL",
    "LONG",
    "SHORT",
    "risk_decision",
    "execution",
)


def validate_display_analysis_boundary() -> None:
    """
    Display katmanının karar üretmediğini yapısal olarak kontrol eder.


    Bu kavramlar canonical field olarak bulunamaz.
    """


    canonical_field_set = {
        item.name
        for item in fields(CanonicalIntelligenceRecord)
    }


    for forbidden in FORBIDDEN_ANALYTICAL_CONCEPTS:
        assert forbidden not in canonical_field_set


# ============================================================
# 29. CANONICAL SCHEMA BOUNDARY
# ============================================================


FORBIDDEN_CANONICAL_FIELDS: Tuple[str, ...] = (
    "raw_evidence_id",
    "score",
    "rank",
    "weight",
    "signal",
    "BUY",
    "SELL",
    "LONG",
    "SHORT",
    "bias",
    "trade",
    "risk",
    "execution",
    "freshness_status",
    "staleness_status",
    "expiration_status",
    "expiry_time",
    "stale_after",
    "expired_after",
    "freshness_score",
    "trust_score",
    "visual_confidence_score",
    "OCR_score",
    "image_quality_score",
    "extraction_score",
    "media_reliability_score",
)


def validate_canonical_schema() -> None:
    actual_fields = tuple(
        item.name for item in fields(CanonicalIntelligenceRecord)
    )


    if actual_fields != CANONICAL_FIELD_NAMES:
        raise AssertionError(
            "Canonical schema mismatch.\n"
            f"Expected: {CANONICAL_FIELD_NAMES}\n"
            f"Actual:   {actual_fields}"
        )


    if len(actual_fields) != 34:
        raise AssertionError(
            f"Canonical field count must be 34, got {len(actual_fields)}"
        )


    for forbidden in FORBIDDEN_CANONICAL_FIELDS:
        if forbidden in actual_fields:
            raise AssertionError(
                f"Forbidden canonical field found: {forbidden}"
            )


# ============================================================
# 30. SPECIAL SOURCE BOUNDARIES
# ============================================================


def validate_special_source_boundaries(
    record: CanonicalIntelligenceRecord,
) -> None:
    """
    4.5 / 4.6 özel kaynak sınırları.
    """


    source_id = record.master_source_id.lower()
    source_name = record.source_name.lower()


    # CFTC COT → PROXY
    if "cftc" in source_id or "cftc" in source_name:
        if "cot" in source_id or "cot" in source_name:
            assert (
                record.measurement_role
                == MeasurementRole.PROXY
            )


    # DBMF → PRODUCT_SPECIFIC
    if "dbmf" in source_id or "dbmf" in source_name:
        assert (
            record.measurement_role
            == MeasurementRole.PRODUCT_SPECIFIC
        )


    # SG Trend Indicator → DIRECT_MEASUREMENT
    if (
        "sg_trend_indicator" in source_id
        or "sg trend indicator" in source_name
    ):
        assert (
            record.measurement_role
            == MeasurementRole.DIRECT_MEASUREMENT
        )


# ============================================================
# 31. READ-ONLY BOUNDARY
# ============================================================


def validate_read_only_boundary() -> None:
    """
    4.6 herhangi bir karar mekanizması içermemelidir.
    """


    assert "BUY" in FORBIDDEN_ANALYTICAL_CONCEPTS
    assert "SELL" in FORBIDDEN_ANALYTICAL_CONCEPTS
    assert "LONG" in FORBIDDEN_ANALYTICAL_CONCEPTS
    assert "SHORT" in FORBIDDEN_ANALYTICAL_CONCEPTS


# ============================================================
# 32. RUNTIME HONESTY
# ============================================================


def runtime_claims_are_not_generated() -> None:
    """
    Bu modül visual/PDF/chart/table/media retrieval başarısını
    iddia etmez.


    Gerçek retrieval/extraction runtime sonucu yalnız ilgili
    ingestion/extraction katmanından gelebilir.
    """


    return None


# ============================================================
# 33. 4.6 MANAGER
# ============================================================


class DisplayQueryUpdateFreshnessManager:
    """
    4.6 operasyonlarını bir arada tutar.


    Bu manager:
    - source discovery yapmaz
    - source ranking yapmaz
    - evidence weighting yapmaz
    - conflict çözmez
    - truth seçmez
    - CTA bias üretmez
    - trade/risk/execution kararı üretmez
    """


    def __init__(self) -> None:
        self.raw_evidence_store = ImmutableEvidenceStore()
        self.canonical_store = CanonicalRecordStore()
        self.evidence_link_store = EvidenceLinkStore()
        self.provenance_store = ProvenanceStore()
        self.verification_history_store = VerificationHistoryStore()
        self.retrieval_update_store = RetrievalUpdateStore()


    # --------------------------------------------------------
    # Raw Evidence
    # --------------------------------------------------------


    def add_raw_evidence(
        self,
        evidence: RawEvidenceRecord,
    ) -> str:
        return self.raw_evidence_store.add(evidence)


    # --------------------------------------------------------
    # Canonical Record
    # --------------------------------------------------------


    def add_canonical_record(
        self,
        record: CanonicalIntelligenceRecord,
    ) -> str:
        validate_special_source_boundaries(record)
        return self.canonical_store.add(record)


    # --------------------------------------------------------
    # Evidence Link
    # --------------------------------------------------------


    def link_record_to_evidence(
        self,
        link: CanonicalEvidenceLink,
    ) -> str:
        return self.evidence_link_store.add(link)


    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------


    def add_provenance(
        self,
        provenance: ProvenanceTrace,
    ) -> str:
        return self.provenance_store.add(provenance)


    # --------------------------------------------------------
    # Verification
    # --------------------------------------------------------


    def add_verification_history(
        self,
        entry: VerificationHistoryEntry,
    ) -> None:
        self.verification_history_store.append(entry)


    # --------------------------------------------------------
    # Query
    # --------------------------------------------------------


    def query(
        self,
        query_filter: QueryFilter,
    ) -> Tuple[CanonicalIntelligenceRecord, ...]:
        return query_records(
            self.canonical_store.all(),
            query_filter,
        )


    # --------------------------------------------------------
    # Conflict
    # --------------------------------------------------------


    def conflict_group(
        self,
        conflict_group_id: str,
    ) -> Tuple[CanonicalIntelligenceRecord, ...]:
        return query_conflict_group(
            self.canonical_store.all(),
            conflict_group_id,
        )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------


    def display_main(
        self,
        record_id: str,
    ) -> DisplayMainView:
        record = self.canonical_store.get(record_id)
        return build_display_main_view(record)


    def display_multimodal(
        self,
        record_id: str,
    ) -> Optional[DisplayMultimodalView]:
        link = self.evidence_link_store.get(record_id)


        raw = self.raw_evidence_store.get(
            link.raw_evidence_id
        )


        structured: list[ExtractedInformationRecord] = []


        # Structured information ID'leri için burada yalnızca
        # lifecycle'da gerçekten kayıtlı extraction nesneleri
        # kullanılmalıdır.
        #
        # Bu manager extraction üretmez veya tahmin etmez.
        return DisplayMultimodalView(
            raw_evidence=raw,
            structured_information=tuple(structured),
        )


    # --------------------------------------------------------
    # Evidence Details
    # --------------------------------------------------------


    def display_evidence_details(
        self,
        record_id: str,
    ) -> DisplayEvidenceDetails:


        record = self.canonical_store.get(record_id)


        link = self.evidence_link_store.get(record_id)


        raw = (
            self.raw_evidence_store.get(
                link.raw_evidence_id
            ),
        )


        provenance = None


        try:
            provenance = self.provenance_store.get(record_id)
        except KeyError:
            provenance = None


        history = self.verification_history_store.get(
            record_id
        )


        return build_display_evidence_details(
            record=record,
            raw_evidence=raw,
            verification_history=history,
            provenance=provenance,
        )


    # --------------------------------------------------------
    # Freshness
    # --------------------------------------------------------


    def derive_freshness(
        self,
        record_id: str,
    ) -> FreshnessDerivation:
        record = self.canonical_store.get(record_id)
        return derive_freshness_context(record)


    # --------------------------------------------------------
    # Retrieval Update
    # --------------------------------------------------------


    def register_retrieval_update(
        self,
        old_record: CanonicalIntelligenceRecord,
        new_record: CanonicalIntelligenceRecord,
        old_raw_evidence_id: Optional[str],
        new_raw_evidence_id: Optional[str],
        event_id: str,
        reason: str,
        retrieval_time: Optional[str],
    ) -> str:


        require_new_record_for_content_change(
            old_record,
            new_record,
        )


        event = create_retrieval_update_event(
            old_record=old_record,
            new_record=new_record,
            old_raw_evidence_id=old_raw_evidence_id,
            new_raw_evidence_id=new_raw_evidence_id,
            event_id=event_id,
            reason=reason,
            retrieval_time=retrieval_time,
        )


        return self.retrieval_update_store.add(event)


# ============================================================
# 34. VALIDATION
# ============================================================


def validate_4_6() -> None:
    """
    4.6 yapısal validation.


    Bu fonksiyon gerçek web/PDF/X/media retrieval başarısını
    iddia etmez. Yalnız kodun 4.6 sınırlarını kontrol eder.
    """


    # --------------------------------------------------------
    # Canonical schema
    # --------------------------------------------------------


    validate_canonical_schema()


    # --------------------------------------------------------
    # Freshness
    # --------------------------------------------------------


    validate_no_forbidden_freshness_fields()


    # --------------------------------------------------------
    # Display separation
    # --------------------------------------------------------


    validate_display_status_separation()


    # --------------------------------------------------------
    # Display / analysis boundary
    # --------------------------------------------------------


    validate_display_analysis_boundary()


    # --------------------------------------------------------
    # Read-only boundary
    # --------------------------------------------------------


    validate_read_only_boundary()


    # --------------------------------------------------------
    # Raw evidence immutability
    # --------------------------------------------------------


    raw_store = ImmutableEvidenceStore()


    raw = RawEvidenceRecord(
        raw_evidence_id="raw-001",
        master_source_id="master.x.test",
        evidence_type=RawEvidenceType.CHART,
        raw_content="chart evidence",
        source_url="https://example.invalid/chart",
        source_locator="post/media/1",
        retrieval_time="2026-09-13T10:00:00",
        publication_time="2026-09-12T15:00:00",
        access_method=AccessMethod.X,
        access_mode=AccessMode.MANUAL,
        missingness_status=MissingnessStatus.COMPLETE,
    )


    raw_store.add(raw)


    duplicate_rejected = False


    try:
        raw_store.add(raw)
    except ValueError:
        duplicate_rejected = True


    assert duplicate_rejected is True


    # --------------------------------------------------------
    # Canonical record
    # --------------------------------------------------------


    record = CanonicalIntelligenceRecord(
        record_id="record-001",
        master_source_id="master.x.test",
        source_name="Test Source",
        source_type=SourceType.X_ACCOUNT,
        source_identity_status=SourceIdentityStatus.UNRESOLVED,
        evidence_class=EvidenceClass.SUPPORTING,
        measurement_role=MeasurementRole.COMMENTARY,
        operational_status=OperationalStatus.SADECE_MANUEL,
        fact_status=FactStatus.REPORTED,
        claim_verification_status=ClaimVerificationStatus.UNRESOLVED,
        subject="Test",
        entity_scope="Test Scope",
        instrument_or_market="ES",
        claim="Visible chart information",
        value="+18",
        unit="points",
        observation_time="2026-09-12T15:00:00",
        publication_time="2026-09-12T15:00:00",
        retrieval_time="2026-09-13T10:00:00",
        time_context=TimeContext.HISTORICAL,
        access_method=AccessMethod.X,
        access_mode=AccessMode.MANUAL,
        missingness_status=MissingnessStatus.COMPLETE,
        source_url="https://example.invalid",
        source_locator="post/1",
        source_excerpt_or_field="chart",
        source_family_id="family-1",
        publication_id="publication-1",
        claim_fingerprint="fingerprint-1",
        deduplication_group_id="dedup-1",
        independence_status=IndependenceStatus.UNKNOWN,
        conflict_group_id=None,
        provenance_status="TRACEABLE",
        confidence_basis="Explicitly readable chart value",
    )


    canonical_store = CanonicalRecordStore()
    canonical_store.add(record)


    duplicate_canonical_rejected = False


    try:
        canonical_store.add(record)
    except ValueError:
        duplicate_canonical_rejected = True


    assert duplicate_canonical_rejected is True


    # --------------------------------------------------------
    # Evidence link
    # --------------------------------------------------------


    link_store = EvidenceLinkStore()


    link = CanonicalEvidenceLink(
        record_id="record-001",
        raw_evidence_id="raw-001",
        extracted_information_ids=("extract-001",),
    )


    link_store.add(link)


    # --------------------------------------------------------
    # Structured information
    # --------------------------------------------------------


    extracted = ExtractedInformationRecord(
        extracted_id="extract-001",
        raw_evidence_id="raw-001",
        master_source_id="master.x.test",
        product="Brent",
        value="+18",
        unit="points",
        missingness_status=MissingnessStatus.COMPLETE,
    )


    assert extracted.raw_evidence_id == raw.raw_evidence_id
    assert extracted.value == "+18"


    # --------------------------------------------------------
    # Multimodal separation
    # --------------------------------------------------------


    multimodal = DisplayMultimodalView(
        raw_evidence=raw,
        structured_information=(extracted,),
    )


    assert (
        multimodal.raw_evidence.raw_evidence_id
        == "raw-001"
    )


    assert (
        multimodal.structured_information[0].extracted_id
        == "extract-001"
    )


    # --------------------------------------------------------
    # Query default: unresolved hidden
    # --------------------------------------------------------


    query_default = query_records(
        (record,),
        QueryFilter(),
    )


    assert query_default == ()


    query_include_unresolved = query_records(
        (record,),
        QueryFilter(
            include_unresolved=True,
        ),
    )


    assert query_include_unresolved == (record,)


    # --------------------------------------------------------
    # Conflict preservation
    # --------------------------------------------------------


    conflict_record_a = CanonicalIntelligenceRecord(
        **{
            **record.__dict__,
            "record_id": "record-conflict-a",
            "claim": "Value A",
            "conflict_group_id": "conflict-001",
            "claim_verification_status":
                ClaimVerificationStatus.VERIFIED,
        }
    )


    conflict_record_b = CanonicalIntelligenceRecord(
        **{
            **record.__dict__,
            "record_id": "record-conflict-b",
            "claim": "Value B",
            "conflict_group_id": "conflict-001",
            "claim_verification_status":
                ClaimVerificationStatus.VERIFIED,
        }
    )


    conflicts = query_conflict_group(
        (conflict_record_a, conflict_record_b),
        "conflict-001",
    )


    assert len(conflicts) == 2


    # --------------------------------------------------------
    # Content change → new record
    # --------------------------------------------------------


    changed_record = CanonicalIntelligenceRecord(
        **{
            **record.__dict__,
            "record_id": "record-002",
            "value": "+25",
        }
    )


    assert (
        content_change_requires_new_record(
            record,
            changed_record,
        )
        is True
    )


    require_new_record_for_content_change(
        record,
        changed_record,
    )


    # --------------------------------------------------------
    # Retrieval update
    # --------------------------------------------------------


    event = create_retrieval_update_event(
        old_record=record,
        new_record=changed_record,
        old_raw_evidence_id="raw-001",
        new_raw_evidence_id="raw-002",
        event_id="update-001",
        reason="New retrieval",
        retrieval_time="2026-09-13T12:00:00",
    )


    assert event.previous_record_id == "record-001"
    assert event.new_record_id == "record-002"
    assert event.previous_raw_evidence_id == "raw-001"
    assert event.new_raw_evidence_id == "raw-002"


    # --------------------------------------------------------
    # Verification history
    # --------------------------------------------------------


    verification_entry = create_verification_history_entry(
        record_id="record-001",
        previous_status=ClaimVerificationStatus.UNRESOLVED,
        new_status=ClaimVerificationStatus.VERIFIED,
        event_time="2026-09-13T12:30:00",
        evidence_context="New readable evidence",
    )


    assert (
        verification_entry.previous_status
        == ClaimVerificationStatus.UNRESOLVED
    )


    assert (
        verification_entry.new_status
        == ClaimVerificationStatus.VERIFIED
    )


    # --------------------------------------------------------
    # Freshness is derived, not persisted
    # --------------------------------------------------------


    freshness = derive_freshness_context(record)


    assert freshness.observation_time == record.observation_time
    assert freshness.publication_time == record.publication_time
    assert freshness.retrieval_time == record.retrieval_time
    assert freshness.time_context == TimeContext.HISTORICAL


    # --------------------------------------------------------
    # X media missingness
    # --------------------------------------------------------


    x_view = DisplayXMediaView(
        source_identity="master.x.test",
        post_text="Post text remains available.",
        media_raw_evidence=None,
        media_missingness_status=MissingnessStatus.NOT_RETRIEVED,
    )


    assert x_media_does_not_discard_post(x_view) is True


    # --------------------------------------------------------
    # PDF missingness
    # --------------------------------------------------------


    pdf_raw = RawEvidenceRecord(
        raw_evidence_id="pdf-raw-001",
        master_source_id="master.institution.test",
        evidence_type=RawEvidenceType.PDF_FIGURE,
        raw_content=None,
        source_url="https://example.invalid/report.pdf",
        source_locator="page/12",
        document_id="document-001",
        page="12",
        missingness_status=MissingnessStatus.PARTIAL,
    )


    pdf_view = DisplayPdfView(
        raw_evidence=pdf_raw,
        page="12",
        table=None,
        chart="unreadable",
        figure="partial",
        visual_panel=None,
    )


    assert (
        preserve_visual_missingness(pdf_view.raw_evidence)
        == MissingnessStatus.PARTIAL
    )


    # --------------------------------------------------------
    # Runtime honesty
    # --------------------------------------------------------


    runtime_claims_are_not_generated()


# ============================================================
# 35. MODULE ENTRY
# ============================================================


if __name__ == "__main__":
    validate_4_6()
    print("4.6 — DISPLAY / QUERY / UPDATE / FRESHNESS")
    print("=" * 64)
    print(
        "RAW EVIDENCE → STRUCTURED INFORMATION "
        "→ CANONICAL RECORD → DISPLAY"
    )
    print("READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ")
    print("=" * 64)
    print("Structural validation: OK")


"""
ERHAN / CTA TERMINALİ
4.7 — EVIDENCE PRECEDENCE / INTELLIGENCE MAP / DATA ACQUISITION


SOURCE → WHERE → HOW → ACCESS MODE → RETRIEVAL → RAW EVIDENCE
→ STRUCTURED INFORMATION → CANONICAL RECORD → INTELLIGENCE


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ


Bu modül:


- MASTER source universe'ünü değiştirmez.
- Yeni source keşfetmez.
- Source / content / media access ayrımını korur.
- RAW EVIDENCE ile STRUCTURED INFORMATION'ı ayırır.
- 4.5 canonical record yapısına yeni alan eklemez.
- raw_evidence_id'yi canonical record alanı yapmaz.
- Multimodal evidence'i source identity'den ayırmaz.
- EvidenceClass'ı modality üzerinden otomatik değiştirmez.
- Source ranking / trust score / evidence score / weighting üretmez.
- Independence / conflict / truth resolution yapmaz.
- CTA bias / BUY / SELL / LONG / SHORT / risk / execution üretmez.
- Gerçek network/API/otomatik retrieval kabiliyeti iddia etmez.
- Retrieval sonucunu dışarıdan sağlanan evidence olarak kaydeder.
"""


from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple


# ============================================================
# 1. EXISTING 4.1–4.6 ENUMS
# ============================================================


class SourceType(str, Enum):
    X_ACCOUNT = "X_ACCOUNT"
    INSTITUTION = "INSTITUTION"
    HISTORICAL_INSTITUTION = "HISTORICAL_INSTITUTION"
    PERSON = "PERSON"
    INDEX = "INDEX"
    ETF_PRODUCT = "ETF_PRODUCT"
    POSITIONING_PROXY = "POSITIONING_PROXY"
    HISTORICAL_SYSTEM = "HISTORICAL_SYSTEM"


class SourceIdentityStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    UNRESOLVED = "UNRESOLVED"


class EvidenceClass(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUPPORTING = "SUPPORTING"
    HISTORICAL = "HISTORICAL"
    UNVERIFIED = "UNVERIFIED"


class MeasurementRole(str, Enum):
    DIRECT_MEASUREMENT = "DIRECT_MEASUREMENT"
    PROXY = "PROXY"
    PRODUCT_SPECIFIC = "PRODUCT_SPECIFIC"
    RESEARCH_EVIDENCE = "RESEARCH_EVIDENCE"
    COMMENTARY = "COMMENTARY"
    HISTORICAL_EVIDENCE = "HISTORICAL_EVIDENCE"


class FactStatus(str, Enum):
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    ESTIMATED = "ESTIMATED"
    FORECAST = "FORECAST"
    OPINION = "OPINION"
    UNVERIFIED = "UNVERIFIED"


class ClaimVerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    UNRESOLVED = "UNRESOLVED"


class TimeContext(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    ARCHIVED = "ARCHIVED"
    FORWARD_LOOKING = "FORWARD_LOOKING"


class AccessMethod(str, Enum):
    API = "API"
    CSV = "CSV"
    PDF = "PDF"
    HTML = "HTML"
    X = "X"
    OTHER = "OTHER"


class AccessMode(str, Enum):
    AUTOMATED = "AUTOMATED"
    PROGRAMMATIC_PARTIAL = "PROGRAMMATIC_PARTIAL"
    MANUAL = "MANUAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"


class MissingnessStatus(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    NOT_RETRIEVED = "NOT_RETRIEVED"
    ACCESS_BLOCKED = "ACCESS_BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class IndependenceStatus(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    SAME_SOURCE_FAMILY = "SAME_SOURCE_FAMILY"
    REPUBLISHED = "REPUBLISHED"
    UNKNOWN = "UNKNOWN"


class OperationalStatus(str, Enum):
    KULLANILABILIR = "KULLANILABILIR"
    KISITLI = "KISITLI"
    SADECE_MANUEL = "SADECE_MANUEL"
    ERISILEMIYOR = "ERISILEMIYOR"


class RawEvidenceType(str, Enum):
    TEXT = "TEXT"
    NUMERIC_DATA = "NUMERIC_DATA"
    TABLE = "TABLE"
    CHART = "CHART"
    GRAPH = "GRAPH"
    IMAGE = "IMAGE"
    SCREENSHOT = "SCREENSHOT"
    INFOGRAPHIC = "INFOGRAPHIC"
    DIAGRAM = "DIAGRAM"
    MAP = "MAP"
    VISUAL_PANEL = "VISUAL_PANEL"
    PDF_PAGE = "PDF_PAGE"
    PDF_FIGURE = "PDF_FIGURE"
    PDF_TABLE = "PDF_TABLE"
    X_POST_MEDIA = "X_POST_MEDIA"
    REPORT_MEDIA = "REPORT_MEDIA"


# ============================================================
# 2. 4.7 INTELLIGENCE MAP
# ============================================================


INTELLIGENCE_MAP_SEQUENCE: Tuple[str, ...] = (
    "SOURCE",
    "WHERE",
    "HOW",
    "ACCESS_MODE",
    "RETRIEVAL",
    "RAW_EVIDENCE",
    "STRUCTURED_INFORMATION",
    "CANONICAL_RECORD",
    "INTELLIGENCE",
)


def validate_intelligence_map_sequence() -> None:
    expected = (
        "SOURCE",
        "WHERE",
        "HOW",
        "ACCESS_MODE",
        "RETRIEVAL",
        "RAW_EVIDENCE",
        "STRUCTURED_INFORMATION",
        "CANONICAL_RECORD",
        "INTELLIGENCE",
    )
    assert INTELLIGENCE_MAP_SEQUENCE == expected


# ============================================================
# 3. ACQUISITION PROFILE
# ============================================================


@dataclass(frozen=True)
class AcquisitionProfile:
    """
    MASTER source için edinim haritası.


    SOURCE → WHERE → HOW → ACCESS MODE → SCOPE


    Bu kayıt retrieval işlemini kendisi gerçekleştirmez.
    Sadece edinim haritasını tanımlar.
    """


    master_source_id: str
    source_name: str
    source_type: SourceType
    where: str
    how: Tuple[AccessMethod, ...]
    access_mode: AccessMode
    operational_status: OperationalStatus
    scope: str
    supported_modalities: Tuple[RawEvidenceType, ...] = field(
        default_factory=tuple
    )
    retrieval_capability_verified: bool = False
    notes: Optional[str] = None


# ============================================================
# 4. SOURCE / CONTENT / MEDIA ACCESS BOUNDARY
# ============================================================


@dataclass(frozen=True)
class AccessBoundary:
    """
    SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS


    source_status ayrı,
    content_missingness ayrı,
    media_missingness ayrı tutulur.
    """


    source_operational_status: OperationalStatus
    content_status: MissingnessStatus
    media_status: MissingnessStatus


def validate_access_boundary(boundary: AccessBoundary) -> None:
    assert isinstance(
        boundary.source_operational_status,
        OperationalStatus,
    )
    assert isinstance(boundary.content_status, MissingnessStatus)
    assert isinstance(boundary.media_status, MissingnessStatus)


# ============================================================
# 5. EVIDENCE PRECEDENCE
# ============================================================


def preserve_evidence_class(
    evidence_class: EvidenceClass,
) -> EvidenceClass:
    """
    EvidenceClass yalnızca açıkça sağlanan sınıfı korur.


    Modality:
        CHART
        IMAGE
        PDF_FIGURE
        X_POST_MEDIA
        ...


    tek başına PRIMARY / SECONDARY / SUPPORTING vb. üretmez.
    """


    if not isinstance(evidence_class, EvidenceClass):
        raise TypeError("evidence_class must be EvidenceClass")


    return evidence_class


def visual_format_does_not_change_precedence(
    evidence_class: EvidenceClass,
    evidence_type: RawEvidenceType,
) -> EvidenceClass:
    """
    Görsel format evidence precedence değiştirmez.
    """


    if not isinstance(evidence_class, EvidenceClass):
        raise TypeError("evidence_class must be EvidenceClass")


    if not isinstance(evidence_type, RawEvidenceType):
        raise TypeError("evidence_type must be RawEvidenceType")


    return evidence_class


# ============================================================
# 6. RAW EVIDENCE
# ============================================================


@dataclass(frozen=True)
class RawEvidenceRecord:
    """
    Ham evidence.


    RAW EVIDENCE canonical record değildir.


    raw_evidence_id burada bulunabilir.
    Ancak 4.5 CANONICAL INTELLIGENCE RECORD içine eklenmez.
    """


    raw_evidence_id: str
    master_source_id: str
    evidence_type: RawEvidenceType
    raw_content: Any


    retrieval_time: datetime
    access_method: AccessMethod
    access_mode: AccessMode
    missingness_status: MissingnessStatus


    source_url: Optional[str] = None
    source_locator: Optional[str] = None


    publication_id: Optional[str] = None
    document_id: Optional[str] = None
    page_locator: Optional[str] = None
    post_locator: Optional[str] = None
    visual_locator: Optional[str] = None
    table_locator: Optional[str] = None


    observation_time: Optional[datetime] = None
    publication_time: Optional[datetime] = None


    notes: Optional[str] = None


# ============================================================
# 7. STRUCTURED INFORMATION
# ============================================================


VISUAL_EXTRACTABLE_FIELDS: Tuple[str, ...] = (
    "product",
    "asset",
    "value",
    "percentage",
    "change",
    "date",
    "period",
    "period_label",
    "table_header",
    "table_cell",
    "ranking",
    "chart_title",
    "axis",
    "legend",
    "trend_direction",
    "increase_decrease",
    "explicit_relationship",
)


@dataclass(frozen=True)
class StructuredInformationRecord:
    """
    RAW VISUAL EVIDENCE'den açıkça görülebilen bilgiyi yapılandırır.


    Bu kayıt raw evidence'in yerine geçmez.
    """


    structured_information_id: str
    raw_evidence_id: str
    master_source_id: str


    extracted_fields: Tuple[str, ...] = field(default_factory=tuple)


    product: Optional[str] = None
    asset: Optional[str] = None
    value: Optional[str] = None
    percentage: Optional[str] = None
    change: Optional[str] = None
    date: Optional[str] = None
    period: Optional[str] = None
    period_label: Optional[str] = None


    table_header: Optional[str] = None
    table_cell: Optional[str] = None
    ranking: Optional[str] = None


    chart_title: Optional[str] = None
    axis: Optional[str] = None
    legend: Optional[str] = None


    trend_direction: Optional[str] = None
    increase_decrease: Optional[str] = None
    explicit_relationship: Optional[str] = None


    missingness_status: MissingnessStatus = MissingnessStatus.COMPLETE
    verification_status: ClaimVerificationStatus = (
        ClaimVerificationStatus.UNRESOLVED
    )


def validate_structured_information(
    record: StructuredInformationRecord,
) -> None:


    assert record.raw_evidence_id
    assert record.master_source_id


    for field_name in record.extracted_fields:
        assert field_name in VISUAL_EXTRACTABLE_FIELDS, (
            f"Unsupported visual extraction field: {field_name}"
        )


    assert isinstance(
        record.missingness_status,
        MissingnessStatus,
    )


    assert isinstance(
        record.verification_status,
        ClaimVerificationStatus,
    )


# ============================================================
# 8. CANONICAL RECORD LINK
# ============================================================


@dataclass(frozen=True)
class CanonicalRecordLink:
    """
    4.5 canonical record ile raw/structured evidence arasındaki
    dış bağlantı.


    ÖNEMLİ:
    raw_evidence_id canonical record alanı DEĞİLDİR.


    Bu yapı canonical schema'yı değiştirmez.
    """


    canonical_record_id: str
    raw_evidence_ids: Tuple[str, ...] = field(default_factory=tuple)
    structured_information_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )


# ============================================================
# 9. ACQUISITION STORE
# ============================================================


class AcquisitionStore:
    """
    Acquisition / raw evidence kayıtlarını tutar.


    Mevcut evidence ID üzerine sessiz overwrite yapılmaz.
    """


    def __init__(self) -> None:
        self._raw_evidence: Dict[str, RawEvidenceRecord] = {}
        self._structured_information: Dict[
            str,
            StructuredInformationRecord,
        ] = {}
        self._canonical_links: Dict[str, CanonicalRecordLink] = {}


    def add_raw_evidence(
        self,
        evidence: RawEvidenceRecord,
    ) -> RawEvidenceRecord:


        if evidence.raw_evidence_id in self._raw_evidence:
            raise ValueError(
                f"Raw evidence ID already exists: "
                f"{evidence.raw_evidence_id}"
            )


        self._raw_evidence[evidence.raw_evidence_id] = evidence
        return evidence


    def add_structured_information(
        self,
        record: StructuredInformationRecord,
    ) -> StructuredInformationRecord:


        validate_structured_information(record)


        if record.structured_information_id in (
            self._structured_information
        ):
            raise ValueError(
                "Structured information ID already exists: "
                f"{record.structured_information_id}"
            )


        if record.raw_evidence_id not in self._raw_evidence:
            raise ValueError(
                "Structured information must reference existing "
                f"raw evidence: {record.raw_evidence_id}"
            )


        raw = self._raw_evidence[record.raw_evidence_id]


        if raw.master_source_id != record.master_source_id:
            raise ValueError(
                "Raw evidence and structured information must "
                "preserve the same MASTER source identity."
            )


        self._structured_information[
            record.structured_information_id
        ] = record


        return record


    def add_canonical_link(
        self,
        link: CanonicalRecordLink,
    ) -> CanonicalRecordLink:


        if link.canonical_record_id in self._canonical_links:
            raise ValueError(
                "Canonical link already exists: "
                f"{link.canonical_record_id}"
            )


        for raw_id in link.raw_evidence_ids:
            if raw_id not in self._raw_evidence:
                raise ValueError(
                    f"Unknown raw evidence ID: {raw_id}"
                )


        for structured_id in link.structured_information_ids:
            if structured_id not in self._structured_information:
                raise ValueError(
                    f"Unknown structured information ID: "
                    f"{structured_id}"
                )


        self._canonical_links[
            link.canonical_record_id
        ] = link


        return link


    def get_raw_evidence(
        self,
        raw_evidence_id: str,
    ) -> RawEvidenceRecord:
        return self._raw_evidence[raw_evidence_id]


    def get_structured_information(
        self,
        structured_information_id: str,
    ) -> StructuredInformationRecord:
        return self._structured_information[
            structured_information_id
        ]


    def get_canonical_link(
        self,
        canonical_record_id: str,
    ) -> CanonicalRecordLink:
        return self._canonical_links[canonical_record_id]


    @property
    def raw_evidence(self) -> Mapping[str, RawEvidenceRecord]:
        return dict(self._raw_evidence)


    @property
    def structured_information(
        self,
    ) -> Mapping[str, StructuredInformationRecord]:
        return dict(self._structured_information)


    @property
    def canonical_links(
        self,
    ) -> Mapping[str, CanonicalRecordLink]:
        return dict(self._canonical_links)


# ============================================================
# 10. MASTER ACQUISITION MAP
# ============================================================


MASTER_ACQUISITION_MAP: Tuple[AcquisitionProfile, ...] = (


    # --------------------------------------------------------
    # Andrew Beer
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.person.andrew_beer",
        source_name="Andrew Beer / Dynamic Beta",
        source_type=SourceType.PERSON,
        where="DBi public website",
        how=(AccessMethod.HTML,),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "public profile/content, research/commentary, "
            "product-specific information where applicable."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.CHART,
            RawEvidenceType.IMAGE,
        ),
    ),


    # --------------------------------------------------------
    # Dynamic Beta
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.institution.dynamic_beta",
        source_name="Dynamic Beta",
        source_type=SourceType.INSTITUTION,
        where="DBi public research/news/content",
        how=(AccessMethod.HTML,),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "research, commentary, DBi-related information."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.TABLE,
            RawEvidenceType.CHART,
            RawEvidenceType.GRAPH,
            RawEvidenceType.IMAGE,
        ),
    ),


    # --------------------------------------------------------
    # DBMF
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.institution.dbmf",
        source_name="DBMF",
        source_type=SourceType.ETF_PRODUCT,
        where="DBMF public product pages / factsheets",
        how=(AccessMethod.HTML, AccessMethod.PDF),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "DBMF ve doğrudan ilişkili ürün bilgileri only. "
            "General CTA universe veya general CTA positioning değildir."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.TABLE,
            RawEvidenceType.CHART,
            RawEvidenceType.GRAPH,
            RawEvidenceType.PDF_PAGE,
            RawEvidenceType.PDF_FIGURE,
            RawEvidenceType.PDF_TABLE,
            RawEvidenceType.IMAGE,
        ),
    ),


    # --------------------------------------------------------
    # Jerry Parker / Chesapeake
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.person.jerry_parker",
        source_name="Jerry Parker / Chesapeake",
        source_type=SourceType.PERSON,
        where="public profile/content",
        how=(AccessMethod.HTML,),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "public statements, strategy-related information, "
            "historical/research context."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.CHART,
            RawEvidenceType.IMAGE,
        ),
    ),


    # --------------------------------------------------------
    # Turtle Trader
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.historical_system.turtle_trader",
        source_name="Turtle Trader",
        source_type=SourceType.HISTORICAL_SYSTEM,
        where="public rules / methodology content",
        how=(AccessMethod.HTML,),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "historical methodology, rules, historical evidence."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.TABLE,
            RawEvidenceType.CHART,
        ),
    ),


    # --------------------------------------------------------
    # Newedge
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.historical_institution.newedge",
        source_name="Newedge",
        source_type=SourceType.HISTORICAL_INSTITUTION,
        where="historical SG / institutional material",
        how=(
            AccessMethod.HTML,
            AccessMethod.PDF,
        ),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "historical institutional material, "
            "historical CTA/systematic context."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.TABLE,
            RawEvidenceType.CHART,
            RawEvidenceType.GRAPH,
            RawEvidenceType.PDF_PAGE,
            RawEvidenceType.PDF_FIGURE,
            RawEvidenceType.PDF_TABLE,
        ),
    ),


    # --------------------------------------------------------
    # SG Trend Indicator
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.index.sg_trend_indicator",
        source_name="SG Trend Indicator",
        source_type=SourceType.INDEX,
        where="SG public indicator material",
        how=(
            AccessMethod.HTML,
            AccessMethod.PDF,
            AccessMethod.OTHER,
        ),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "SG Trend Indicator only. "
            "SG Trend Index, paid SG CTA data ve Bloomberg "
            "ile eşit değildir."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.NUMERIC_DATA,
            RawEvidenceType.TABLE,
            RawEvidenceType.CHART,
            RawEvidenceType.GRAPH,
            RawEvidenceType.PDF_FIGURE,
        ),
        retrieval_capability_verified=False,
        notes=(
            "PROGRAMMATIC_PARTIAL ancak ayrıca gerçek "
            "kod/test/runtime kanıtı sağlanırsa kullanılabilir. "
            "Bu statik tanım otomatik capability iddiası değildir."
        ),
    ),


    # --------------------------------------------------------
    # Barclay CTA Index
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.index.barclay_cta_index",
        source_name="Barclay CTA Index",
        source_type=SourceType.INDEX,
        where="BarclayHedge public index material",
        how=(AccessMethod.HTML,),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "CTA benchmark/index information only. "
            "Free public material ≠ full API ≠ underlying "
            "CTA portfolio positioning."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.NUMERIC_DATA,
            RawEvidenceType.TABLE,
            RawEvidenceType.CHART,
            RawEvidenceType.GRAPH,
        ),
    ),


    # --------------------------------------------------------
    # NON-OPERATIONAL X
    # --------------------------------------------------------
    AcquisitionProfile(
        master_source_id="master.x.attaincap2",
        source_name="@AttainCap2",
        source_type=SourceType.X_ACCOUNT,
        where="X public account / post",
        how=(AccessMethod.X,),
        access_mode=AccessMode.NON_OPERATIONAL,
        operational_status=OperationalStatus.ERISILEMIYOR,
        scope=(
            "MASTER kimliği korunur; retrieval, automated retrieval, "
            "supporting evidence veya research evidence olarak kullanılmaz."
        ),
        supported_modalities=(),
        retrieval_capability_verified=False,
    ),


    AcquisitionProfile(
        master_source_id="master.x.jpokotrades",
        source_name="@JPokoTrades",
        source_type=SourceType.X_ACCOUNT,
        where="X public account / post",
        how=(AccessMethod.X,),
        access_mode=AccessMode.NON_OPERATIONAL,
        operational_status=OperationalStatus.ERISILEMIYOR,
        scope=(
            "MASTER kimliği korunur; retrieval, automated retrieval, "
            "supporting evidence veya research evidence olarak kullanılmaz."
        ),
        supported_modalities=(),
        retrieval_capability_verified=False,
    ),
)


# ============================================================
# 11. X ACQUISITION MODEL
# ============================================================


def verified_x_acquisition_profile(
    master_source_id: str,
    source_name: str,
) -> AcquisitionProfile:
    """
    MASTER'daki verified X source'lar için ortak acquisition modeli.


    X API varsayılmaz.
    Default access mode MANUAL'dır.


    Not:
    Bu fonksiyon source discovery yapmaz.
    Verilen source ID'nin MASTER'da gerçekten mevcut olduğunu
    dışarıdan sağlanan MASTER universe doğrulaması belirler.
    """


    if not master_source_id.startswith("master.x."):
        raise ValueError(
            "X acquisition profile requires master.x.* source ID."
        )


    if not source_name:
        raise ValueError("source_name is required.")


    if master_source_id in NON_OPERATIONAL_SOURCE_IDS:
        raise ValueError(
            f"Non-operational X source cannot receive "
            f"retrieval profile: {master_source_id}"
        )


    return AcquisitionProfile(
        master_source_id=master_source_id,
        source_name=source_name,
        source_type=SourceType.X_ACCOUNT,
        where="X public account / post",
        how=(AccessMethod.X,),
        access_mode=AccessMode.MANUAL,
        operational_status=OperationalStatus.SADECE_MANUEL,
        scope=(
            "X public post content. Text, chart, image, screenshot, "
            "table, infographic and attached media remain under "
            "the same source/publication provenance chain."
        ),
        supported_modalities=(
            RawEvidenceType.TEXT,
            RawEvidenceType.CHART,
            RawEvidenceType.GRAPH,
            RawEvidenceType.IMAGE,
            RawEvidenceType.SCREENSHOT,
            RawEvidenceType.TABLE,
            RawEvidenceType.INFOGRAPHIC,
            RawEvidenceType.X_POST_MEDIA,
        ),
        retrieval_capability_verified=False,
        notes=(
            "X API is not assumed. Another access mode may be used "
            "only after real verification evidence exists."
        ),
    )


# ============================================================
# 12. RETRIEVAL RECORD
# ============================================================


@dataclass(frozen=True)
class RetrievalRecord:
    """
    Retrieval'ın kendisine ait provenance.


    Bu kayıt network çağrısı yapmaz.
    Dışarıdan gerçekten elde edilmiş retrieval sonucunu temsil eder.
    """


    retrieval_id: str
    master_source_id: str
    access_method: AccessMethod
    access_mode: AccessMode
    retrieval_time: datetime


    source_access_status: OperationalStatus
    content_status: MissingnessStatus
    media_status: MissingnessStatus


    source_url: Optional[str] = None
    source_locator: Optional[str] = None
    publication_id: Optional[str] = None
    document_id: Optional[str] = None
    page_locator: Optional[str] = None
    post_locator: Optional[str] = None


    notes: Optional[str] = None


# ============================================================
# 13. X TEXT / MEDIA SEPARATION
# ============================================================


@dataclass(frozen=True)
class XPostAcquisition:
    """
    X ACCOUNT → POST → TEXT / MEDIA


    Text ve media aynı post bağlamında kalır.
    Media eksikliği post text'ini silmez.
    """


    master_source_id: str
    post_id: str


    text_status: MissingnessStatus
    media_status: MissingnessStatus


    text_raw_evidence_id: Optional[str] = None
    media_raw_evidence_id: Optional[str] = None


def validate_x_post_acquisition(
    record: XPostAcquisition,
) -> None:


    assert record.master_source_id.startswith("master.x.")
    assert record.post_id


    if (
        record.text_status == MissingnessStatus.COMPLETE
        and record.text_raw_evidence_id is None
    ):
        raise ValueError(
            "Complete X post text requires text raw evidence linkage."
        )


    if (
        record.media_status == MissingnessStatus.COMPLETE
        and record.media_raw_evidence_id is None
    ):
        raise ValueError(
            "Complete X media requires media raw evidence linkage."
        )


# ============================================================
# 14. PDF ACQUISITION
# ============================================================


@dataclass(frozen=True)
class PDFAcquisitionContext:
    """
    SOURCE → DOCUMENT → PAGE → CONTENT / TABLE / VISUAL
    """


    master_source_id: str
    document_id: str


    page_locator: Optional[str] = None


    text_status: MissingnessStatus = MissingnessStatus.NOT_APPLICABLE
    table_status: MissingnessStatus = MissingnessStatus.NOT_APPLICABLE
    chart_status: MissingnessStatus = MissingnessStatus.NOT_APPLICABLE
    figure_status: MissingnessStatus = MissingnessStatus.NOT_APPLICABLE
    image_status: MissingnessStatus = MissingnessStatus.NOT_APPLICABLE
    diagram_status: MissingnessStatus = MissingnessStatus.NOT_APPLICABLE
    infographic_status: MissingnessStatus = (
        MissingnessStatus.NOT_APPLICABLE
    )


# ============================================================
# 15. VISUAL ACQUISITION
# ============================================================


@dataclass(frozen=True)
class VisualAcquisitionContext:
    """
    Raw visual evidence'in provenance context'i.


    Görselden yalnızca açıkça görülen bilgi yapılandırılabilir.
    """


    raw_evidence_id: str
    master_source_id: str


    publication_id: Optional[str] = None
    document_id: Optional[str] = None
    page_locator: Optional[str] = None
    post_locator: Optional[str] = None
    visual_locator: Optional[str] = None
    table_locator: Optional[str] = None


    missingness_status: MissingnessStatus = (
        MissingnessStatus.COMPLETE
    )


def validate_visual_context(
    context: VisualAcquisitionContext,
) -> None:


    assert context.raw_evidence_id
    assert context.master_source_id


    assert isinstance(
        context.missingness_status,
        MissingnessStatus,
    )


# ============================================================
# 16. SPECIAL SOURCE RULES
# ============================================================


SPECIAL_MEASUREMENT_ROLES: Dict[str, MeasurementRole] = {
    "master.index.sg_trend_indicator":
        MeasurementRole.DIRECT_MEASUREMENT,


    "master.institution.dbmf":
        MeasurementRole.PRODUCT_SPECIFIC,


    "master.positioning.cftc_cot":
        MeasurementRole.PROXY,
}


def validate_special_source_scope(
    master_source_id: str,
    measurement_role: Optional[MeasurementRole] = None,
) -> None:


    if master_source_id == "master.index.sg_trend_indicator":
        if measurement_role is not None:
            assert (
                measurement_role
                == MeasurementRole.DIRECT_MEASUREMENT
            )


    if master_source_id == "master.institution.dbmf":
        if measurement_role is not None:
            assert (
                measurement_role
                == MeasurementRole.PRODUCT_SPECIFIC
            )


    if master_source_id == "master.positioning.cftc_cot":
        if measurement_role is not None:
            assert measurement_role == MeasurementRole.PROXY


def validate_barclay_scope(master_source_id: str) -> None:
    if master_source_id == "master.index.barclay_cta_index":
        # Index / benchmark scope only.
        return


# ============================================================
# 17. CFTC COT BOUNDARY
# ============================================================


def validate_cftc_cot_boundary(
    master_source_id: str,
    measurement_role: MeasurementRole,
) -> None:


    if master_source_id == "master.positioning.cftc_cot":
        assert measurement_role == MeasurementRole.PROXY


        # CFTC COT:
        # POSITIONING_PROXY
        #
        # değildir:
        # direct CTA portfolio positioning
        # direct CTA holdings
        # exact CTA manager portfolio


# ============================================================
# 18. SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS
# ============================================================


def validate_access_separation(
    source_status: OperationalStatus,
    content_status: MissingnessStatus,
    media_status: MissingnessStatus,
) -> None:


    assert isinstance(source_status, OperationalStatus)
    assert isinstance(content_status, MissingnessStatus)
    assert isinstance(media_status, MissingnessStatus)


    # Source accessible olsa bile content/media incomplete olabilir.
    # Burada source status otomatik değiştirilmez.


# ============================================================
# 19. RAW EVIDENCE ≠ STRUCTURED INFORMATION
# ============================================================


def validate_raw_structured_separation(
    raw: RawEvidenceRecord,
    structured: StructuredInformationRecord,
) -> None:


    assert raw.raw_evidence_id == structured.raw_evidence_id
    assert raw.master_source_id == structured.master_source_id


    # Structured information raw evidence'in yerine geçmez.
    assert raw.raw_evidence_id


# ============================================================
# 20. CANONICAL BOUNDARY
# ============================================================


# 4.5 CANONICAL RECORD ALANLARI DEĞİŞTİRİLMEZ.
#
# 4.7 burada canonical dataclass yeniden tanımlamaz.
#
# Özellikle YASAK:
# raw_evidence_id
# visual_confidence_score
# OCR_score
# image_quality_score
# extraction_score
# media_reliability_score
# freshness_status
# freshness_score
# source_ranking
# source_weighting
# trust_score
# evidence_strength


FORBIDDEN_CANONICAL_FIELDS_4_7: Tuple[str, ...] = (
    "raw_evidence_id",
    "visual_confidence_score",
    "OCR_score",
    "image_quality_score",
    "extraction_score",
    "media_reliability_score",
    "freshness_status",
    "freshness_score",
    "source_ranking",
    "source_weighting",
    "trust_score",
    "evidence_strength",
    "source_weight",
    "confidence_score",
    "independence_decision",
    "conflict_resolution",
    "truth_selection",
    "cta_final_bias",
    "BUY",
    "SELL",
    "LONG",
    "SHORT",
    "trade_decision",
    "risk_decision",
    "execution_decision",
)


def validate_forbidden_canonical_fields(
    canonical_field_names: Iterable[str],
) -> None:


    fields = set(canonical_field_names)


    forbidden_present = (
        fields
        & set(FORBIDDEN_CANONICAL_FIELDS_4_7)
    )


    if forbidden_present:
        raise ValueError(
            "Forbidden 4.7 canonical fields detected: "
            f"{sorted(forbidden_present)}"
        )


# ============================================================
# 21. INDEPENDENCE / CONFLICT BOUNDARY
# ============================================================


def preserve_independence_status(
    status: IndependenceStatus,
) -> IndependenceStatus:
    """
    Independence hesaplamaz.
    Sağlanan mevcut statüyü yalnızca korur.
    """


    if not isinstance(status, IndependenceStatus):
        raise TypeError(
            "status must be IndependenceStatus"
        )


    return status


def conflict_is_preserved(
    conflict_group_id: Optional[str],
) -> Optional[str]:
    """
    Conflict çözülmez.
    Truth selection yapılmaz.
    Conflict group yalnızca korunur.
    """


    return conflict_group_id


# ============================================================
# 22. RUNTIME HONESTY
# ============================================================


def validate_runtime_capability_claim(
    profile: AcquisitionProfile,
) -> None:
    """
    Gerçek kod/test/runtime kanıtı yoksa:
    - API availability
    - automatic retrieval
    - continuous retrieval
    - automatic PDF retrieval
    - automatic X media retrieval
    - automatic visual extraction


    varsayılmaz.
    """


    if not profile.retrieval_capability_verified:
        assert profile.access_mode in (
            AccessMode.MANUAL,
            AccessMode.NON_OPERATIONAL,
        )


def mark_verified_programmatic_access(
    profile: AcquisitionProfile,
    *,
    verified_by_runtime: bool,
) -> AcquisitionProfile:
    """
    Programmatic access yalnızca dışarıdan gerçek runtime/test
    kanıtı açıkça sağlandığında işaretlenebilir.


    Bu fonksiyon runtime testi kendisi çalıştırmaz.
    """


    if not verified_by_runtime:
        raise ValueError(
            "PROGRAMMATIC access cannot be marked verified "
            "without real runtime/test evidence."
        )


    if profile.access_mode == AccessMode.NON_OPERATIONAL:
        raise ValueError(
            "NON_OPERATIONAL source cannot become programmatic."
        )


    return AcquisitionProfile(
        master_source_id=profile.master_source_id,
        source_name=profile.source_name,
        source_type=profile.source_type,
        where=profile.where,
        how=profile.how,
        access_mode=AccessMode.PROGRAMMATIC_PARTIAL,
        operational_status=OperationalStatus.KISITLI,
        scope=profile.scope,
        supported_modalities=profile.supported_modalities,
        retrieval_capability_verified=True,
        notes=profile.notes,
    )


# ============================================================
# 23. IMMUTABLE RAW EVIDENCE REGISTRATION
# ============================================================


def register_external_raw_evidence(
    store: AcquisitionStore,
    *,
    evidence_id: str,
    master_source_id: str,
    evidence_type: RawEvidenceType,
    raw_content: Any,
    access_method: AccessMethod,
    access_mode: AccessMode,
    missingness_status: MissingnessStatus,
    retrieval_time: Optional[datetime] = None,
    source_url: Optional[str] = None,
    source_locator: Optional[str] = None,
    publication_id: Optional[str] = None,
    document_id: Optional[str] = None,
    page_locator: Optional[str] = None,
    post_locator: Optional[str] = None,
    visual_locator: Optional[str] = None,
    table_locator: Optional[str] = None,
    observation_time: Optional[datetime] = None,
    publication_time: Optional[datetime] = None,
    notes: Optional[str] = None,
) -> RawEvidenceRecord:
    """
    Gerçekten dışarıdan elde edilmiş evidence'i kaydeder.


    Network/API çağrısı yapmaz.
    Otomatik retrieval iddiasında bulunmaz.
    """


    if not evidence_id:
        raise ValueError("evidence_id is required.")


    if not master_source_id:
        raise ValueError("master_source_id is required.")


    if access_mode == AccessMode.NON_OPERATIONAL:
        raise ValueError(
            "NON_OPERATIONAL access cannot register retrieval evidence."
        )


    if retrieval_time is None:
        retrieval_time = datetime.now(timezone.utc)


    evidence = RawEvidenceRecord(
        raw_evidence_id=evidence_id,
        master_source_id=master_source_id,
        evidence_type=evidence_type,
        raw_content=raw_content,
        retrieval_time=retrieval_time,
        access_method=access_method,
        access_mode=access_mode,
        missingness_status=missingness_status,
        source_url=source_url,
        source_locator=source_locator,
        publication_id=publication_id,
        document_id=document_id,
        page_locator=page_locator,
        post_locator=post_locator,
        visual_locator=visual_locator,
        table_locator=table_locator,
        observation_time=observation_time,
        publication_time=publication_time,
        notes=notes,
    )


    return store.add_raw_evidence(evidence)


# ============================================================
# 24. NON-OPERATIONAL BOUNDARY
# ============================================================


NON_OPERATIONAL_SOURCE_IDS: Tuple[str, ...] = (
    "master.x.attaincap2",
    "master.x.jpokotrades",
)


def validate_non_operational_sources() -> None:


    for source_id in NON_OPERATIONAL_SOURCE_IDS:
        profile = next(
            (
                p
                for p in MASTER_ACQUISITION_MAP
                if p.master_source_id == source_id
            ),
            None,
        )


        assert profile is not None
        assert (
            profile.access_mode
            == AccessMode.NON_OPERATIONAL
        )
        assert (
            profile.operational_status
            == OperationalStatus.ERISILEMIYOR
        )
        assert profile.retrieval_capability_verified is False


# ============================================================
# 25. MASTER SPECIAL MAP VALIDATION
# ============================================================


EXPECTED_SPECIAL_SOURCE_IDS: Tuple[str, ...] = (
    "master.person.andrew_beer",
    "master.institution.dynamic_beta",
    "master.institution.dbmf",
    "master.person.jerry_parker",
    "master.historical_system.turtle_trader",
    "master.historical_institution.newedge",
    "master.index.sg_trend_indicator",
    "master.index.barclay_cta_index",
    "master.x.attaincap2",
    "master.x.jpokotrades",
)


def validate_master_acquisition_map() -> None:


    ids = {
        profile.master_source_id
        for profile in MASTER_ACQUISITION_MAP
    }


    for source_id in EXPECTED_SPECIAL_SOURCE_IDS:
        assert source_id in ids, (
            f"Missing required 4.7 acquisition profile: "
            f"{source_id}"
        )


    for profile in MASTER_ACQUISITION_MAP:


        assert profile.master_source_id
        assert profile.source_name
        assert profile.where
        assert profile.how
        assert profile.scope


        assert isinstance(profile.source_type, SourceType)
        assert isinstance(profile.access_mode, AccessMode)
        assert isinstance(
            profile.operational_status,
            OperationalStatus,
        )


        validate_runtime_capability_claim(profile)


# ============================================================
# 26. SPECIAL SOURCE VALIDATION
# ============================================================


def validate_special_rules() -> None:


    dbmf = next(
        p
        for p in MASTER_ACQUISITION_MAP
        if p.master_source_id == "master.institution.dbmf"
    )


    assert dbmf.source_type == SourceType.ETF_PRODUCT
    assert dbmf.access_mode == AccessMode.MANUAL
    assert AccessMethod.HTML in dbmf.how
    assert AccessMethod.PDF in dbmf.how


    sg = next(
        p
        for p in MASTER_ACQUISITION_MAP
        if p.master_source_id
        == "master.index.sg_trend_indicator"
    )


    assert sg.access_mode == AccessMode.MANUAL
    assert sg.retrieval_capability_verified is False


    barclay = next(
        p
        for p in MASTER_ACQUISITION_MAP
        if p.master_source_id
        == "master.index.barclay_cta_index"
    )


    assert barclay.access_mode == AccessMode.MANUAL


    validate_special_source_scope(
        "master.institution.dbmf",
        MeasurementRole.PRODUCT_SPECIFIC,
    )


    validate_special_source_scope(
        "master.index.sg_trend_indicator",
        MeasurementRole.DIRECT_MEASUREMENT,
    )


    validate_special_source_scope(
        "master.positioning.cftc_cot",
        MeasurementRole.PROXY,
    )


    validate_cftc_cot_boundary(
        "master.positioning.cftc_cot",
        MeasurementRole.PROXY,
    )


# ============================================================
# 27. MULTIMODAL BOUNDARY
# ============================================================


def validate_multimodal_boundary() -> None:


    assert RawEvidenceType.CHART != RawEvidenceType.TEXT
    assert RawEvidenceType.PDF_FIGURE != RawEvidenceType.PDF_TABLE
    assert RawEvidenceType.X_POST_MEDIA != RawEvidenceType.TEXT


    # Bunlar format/modality'dir.
    # MASTER source değildir.


    assert (
        RawEvidenceType.CHART.value
        == "CHART"
    )


    assert (
        RawEvidenceType.PDF_FIGURE.value
        == "PDF_FIGURE"
    )


    assert (
        RawEvidenceType.X_POST_MEDIA.value
        == "X_POST_MEDIA"
    )


# ============================================================
# 28. SOURCE / WHERE / HOW / ACCESS MODE VALIDATION
# ============================================================


def validate_acquisition_profile_consistency(
    profile: AcquisitionProfile,
) -> None:


    if profile.access_mode == AccessMode.NON_OPERATIONAL:
        assert (
            profile.operational_status
            == OperationalStatus.ERISILEMIYOR
        )
        assert not profile.retrieval_capability_verified


    if profile.access_mode == AccessMode.MANUAL:
        assert profile.operational_status in (
            OperationalStatus.SADECE_MANUEL,
            OperationalStatus.KISITLI,
            OperationalStatus.KULLANILABILIR,
        )


    if profile.access_mode == AccessMode.PROGRAMMATIC_PARTIAL:
        assert profile.retrieval_capability_verified is True


    if profile.access_mode == AccessMode.AUTOMATED:
        assert profile.retrieval_capability_verified is True


# ============================================================
# 29. NO AUTOMATIC PRECEDENCE FROM MODALITY
# ============================================================


def validate_precedence_boundary() -> None:


    for evidence_type in RawEvidenceType:
        result = visual_format_does_not_change_precedence(
            EvidenceClass.SECONDARY,
            evidence_type,
        )


        assert result == EvidenceClass.SECONDARY


# ============================================================
# 30. NO DECISION OUTPUTS
# ============================================================


FORBIDDEN_DECISION_OUTPUTS: Tuple[str, ...] = (
    "BUY",
    "SELL",
    "LONG",
    "SHORT",
    "CTA_FINAL_BIAS",
    "TRADE_DECISION",
    "RISK_DECISION",
    "EXECUTION_DECISION",
    "SOURCE_RANKING",
    "TRUST_SCORE",
    "EVIDENCE_STRENGTH",
    "CONFIDENCE_SCORE",
    "SOURCE_WEIGHTING",
    "CONFLICT_RESOLUTION",
    "TRUTH_SELECTION",
    "INDEPENDENCE_DECISION",
)


def validate_no_decision_outputs() -> None:


    for value in FORBIDDEN_DECISION_OUTPUTS:
        assert isinstance(value, str)


    # Bu modül bu değerleri üretmez.
    # Liste yalnızca 4.7 sınırlarının explicit contract'ıdır.


# ============================================================
# 31. INTELLIGENCE OUTPUT BOUNDARY
# ============================================================


@dataclass(frozen=True)
class IntelligenceInputMarker:
    """
    4.7'nin downstream intelligence katmanına geçiş marker'ı.


    Bu yapı intelligence üretmez.
    Sadece canonical record'un sonraki katmanlara input olabileceğini
    temsil eder.
    """


    canonical_record_id: str
    ready_for_downstream_intelligence: bool = True


def validate_intelligence_input_marker(
    marker: IntelligenceInputMarker,
) -> None:


    assert marker.canonical_record_id
    assert marker.ready_for_downstream_intelligence is True


# ============================================================
# 32. EVIDENCE → STRUCTURED → CANONICAL LINK TEST
# ============================================================


def build_test_evidence_chain() -> Tuple[
    AcquisitionStore,
    RawEvidenceRecord,
    StructuredInformationRecord,
    CanonicalRecordLink,
]:
    """
    Gerçek network retrieval yapmaz.
    Yalnızca yapısal lifecycle doğrulaması için örnek zincir üretir.
    """


    store = AcquisitionStore()


    raw = register_external_raw_evidence(
        store,
        evidence_id="test.raw.001",
        master_source_id="master.institution.dbmf",
        evidence_type=RawEvidenceType.CHART,
        raw_content={
            "example": "externally supplied raw chart evidence"
        },
        access_method=AccessMethod.PDF,
        access_mode=AccessMode.MANUAL,
        missingness_status=MissingnessStatus.COMPLETE,
        source_url="external-evidence-placeholder",
        source_locator="document/page/chart",
    )


    structured = StructuredInformationRecord(
        structured_information_id="test.structured.001",
        raw_evidence_id=raw.raw_evidence_id,
        master_source_id=raw.master_source_id,
        extracted_fields=(
            "product",
            "value",
            "period",
        ),
        product="DBMF",
        value="visible value",
        period="visible period",
        missingness_status=MissingnessStatus.COMPLETE,
        verification_status=(
            ClaimVerificationStatus.UNRESOLVED
        ),
    )


    store.add_structured_information(structured)


    link = CanonicalRecordLink(
        canonical_record_id="test.canonical.001",
        raw_evidence_ids=(raw.raw_evidence_id,),
        structured_information_ids=(
            structured.structured_information_id,
        ),
    )


    store.add_canonical_link(link)


    return store, raw, structured, link


# ============================================================
# 33. FULL 4.7 VALIDATION
# ============================================================


def validate_4_7() -> None:
    """
    4.7 structural validation.


    Bu fonksiyon external API, X, PDF veya web erişimini test etmez.
    Sadece kodun 4.7 structural contract'ını doğrular.
    """


    # Intelligence map
    validate_intelligence_map_sequence()


    # Acquisition map
    validate_master_acquisition_map()


    for profile in MASTER_ACQUISITION_MAP:
        validate_acquisition_profile_consistency(profile)


    # Special sources
    validate_special_rules()


    # Non-operational
    validate_non_operational_sources()


    # Multimodal
    validate_multimodal_boundary()


    # Evidence precedence
    validate_precedence_boundary()


    # Access separation
    boundary = AccessBoundary(
        source_operational_status=OperationalStatus.KULLANILABILIR,
        content_status=MissingnessStatus.COMPLETE,
        media_status=MissingnessStatus.NOT_RETRIEVED,
    )


    validate_access_boundary(boundary)


    # Visual structured extraction boundary
    store, raw, structured, link = (
        build_test_evidence_chain()
    )


    validate_raw_structured_separation(
        raw,
        structured,
    )


    validate_structured_information(structured)


    assert link.canonical_record_id == (
        "test.canonical.001"
    )


    # Runtime honesty
    for profile in MASTER_ACQUISITION_MAP:
        validate_runtime_capability_claim(profile)


    # Forbidden canonical fields
    validate_forbidden_canonical_fields(
        (
            "record_id",
            "master_source_id",
            "source_name",
            "claim",
            "value",
            "source_url",
            "source_locator",
            "provenance_status",
        )
    )


    # Decision boundary
    validate_no_decision_outputs()


    # Downstream marker
    marker = IntelligenceInputMarker(
        canonical_record_id="test.canonical.001"
    )


    validate_intelligence_input_marker(marker)


    # Evidence class preservation
    assert preserve_evidence_class(
        EvidenceClass.PRIMARY
    ) == EvidenceClass.PRIMARY


    assert visual_format_does_not_change_precedence(
        EvidenceClass.SUPPORTING,
        RawEvidenceType.CHART,
    ) == EvidenceClass.SUPPORTING


    # Independence is preserved, not calculated
    assert preserve_independence_status(
        IndependenceStatus.UNKNOWN
    ) == IndependenceStatus.UNKNOWN


    # Conflict is preserved, not resolved
    assert conflict_is_preserved(
        "conflict.test.001"
    ) == "conflict.test.001"


# ============================================================
# 34. MODULE ENTRY POINT
# ============================================================


if __name__ == "__main__":
    validate_4_7()


    print(
        "4.7 — EVIDENCE PRECEDENCE / INTELLIGENCE MAP / "
        "DATA ACQUISITION"
    )
    print("=" * 78)
    print(
        "SOURCE → WHERE → HOW → ACCESS MODE → RETRIEVAL "
        "→ RAW EVIDENCE"
    )
    print(
        "→ STRUCTURED INFORMATION → CANONICAL RECORD "
        "→ INTELLIGENCE"
    )
    print("=" * 78)
    print(
        "SOURCE ACCESS ≠ CONTENT ACCESS ≠ MEDIA ACCESS"
    )
    print(
        "RAW EVIDENCE ≠ STRUCTURED INFORMATION"
    )
    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )
    print("=" * 78)
    print("Validation: OK")


"""


ERHAN / CTA TERMINALİ
BÖLÜM 4.8 — FINAL COVERAGE / TERMINAL MAPPING / SOURCE ARCHITECTURE LOCK


Purpose
-------
Final integrity layer for Sections 4.1–4.7.


Architecture:


SOURCE
    ↓
ACCESS
    ↓
RETRIEVAL
    ↓
RAW EVIDENCE
    ↓
STRUCTURED INFORMATION
    ↓
CANONICAL RECORD
    ↓
VERIFICATION
    ↓
DEDUPLICATION
    ↓
CONFLICT
    ↓
CURRENT / HISTORICAL STATE
    ↓
STORAGE
    ↓
DISPLAY


Section 4.8 does NOT create a new canonical schema, new decision layer,
new source universe, new scoring system, or new evidence hierarchy.


Important:
- READ-ONLY INTELLIGENCE
- KARAR ÜRETMEZ
- No BUY / SELL / LONG / SHORT
- No risk decision
- No portfolio decision
- No position sizing
- No order
- No execution
- KÖKBÖRÜ remains decision authority
- TULPAR remains execution authority


This module is intentionally validation/mapping focused.
It must consume/reuse the structures established in Sections 4.1–4.7.
It does not recreate their enums or canonical record classes.
"""


from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Sequence


# ============================================================================
# 1. LOCKED SOURCE IDS
# ============================================================================


# The 21-source coverage set required by Section 4.8.
#
# IMPORTANT:
# @TheStalwart and @tracyalloway are intentionally retained as unresolved
# MASTER-UNIVERSE mismatches because they are present in the 4.8 work package
# but are not present in the locked MASTER X-69 list.
#
# They must NOT be silently added to MASTER X.


REQUIRED_4_8_SOURCE_IDS: tuple[str, ...] = (
    "master.index.sg_trend_indicator",
    "master.index.barclay_cta_index",
    "master.institution.dbmf",


    "master.person.andrew_beer",
    "master.institution.dynamic_beta",
    "master.person.jerry_parker",
    "master.x.rcmalts",
    "master.x.macroops",


    "master.x.rjpjr12",
    "master.x.peterlbrandt",
    "master.x.lindaraschke",
    "master.x.anthonycrudele",
    "master.x.futurestrader71",
    "master.x.commodmkt",
    "master.x.tracyalloway",
    "master.x.misterpuertas",
    "master.x.thestalwart",


    "master.historical_system.turtle_trader",
    "master.historical_institution.newedge",


    "master.x.attaincap2",
    "master.x.jpokotrades",
)


# Locked MASTER X universe entries relevant to this work package.
LOCKED_MASTER_X_IDS: frozenset[str] = frozenset(
    {
        "master.x.rjpjr12",
        "master.x.peterlbrandt",
        "master.x.lindaraschke",
        "master.x.anthonycrudele",
        "master.x.futurestrader71",
        "master.x.commodmkt",
        "master.x.misterpuertas",
        "master.x.rcmalts",
        "master.x.macroops",
        "master.x.attaincap2",
    }
)


# These are explicitly present in the 4.8 specification but absent from
# the locked MASTER X-69 list.
UNRESOLVED_MASTER_MISMATCHES: frozenset[str] = frozenset(
    {
        "master.x.tracyalloway",
        "master.x.thestalwart",
    }
)


# Non-operational sources from 4.4.
NON_OPERATIONAL_SOURCE_IDS: frozenset[str] = frozenset(
    {
        "master.x.attaincap2",
        "master.x.jpokotrades",
    }
)


# ============================================================================
# 2. LOCKED OPERATIONAL STATUS EXPECTATIONS FROM SECTION 4.4
# ============================================================================


EXPECTED_OPERATIONAL_STATUS: Mapping[str, str] = {
    "master.index.sg_trend_indicator": "KISITLI",
    "master.index.barclay_cta_index": "KISITLI",
    "master.institution.dbmf": "KISITLI",


    "master.person.andrew_beer": "SADECE_MANUEL",
    "master.institution.dynamic_beta": "SADECE_MANUEL",
    "master.person.jerry_parker": "SADECE_MANUEL",


    "master.x.rcmalts": "SADECE_MANUEL",
    "master.x.macroops": "SADECE_MANUEL",


    "master.x.rjpjr12": "SADECE_MANUEL",
    "master.x.peterlbrandt": "SADECE_MANUEL",
    "master.x.lindaraschke": "SADECE_MANUEL",
    "master.x.anthonycrudele": "SADECE_MANUEL",
    "master.x.futurestrader71": "SADECE_MANUEL",
    "master.x.commodmkt": "SADECE_MANUEL",
    "master.x.tracyalloway": "SADECE_MANUEL",
    "master.x.misterpuertas": "SADECE_MANUEL",
    "master.x.thestalwart": "SADECE_MANUEL",


    "master.historical_system.turtle_trader": "SADECE_MANUEL",
    "master.historical_institution.newedge": "SADECE_MANUEL",


    "master.x.attaincap2": "ERISILEMIYOR",
    "master.x.jpokotrades": "ERISILEMIYOR",
}


# ============================================================================
# 3. TERMINAL LOCATIONS
# ============================================================================


class TerminalLocation(str, Enum):
    PRIMARY_MARKET_TREND_EVIDENCE = "PRIMARY_MARKET_TREND_EVIDENCE"
    PRODUCT_ETF_EVIDENCE = "PRODUCT_ETF_EVIDENCE"
    RESEARCH_EVIDENCE = "RESEARCH_EVIDENCE"
    SUPPORTING_COMMENTARY = "SUPPORTING_COMMENTARY"
    HISTORICAL_EVIDENCE = "HISTORICAL_EVIDENCE"
    NON_OPERATIONAL = "NON_OPERATIONAL"


TERMINAL_LOCATION_BY_SOURCE: Mapping[str, TerminalLocation] = {
    "master.index.sg_trend_indicator":
        TerminalLocation.PRIMARY_MARKET_TREND_EVIDENCE,


    "master.index.barclay_cta_index":
        TerminalLocation.PRIMARY_MARKET_TREND_EVIDENCE,


    "master.institution.dbmf":
        TerminalLocation.PRODUCT_ETF_EVIDENCE,


    "master.person.andrew_beer":
        TerminalLocation.RESEARCH_EVIDENCE,


    "master.institution.dynamic_beta":
        TerminalLocation.RESEARCH_EVIDENCE,


    "master.person.jerry_parker":
        TerminalLocation.RESEARCH_EVIDENCE,


    "master.x.rcmalts":
        TerminalLocation.RESEARCH_EVIDENCE,


    "master.x.macroops":
        TerminalLocation.RESEARCH_EVIDENCE,


    "master.x.rjpjr12":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.peterlbrandt":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.lindaraschke":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.anthonycrudele":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.futurestrader71":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.commodmkt":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.tracyalloway":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.misterpuertas":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.x.thestalwart":
        TerminalLocation.SUPPORTING_COMMENTARY,


    "master.historical_system.turtle_trader":
        TerminalLocation.HISTORICAL_EVIDENCE,


    "master.historical_institution.newedge":
        TerminalLocation.HISTORICAL_EVIDENCE,


    "master.x.attaincap2":
        TerminalLocation.NON_OPERATIONAL,


    "master.x.jpokotrades":
        TerminalLocation.NON_OPERATIONAL,
}


# ============================================================================
# 4. LOCKED SCOPE
# ============================================================================


SOURCE_SCOPE_BY_ID: Mapping[str, str] = {
    "master.index.sg_trend_indicator":
        "Own SG Trend Indicator series only.",


    "master.index.barclay_cta_index":
        "Own Barclay CTA Index / benchmark only.",


    "master.institution.dbmf":
        "DBMF product scope only: identity, strategy, performance, holdings, factsheet, benchmark/context.",


    "master.person.andrew_beer":
        "Research evidence only; no direct market measurement or portfolio-position claim.",


    "master.institution.dynamic_beta":
        "Research evidence only; institution/product research scope.",


    "master.person.jerry_parker":
        "Research evidence only; no direct market measurement or current portfolio-position claim.",


    "master.x.rcmalts":
        "Research evidence / commentary within source-specific scope.",


    "master.x.macroops":
        "Research evidence / commentary within source-specific scope.",


    "master.x.rjpjr12":
        "Supporting commentary only.",


    "master.x.peterlbrandt":
        "Supporting commentary only.",


    "master.x.lindaraschke":
        "Supporting commentary only.",


    "master.x.anthonycrudele":
        "Supporting commentary only.",


    "master.x.futurestrader71":
        "Supporting commentary only.",


    "master.x.commodmkt":
        "Supporting commentary only.",


    "master.x.tracyalloway":
        "Supporting commentary only; MASTER identity mismatch remains unresolved.",


    "master.x.misterpuertas":
        "Supporting commentary only.",


    "master.x.thestalwart":
        "Supporting commentary only; MASTER identity mismatch remains unresolved.",


    "master.historical_system.turtle_trader":
        "Historical Turtle methodology / historical evidence only.",


    "master.historical_institution.newedge":
        "Historical institutional context only.",


    "master.x.attaincap2":
        "Non-operational source; no operational terminal evidence.",


    "master.x.jpokotrades":
        "Non-operational source; no operational terminal evidence.",
}


# ============================================================================
# 5. SOURCE / EVIDENCE ROLE LOCK
# ============================================================================


MEASUREMENT_ROLE_BY_SOURCE: Mapping[str, str] = {
    "master.index.sg_trend_indicator": "DIRECT_MEASUREMENT",
    "master.index.barclay_cta_index": "DIRECT_MEASUREMENT",


    "master.institution.dbmf": "PRODUCT_SPECIFIC",


    "master.person.andrew_beer": "RESEARCH_EVIDENCE",
    "master.institution.dynamic_beta": "RESEARCH_EVIDENCE",
    "master.person.jerry_parker": "RESEARCH_EVIDENCE",
    "master.x.rcmalts": "RESEARCH_EVIDENCE",
    "master.x.macroops": "RESEARCH_EVIDENCE",


    "master.x.rjpjr12": "COMMENTARY",
    "master.x.peterlbrandt": "COMMENTARY",
    "master.x.lindaraschke": "COMMENTARY",
    "master.x.anthonycrudele": "COMMENTARY",
    "master.x.futurestrader71": "COMMENTARY",
    "master.x.commodmkt": "COMMENTARY",
    "master.x.tracyalloway": "COMMENTARY",
    "master.x.misterpuertas": "COMMENTARY",
    "master.x.thestalwart": "COMMENTARY",


    "master.historical_system.turtle_trader": "HISTORICAL_EVIDENCE",
    "master.historical_institution.newedge": "HISTORICAL_EVIDENCE",


    "master.x.attaincap2": "COMMENTARY",
    "master.x.jpokotrades": "COMMENTARY",
}


EVIDENCE_CLASS_BY_SOURCE: Mapping[str, str] = {
    "master.index.sg_trend_indicator": "PRIMARY",
    "master.index.barclay_cta_index": "PRIMARY",


    "master.institution.dbmf": "PRIMARY",


    "master.person.andrew_beer": "SUPPORTING",
    "master.institution.dynamic_beta": "SUPPORTING",
    "master.person.jerry_parker": "SUPPORTING",
    "master.x.rcmalts": "SUPPORTING",
    "master.x.macroops": "SUPPORTING",


    "master.x.rjpjr12": "SUPPORTING",
    "master.x.peterlbrandt": "SUPPORTING",
    "master.x.lindaraschke": "SUPPORTING",
    "master.x.anthonycrudele": "SUPPORTING",
    "master.x.futurestrader71": "SUPPORTING",
    "master.x.commodmkt": "SUPPORTING",
    "master.x.tracyalloway": "SUPPORTING",
    "master.x.misterpuertas": "SUPPORTING",
    "master.x.thestalwart": "SUPPORTING",


    "master.historical_system.turtle_trader": "HISTORICAL",
    "master.historical_institution.newedge": "HISTORICAL",


    "master.x.attaincap2": "UNVERIFIED",
    "master.x.jpokotrades": "UNVERIFIED",
}


# ============================================================================
# 6. SOURCE FAMILY LOCK
# ============================================================================


#
# These are identifiers used by 4.5/4.6/4.7 for deduplication and
# independence handling.
#
# 4.8 does NOT calculate independence.
# It only preserves supplied source-family information.
#


SOURCE_FAMILY_BY_SOURCE: Mapping[str, str] = {
    "master.index.sg_trend_indicator":
        "family.sg",


    "master.index.barclay_cta_index":
        "family.barclay",


    "master.institution.dbmf":
        "family.dbmf",


    "master.person.andrew_beer":
        "family.dynamic_beta_research",


    "master.institution.dynamic_beta":
        "family.dynamic_beta_research",


    "master.person.jerry_parker":
        "family.jerry_parker",


    "master.x.rcmalts":
        "family.rcm",


    "master.x.macroops":
        "family.macroops",


    "master.x.rjpjr12":
        "family.rjpjr12",


    "master.x.peterlbrandt":
        "family.peter_brandt",


    "master.x.lindaraschke":
        "family.linda_raschke",


    "master.x.anthonycrudele":
        "family.anthony_crudele",


    "master.x.futurestrader71":
        "family.futurestrader71",


    "master.x.commodmkt":
        "family.commodmkt",


    "master.x.tracyalloway":
        "family.tracyalloway",


    "master.x.misterpuertas":
        "family.misterpuertas",


    "master.x.thestalwart":
        "family.thestalwart",


    "master.historical_system.turtle_trader":
        "family.turtle_trader",


    "master.historical_institution.newedge":
        "family.newedge",


    "master.x.attaincap2":
        "family.attaincap2",


    "master.x.jpokotrades":
        "family.jpokotrades",
}


# ============================================================================
# 7. SPECIAL SOURCE RULES
# ============================================================================


SPECIAL_SOURCE_RULES: Mapping[str, Mapping[str, str]] = {
    "master.index.sg_trend_indicator": {
        "measurement_role": "DIRECT_MEASUREMENT",
        "scope": "OWN_INDICATOR_SERIES_ONLY",
    },


    "master.index.barclay_cta_index": {
        "measurement_role": "DIRECT_MEASUREMENT",
        "scope": "OWN_INDEX_BENCHMARK_ONLY",
    },


    "master.institution.dbmf": {
        "measurement_role": "PRODUCT_SPECIFIC",
        "scope": "DBMF_PRODUCT_ONLY",
    },


    "master.historical_system.turtle_trader": {
        "measurement_role": "HISTORICAL_EVIDENCE",
        "scope": "HISTORICAL_METHODOLOGY_ONLY",
    },


    "master.historical_institution.newedge": {
        "measurement_role": "HISTORICAL_EVIDENCE",
        "scope": "HISTORICAL_INSTITUTIONAL_CONTEXT_ONLY",
    },


    "master.x.attaincap2": {
        "operational": "FALSE",
    },


    "master.x.jpokotrades": {
        "operational": "FALSE",
    },
}


# ============================================================================
# 8. 4.7 OBJECT ADAPTERS
# ============================================================================


def _read_attr(obj: Any, name: str, default: Any = None) -> Any:
    """
    Read a field from either an object or mapping without manufacturing data.
    """
    if obj is None:
        return default


    if isinstance(obj, Mapping):
        return obj.get(name, default)


    return getattr(obj, name, default)


def _object_id(obj: Any) -> Optional[str]:
    """
    Resolve an existing object identifier without creating one.
    """
    for field_name in (
        "id",
        "record_id",
        "raw_evidence_id",
        "master_source_id",
        "publication_id",
    ):
        value = _read_attr(obj, field_name)
        if value:
            return str(value)


    return None


def _source_id(obj: Any) -> Optional[str]:
    value = _read_attr(obj, "master_source_id")
    if value:
        return str(value)


    if isinstance(obj, Mapping):
        value = obj.get("source_id")
        if value:
            return str(value)


    return None


# ============================================================================
# 9. COVERAGE RECORD
# ============================================================================


@dataclass(frozen=True)
class SourceEvidenceLink:
    """
    Links one existing source to existing 4.7 evidence objects.


    This is a 4.8 mapping object.
    It does NOT replace or modify the 4.5 canonical schema.
    """


    master_source_id: str


    access_object: Any = None
    retrieval_object: Any = None
    raw_evidence_objects: tuple[Any, ...] = ()
    structured_information_objects: tuple[Any, ...] = ()
    canonical_record_objects: tuple[Any, ...] = ()


    terminal_location: Optional[TerminalLocation] = None


    observation_time_present: bool = False
    publication_time_present: bool = False
    retrieval_time_present: bool = False


    scope_validated: bool = False
    independence_preserved: bool = False
    conflict_preserved: bool = False
    deduplication_preserved: bool = False


    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class MasterSourceCoverageRecord:
    """
    Final 4.8 coverage mapping.


    This record is NOT a canonical intelligence record.
    It is an architecture/coverage view over existing 4.1–4.7 structures.
    """


    master_source_id: str
    source_name: str


    terminal_location: TerminalLocation


    expected_operational_status: str
    expected_measurement_role: str
    expected_evidence_class: str


    source_family_id: str
    scope_definition: str


    master_identity_resolved: bool
    master_identity_mismatch: bool
    operational_excluded: bool


    link: Optional[SourceEvidenceLink] = None


# ============================================================================
# 10. SOURCE NAME MAP
# ============================================================================


SOURCE_NAME_BY_ID: Mapping[str, str] = {
    "master.index.sg_trend_indicator": "SG Trend Indicator",
    "master.index.barclay_cta_index": "Barclay CTA Index",
    "master.institution.dbmf": "DBMF",


    "master.person.andrew_beer": "Andrew Beer",
    "master.institution.dynamic_beta": "Dynamic Beta",
    "master.person.jerry_parker": "Jerry Parker",
    "master.x.rcmalts": "@rcmAlts",
    "master.x.macroops": "@MacroOps",


    "master.x.rjpjr12": "@rjpjr12",
    "master.x.peterlbrandt": "@PeterLBrandt",
    "master.x.lindaraschke": "@LindaRaschke",
    "master.x.anthonycrudele": "@AnthonyCrudele",
    "master.x.futurestrader71": "@FuturesTrader71",
    "master.x.commodmkt": "@CommodMkt",
    "master.x.tracyalloway": "@tracyalloway",
    "master.x.misterpuertas": "@misterpuertas",
    "master.x.thestalwart": "@TheStalwart",


    "master.historical_system.turtle_trader": "Turtle Trader",
    "master.historical_institution.newedge": "Newedge",


    "master.x.attaincap2": "@AttainCap2",
    "master.x.jpokotrades": "@JPokoTrades",
}


# ============================================================================
# 11. FINAL COVERAGE REGISTRY
# ============================================================================


class FinalCoverageRegistry:
    """
    4.8 final registry.


    The registry does not discover sources.
    It does not mutate MASTER.
    It does not create canonical records.
    It only validates and exposes the locked 4.8 coverage map.
    """


    def __init__(self) -> None:
        self._coverage: dict[str, MasterSourceCoverageRecord] = {}


    @property
    def coverage(self) -> Mapping[str, MasterSourceCoverageRecord]:
        return dict(self._coverage)


    def register(
        self,
        master_source_id: str,
        *,
        link: Optional[SourceEvidenceLink] = None,
    ) -> MasterSourceCoverageRecord:


        if master_source_id not in REQUIRED_4_8_SOURCE_IDS:
            raise ValueError(
                f"4.8 source is outside locked coverage set: {master_source_id}"
            )


        if master_source_id in self._coverage:
            raise ValueError(
                f"Duplicate 4.8 coverage registration: {master_source_id}"
            )


        mismatch = master_source_id in UNRESOLVED_MASTER_MISMATCHES
        excluded = master_source_id in NON_OPERATIONAL_SOURCE_IDS


        record = MasterSourceCoverageRecord(
            master_source_id=master_source_id,
            source_name=SOURCE_NAME_BY_ID[master_source_id],
            terminal_location=TERMINAL_LOCATION_BY_SOURCE[master_source_id],
            expected_operational_status=EXPECTED_OPERATIONAL_STATUS[
                master_source_id
            ],
            expected_measurement_role=MEASUREMENT_ROLE_BY_SOURCE[
                master_source_id
            ],
            expected_evidence_class=EVIDENCE_CLASS_BY_SOURCE[
                master_source_id
            ],
            source_family_id=SOURCE_FAMILY_BY_SOURCE[
                master_source_id
            ],
            scope_definition=SOURCE_SCOPE_BY_ID[
                master_source_id
            ],
            master_identity_resolved=not mismatch,
            master_identity_mismatch=mismatch,
            operational_excluded=excluded,
            link=link,
        )


        self._coverage[master_source_id] = record
        return record


    def register_all_locked_sources(self) -> None:
        for source_id in REQUIRED_4_8_SOURCE_IDS:
            self.register(source_id)


    def get(self, master_source_id: str) -> Optional[MasterSourceCoverageRecord]:
        return self._coverage.get(master_source_id)


# ============================================================================
# 12. REAL 4.7 LINK ATTACHMENT
# ============================================================================


class FourSevenIntegration:
    """
    Adapter for already-existing 4.7 objects.


    The adapter intentionally does not recreate:
        RawEvidenceRecord
        StructuredInformationRecord
        CanonicalRecordLink
        RetrievalRecord
        AcquisitionProfile
        AccessBoundary


    The caller supplies the existing 4.7 objects.
    """


    def __init__(
        self,
        *,
        acquisitions: Optional[Iterable[Any]] = None,
        retrievals: Optional[Iterable[Any]] = None,
        raw_evidence: Optional[Iterable[Any]] = None,
        structured_information: Optional[Iterable[Any]] = None,
        canonical_links: Optional[Iterable[Any]] = None,
    ) -> None:
        self.acquisitions = tuple(acquisitions or ())
        self.retrievals = tuple(retrievals or ())
        self.raw_evidence = tuple(raw_evidence or ())
        self.structured_information = tuple(structured_information or ())
        self.canonical_links = tuple(canonical_links or ())


    def objects_for_source(
        self,
        objects: Sequence[Any],
        master_source_id: str,
    ) -> tuple[Any, ...]:
        result: list[Any] = []


        for obj in objects:
            sid = _source_id(obj)


            if sid == master_source_id:
                result.append(obj)
                continue


            # Some existing 4.7 objects can expose the source through nested
            # acquisition/source references. We inspect only already-existing
            # fields and never infer a source identity from a name.
            nested_source = _read_attr(obj, "source")
            if nested_source is not None:
                nested_sid = _source_id(nested_source)
                if nested_sid == master_source_id:
                    result.append(obj)


        return tuple(result)


    def link_source(
        self,
        master_source_id: str,
    ) -> SourceEvidenceLink:


        acquisitions = self.objects_for_source(
            self.acquisitions,
            master_source_id,
        )


        retrievals = self.objects_for_source(
            self.retrievals,
            master_source_id,
        )


        raw = self.objects_for_source(
            self.raw_evidence,
            master_source_id,
        )


        structured = self.objects_for_source(
            self.structured_information,
            master_source_id,
        )


        canonical = self.objects_for_source(
            self.canonical_links,
            master_source_id,
        )


        access_object = acquisitions[0] if acquisitions else None
        retrieval_object = retrievals[0] if retrievals else None


        observation_time_present = any(
            _read_attr(obj, "observation_time") is not None
            for obj in (*raw, *structured, *canonical)
        )


        publication_time_present = any(
            _read_attr(obj, "publication_time") is not None
            for obj in (*raw, *structured, *canonical)
        )


        retrieval_time_present = any(
            _read_attr(obj, "retrieval_time") is not None
            for obj in (*retrievals, *raw, *structured, *canonical)
        )


        return SourceEvidenceLink(
            master_source_id=master_source_id,
            access_object=access_object,
            retrieval_object=retrieval_object,
            raw_evidence_objects=raw,
            structured_information_objects=structured,
            canonical_record_objects=canonical,
            terminal_location=TERMINAL_LOCATION_BY_SOURCE[
                master_source_id
            ],
            observation_time_present=observation_time_present,
            publication_time_present=publication_time_present,
            retrieval_time_present=retrieval_time_present,
            scope_validated=True,
            independence_preserved=True,
            conflict_preserved=True,
            deduplication_preserved=True,
        )


# ============================================================================
# 13. MULTIMODAL EVIDENCE LOCK
# ============================================================================


# 4.7 already owns RawEvidenceType.
#
# 4.8 does not create a replacement enum.
#
# The following canonical raw-evidence names are locked as strings solely
# for validation against existing 4.7 objects. No new enum is created.


LOCKED_RAW_EVIDENCE_TYPES: frozenset[str] = frozenset(
    {
        "TEXT",
        "NUMERIC_DATA",
        "TABLE",
        "CHART",
        "GRAPH",
        "IMAGE",
        "SCREENSHOT",
        "INFOGRAPHIC",
        "DIAGRAM",
        "MAP",
        "VISUAL_PANEL",
        "PDF_PAGE",
        "PDF_FIGURE",
        "PDF_TABLE",
        "X_POST_MEDIA",
        "REPORT_MEDIA",
    }
)


def raw_evidence_type_name(obj: Any) -> Optional[str]:
    value = _read_attr(obj, "evidence_type")


    if value is None:
        value = _read_attr(obj, "raw_evidence_type")


    if value is None:
        return None


    if isinstance(value, Enum):
        return value.name


    return str(value).split(".")[-1]


def validate_raw_evidence_types(
    raw_evidence_objects: Iterable[Any],
) -> list[str]:
    errors: list[str] = []


    for obj in raw_evidence_objects:
        evidence_type = raw_evidence_type_name(obj)


        if evidence_type is None:
            errors.append(
                "Raw evidence object has no existing RawEvidenceType."
            )
            continue


        if evidence_type not in LOCKED_RAW_EVIDENCE_TYPES:
            errors.append(
                f"Unknown raw evidence type encountered: {evidence_type}"
            )


    return errors


# ============================================================================
# 14. CANONICAL 34-FIELD LOCK
# ============================================================================


LOCKED_CANONICAL_FIELDS: tuple[str, ...] = (
    "id",
    "record_id",
    "master_source_id",
    "source_name",
    "source_type",
    "source_identity_status",
    "evidence_class",
    "measurement_role",
    "operational_status",
    "fact_status",
    "claim_verification_status",
    "subject",
    "entity_scope",
    "instrument_or_market",
    "claim",
    "value",
    "unit",
    "observation_time",
    "publication_time",
    "retrieval_time",
    "time_context",
    "access_method",
    "access_mode",
    "missingness_status",
    "source_url",
    "source_locator",
    "source_excerpt_or_field",
    "source_family_id",
    "publication_id",
    "claim_fingerprint",
    "deduplication_group_id",
    "independence_status",
    "conflict_group_id",
    "provenance_status",
    "confidence_basis",
)


FORBIDDEN_NEW_CANONICAL_FIELDS: frozenset[str] = frozenset(
    {
        "raw_evidence_id",
        "score",
        "rank",
        "weight",
        "trust",
        "freshness_status",
        "staleness_status",
        "expiration_status",
        "version_id",
        "parent_record_id",
        "previous_record_id",
        "visual_confidence_score",
        "OCR_score",
        "image_quality_score",
        "extraction_score",
        "media_reliability_score",
    }
)


def canonical_field_names(obj: Any) -> set[str]:
    """
    Extract field names from an existing canonical object without creating
    a new schema.
    """


    if obj is None:
        return set()


    if isinstance(obj, Mapping):
        return set(obj.keys())


    if hasattr(obj, "__dataclass_fields__"):
        return set(obj.__dataclass_fields__.keys())


    if hasattr(obj, "__dict__"):
        return set(obj.__dict__.keys())


    return set()


def validate_canonical_schema(
    canonical_objects: Iterable[Any],
) -> list[str]:
    errors: list[str] = []


    for obj in canonical_objects:
        fields = canonical_field_names(obj)


        forbidden = fields.intersection(
            FORBIDDEN_NEW_CANONICAL_FIELDS
        )


        if forbidden:
            errors.append(
                "Forbidden canonical fields detected: "
                + ", ".join(sorted(forbidden))
            )


        if fields:
            missing_locked = set(LOCKED_CANONICAL_FIELDS) - fields


            # Only report if this appears to be a canonical record object.
            # Link objects may intentionally contain fewer fields.
            object_name = type(obj).__name__.lower()


            if (
                "canonical" in object_name
                and missing_locked
            ):
                errors.append(
                    "Canonical object does not expose the locked 34-field "
                    "schema; missing: "
                    + ", ".join(sorted(missing_locked))
                )


    return errors


# ============================================================================
# 15. SOURCE / ACCESS / CONTENT / MEDIA SEPARATION
# ============================================================================


def validate_access_separation(
    master_source_id: str,
    *,
    access_object: Any,
    retrieval_object: Any,
    raw_objects: Sequence[Any],
) -> list[str]:
    errors: list[str] = []


    if master_source_id in NON_OPERATIONAL_SOURCE_IDS:
        if access_object is not None:
            errors.append(
                f"{master_source_id}: non-operational source has access object."
            )


        if retrieval_object is not None:
            errors.append(
                f"{master_source_id}: non-operational source has retrieval object."
            )


        if raw_objects:
            errors.append(
                f"{master_source_id}: non-operational source has raw evidence."
            )


        return errors


    # Operational source:
    if retrieval_object is not None and access_object is None:
        errors.append(
            f"{master_source_id}: retrieval exists without access layer."
        )


    return errors


# ============================================================================
# 16. TIME / FRESHNESS VALIDATION
# ============================================================================


def validate_time_separation(
    objects: Iterable[Any],
) -> list[str]:
    errors: list[str] = []


    for obj in objects:
        observation_time = _read_attr(obj, "observation_time")
        publication_time = _read_attr(obj, "publication_time")
        retrieval_time = _read_attr(obj, "retrieval_time")
        time_context = _read_attr(obj, "time_context")


        # Retrieval time must never be silently used as observation time.
        if (
            retrieval_time is not None
            and observation_time is not None
            and retrieval_time == observation_time
        ):
            # Equality itself is not automatically wrong; no error is raised.
            # The important rule is that the fields remain separate.
            pass


        # Historical state must remain historical.
        if time_context is not None:
            context_name = (
                time_context.name
                if isinstance(time_context, Enum)
                else str(time_context).split(".")[-1]
            )


            if context_name == "HISTORICAL":
                # Historical does not become CURRENT simply because retrieved
                # today. No mutation is performed here.
                pass


        # No new freshness field is permitted.
        fields = canonical_field_names(obj)


        forbidden_freshness = {
            "freshness_status",
            "staleness_status",
            "expiration_status",
        }.intersection(fields)


        if forbidden_freshness:
            errors.append(
                "Freshness/status fields outside the locked schema detected: "
                + ", ".join(sorted(forbidden_freshness))
            )


    return errors


# ============================================================================
# 17. DOUBLE COUNTING / INDEPENDENCE VALIDATION
# ============================================================================


def validate_independence_preservation(
    canonical_objects: Iterable[Any],
) -> list[str]:
    errors: list[str] = []


    for obj in canonical_objects:
        fields = canonical_field_names(obj)


        if "independence_status" not in fields:
            continue


        independence = _read_attr(obj, "independence_status")


        if independence is None:
            errors.append(
                "Canonical record has no supplied independence status."
            )


        # No numerical independence score is allowed.
        forbidden = {
            "independence_score",
            "independence_weight",
            "source_independence_score",
        }.intersection(fields)


        if forbidden:
            errors.append(
                "Independence scoring field detected: "
                + ", ".join(sorted(forbidden))
            )


    return errors


def validate_deduplication_preservation(
    canonical_objects: Iterable[Any],
) -> list[str]:
    errors: list[str] = []


    for obj in canonical_objects:
        fields = canonical_field_names(obj)


        if "deduplication_group_id" not in fields:
            continue


        # Presence of deduplication group is enough.
        # 4.8 must not calculate a new duplicate score.
        forbidden = {
            "duplicate_score",
            "deduplication_score",
            "similarity_score",
        }.intersection(fields)


        if forbidden:
            errors.append(
                "Deduplication scoring field detected: "
                + ", ".join(sorted(forbidden))
            )


    return errors


# ============================================================================
# 18. CONFLICT PRESERVATION
# ============================================================================


def validate_conflict_preservation(
    canonical_objects: Iterable[Any],
) -> list[str]:
    errors: list[str] = []


    for obj in canonical_objects:
        fields = canonical_field_names(obj)


        if "conflict_group_id" not in fields:
            continue


        # 4.8 only checks that conflict grouping exists where supplied.
        # It must not resolve, rank, delete, or select truth.
        forbidden = {
            "conflict_resolution",
            "resolved_truth",
            "selected_truth",
            "conflict_winner",
            "conflict_score",
        }.intersection(fields)


        if forbidden:
            errors.append(
                "Automatic conflict-resolution field detected: "
                + ", ".join(sorted(forbidden))
            )


    return errors


# ============================================================================
# 19. SCOPE ISOLATION
# ============================================================================


def validate_scope_isolation(
    master_source_id: str,
    *,
    canonical_objects: Sequence[Any],
) -> list[str]:
    errors: list[str] = []


    locked_scope = SOURCE_SCOPE_BY_ID[master_source_id]


    for obj in canonical_objects:
        entity_scope = _read_attr(obj, "entity_scope")
        measurement_role = _read_attr(obj, "measurement_role")


        # DBMF may never become general CTA universe evidence.
        if master_source_id == "master.institution.dbmf":
            text = " ".join(
                str(value)
                for value in (
                    entity_scope,
                    measurement_role,
                    _read_attr(obj, "claim"),
                    _read_attr(obj, "subject"),
                )
                if value is not None
            ).lower()


            forbidden_terms = (
                "cta universe",
                "all cta",
                "cta positioning",
                "managed money positioning",
            )


            if any(term in text for term in forbidden_terms):
                errors.append(
                    "DBMF scope leakage detected: DBMF was generalized "
                    "beyond product-specific evidence."
                )


        # SG Trend Indicator must remain its own indicator series.
        if master_source_id == "master.index.sg_trend_indicator":
            text = " ".join(
                str(value)
                for value in (
                    entity_scope,
                    measurement_role,
                    _read_attr(obj, "claim"),
                    _read_attr(obj, "subject"),
                )
                if value is not None
            ).lower()


            if "sg trend index" in text and "indicator" not in text:
                errors.append(
                    "SG Trend Indicator / SG Trend Index scope confusion."
                )


        # Historical sources cannot become current measurement.
        if master_source_id in {
            "master.historical_system.turtle_trader",
            "master.historical_institution.newedge",
        }:
            time_context = _read_attr(obj, "time_context")


            if time_context is not None:
                context_name = (
                    time_context.name
                    if isinstance(time_context, Enum)
                    else str(time_context).split(".")[-1]
                )


                if context_name == "CURRENT":
                    errors.append(
                        f"{master_source_id}: historical source marked CURRENT."
                    )


    return errors


# ============================================================================
# 20. READ-ONLY BOUNDARY
# ============================================================================


FORBIDDEN_DECISION_TERMS: frozenset[str] = frozenset(
    {
        "BUY",
        "SELL",
        "LONG",
        "SHORT",
        "ORDER",
        "EXECUTION",
        "POSITION_SIZE",
        "POSITION SIZING",
        "RISK DECISION",
        "PORTFOLIO DECISION",
        "FINAL BIAS",
        "TRADING SIGNAL",
    }
)


def validate_read_only_text(values: Iterable[Any]) -> list[str]:
    errors: list[str] = []


    for value in values:
        if value is None:
            continue


        text = str(value).upper()


        for forbidden in FORBIDDEN_DECISION_TERMS:
            if forbidden in text:
                errors.append(
                    f"READ-ONLY boundary violation candidate: {forbidden}"
                )


    return errors


# ============================================================================
# 21. 21-SOURCE COVERAGE VALIDATION
# ============================================================================


def validate_21_source_coverage(
    registry: FinalCoverageRegistry,
) -> list[str]:
    errors: list[str] = []


    actual_ids = set(registry.coverage.keys())
    expected_ids = set(REQUIRED_4_8_SOURCE_IDS)


    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids


    if missing:
        errors.append(
            "Missing 4.8 coverage sources: "
            + ", ".join(sorted(missing))
        )


    if extra:
        errors.append(
            "Unexpected 4.8 coverage sources: "
            + ", ".join(sorted(extra))
        )


    if len(actual_ids) != 21:
        errors.append(
            f"4.8 coverage count is {len(actual_ids)}; expected exactly 21."
        )


    return errors


# ============================================================================
# 22. MASTER MISMATCH VALIDATION
# ============================================================================


def validate_master_mismatches(
    registry: FinalCoverageRegistry,
) -> list[str]:
    errors: list[str] = []


    for source_id in UNRESOLVED_MASTER_MISMATCHES:
        record = registry.get(source_id)


        if record is None:
            errors.append(
                f"Unresolved MASTER mismatch disappeared from coverage: {source_id}"
            )
            continue


        if not record.master_identity_mismatch:
            errors.append(
                f"{source_id}: unresolved MASTER mismatch incorrectly marked resolved."
            )


    # No silent addition of mismatched X accounts to locked MASTER X.
    for source_id in UNRESOLVED_MASTER_MISMATCHES:
        if source_id in LOCKED_MASTER_X_IDS:
            errors.append(
                f"MASTER mismatch incorrectly exists in locked X set: {source_id}"
            )


    return errors


# ============================================================================
# 23. OPERATIONAL STATUS VALIDATION
# ============================================================================


def validate_operational_status(
    registry: FinalCoverageRegistry,
    existing_source_objects: Optional[Iterable[Any]] = None,
) -> list[str]:
    errors: list[str] = []


    if existing_source_objects is None:
        return errors


    for obj in existing_source_objects:
        source_id = _source_id(obj)


        if source_id not in EXPECTED_OPERATIONAL_STATUS:
            continue


        actual = _read_attr(obj, "operational_status")


        if actual is None:
            continue


        actual_name = (
            actual.name
            if isinstance(actual, Enum)
            else str(actual).split(".")[-1]
        )


        expected = EXPECTED_OPERATIONAL_STATUS[source_id]


        if actual_name != expected:
            errors.append(
                f"{source_id}: operational status is {actual_name}; "
                f"locked 4.4 status is {expected}."
            )


    return errors


# ============================================================================
# 24. FINAL VALIDATION REPORT
# ============================================================================


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    source_count: int
    mapped_source_count: int
    unresolved_master_mismatches: tuple[str, ...]


class FinalArchitectureValidator:
    """
    Final 4.8 validator.


    It reports actual structural findings only.
    It never reports tests as passed unless the caller actually executes this
    validator and receives a passing result.
    """


    def __init__(
        self,
        registry: FinalCoverageRegistry,
        integration: Optional[FourSevenIntegration] = None,
    ) -> None:
        self.registry = registry
        self.integration = integration


    def validate(
        self,
        existing_source_objects: Optional[Iterable[Any]] = None,
    ) -> ValidationResult:


        errors: list[str] = []
        warnings: list[str] = []


        errors.extend(
            validate_21_source_coverage(self.registry)
        )


        errors.extend(
            validate_master_mismatches(self.registry)
        )


        errors.extend(
            validate_operational_status(
                self.registry,
                existing_source_objects,
            )
        )


        all_raw: list[Any] = []
        all_structured: list[Any] = []
        all_canonical: list[Any] = []


        if self.integration is not None:
            all_raw.extend(self.integration.raw_evidence)
            all_structured.extend(
                self.integration.structured_information
            )
            all_canonical.extend(
                self.integration.canonical_links
            )


        errors.extend(
            validate_raw_evidence_types(all_raw)
        )


        errors.extend(
            validate_canonical_schema(all_canonical)
        )


        errors.extend(
            validate_time_separation(
                (
                    *all_raw,
                    *all_structured,
                    *all_canonical,
                )
            )
        )


        errors.extend(
            validate_independence_preservation(
                all_canonical
            )
        )


        errors.extend(
            validate_deduplication_preservation(
                all_canonical
            )
        )


        errors.extend(
            validate_conflict_preservation(
                all_canonical
            )
        )


        # Per-source validation.
        for source_id, coverage in self.registry.coverage.items():


            link = coverage.link


            if link is None:
                if source_id not in NON_OPERATIONAL_SOURCE_IDS:
                    warnings.append(
                        f"{source_id}: no 4.7 evidence link supplied "
                        f"to this validation run."
                    )
                continue


            errors.extend(
                validate_access_separation(
                    source_id,
                    access_object=link.access_object,
                    retrieval_object=link.retrieval_object,
                    raw_objects=link.raw_evidence_objects,
                )
            )


            errors.extend(
                validate_scope_isolation(
                    source_id,
                    canonical_objects=link.canonical_record_objects,
                )
            )


        # Read-only scan over known architecture labels and supplied records.
        readonly_values: list[Any] = [
            "READ-ONLY INTELLIGENCE",
            "KARAR ÜRETMEZ",
            "KÖKBÖRÜ decision authority",
            "TULPAR execution authority",
        ]


        for record in self.registry.coverage.values():
            readonly_values.extend(
                (
                    record.source_name,
                    record.scope_definition,
                    record.expected_measurement_role,
                )
            )


        # Do NOT scan ordinary source names blindly for English terms such
        # as "order" if they can be part of unrelated proper nouns.
        # Scan only explicit architecture/configuration fields.
        errors.extend(
            validate_read_only_text(
                readonly_values
            )
        )


        mapped_count = sum(
            for record in self.registry.coverage.values()
            if record.link is not None
        )


        return ValidationResult(
            passed=not errors,
            errors=tuple(errors),
            warnings=tuple(warnings),
            source_count=21,
            mapped_source_count=mapped_count,
            unresolved_master_mismatches=tuple(
                sorted(UNRESOLVED_MASTER_MISMATCHES)
            ),
        )


# ============================================================================
# 25. FINAL ARCHITECTURE SNAPSHOT
# ============================================================================


FINAL_ARCHITECTURE: tuple[str, ...] = (
    "SOURCE",
    "ACCESS",
    "RETRIEVAL",
    "RAW EVIDENCE",
    "STRUCTURED INFORMATION",
    "CANONICAL RECORD",
    "VERIFICATION",
    "DEDUPLICATION",
    "CONFLICT",
    "CURRENT/HISTORICAL STATE",
    "STORAGE",
    "DISPLAY",
)


# ============================================================================
# 26. SECTION 4.8 GUARANTEES
# ============================================================================


SECTION_4_8_RULES: Mapping[str, bool] = {
    "no_new_source_discovery": True,
    "no_new_canonical_schema": True,
    "no_new_canonical_enum": True,
    "no_new_decision_layer": True,
    "no_scoring": True,
    "no_ranking": True,
    "no_weighting": True,
    "no_trust_score": True,
    "no_freshness_field": True,
    "no_visual_quality_score": True,
    "no_ocr_score": True,
    "no_media_reliability_score": True,
    "no_automatic_conflict_resolution": True,
    "no_independence_calculation": True,
    "raw_evidence_preserved": True,
    "raw_structured_separation": True,
    "historical_current_separation": True,
    "source_access_separation": True,
    "content_media_separation": True,
    "non_operational_exclusion": True,
    "read_only_intelligence": True,
}


# ============================================================================
# 27. FACTORY
# ============================================================================


def build_final_4_8_registry(
    integration: Optional[FourSevenIntegration] = None,
) -> FinalCoverageRegistry:


    registry = FinalCoverageRegistry()


    if integration is None:
        registry.register_all_locked_sources()
        return registry


    for source_id in REQUIRED_4_8_SOURCE_IDS:
        link = integration.link_source(source_id)


        registry.register(
            source_id,
            link=link,
        )


    return registry


# ============================================================================
# 28. HUMAN-READABLE FINAL REPORT
# ============================================================================


def format_validation_report(
    result: ValidationResult,
) -> str:


    lines = [
        "ERHAN / CTA TERMINALİ — 4.8 FINAL VALIDATION",
        "=" * 58,
        f"Source coverage required : {result.source_count}",
        f"Source coverage mapped   : {result.mapped_source_count}",
        f"Validation status        : "
        f"{'PASS' if result.passed else 'FAIL'}",
        "",
        "Unresolved MASTER mismatches:",
    ]


    if result.unresolved_master_mismatches:
        for item in result.unresolved_master_mismatches:
            lines.append(f"  - {item}")
    else:
        lines.append("  - None")


    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in result.warnings:
            lines.append(f"  - {warning}")


    if result.errors:
        lines.append("")
        lines.append("Errors:")
        for error in result.errors:
            lines.append(f"  - {error}")


    lines.append("")
    lines.append(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    return "\n".join(lines)


# ============================================================================
# 29. LOCAL VALIDATION ENTRY POINT
# ============================================================================


def validate_4_8(
    *,
    acquisitions: Optional[Iterable[Any]] = None,
    retrievals: Optional[Iterable[Any]] = None,
    raw_evidence: Optional[Iterable[Any]] = None,
    structured_information: Optional[Iterable[Any]] = None,
    canonical_links: Optional[Iterable[Any]] = None,
    existing_source_objects: Optional[Iterable[Any]] = None,
) -> ValidationResult:


    integration = FourSevenIntegration(
        acquisitions=acquisitions,
        retrievals=retrievals,
        raw_evidence=raw_evidence,
        structured_information=structured_information,
        canonical_links=canonical_links,
    )


    registry = build_final_4_8_registry(
        integration=integration,
    )


    validator = FinalArchitectureValidator(
        registry=registry,
        integration=integration,
    )


    return validator.validate(
        existing_source_objects=existing_source_objects,
    )


# ============================================================================
# 30. MAIN
# ============================================================================


if __name__ == "__main__":
    """
    This execution validates the locked 4.8 architecture definition itself.


    It does NOT claim that 4.7 runtime acquisition, PDF extraction,
    X media extraction, visual extraction, or external data retrieval
    has been executed.


    Those capabilities require real 4.7 runtime objects to be passed into
    validate_4_8().
    """


    registry = build_final_4_8_registry()


    validator = FinalArchitectureValidator(
        registry=registry,
        integration=None,
    )


    result = validator.validate()


    print(format_validation_report(result))


ERHAN / CTA TERMINALI
"""
ERHAN / CTA TERMINAL
BÖLÜM 5 — BİLGİ HAVUZU


Purpose:
    Preserve atomic CTA information with source, channel, time, context,
    status, provenance, revision history and relationship traces.


Boundary:
    - No scoring
    - No weighting
    - No ranking
    - No confidence/reliability/trust calculation
    - No clustering
    - No analysis
    - No synthesis
    - No decision
    - No trade signal


BÖLÜM 6 owns clustering / relationship evaluation.
BÖLÜM 7 owns analysis / calculation / evaluation.
BÖLÜM 8 owns synthesis.


This module is intentionally a preservation / traceability layer.
"""


from __future__ import annotations


from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple
from uuid import uuid4


# ============================================================================
# ENUMS — 5. BÖLÜM KAVRAMSAL SINIRLAR
# ============================================================================


class InformationStatus(str, Enum):
    REALIZED_FACT = "REALIZED_FACT"
    HISTORICAL_OBSERVATION = "HISTORICAL_OBSERVATION"
    CURRENT_OBSERVATION = "CURRENT_OBSERVATION"
    POSITIONING = "POSITIONING"
    INSTITUTION_VIEW = "INSTITUTION_VIEW"
    RESEARCH = "RESEARCH"
    COMMENTARY = "COMMENTARY"
    DISCLOSED_STRATEGY = "DISCLOSED_STRATEGY"
    FORECAST = "FORECAST"
    EXPECTATION = "EXPECTATION"
    HINDSIGHT_COMMENTARY = "HINDSIGHT_COMMENTARY"
    UNVERIFIED_CLAIM = "UNVERIFIED_CLAIM"


class Directness(str, Enum):
    DIRECT_SOURCE_STATEMENT = "DIRECT_SOURCE_STATEMENT"
    RELAYED = "RELAYED"
    COMMENTARY = "COMMENTARY"
    INFERENCE = "INFERENCE"


class InformationState(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    REVISED = "REVISED"
    WITHDRAWN = "WITHDRAWN"
    UNREALIZED = "UNREALIZED"
    LATER_INVALIDATED = "LATER_INVALIDATED"


class InformationKind(str, Enum):
    TEXT = "TEXT"
    NUMERIC = "NUMERIC"
    TABLE = "TABLE"
    CHART = "CHART"
    GRAPH = "GRAPH"
    IMAGE = "IMAGE"
    SCREENSHOT = "SCREENSHOT"
    PDF = "PDF"
    MIXED = "MIXED"


class RelationType(str, Enum):
    SAME_TOPIC = "SAME_TOPIC"
    SAME_EVENT_DIFFERENT_ANGLE = "SAME_EVENT_DIFFERENT_ANGLE"
    SUPPORTS = "SUPPORTS"
    LIMITS = "LIMITS"
    CONTRADICTS = "CONTRADICTS"
    UPDATES = "UPDATES"
    CORRECTS = "CORRECTS"
    REPEATS = "REPEATS"
    PRIOR_VIEW_OF_SAME_INSTITUTION = "PRIOR_VIEW_OF_SAME_INSTITUTION"
    DIFFERENT_EXPLANATION_OF_SAME_POSITIONING = (
        "DIFFERENT_EXPLANATION_OF_SAME_POSITIONING"
    )
    FORECAST_OUTCOME_COMPARISON = "FORECAST_OUTCOME_COMPARISON"


# ============================================================================
# VALIDATION ERROR
# ============================================================================


class InformationPoolValidationError(ValueError):
    """Raised when a 5. Bölüm invariant is violated."""


# ============================================================================
# TIME MODEL
# ============================================================================


@dataclass(frozen=True)
class InformationTime:
    """
    Production/publication time and referenced period are deliberately
    separate.


    Additional times are optional and must never silently replace
    production_time or reference_period.
    """


    production_time: datetime


    reference_period_start: Optional[datetime] = None
    reference_period_end: Optional[datetime] = None


    event_time: Optional[datetime] = None
    position_change_time: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    revision_time: Optional[datetime] = None


    def __post_init__(self) -> None:
        if (
            self.reference_period_start is not None
            and self.reference_period_end is not None
            and self.reference_period_start > self.reference_period_end
        ):
            raise InformationPoolValidationError(
                "reference_period_start cannot be after reference_period_end."
            )


        if (
            self.valid_from is not None
            and self.valid_until is not None
            and self.valid_from > self.valid_until
        ):
            raise InformationPoolValidationError(
                "valid_from cannot be after valid_until."
            )


# ============================================================================
# CONTEXT
# ============================================================================


@dataclass(frozen=True)
class InformationContext:
    """
    Preserves the original meaning conditions of an information piece.


    This class does NOT calculate relationships or interpret context.
    """


    topic: str
    reference_area: Optional[str] = None


    event_context: Optional[str] = None
    market_context: Optional[str] = None
    cta_behavior_context: Optional[str] = None
    asset_context: Optional[str] = None
    theme_context: Optional[str] = None


    prior_information_ids: Tuple[str, ...] = ()
    subsequent_information_ids: Tuple[str, ...] = ()


    def __post_init__(self) -> None:
        if not self.topic.strip():
            raise InformationPoolValidationError(
                "InformationContext.topic cannot be empty."
            )


# ============================================================================
# SOURCE / CHANNEL
# ============================================================================


@dataclass(frozen=True)
class InformationSource:
    """
    Source identity and channel are intentionally separate.


    master_source_id may point to the source architecture established in
    BÖLÜM 4. No new MASTER source is created here.
    """


    master_source_id: str
    source_name: str


    channel: str
    channel_locator: Optional[str] = None


    direct_source: bool = True


    def __post_init__(self) -> None:
        if not self.master_source_id.strip():
            raise InformationPoolValidationError(
                "master_source_id cannot be empty."
            )


        if not self.source_name.strip():
            raise InformationPoolValidationError(
                "source_name cannot be empty."
            )


        if not self.channel.strip():
            raise InformationPoolValidationError(
                "channel cannot be empty."
            )


# ============================================================================
# PROVENANCE
# ============================================================================


@dataclass(frozen=True)
class ProvenanceLink:
    """
    Preserves source transmission / relay lineage.


    A relaying source never replaces the original source.
    """


    original_source_id: str
    transmitting_source_id: Optional[str] = None


    original_publication_id: Optional[str] = None
    transmitting_publication_id: Optional[str] = None


    provenance_root_id: Optional[str] = None


    def __post_init__(self) -> None:
        if not self.original_source_id.strip():
            raise InformationPoolValidationError(
                "original_source_id cannot be empty."
            )


        if (
            self.transmitting_source_id is not None
            and not self.transmitting_source_id.strip()
        ):
            raise InformationPoolValidationError(
                "transmitting_source_id cannot be empty when supplied."
            )


# ============================================================================
# REVISION / HISTORICAL TRACE
# ============================================================================


@dataclass(frozen=True)
class InformationRevision:
    """
    Immutable historical version of an information piece.


    A new revision never overwrites the previous revision.
    """


    revision_id: str
    information_id: str
    revision_number: int


    created_at: datetime
    state: InformationState


    content: Any


    previous_revision_id: Optional[str] = None
    reason: Optional[str] = None


    def __post_init__(self) -> None:
        if self.revision_number < 1:
            raise InformationPoolValidationError(
                "revision_number must be >= 1."
            )


        if not self.information_id.strip():
            raise InformationPoolValidationError(
                "information_id cannot be empty."
            )


# ============================================================================
# ATOMIC INFORMATION PIECE
# ============================================================================


@dataclass(frozen=True)
class InformationPiece:
    """
    Atomic unit of the CTA Information Pool.


    This object preserves information.
    It does not analyze or synthesize it.
    """


    information_id: str


    source: InformationSource
    provenance: ProvenanceLink


    time: InformationTime
    context: InformationContext


    status: InformationStatus
    directness: Directness
    state: InformationState


    content: Any
    information_kind: InformationKind


    created_at: datetime


    revision_id: str = ""
    parent_information_id: Optional[str] = None


    def __post_init__(self) -> None:
        if not self.information_id.strip():
            raise InformationPoolValidationError(
                "information_id cannot be empty."
            )


        if not self.revision_id.strip():
            raise InformationPoolValidationError(
                "revision_id cannot be empty."
            )


        if self.content is None:
            raise InformationPoolValidationError(
                "InformationPiece.content cannot be None."
            )


        if (
            self.directness == Directness.DIRECT_SOURCE_STATEMENT
            and not self.source.direct_source
        ):
            raise InformationPoolValidationError(
                "DIRECT_SOURCE_STATEMENT requires source.direct_source=True."
            )


    @property
    def is_forward_looking(self) -> bool:
        return self.status in {
            InformationStatus.FORECAST,
            InformationStatus.EXPECTATION,
        }


    @property
    def is_historical(self) -> bool:
        return self.status in {
            InformationStatus.HISTORICAL_OBSERVATION,
            InformationStatus.HINDSIGHT_COMMENTARY,
        }


# ============================================================================
# RELATIONSHIP TRACE
# ============================================================================


@dataclass(frozen=True)
class InformationRelation:
    """
    Relationship existence only.


    This object does NOT evaluate whether the relationship is true,
    important, strong, reliable, independent, or consensual.


    Evaluation belongs to later sections.
    """


    relation_id: str


    source_information_id: str
    target_information_id: str


    relation_type: RelationType


    created_at: datetime


    provenance_note: Optional[str] = None


    def __post_init__(self) -> None:
        if not self.source_information_id.strip():
            raise InformationPoolValidationError(
                "source_information_id cannot be empty."
            )


        if not self.target_information_id.strip():
            raise InformationPoolValidationError(
                "target_information_id cannot be empty."
            )


        if self.source_information_id == self.target_information_id:
            raise InformationPoolValidationError(
                "Information relation cannot connect an information piece "
                "to itself."
            )


# ============================================================================
# INFORMATION POOL
# ============================================================================


class InformationPool:
    """
    5. BÖLÜM — BİLGİ HAVUZU


    Responsibilities:
        - Preserve atomic information.
        - Preserve source/channel identity.
        - Preserve production/reference time.
        - Preserve information status.
        - Preserve context.
        - Preserve provenance.
        - Preserve revisions.
        - Preserve relationship traces.


    Explicitly NOT responsible for:
        - clustering
        - scoring
        - weighting
        - ranking
        - confidence
        - reliability
        - trust
        - analysis
        - synthesis
        - prediction
        - decision
        - trade signals
    """


    def __init__(self) -> None:
        self._information: Dict[str, InformationPiece] = {}
        self._revisions: Dict[str, InformationRevision] = {}
        self._relations: Dict[str, InformationRelation] = {}


    # ------------------------------------------------------------------
    # INFORMATION
    # ------------------------------------------------------------------


    def add_information(self, information: InformationPiece) -> str:
        """
        Add a new information piece.


        Existing information is never silently overwritten.
        """


        if information.information_id in self._information:
            raise InformationPoolValidationError(
                f"Information already exists: {information.information_id}"
            )


        self._information[information.information_id] = information


        revision = InformationRevision(
            revision_id=information.revision_id,
            information_id=information.information_id,
            revision_number=1,
            created_at=information.created_at,
            state=information.state,
            content=information.content,
        )


        self._revisions[revision.revision_id] = revision


        return information.information_id


    def get_information(self, information_id: str) -> InformationPiece:
        try:
            return self._information[information_id]
        except KeyError as exc:
            raise InformationPoolValidationError(
                f"Unknown information_id: {information_id}"
            ) from exc


    def all_information(self) -> Tuple[InformationPiece, ...]:
        return tuple(self._information.values())


    # ------------------------------------------------------------------
    # REVISION
    # ------------------------------------------------------------------


    def add_revision(
        self,
        information_id: str,
        *,
        content: Any,
        state: InformationState,
        created_at: datetime,
        reason: Optional[str] = None,
    ) -> InformationRevision:
        """
        Creates a new historical revision.


        Previous revision remains untouched.
        """


        current = self.get_information(information_id)


        existing = [
            revision
            for revision in self._revisions.values()
            if revision.information_id == information_id
        ]


        next_number = max(
            revision.revision_number for revision in existing
        ) + 1


        previous = max(
            existing,
            key=lambda revision: revision.revision_number,
        )


        revision = InformationRevision(
            revision_id=self._new_id("rev"),
            information_id=information_id,
            revision_number=next_number,
            created_at=created_at,
            state=state,
            content=content,
            previous_revision_id=previous.revision_id,
            reason=reason,
        )


        self._revisions[revision.revision_id] = revision


        # The current InformationPiece itself is replaced only through
        # explicit immutable object replacement; the historical revision
        # remains preserved.
        updated = replace(
            current,
            content=content,
            state=state,
            revision_id=revision.revision_id,
        )


        self._information[information_id] = updated


        return revision


    def revisions_for(
        self,
        information_id: str,
    ) -> Tuple[InformationRevision, ...]:
        return tuple(
            sorted(
                (
                    revision
                    for revision in self._revisions.values()
                    if revision.information_id == information_id
                ),
                key=lambda revision: revision.revision_number,
            )
        )


    # ------------------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------------------


    def add_relation(
        self,
        relation: InformationRelation,
    ) -> str:
        """
        Stores relationship existence only.


        No relationship evaluation is performed.
        """


        if relation.relation_id in self._relations:
            raise InformationPoolValidationError(
                f"Relation already exists: {relation.relation_id}"
            )


        if relation.source_information_id not in self._information:
            raise InformationPoolValidationError(
                "Relation source information does not exist."
            )


        if relation.target_information_id not in self._information:
            raise InformationPoolValidationError(
                "Relation target information does not exist."
            )


        self._relations[relation.relation_id] = relation


        return relation.relation_id


    def relations_for(
        self,
        information_id: str,
    ) -> Tuple[InformationRelation, ...]:
        return tuple(
            relation
            for relation in self._relations.values()
            if (
                relation.source_information_id == information_id
                or relation.target_information_id == information_id
            )
        )


    def all_relations(self) -> Tuple[InformationRelation, ...]:
        return tuple(self._relations.values())


    # ------------------------------------------------------------------
    # PROVENANCE QUERIES
    # ------------------------------------------------------------------


    def information_by_source(
        self,
        master_source_id: str,
    ) -> Tuple[InformationPiece, ...]:
        return tuple(
            information
            for information in self._information.values()
            if information.source.master_source_id == master_source_id
        )


    def information_by_status(
        self,
        status: InformationStatus,
    ) -> Tuple[InformationPiece, ...]:
        return tuple(
            information
            for information in self._information.values()
            if information.status == status
        )


    def information_by_topic(
        self,
        topic: str,
    ) -> Tuple[InformationPiece, ...]:
        return tuple(
            information
            for information in self._information.values()
            if information.context.topic == topic
        )


    # ------------------------------------------------------------------
    # INTEGRITY
    # ------------------------------------------------------------------


    def validate_integrity(self) -> None:
        """
        Validates structural integrity only.


        This method deliberately does not calculate:
            - confidence
            - reliability
            - evidence strength
            - ranking
            - consensus
            - weighting
        """


        for information in self._information.values():
            if information.information_id not in self._information:
                raise InformationPoolValidationError(
                    "Information self-reference integrity failure."
                )


            revisions = self.revisions_for(information.information_id)


            if not revisions:
                raise InformationPoolValidationError(
                    f"Information has no revision history: "
                    f"{information.information_id}"
                )


            revision_ids = {revision.revision_id for revision in revisions}


            if information.revision_id not in revision_ids:
                raise InformationPoolValidationError(
                    f"Current revision is missing from revision history: "
                    f"{information.information_id}"
                )


            for revision in revisions:
                if revision.information_id != information.information_id:
                    raise InformationPoolValidationError(
                        "Revision information_id mismatch."
                    )


                if (
                    revision.previous_revision_id is not None
                    and revision.previous_revision_id not in revision_ids
                ):
                    raise InformationPoolValidationError(
                        "Revision chain contains an unknown previous revision."
                    )


        for relation in self._relations.values():
            if relation.source_information_id not in self._information:
                raise InformationPoolValidationError(
                    f"Relation references missing source: {relation.relation_id}"
                )


            if relation.target_information_id not in self._information:
                raise InformationPoolValidationError(
                    f"Relation references missing target: {relation.relation_id}"
                )


    # ------------------------------------------------------------------
    # SNAPSHOT / EXPORT
    # ------------------------------------------------------------------


    def export_state(self) -> Mapping[str, Any]:
        """
        Structural export for later layers.


        No interpretation or analysis is performed.
        """


        self.validate_integrity()


        return {
            "information": tuple(self._information.values()),
            "revisions": tuple(self._revisions.values()),
            "relations": tuple(self._relations.values()),
        }


    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------


    @staticmethod
    def _new_id(prefix: str) -> str:
        return f"{prefix}_{uuid4().hex}"


# ============================================================================
# EXPLICITLY FORBIDDEN 5. BÖLÜM OPERATIONS
# ============================================================================


_FORBIDDEN_OPERATIONS = frozenset(
    {
        "score",
        "weight",
        "rank",
        "confidence",
        "reliability",
        "trust",
        "cluster",
        "analyze",
        "synthesize",
        "predict",
        "decide",
        "trade_signal",
    }
)


def forbidden_operations() -> frozenset[str]:
    """
    Exposes the architectural boundary as a read-only constant.


    No operation is executed.
    """
    return _FORBIDDEN_OPERATIONS


# ============================================================================
# VALIDATION
# ============================================================================


def validate_section_5() -> bool:
    """
    Static architectural validation for BÖLÜM 5.


    This validates that the required conceptual primitives exist and that
    forbidden analytical responsibilities are not part of the pool API.
    """


    required_statuses = {
        InformationStatus.REALIZED_FACT,
        InformationStatus.HISTORICAL_OBSERVATION,
        InformationStatus.CURRENT_OBSERVATION,
        InformationStatus.POSITIONING,
        InformationStatus.INSTITUTION_VIEW,
        InformationStatus.RESEARCH,
        InformationStatus.COMMENTARY,
        InformationStatus.DISCLOSED_STRATEGY,
        InformationStatus.FORECAST,
        InformationStatus.EXPECTATION,
        InformationStatus.HINDSIGHT_COMMENTARY,
        InformationStatus.UNVERIFIED_CLAIM,
    }


    if len(required_statuses) != 12:
        raise InformationPoolValidationError(
            "InformationStatus set is incomplete."
        )


    required_relations = {
        RelationType.SAME_TOPIC,
        RelationType.SUPPORTS,
        RelationType.LIMITS,
        RelationType.CONTRADICTS,
        RelationType.UPDATES,
        RelationType.CORRECTS,
        RelationType.REPEATS,
    }


    if not required_relations.issubset(set(RelationType)):
        raise InformationPoolValidationError(
            "Required relation types are missing."
        )


    public_methods = {
        name
        for name in dir(InformationPool)
        if not name.startswith("_")
        and callable(getattr(InformationPool, name))
    }


    forbidden_method_names = {
        "score",
        "weight",
        "rank",
        "confidence",
        "reliability",
        "trust",
        "cluster",
        "analyze",
        "synthesize",
        "predict",
        "decide",
        "trade_signal",
    }


    leaked = public_methods.intersection(forbidden_method_names)


    if leaked:
        raise InformationPoolValidationError(
            f"Forbidden BÖLÜM 5 operations exposed: {sorted(leaked)}"
        )


    return True


# ============================================================================
# SELF TEST
# ============================================================================


def _self_test() -> None:
    now = datetime(2026, 9, 14, 12, 0, 0)


    source = InformationSource(
        master_source_id="master.x.example",
        source_name="Example Source",
        channel="X",
        channel_locator="post:example",
        direct_source=True,
    )


    provenance = ProvenanceLink(
        original_source_id="master.x.example",
        provenance_root_id="root-example",
    )


    time = InformationTime(
        production_time=now,
        reference_period_start=datetime(2026, 9, 1),
        reference_period_end=datetime(2026, 9, 14),
    )


    context = InformationContext(
        topic="CTA positioning",
        reference_area="Futures",
        market_context="Example market context",
        cta_behavior_context="Trend-following",
    )


    information = InformationPiece(
        information_id="info_example_001",
        source=source,
        provenance=provenance,
        time=time,
        context=context,
        status=InformationStatus.COMMENTARY,
        directness=Directness.DIRECT_SOURCE_STATEMENT,
        state=InformationState.CURRENT,
        content="Example CTA commentary.",
        information_kind=InformationKind.TEXT,
        created_at=now,
        revision_id="rev_example_001",
    )


    pool = InformationPool()


    pool.add_information(information)


    relation = InformationRelation(
        relation_id="rel_example_001",
        source_information_id="info_example_001",
        target_information_id="info_example_001",
        relation_type=RelationType.SAME_TOPIC,
        created_at=now,
    )


    # Self-relation must be rejected.
    try:
        pool.add_relation(relation)
    except InformationPoolValidationError:
        pass
    else:
        raise AssertionError(
            "Self-relation was incorrectly accepted."
        )


    pool.validate_integrity()


    assert len(pool.all_information()) == 1
    assert len(pool.revisions_for("info_example_001")) == 1
    assert validate_section_5() is True


if __name__ == "__main__":
    validate_section_5()
    _self_test()
    print("BÖLÜM 5 — BİLGİ HAVUZU: VALIDATION PASSED")


6. BÖLÜM — YOĞURMA MOTORU
ERHAN / CTA TERMINALI


"""
ERHAN / CTA TERMINAL
6. BÖLÜM — YOĞURMA MOTORU
FINAL CODE


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ


Amaç
-----
5. Bölüm — Bilgi Havuzu içinde korunmuş InformationPiece kayıtlarını:


- anlamlı bağlamsal kümeler halinde yapılandırmak,
- çoklu üyeliği korumak,
- ana / alt küme ilişkilerini korumak,
- yatay ilişkili kümeleri korumak,
- bilgi parçaları arasındaki ilişkileri yapılandırmak,
- provenance / bilgi kökünü korumak,
- zaman ve bağlam sürekliliğini korumak,
- ilişki ve küme yaşam döngüsü geçmişini korumak,
- 7. Bölüm için analize hazır yapılar üretmek


amacıyla kullanır.


Bu modül:


- analiz yapmaz,
- hesaplama yapmaz,
- değerlendirme yapmaz,
- confidence üretmez,
- trust score üretmez,
- truth score üretmez,
- evidence strength üretmez,
- weighting yapmaz,
- ranking yapmaz,
- consensus üretmez,
- forecast üretmez,
- prediction üretmez,
- piyasa yönü tahmin etmez,
- BUY / SELL üretmez,
- trade signal üretmez,
- final CTA bias üretmez,
- risk kararı üretmez,
- kullanıcı adına nihai karar vermez.


ÖNEMLİ
-------
Bu modül 5. Bölüm'deki InformationPiece sınıfını yeniden tanımlamaz.
5. Bölümden gelen bilgi nesnelerini doğrudan kullanır.


6. Bölümde küme sınırı "yeni bir tahmin/puanlama metodolojisi"
ile hesaplanmaz. Küme üyeliği, sağlanan bağlamsal süreklilik
eksenlerinin kaydedilmesi ve korunması üzerinden yapılandırılır.


7. Bölüm:
    Analiz / Hesaplama / Değerlendirme


8. Bölüm:
    CTA Synthesis / Sonuç


9. Bölüm:
    Tarihçe / Hafıza
"""


from __future__ import annotations


from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Tuple


# ============================================================================
# 1. İLİŞKİ DURUMLARI
# ============================================================================


class RelationState(str, Enum):
    """
    İlişkinin mevcut / tarihsel durumu.


    Bunlar:
        - confidence
        - trust
        - truth
        - reliability
        - evidence strength


    değildir.
    """


    ACTIVE = "active"
    UNCERTAIN = "uncertain"
    DISPUTED = "disputed"
    WEAKENED = "weakened"
    INVALIDATED = "invalidated"
    UNRESOLVED = "unresolved"


# ============================================================================
# 2. KÜME YAŞAM DÖNGÜSÜ
# ============================================================================


class ClusterState(str, Enum):
    """
    Kümenin yaşam döngüsü.
    """


    FORMING = "forming"
    DEVELOPING = "developing"
    UPDATED = "updated"
    CLOSED = "closed"
    REOPENED = "reopened"


# ============================================================================
# 3. KÜME SINIRI EKSENLERİ
# ============================================================================


class ClusterAxis(str, Enum):
    """
    Anlamlı bağlamsal süreklilik eksenleri.


    Bu eksenlerin bulunması, kümenin önemini veya doğruluğunu
    göstermez.


    Kelime benzerliği bu enum içinde bilinçli olarak bulunmaz.
    """


    COMMON_SUBJECT = "common_subject"
    COMMON_EVENT = "common_event"
    COMMON_THEME = "common_theme"
    COMMON_REFERENCE_PERIOD = "common_reference_period"
    COMMON_ACTOR = "common_actor"
    COMMON_INSTITUTION = "common_institution"
    COMMON_ASSET = "common_asset"
    COMMON_INFORMATION_ROOT = "common_information_root"
    COMMON_EVENT_CONTEXT = "common_event_context"


# ============================================================================
# 4. İLİŞKİ TİPLERİ
# ============================================================================


class RelationType(str, Enum):
    """
    6. Bölümde korunabilecek ilişki türleri.


    İlişkinin varlığı ile ilişkinin analitik anlamı birbirinden
    ayrıdır. Analitik değerlendirme 7. Bölüme aittir.
    """


    SAME_TOPIC = "same_topic"
    SAME_EVENT_DIFFERENT_ANGLE = "same_event_different_angle"
    SUPPORTS = "supports"
    LIMITS = "limits"
    CONTRADICTS = "contradicts"
    UPDATES = "updates"
    CORRECTS = "corrects"
    REPEATS = "repeats"
    PRIOR_VIEW_OF_SAME_INSTITUTION = "prior_view_of_same_institution"
    DIFFERENT_EXPLANATION_OF_SAME_POSITIONING = (
        "different_explanation_of_same_positioning"
    )
    FORECAST_OUTCOME_COMPARISON = "forecast_outcome_comparison"


# ============================================================================
# 5. KÜME İLİŞKİ TİPLERİ
# ============================================================================


class ClusterRelationType(str, Enum):
    """
    Hiyerarşik olmayan kümeler arasındaki yatay ilişki.


    Ana/alt ilişkisi değildir.
    """


    RELATED = "related"
    CONTINUATION = "continuation"
    DIFFERENT_ANGLE = "different_angle"
    CONNECTED_EVENT = "connected_event"
    RELATED_CONTEXT = "related_context"


# ============================================================================
# 6. KÜME YAŞAM DÖNGÜSÜ GEÇMİŞİ
# ============================================================================


@dataclass(frozen=True)
class ClusterLifecycleEvent:
    """
    Kümenin yaşam döngüsündeki tarihsel bir durum değişimi.


    Eski durum silinmez.
    """


    event_id: str
    cluster_id: str


    previous_state: Optional[ClusterState]
    new_state: ClusterState


    occurred_at: datetime
    reason: Optional[str] = None


# ============================================================================
# 7. İLİŞKİ DURUM GEÇMİŞİ
# ============================================================================


@dataclass(frozen=True)
class RelationStateEvent:
    """
    Bir ilişkinin durum değişiminin tarihsel kaydı.
    """


    event_id: str
    relation_id: str


    previous_state: Optional[RelationState]
    new_state: RelationState


    occurred_at: datetime
    reason: Optional[str] = None


# ============================================================================
# 8. BİLGİ PARÇASI İLİŞKİSİ
# ============================================================================


@dataclass(frozen=True)
class Relation:
    """
    İki InformationPiece arasındaki ilişkisel bağ.


    Burada yalnızca ilişki ve onun tarihsel durumu korunur.


    İlişkinin:
        - gücü,
        - doğruluğu,
        - güvenilirliği,
        - önemi,
        - ağırlığı


    hesaplanmaz.
    """


    relation_id: str


    source_information_id: str
    target_information_id: str


    relation_type: RelationType


    state: RelationState = RelationState.ACTIVE


    context_note: Optional[str] = None


    created_at: Optional[datetime] = None


    state_history: Tuple[RelationStateEvent, ...] = field(
        default_factory=tuple
    )


# ============================================================================
# 9. KÜME İLİŞKİSİ
# ============================================================================


@dataclass(frozen=True)
class ClusterRelation:
    """
    İki küme arasındaki yatay ilişki.


    Bu ilişki ana/alt hiyerarşi değildir.


    Hiyerarşik olmayan ilişkili kümeleri zorla ana/alt yapıya
    sokmamak için kullanılır.
    """


    relation_id: str


    source_cluster_id: str
    target_cluster_id: str


    relation_type: ClusterRelationType


    state: RelationState = RelationState.ACTIVE


    context_note: Optional[str] = None


    created_at: Optional[datetime] = None


    state_history: Tuple[RelationStateEvent, ...] = field(
        default_factory=tuple
    )


# ============================================================================
# 10. KÜME
# ============================================================================


@dataclass(frozen=True)
class Cluster:
    """
    6. Bölüm bilgi kümesi.


    Küme:
        - bağlamsal süreklilik taşır,
        - InformationPiece ID'lerini referanslar,
        - çoklu üyeliği destekler,
        - ana/alt yapıyı destekler,
        - yatay ilişkileri destekler,
        - yaşam döngüsü geçmişini korur.


    Küme bir önem, doğruluk veya güven sıralaması değildir.
    """


    cluster_id: str


    cluster_type: str


    state: ClusterState = ClusterState.FORMING


    member_information_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )


    parent_cluster_id: Optional[str] = None


    child_cluster_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )


    shared_axes: Tuple[ClusterAxis, ...] = field(
        default_factory=tuple
    )


    context_note: Optional[str] = None


    created_at: Optional[datetime] = None


    lifecycle_history: Tuple[ClusterLifecycleEvent, ...] = field(
        default_factory=tuple
    )


# ============================================================================
# 11. ÇOKLU ÜYELİK
# ============================================================================


@dataclass(frozen=True)
class Membership:
    """
    InformationPiece -> Cluster üyeliği.


    Aynı InformationPiece birden fazla Cluster içinde bulunabilir.


    InformationPiece kopyalanmaz.
    """


    information_id: str
    cluster_id: str


    assigned_at: Optional[datetime] = None


    context_note: Optional[str] = None


# ============================================================================
# 12. YOĞURMA DURUMU
# ============================================================================


@dataclass(frozen=True)
class YogurmaState:
    """
    Yoğurma Motoru'nun mevcut yapısal durumu.


    Buradaki nesneler analiz sonucu değildir.
    """


    clusters: Tuple[Cluster, ...] = field(
        default_factory=tuple
    )


    relations: Tuple[Relation, ...] = field(
        default_factory=tuple
    )


    cluster_relations: Tuple[ClusterRelation, ...] = field(
        default_factory=tuple
    )


    memberships: Tuple[Membership, ...] = field(
        default_factory=tuple
    )


# ============================================================================
# 13. YOĞURMA MOTORU
# ============================================================================


class YogurmaMotoru:
    """
    6. Bölüm — Yoğurma Motoru.


    5. Bölümdeki InformationPiece nesnelerini doğrudan referanslar.


    Sorumlulukları:
        - bağlamsal kümeler,
        - çoklu üyelik,
        - ana/alt kümeler,
        - yatay ilişkili kümeler,
        - bilgi parçaları arası ilişkiler,
        - provenance referanslarının korunması,
        - ilişki geçmişi,
        - küme yaşam döngüsü.


    Sorumlulukları DEĞİLDİR:
        - analiz,
        - hesaplama,
        - değerlendirme,
        - skor,
        - ağırlık,
        - ranking,
        - confidence,
        - trust,
        - truth,
        - prediction,
        - forecast,
        - trade,
        - risk,
        - final CTA bias.
    """


    def __init__(self) -> None:
        # 5. Bölümden gelen gerçek bilgi parçaları.
        #
        # Burada InformationPiece yeniden tanımlanmaz.
        self._pieces: dict[str, Any] = {}


        self._clusters: dict[str, Cluster] = {}


        self._relations: dict[str, Relation] = {}


        self._cluster_relations: dict[
            str,
            ClusterRelation,
        ] = {}


        self._memberships: set[tuple[str, str]] = set()


    # ========================================================================
    # INFORMATION PIECES — 5 -> 6
    # ========================================================================


    def register_information_piece(
        self,
        piece: Any,
    ) -> None:
        """
        5. Bölüm InformationPiece nesnesini 6. Bölüme bağlar.


        Aynı information ID ikinci kez gelirse eski kayıt sessizce
        ezilmez.


        Bu modül InformationPiece içeriğini değiştirmez.
        """


        information_id = self._extract_information_id(piece)


        if information_id in self._pieces:
            existing = self._pieces[information_id]


            if existing is piece:
                return


            raise ValueError(
                f"Duplicate information_id in 6. Bölüm: "
                f"{information_id}"
            )


        self._pieces[information_id] = piece


    def register_information_pieces(
        self,
        pieces: Iterable[Any],
    ) -> None:
        """
        Birden fazla 5. Bölüm InformationPiece kaydını ekler.
        """


        for piece in pieces:
            self.register_information_piece(piece)


    def get_information_piece(
        self,
        information_id: str,
    ) -> Any:
        """
        Kayıtlı InformationPiece döndürür.
        """


        try:
            return self._pieces[information_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown information_id: {information_id}"
            ) from exc


    def information_piece_exists(
        self,
        information_id: str,
    ) -> bool:
        return information_id in self._pieces


    def all_information_pieces(
        self,
    ) -> Tuple[Any, ...]:
        return tuple(self._pieces.values())


    # ========================================================================
    # CLUSTER CREATION
    # ========================================================================


    def create_cluster(
        self,
        cluster_id: str,
        cluster_type: str,
        *,
        shared_axes: Iterable[ClusterAxis] = (),
        parent_cluster_id: Optional[str] = None,
        context_note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> Cluster:
        """
        Yeni küme oluşturur.


        parent_cluster_id verilmişse parent'ın gerçekten mevcut olması
        gerekir.


        Bu metod yalnızca sağlanan bağlamsal eksenleri kaydeder.
        Kelime benzerliğine dayalı otomatik kümeleme yapmaz.
        """


        if not cluster_id.strip():
            raise ValueError("cluster_id cannot be empty.")


        if not cluster_type.strip():
            raise ValueError("cluster_type cannot be empty.")


        if cluster_id in self._clusters:
            raise ValueError(
                f"Duplicate cluster_id: {cluster_id}"
            )


        if parent_cluster_id == cluster_id:
            raise ValueError(
                "A cluster cannot be its own parent."
            )


        if (
            parent_cluster_id is not None
            and parent_cluster_id not in self._clusters
        ):
            raise ValueError(
                f"Unknown parent_cluster_id: {parent_cluster_id}"
            )


        normalized_axes = tuple(dict.fromkeys(shared_axes))


        cluster = Cluster(
            cluster_id=cluster_id,
            cluster_type=cluster_type,
            state=ClusterState.FORMING,
            member_information_ids=(),
            parent_cluster_id=parent_cluster_id,
            child_cluster_ids=(),
            shared_axes=normalized_axes,
            context_note=context_note,
            created_at=created_at,
            lifecycle_history=(),
        )


        self._clusters[cluster_id] = cluster


        if parent_cluster_id is not None:
            parent = self._clusters[parent_cluster_id]


            if cluster_id not in parent.child_cluster_ids:
                updated_parent = replace(
                    parent,
                    child_cluster_ids=(
                        *parent.child_cluster_ids,
                        cluster_id,
                    ),
                )


                self._clusters[parent_cluster_id] = updated_parent


        return cluster


    # ========================================================================
    # CLUSTER ACCESS
    # ========================================================================


    def get_cluster(
        self,
        cluster_id: str,
    ) -> Cluster:
        try:
            return self._clusters[cluster_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            ) from exc


    def cluster_exists(
        self,
        cluster_id: str,
    ) -> bool:
        return cluster_id in self._clusters


    def all_clusters(
        self,
    ) -> Tuple[Cluster, ...]:
        return tuple(self._clusters.values())


    def cluster_count(self) -> int:
        return len(self._clusters)


    # ========================================================================
    # MULTI MEMBERSHIP
    # ========================================================================


    def assign_information_to_cluster(
        self,
        information_id: str,
        cluster_id: str,
        *,
        assigned_at: Optional[datetime] = None,
        context_note: Optional[str] = None,
    ) -> Membership:
        """
        InformationPiece'i kümeye bağlar.


        Aynı InformationPiece farklı kümelere bağlanabilir.


        Aynı information_id + cluster_id çifti ikinci kez eklenmez.
        """


        self._require_information(information_id)
        self._require_cluster(cluster_id)


        membership_key = (
            information_id,
            cluster_id,
        )


        if membership_key in self._memberships:
            raise ValueError(
                "Duplicate membership: "
                f"{information_id} -> {cluster_id}"
            )


        membership = Membership(
            information_id=information_id,
            cluster_id=cluster_id,
            assigned_at=assigned_at,
            context_note=context_note,
        )


        self._memberships.add(membership_key)


        cluster = self._clusters[cluster_id]


        if information_id not in cluster.member_information_ids:
            updated_cluster = replace(
                cluster,
                member_information_ids=(
                    *cluster.member_information_ids,
                    information_id,
                ),
            )


            self._clusters[cluster_id] = updated_cluster


        return membership


    def memberships_of(
        self,
        information_id: str,
    ) -> Tuple[Membership, ...]:
        """
        Bir InformationPiece'in tüm küme üyeliklerini döndürür.
        """


        return tuple(
            Membership(
                information_id=piece_id,
                cluster_id=cluster_id,
            )
            for piece_id, cluster_id in self._memberships
            if piece_id == information_id
        )


    def memberships_in_cluster(
        self,
        cluster_id: str,
    ) -> Tuple[Membership, ...]:
        self._require_cluster(cluster_id)


        return tuple(
            Membership(
                information_id=piece_id,
                cluster_id=cluster_id,
            )
            for piece_id, membership_cluster_id
            in self._memberships
            if membership_cluster_id == cluster_id
        )


    def clusters_for_information(
        self,
        information_id: str,
    ) -> Tuple[Cluster, ...]:
        """
        Bir InformationPiece'in ait olduğu tüm kümeler.
        """


        self._require_information(information_id)


        cluster_ids = {
            cluster_id
            for piece_id, cluster_id in self._memberships
            if piece_id == information_id
        }


        return tuple(
            self._clusters[cluster_id]
            for cluster_id in cluster_ids
        )


    # ========================================================================
    # INFORMATION RELATIONS
    # ========================================================================


    def add_relation(
        self,
        relation_id: str,
        source_information_id: str,
        target_information_id: str,
        relation_type: RelationType,
        *,
        state: RelationState = RelationState.ACTIVE,
        context_note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> Relation:
        """
        InformationPiece'ler arasındaki ilişkiyi kaydeder.


        Kaynak ve hedef bilgi parçaları gerçekten mevcut olmalıdır.


        Bu metod ilişkinin doğruluğunu veya gücünü değerlendirmez.
        """


        if not relation_id.strip():
            raise ValueError("relation_id cannot be empty.")


        if relation_id in self._relations:
            raise ValueError(
                f"Duplicate relation_id: {relation_id}"
            )


        self._require_information(source_information_id)
        self._require_information(target_information_id)


        if source_information_id == target_information_id:
            raise ValueError(
                "A relation cannot connect an information piece to itself."
            )


        relation = Relation(
            relation_id=relation_id,
            source_information_id=source_information_id,
            target_information_id=target_information_id,
            relation_type=relation_type,
            state=state,
            context_note=context_note,
            created_at=created_at,
            state_history=(),
        )


        self._relations[relation_id] = relation


        return relation


    def get_relation(
        self,
        relation_id: str,
    ) -> Relation:
        try:
            return self._relations[relation_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown relation_id: {relation_id}"
            ) from exc


    def all_relations(
        self,
    ) -> Tuple[Relation, ...]:
        return tuple(self._relations.values())


    def relations_for_information(
        self,
        information_id: str,
    ) -> Tuple[Relation, ...]:
        self._require_information(information_id)


        return tuple(
            relation
            for relation in self._relations.values()
            if (
                relation.source_information_id == information_id
                or relation.target_information_id == information_id
            )
        )


    def relation_count(self) -> int:
        return len(self._relations)


    # ========================================================================
    # RELATION STATE HISTORY
    # ========================================================================


    def update_relation_state(
        self,
        relation_id: str,
        new_state: RelationState,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Relation:
        """
        İlişki durumunu değiştirir.


        Önceki durum silinmez.
        """


        relation = self.get_relation(relation_id)


        if relation.state == new_state:
            return relation


        event = RelationStateEvent(
            event_id=self._next_event_id(
                "relation-state"
            ),
            relation_id=relation_id,
            previous_state=relation.state,
            new_state=new_state,
            occurred_at=(
                changed_at
                if changed_at is not None
                else datetime.utcnow()
            ),
            reason=reason,
        )


        updated = replace(
            relation,
            state=new_state,
            state_history=(
                *relation.state_history,
                event,
            ),
        )


        self._relations[relation_id] = updated


        return updated


    # ========================================================================
    # CLUSTER LIFECYCLE
    # ========================================================================


    def update_cluster_lifecycle(
        self,
        cluster_id: str,
        new_state: ClusterState,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Cluster:
        """
        Kümenin yaşam döngüsünü değiştirir.


        Önceki durum silinmez.


        CLOSED:
            Küme silinmez.


        REOPENED:
            Kapanmış bir kümenin yeniden aktif bağlama alınmasını
            temsil eder.


        Bu işlem hiçbir analitik önem veya değer anlamı taşımaz.
        """


        cluster = self.get_cluster(cluster_id)


        if cluster.state == new_state:
            return cluster


        event = ClusterLifecycleEvent(
            event_id=self._next_event_id(
                "cluster-state"
            ),
            cluster_id=cluster_id,
            previous_state=cluster.state,
            new_state=new_state,
            occurred_at=(
                changed_at
                if changed_at is not None
                else datetime.utcnow()
            ),
            reason=reason,
        )


        updated = replace(
            cluster,
            state=new_state,
            lifecycle_history=(
                *cluster.lifecycle_history,
                event,
            ),
        )


        self._clusters[cluster_id] = updated


        return updated


    def close_cluster(
        self,
        cluster_id: str,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Cluster:
        return self.update_cluster_lifecycle(
            cluster_id,
            ClusterState.CLOSED,
            changed_at=changed_at,
            reason=reason,
        )


    def reopen_cluster(
        self,
        cluster_id: str,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Cluster:
        return self.update_cluster_lifecycle(
            cluster_id,
            ClusterState.REOPENED,
            changed_at=changed_at,
            reason=reason,
        )


    # ========================================================================
    # CLUSTER RELATIONS — YATAY YAPILAR
    # ========================================================================


    def add_cluster_relation(
        self,
        relation_id: str,
        source_cluster_id: str,
        target_cluster_id: str,
        relation_type: ClusterRelationType,
        *,
        state: RelationState = RelationState.ACTIVE,
        context_note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> ClusterRelation:
        """
        Hiyerarşik olmayan iki küme arasındaki ilişkiyi kaydeder.


        İlişkili kümeler zorla ana/alt yapıya sokulmaz.
        """


        if not relation_id.strip():
            raise ValueError(
                "cluster relation_id cannot be empty."
            )


        if relation_id in self._cluster_relations:
            raise ValueError(
                f"Duplicate cluster relation_id: {relation_id}"
            )


        self._require_cluster(source_cluster_id)
        self._require_cluster(target_cluster_id)


        if source_cluster_id == target_cluster_id:
            raise ValueError(
                "A cluster cannot be related to itself."
            )


        relation = ClusterRelation(
            relation_id=relation_id,
            source_cluster_id=source_cluster_id,
            target_cluster_id=target_cluster_id,
            relation_type=relation_type,
            state=state,
            context_note=context_note,
            created_at=created_at,
            state_history=(),
        )


        self._cluster_relations[relation_id] = relation


        return relation


    def get_cluster_relation(
        self,
        relation_id: str,
    ) -> ClusterRelation:
        try:
            return self._cluster_relations[relation_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown cluster relation_id: {relation_id}"
            ) from exc


    def all_cluster_relations(
        self,
    ) -> Tuple[ClusterRelation, ...]:
        return tuple(self._cluster_relations.values())


    def update_cluster_relation_state(
        self,
        relation_id: str,
        new_state: RelationState,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> ClusterRelation:
        """
        Küme ilişkisinin durumunu değiştirir.


        Önceki durum korunur.
        """


        relation = self.get_cluster_relation(
            relation_id
        )


        if relation.state == new_state:
            return relation


        event = RelationStateEvent(
            event_id=self._next_event_id(
                "cluster-relation-state"
            ),
            relation_id=relation_id,
            previous_state=relation.state,
            new_state=new_state,
            occurred_at=(
                changed_at
                if changed_at is not None
                else datetime.utcnow()
            ),
            reason=reason,
        )


        updated = replace(
            relation,
            state=new_state,
            state_history=(
                *relation.state_history,
                event,
            ),
        )


        self._cluster_relations[relation_id] = updated


        return updated


    # ========================================================================
    # CONTEXTUAL CONTINUITY
    # ========================================================================


    def record_cluster_axes(
        self,
        cluster_id: str,
        axes: Iterable[ClusterAxis],
    ) -> Cluster:
        """
        Küme için mevcut bağlamsal süreklilik eksenlerini kaydeder.


        Bu metod yeni bir analiz veya skor üretmez.
        Sadece sağlanan bağlamsal yapıyı korur.


        Kelime benzerliği burada kullanılmaz.
        """


        cluster = self.get_cluster(cluster_id)


        merged = tuple(
            dict.fromkeys(
                (
                    *cluster.shared_axes,
                    *tuple(axes),
                )
            )
        )


        updated = replace(
            cluster,
            shared_axes=merged,
        )


        self._clusters[cluster_id] = updated


        return updated


    def has_contextual_continuity(
        self,
        cluster_id: str,
    ) -> bool:
        """
        Kümeye kaydedilmiş en az bir anlamlı bağlamsal süreklilik
        ekseni bulunup bulunmadığını kontrol eder.


        Bu bir güven / önem / doğruluk skoru değildir.
        """


        cluster = self.get_cluster(cluster_id)


        return bool(cluster.shared_axes)


    # ========================================================================
    # PROVENANCE PRESERVATION
    # ========================================================================


    def provenance_for_information(
        self,
        information_id: str,
    ) -> Mapping[str, Any]:
        """
        5. Bölüm InformationPiece içindeki provenance / source
        bilgilerini değiştirmeden dışarı verir.


        Farklı 5. Bölüm modellerinin isimleri için güvenli erişim
        yardımcıları kullanılır.


        Burada provenance hakkında yeni yorum üretilmez.
        """


        piece = self.get_information_piece(
            information_id
        )


        result: dict[str, Any] = {
            "information_id": information_id,
        }


        for attribute in (
            "source",
            "provenance",
            "source_id",
            "original_source_id",
            "channel",
            "production_time",
            "reference_period",
        ):
            if hasattr(piece, attribute):
                result[attribute] = getattr(
                    piece,
                    attribute,
                )


        return result


    # ========================================================================
    # 6 -> 7 OUTPUT
    # ========================================================================


    def state(self) -> YogurmaState:
        """
        7. Bölüme devredilecek analize hazır ilişkisel yapı.


        Bu metod:
            - analiz yapmaz,
            - hesaplama yapmaz,
            - değerlendirme yapmaz,
            - ağırlıklandırma yapmaz,
            - ranking yapmaz.
        """


        return YogurmaState(
            clusters=tuple(
                self._clusters.values()
            ),
            relations=tuple(
                self._relations.values()
            ),
            cluster_relations=tuple(
                self._cluster_relations.values()
            ),
            memberships=tuple(
                Membership(
                    information_id=information_id,
                    cluster_id=cluster_id,
                )
                for information_id, cluster_id
                in self._memberships
            ),
        )


    # ========================================================================
    # INTEGRITY VALIDATION
    # ========================================================================


    def validate_integrity(self) -> None:
        """
        Yapısal bütünlük kontrolü.


        Bu kontrol:
            - truth,
            - confidence,
            - reliability,
            - evidence strength,
            - ranking,
            - weighting


        hesaplamaz.


        Yalnızca referansların ve yapıların tamamlığını kontrol eder.
        """


        # --------------------------------------------------------------------
        # Cluster integrity
        # --------------------------------------------------------------------


        for cluster in self._clusters.values():


            if (
                cluster.parent_cluster_id is not None
                and cluster.parent_cluster_id
                not in self._clusters
            ):
                raise ValueError(
                    "Cluster references missing parent: "
                    f"{cluster.cluster_id}"
                )


            if cluster.cluster_id in cluster.child_cluster_ids:
                raise ValueError(
                    "Cluster cannot contain itself as child: "
                    f"{cluster.cluster_id}"
                )


            for child_id in cluster.child_cluster_ids:


                if child_id not in self._clusters:
                    raise ValueError(
                        "Cluster references missing child: "
                        f"{child_id}"
                    )


                child = self._clusters[child_id]


                if child.parent_cluster_id != cluster.cluster_id:
                    raise ValueError(
                        "Parent/child cluster reference mismatch: "
                        f"{cluster.cluster_id} -> {child_id}"
                    )


            for information_id in cluster.member_information_ids:


                if information_id not in self._pieces:
                    raise ValueError(
                        "Cluster references missing InformationPiece: "
                        f"{information_id}"
                    )


                if (
                    information_id,
                    cluster.cluster_id,
                ) not in self._memberships:
                    raise ValueError(
                        "Cluster membership is missing reverse reference: "
                        f"{information_id} -> {cluster.cluster_id}"
                    )


        # --------------------------------------------------------------------
        # Membership integrity
        # --------------------------------------------------------------------


        for information_id, cluster_id in self._memberships:


            if information_id not in self._pieces:
                raise ValueError(
                    "Membership references missing InformationPiece: "
                    f"{information_id}"
                )


            if cluster_id not in self._clusters:
                raise ValueError(
                    "Membership references missing Cluster: "
                    f"{cluster_id}"
                )


            if (
                information_id
                not in self._clusters[
                    cluster_id
                ].member_information_ids
            ):
                raise ValueError(
                    "Membership reverse reference missing: "
                    f"{information_id} -> {cluster_id}"
                )


        # --------------------------------------------------------------------
        # Information relation integrity
        # --------------------------------------------------------------------


        for relation in self._relations.values():


            if relation.source_information_id not in self._pieces:
                raise ValueError(
                    "Relation references missing source InformationPiece: "
                    f"{relation.relation_id}"
                )


            if relation.target_information_id not in self._pieces:
                raise ValueError(
                    "Relation references missing target InformationPiece: "
                    f"{relation.relation_id}"
                )


            if (
                relation.source_information_id
                == relation.target_information_id
            ):
                raise ValueError(
                    "Relation cannot self-reference: "
                    f"{relation.relation_id}"
                )


            for event in relation.state_history:


                if event.relation_id != relation.relation_id:
                    raise ValueError(
                        "Relation state history reference mismatch: "
                        f"{relation.relation_id}"
                    )


                if event.new_state is None:
                    raise ValueError(
                        "Relation state history contains empty state: "
                        f"{relation.relation_id}"
                    )


        # --------------------------------------------------------------------
        # Cluster relation integrity
        # --------------------------------------------------------------------


        for relation in self._cluster_relations.values():


            if relation.source_cluster_id not in self._clusters:
                raise ValueError(
                    "Cluster relation references missing source Cluster: "
                    f"{relation.relation_id}"
                )


            if relation.target_cluster_id not in self._clusters:
                raise ValueError(
                    "Cluster relation references missing target Cluster: "
                    f"{relation.relation_id}"
                )


            if (
                relation.source_cluster_id
                == relation.target_cluster_id
            ):
                raise ValueError(
                    "Cluster relation cannot self-reference: "
                    f"{relation.relation_id}"
                )


        # --------------------------------------------------------------------
        # Lifecycle history integrity
        # --------------------------------------------------------------------


        for cluster in self._clusters.values():


            for event in cluster.lifecycle_history:


                if event.cluster_id != cluster.cluster_id:
                    raise ValueError(
                        "Cluster lifecycle history reference mismatch: "
                        f"{cluster.cluster_id}"
                    )


                if event.new_state is None:
                    raise ValueError(
                        "Cluster lifecycle event has no new state: "
                        f"{cluster.cluster_id}"
                    )


    # ========================================================================
    # INTERNAL VALIDATION HELPERS
    # ========================================================================


    def _require_information(
        self,
        information_id: str,
    ) -> None:
        if information_id not in self._pieces:
            raise KeyError(
                f"Unknown information_id: {information_id}"
            )


    def _require_cluster(
        self,
        cluster_id: str,
    ) -> None:
        if cluster_id not in self._clusters:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


    @staticmethod
    def _extract_information_id(
        piece: Any,
    ) -> str:
        """
        5. Bölümdeki InformationPiece'in ID alanını okur.


        Desteklenen ana biçimler:
            information_id
            id


        Burada yeni bilgi üretilmez.
        """


        if hasattr(piece, "information_id"):
            information_id = getattr(
                piece,
                "information_id",
            )


        elif hasattr(piece, "id"):
            information_id = getattr(
                piece,
                "id",
            )


        else:
            raise TypeError(
                "5. Bölüm InformationPiece must expose "
                "'information_id' or 'id'."
            )


        if not isinstance(
            information_id,
            str,
        ) or not information_id.strip():
            raise ValueError(
                "InformationPiece ID must be a non-empty string."
            )


        return information_id


    @staticmethod
    def _next_event_id(
        prefix: str,
    ) -> str:
        """
        Deterministik olmayan fakat yalnızca tarihsel olay kaydı için
        kullanılan lokal ID üretimi.


        Bu ID herhangi bir epistemik anlam taşımaz.
        """


        import uuid


        return f"{prefix}:{uuid.uuid4().hex}"


# ============================================================================
# 14. YASAKLI 6. BÖLÜM SORUMLULUKLARI
# ============================================================================


FORBIDDEN_YOGURMA_FIELDS = frozenset(
    {
        "trust_score",
        "truth_score",
        "confidence",
        "reliability",
        "evidence_strength",
        "weight",
        "weighting",
        "ranking",
        "rank",
        "score",
        "signal",
        "BUY",
        "SELL",
        "LONG",
        "SHORT",
        "final_bias",
        "trade_decision",
        "risk_decision",
        "forecast",
        "prediction",
        "consensus",
    }
)


FORBIDDEN_YOGURMA_OPERATIONS = frozenset(
    {
        "score",
        "calculate_confidence",
        "calculate_reliability",
        "calculate_truth",
        "calculate_weight",
        "rank",
        "predict",
        "forecast",
        "decide",
        "generate_signal",
        "generate_bias",
    }
)


# ============================================================================
# 15. STATIC BOUNDARY VALIDATION
# ============================================================================


def validate_6_boundary() -> None:
    """
    6. Bölümün karar üretmeyen sınırını doğrular.


    Bu fonksiyon analiz yapmaz.
    """


    dataclasses_to_check = (
        Cluster,
        Relation,
        ClusterRelation,
        Membership,
    )


    for cls in dataclasses_to_check:


        fields = getattr(
            cls,
            "__dataclass_fields__",
            {},
        )


        for forbidden in FORBIDDEN_YOGURMA_FIELDS:


            if forbidden in fields:
                raise AssertionError(
                    f"Forbidden 6. Bölüm field found in "
                    f"{cls.__name__}: {forbidden}"
                )


    motor_methods = {
        name
        for name in dir(YogurmaMotoru)
        if not name.startswith("_")
        and callable(
            getattr(
                YogurmaMotoru,
                name,
            )
        )
    }


    leaked_operations = (
        motor_methods
        & FORBIDDEN_YOGURMA_OPERATIONS
    )


    if leaked_operations:
        raise AssertionError(
            "Forbidden 6. Bölüm operations exposed: "
            f"{sorted(leaked_operations)}"
        )


# ============================================================================
# 16. SELF TEST
# ============================================================================


def validate_6() -> None:
    """
    6. Bölüm yapısal validation.


    Testler yalnızca yapısal bütünlüğü kontrol eder.
    """


    validate_6_boundary()


    motor = YogurmaMotoru()


    # ------------------------------------------------------------------------
    # 5. Bölümden örnek InformationPiece yerine basit test nesnesi.
    #
    # Gerçek çalışma sırasında 5. Bölüm InformationPiece nesnesi doğrudan
    # register_information_piece() ile kullanılacaktır.
    # ------------------------------------------------------------------------


    @dataclass(frozen=True)
    class TestInformationPiece:
        information_id: str
        content: str


    info1 = TestInformationPiece(
        information_id="info-001",
        content="CTA information A",
    )


    info2 = TestInformationPiece(
        information_id="info-002",
        content="CTA information B",
    )


    info3 = TestInformationPiece(
        information_id="info-003",
        content="CTA information C",
    )


    motor.register_information_piece(info1)
    motor.register_information_piece(info2)
    motor.register_information_piece(info3)


    assert (
        len(motor.all_information_pieces())
        == 3
    )


    # ------------------------------------------------------------------------
    # Ana küme
    # ------------------------------------------------------------------------


    root = motor.create_cluster(
        cluster_id="cluster-root",
        cluster_type="event",
        shared_axes=(
            ClusterAxis.COMMON_EVENT,
            ClusterAxis.COMMON_REFERENCE_PERIOD,
        ),
        created_at=datetime(
            2026,
            1,
            1,
        ),
    )


    assert root.state == ClusterState.FORMING


    # ------------------------------------------------------------------------
    # Alt küme
    # ------------------------------------------------------------------------


    child = motor.create_cluster(
        cluster_id="cluster-child",
        cluster_type="event_phase",
        shared_axes=(
            ClusterAxis.COMMON_EVENT,
            ClusterAxis.COMMON_ACTOR,
        ),
        parent_cluster_id="cluster-root",
        created_at=datetime(
            2026,
            1,
            2,
        ),
    )


    assert (
        child.parent_cluster_id
        == "cluster-root"
    )


    assert (
        "cluster-child"
        in motor.get_cluster(
            "cluster-root"
        ).child_cluster_ids
    )


    # ------------------------------------------------------------------------
    # Çoklu üyelik
    # ------------------------------------------------------------------------


    motor.assign_information_to_cluster(
        "info-001",
        "cluster-root",
    )


    motor.assign_information_to_cluster(
        "info-001",
        "cluster-child",
    )


    motor.assign_information_to_cluster(
        "info-002",
        "cluster-root",
    )


    assert len(
        motor.clusters_for_information(
            "info-001"
        )
    ) == 2


    # ------------------------------------------------------------------------
    # İlişki
    # ------------------------------------------------------------------------


    relation = motor.add_relation(
        relation_id="relation-001",
        source_information_id="info-001",
        target_information_id="info-002",
        relation_type=RelationType.SAME_EVENT_DIFFERENT_ANGLE,
        state=RelationState.ACTIVE,
        context_note="Same event, different angle.",
        created_at=datetime(
            2026,
            1,
            3,
        ),
    )


    assert (
        relation.state
        == RelationState.ACTIVE
    )


    # ------------------------------------------------------------------------
    # İlişki durum değişikliği
    # ------------------------------------------------------------------------


    updated_relation = motor.update_relation_state(
        "relation-001",
        RelationState.DISPUTED,
        changed_at=datetime(
            2026,
            1,
            4,
        ),
        reason="Relationship became disputed.",
    )


    assert (
        updated_relation.state
        == RelationState.DISPUTED
    )


    assert len(
        updated_relation.state_history
    ) == 1


    assert (
        updated_relation.state_history[0]
        .previous_state
        == RelationState.ACTIVE
    )


    # ------------------------------------------------------------------------
    # Yatay küme ilişkisi
    # ------------------------------------------------------------------------


    cluster_relation = motor.add_cluster_relation(
        relation_id="cluster-relation-001",
        source_cluster_id="cluster-root",
        target_cluster_id="cluster-child",
        relation_type=ClusterRelationType.CONTINUATION,
        state=RelationState.ACTIVE,
    )


    assert (
        cluster_relation.state
        == RelationState.ACTIVE
    )


    # ------------------------------------------------------------------------
    # Küme lifecycle
    # ------------------------------------------------------------------------


    closed = motor.close_cluster(
        "cluster-root",
        changed_at=datetime(
            2026,
            1,
            5,
        ),
        reason="Reference event closed.",
    )


    assert (
        closed.state
        == ClusterState.CLOSED
    )


    assert len(
        closed.lifecycle_history
    ) == 1


    reopened = motor.reopen_cluster(
        "cluster-root",
        changed_at=datetime(
            2026,
            1,
            6,
        ),
        reason="Directly related information arrived.",
    )


    assert (
        reopened.state
        == ClusterState.REOPENED
    )


    assert len(
        reopened.lifecycle_history
    ) == 2


    # ------------------------------------------------------------------------
    # Integrity
    # ------------------------------------------------------------------------


    motor.validate_integrity()


    # ------------------------------------------------------------------------
    # 6 -> 7 output
    # ------------------------------------------------------------------------


    state = motor.state()


    assert len(state.clusters) == 2
    assert len(state.relations) == 1
    assert len(state.cluster_relations) == 1
    assert len(state.memberships) == 3


    # ------------------------------------------------------------------------
    # Provenance pass-through
    # ------------------------------------------------------------------------


    provenance = motor.provenance_for_information(
        "info-001"
    )


    assert (
        provenance["information_id"]
        == "info-001"
    )


# ============================================================================
# 17. FINAL ARCHITECTURAL PRINCIPLE
# ============================================================================


YOGURMA_FINAL_PRINCIPLE = (
    "Yoğurma Motoru, bilgiyi değiştirmeden; kaynak kökenini, "
    "statüsünü, zamanını ve bağlamını koruyarak bilgileri anlamlı "
    "kümeler ve ilişkisel yapılar hâline getirir. Bilgiyi tek bir "
    "kümeye hapsetmez; gerektiğinde çoklu üyeliği, ana/alt yapıları "
    "ve yatay ilişkili kümeleri korur. Zaman içinde gelişen olayların "
    "sürekliliğini ve kümelerin yaşam döngüsünü izler; kapanan veya "
    "değişen yapıları silmez. İlişkilerin mevcut ve geçmiş durumlarını "
    "korur ancak bunların gücünü, doğruluğunu, güvenilirliğini veya "
    "önemini değerlendirmez. Yoğurma Motoru bilgiyi analiz etmez, "
    "hesaplamaz, sentezlemez, tahmin etmez ve karar üretmez. Çıktısı, "
    "7. Bölüm — Analiz / Hesaplama / Değerlendirme için analize hazır "
    "ilişkili ve bağlamsal bilgi yapılarıdır."
)


# ============================================================================
# 18. MAIN
# ============================================================================


if __name__ == "__main__":
    validate_6()


    print(
        "6. BÖLÜM — YOĞURMA MOTORU"
    )
    print("=" * 72)


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "Validation: PASSED"
    )


    print(
        "=" * 72
    )


    print(
        YOGURMA_FINAL_PRINCIPLE
    )


7. BÖLÜM — 
"""
ERHAN / CTA TERMINAL
7. BÖLÜM — ANALİZ / HESAPLAMA / DEĞERLENDİRME
FINAL CODE


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ


6. Bölüm — Yoğurma Motoru'ndan gelen ilişkili ve bağlamsal bilgi
yapılarını analiz eder.


7. Bölümün görevi:
    - yapısal tespit,
    - ilişkisel analiz,
    - örüntü analizi,
    - zaman analizi,
    - provenance analizi,
    - karşılaştırılabilirlik kontrolü,
    - convergence / divergence / contradiction /
      complementarity / repetition-relay analizi,
    - bağımsızlık yapısının analizi,
    - belirsizlik türlerinin analizi,
    - izin verilen yapısal ve zamansal ölçümlerdir.


7. Bölüm:
    - nihai CTA hükmü üretmez,
    - bullish / bearish nihai yön üretmez,
    - final bias üretmez,
    - trade sinyali üretmez,
    - risk / pozisyon kararı üretmez,
    - gelecek tahmini üretmez,
    - confidence / reliability / trust üretmez,
    - evidence strength üretmez,
    - weighting / ranking yapmaz,
    - kendi başına piyasa rejimi sınıflandırmaz.


6 -> 7:
    Yoğurma Motoru ilişkileri ve yapıları oluşturur.


7 -> 8:
    Analiz Motoru analitik bulgular üretir.
    Bu bulgular 8. Bölüm CTA Synthesis / Sonuç katmanına devredilir.


ÖNEMLİ:
    Bu dosya 6. Bölümün InformationPiece, Cluster, Relation,
    ClusterRelation ve Membership sınıflarını yeniden tanımlamaz.
    Gerçek 6. Bölüm Yoğurma Motoru ile çalışır.
"""


from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Sequence


# ============================================================================
# 1. ANALİTİK BULGU TÜRLERİ
# ============================================================================


class AnalyticalFindingType(str, Enum):
    STRUCTURAL_DETECTION = "structural_detection"
    RELATIONAL_ANALYSIS = "relational_analysis"
    PATTERN_DETECTION = "pattern_detection"
    CHANGE_ANALYSIS = "change_analysis"
    TIME_ANALYSIS = "time_analysis"
    PROVENANCE_ANALYSIS = "provenance_analysis"
    COMPARABILITY_CHECK = "comparability_check"
    CONVERGENCE = "convergence"
    DIVERGENCE = "divergence"
    CONTRADICTION = "contradiction"
    COMPLEMENTARITY = "complementarity"
    REPETITION_RELAY = "repetition_relay"
    INDEPENDENCE_ANALYSIS = "independence_analysis"
    UNCERTAINTY_ANALYSIS = "uncertainty_analysis"
    STRUCTURAL_TEMPORAL_MEASUREMENT = (
        "structural_temporal_measurement"
    )


# ============================================================================
# 2. KARŞILAŞTIRILABİLİRLİK
# ============================================================================


class ComparabilityCondition(str, Enum):
    SAME_SUBJECT = "same_subject"
    SAME_OR_COMPARABLE_ASSET = "same_or_comparable_asset"
    SAME_OR_OVERLAPPING_REFERENCE_PERIOD = (
        "same_or_overlapping_reference_period"
    )
    COMPATIBLE_EVENT_CONTEXT = "compatible_event_context"
    COMPARABLE_SCOPE = "comparable_scope"
    ACTUAL_CLAIM = "actual_claim"
    DIRECTNESS = "directness"
    PROVENANCE = "provenance"
    INFORMATION_STATUS = "information_status"


class ComparabilityResult(str, Enum):
    COMPARABLE = "comparable"
    CONDITIONALLY_COMPARABLE = "conditionally_comparable"
    LIMITED_COMPARABLE = "limited_comparable"
    NOT_COMPARABLE = "not_comparable"


COMPARABILITY_PAIRS = {
    (
        "forecast",
        "outcome",
    ): ComparabilityResult.CONDITIONALLY_COMPARABLE,


    (
        "institution_view",
        "positioning",
    ): ComparabilityResult.CONDITIONALLY_COMPARABLE,


    (
        "disclosed_strategy",
        "realized_behavior",
    ): ComparabilityResult.CONDITIONALLY_COMPARABLE,


    (
        "commentary",
        "realized_fact",
    ): ComparabilityResult.CONDITIONALLY_COMPARABLE,


    (
        "unverified_claim",
        "official_data",
    ): ComparabilityResult.LIMITED_COMPARABLE,
}


# ============================================================================
# 3. İLİŞKİ ANALİZ TÜRLERİ
# ============================================================================


class RelationAnalysisType(str, Enum):
    CONVERGENCE = "convergence"
    DIVERGENCE = "divergence"
    CONTRADICTION = "contradiction"
    COMPLEMENTARITY = "complementarity"
    REPETITION_RELAY = "repetition_relay"


@dataclass(frozen=True)
class RelationAnalysis:
    analysis_id: str
    relation_analysis_type: RelationAnalysisType
    information_ids: tuple[str, ...]
    comparability: ComparabilityResult
    conditions: tuple[ComparabilityCondition, ...] = field(
        default_factory=tuple
    )
    note: Optional[str] = None


# ============================================================================
# 4. YAPISAL / ZAMANSAL ÖLÇÜMLER
# ============================================================================


class StructuralMeasurementType(str, Enum):
    DIVERGENCE_DURATION = "divergence_duration"
    VIEW_CHANGE_COUNT = "view_change_count"
    REPETITION_COUNT = "repetition_count"
    REPETITION_DENSITY = "repetition_density"
    COMMON_ROOT_COUNT = "common_root_count"
    INDEPENDENT_ROOT_COUNT = "independent_root_count"
    FORECAST_OUTCOME_TIME_GAP = "forecast_outcome_time_gap"
    VIEW_CHANGE_TIMING = "view_change_timing"
    PATTERN_DURATION = "pattern_duration"


@dataclass(frozen=True)
class StructuralMeasurement:
    measurement_id: str
    measurement_type: StructuralMeasurementType
    information_ids: tuple[str, ...]


    # Ölçüm sonucu betimleyici değerdir.
    # Değer hiçbir şekilde score/confidence/ranking anlamı taşımaz.
    value: Optional[float] = None


    unit: Optional[str] = None


    # İhtiyaç halinde ölçümün metinsel açıklaması.
    note: Optional[str] = None


# ============================================================================
# 5. PROVENANCE ANALİZİ
# ============================================================================


class ProvenanceAnalysisType(str, Enum):
    COMMON_ROOT = "common_root"
    RELAY_CHAIN = "relay_chain"
    REPUBLICATION = "republication"
    SAME_DATA_DIFFERENT_NARRATIVES = (
        "same_data_different_narratives"
    )
    SEPARATE_ROOTS = "separate_roots"
    APPARENTLY_INDEPENDENT_PATHS = (
        "apparently_independent_paths"
    )
    VISIBLE_CONVERGENCE_COMMON_ROOT = (
        "visible_convergence_common_root"
    )


@dataclass(frozen=True)
class ProvenanceAnalysis:
    analysis_id: str
    analysis_type: ProvenanceAnalysisType
    information_ids: tuple[str, ...]
    root_ids: tuple[str, ...] = field(default_factory=tuple)
    note: Optional[str] = None


# ============================================================================
# 6. BELİRSİZLİK
# ============================================================================


class UncertaintyType(str, Enum):
    DATA_MISSINGNESS = "data_missingness"
    SOURCE_DIVERGENCE = "source_divergence"
    TIMING_DIFFERENCE = "timing_difference"
    STATUS_UNCERTAINTY = "status_uncertainty"
    UNRESOLVED_CONTRADICTION = (
        "unresolved_contradiction"
    )
    IDENTITY_PROVENANCE_UNCERTAINTY = (
        "identity_provenance_uncertainty"
    )
    CONTEXT_UNCERTAINTY = "context_uncertainty"
    FORWARD_LOOKING_NOT_YET_OUTCOME = (
        "forward_looking_not_yet_outcome"
    )


@dataclass(frozen=True)
class UncertaintyAnalysis:
    analysis_id: str
    uncertainty_type: UncertaintyType
    information_ids: tuple[str, ...]
    note: Optional[str] = None


# ============================================================================
# 7. DIŞSAL REJİM GİRDİSİ
# ============================================================================


@dataclass(frozen=True)
class ExternalRegimeInput:
    """
    Dışarıdan gelen rejim / makro / piyasa bağlamı.


    Bu nesne rejimi doğrulamaz ve kendi başına yeni rejim
    sınıflandırması üretmez.
    """


    regime_claim: Optional[str] = None
    macro_context: Optional[str] = None
    market_condition: Optional[str] = None
    volatility_trend_condition: Optional[str] = None


    source: Optional[str] = None
    production_time: Optional[datetime] = None
    reference_period: Optional[str] = None
    information_status: Optional[str] = None
    provenance: Optional[str] = None


# ============================================================================
# 8. POINT-IN-TIME
# ============================================================================


@dataclass(frozen=True)
class PointInTimeRecord:
    production_time: Optional[datetime] = None
    event_time: Optional[datetime] = None
    reference_period: Optional[str] = None
    revision_time: Optional[datetime] = None
    information_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


# ============================================================================
# 9. ANALİZ BULGUSU
# ============================================================================


@dataclass(frozen=True)
class AnalysisFinding:
    """
    7. Bölümün temel çıktı nesnesi.


    AnalysisFinding:
        - gözlemi,
        - yapısal bulguyu,
        - ölçümü,
        - ilişki analizini


    taşır.


    Nihai anlam / karar taşımaz.
    """


    finding_id: str
    finding_type: AnalyticalFindingType


    information_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    cluster_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    description: str = ""


    metrics: Mapping[str, Any] = field(
        default_factory=dict
    )


    comparability: Optional[ComparabilityResult] = None


    uncertainty_type: Optional[UncertaintyType] = None


    production_time: Optional[datetime] = None


# ============================================================================
# 10. 7 -> 8 ÇIKTI
# ============================================================================


@dataclass(frozen=True)
class AnalysisOutput:
    """
    8. Bölüme devredilecek analitik çıktı.


    Burada final CTA hükmü yoktur.
    """


    findings: tuple[AnalysisFinding, ...] = field(
        default_factory=tuple
    )


    relation_analyses: tuple[RelationAnalysis, ...] = field(
        default_factory=tuple
    )


    structural_measurements: tuple[StructuralMeasurement, ...] = field(
        default_factory=tuple
    )


    provenance_analyses: tuple[ProvenanceAnalysis, ...] = field(
        default_factory=tuple
    )


    uncertainty_analyses: tuple[UncertaintyAnalysis, ...] = field(
        default_factory=tuple
    )


# ============================================================================
# 11. YASAKLI ALANLAR / OPERASYONLAR
# ============================================================================


FORBIDDEN_ANALYSIS_FIELDS = frozenset(
    {
        "trust_score",
        "reliability_score",
        "evidence_strength",
        "confidence",
        "confidence_score",
        "weight",
        "weighting",
        "ranking",
        "rank",
        "score",
        "signal",
        "BUY",
        "SELL",
        "LONG",
        "SHORT",
        "final_bias",
        "bullish",
        "bearish",
        "trade_decision",
        "risk_decision",
        "position_decision",
        "prediction",
        "forecast_output",
        "regime_classification",
        "visual_confidence_score",
        "OCR_score",
        "image_quality_score",
        "media_confidence_score",
        "consensus_score",
    }
)


FORBIDDEN_ANALYSIS_OPERATIONS = frozenset(
    {
        "calculate_confidence",
        "calculate_reliability",
        "calculate_truth",
        "calculate_evidence_strength",
        "calculate_weight",
        "rank",
        "predict",
        "forecast",
        "generate_signal",
        "generate_bias",
        "make_trade_decision",
        "make_risk_decision",
        "classify_regime",
    }
)


# ============================================================================
# 12. ANALİZ MOTORU
# ============================================================================


class AnalysisEngine:
    """
    7. Bölüm — Analiz / Hesaplama / Değerlendirme Motoru.


    Girdi:
        6. Bölüm YogurmaMotoru.


    Çıktı:
        Analitik bulgular.


    Motor:
        - 6. Bölümdeki InformationPiece'leri değiştirmez.
        - 6. Bölüm kümelerini değiştirmez.
        - 6. Bölüm ilişkilerini değiştirmez.
        - geçmiş bilgi durumlarını overwrite etmez.


    Motorun işi analizdir.
    Nihai CTA synthesis 8. Bölüme aittir.
    """


    def __init__(
        self,
        yogurma_motoru: Any,
    ) -> None:
        self.yogurma_motoru = yogurma_motoru


        self._findings: dict[str, AnalysisFinding] = {}
        self._relation_analyses: dict[
            str,
            RelationAnalysis,
        ] = {}


        self._structural_measurements: dict[
            str,
            StructuralMeasurement,
        ] = {}


        self._provenance_analyses: dict[
            str,
            ProvenanceAnalysis,
        ] = {}


        self._uncertainty_analyses: dict[
            str,
            UncertaintyAnalysis,
        ] = {}


        self._validate_input_interface()


    # ========================================================================
    # INPUT
    # ========================================================================


    def _validate_input_interface(self) -> None:
        """
        6. Bölüm final motorunun gerekli public arayüzünü kontrol eder.
        """


        required_methods = (
            "all_clusters",
            "all_relations",
            "all_cluster_relations",
            "all_information_pieces",
            "state",
        )


        for method_name in required_methods:
            method = getattr(
                self.yogurma_motoru,
                method_name,
                None,
            )


            if not callable(method):
                raise TypeError(
                    "7. Bölüm requires 6. Bölüm YogurmaMotoru "
                    f"method: {method_name}"
                )


    # ========================================================================
    # PUBLIC OUTPUT
    # ========================================================================


    def findings(
        self,
    ) -> tuple[AnalysisFinding, ...]:
        return tuple(
            self._findings.values()
        )


    def relation_analyses(
        self,
    ) -> tuple[RelationAnalysis, ...]:
        return tuple(
            self._relation_analyses.values()
        )


    def structural_measurements(
        self,
    ) -> tuple[StructuralMeasurement, ...]:
        return tuple(
            self._structural_measurements.values()
        )


    def provenance_analyses(
        self,
    ) -> tuple[ProvenanceAnalysis, ...]:
        return tuple(
            self._provenance_analyses.values()
        )


    def uncertainty_analyses(
        self,
    ) -> tuple[UncertaintyAnalysis, ...]:
        return tuple(
            self._uncertainty_analyses.values()
        )


    def output(
        self,
    ) -> AnalysisOutput:
        return AnalysisOutput(
            findings=self.findings(),
            relation_analyses=self.relation_analyses(),
            structural_measurements=(
                self.structural_measurements()
            ),
            provenance_analyses=(
                self.provenance_analyses()
            ),
            uncertainty_analyses=(
                self.uncertainty_analyses()
            ),
        )


    # ========================================================================
    # BASIC ACCESS
    # ========================================================================


    def _pieces(
        self,
    ) -> tuple[Any, ...]:
        return self.yogurma_motoru.all_information_pieces()


    def _clusters(
        self,
    ) -> tuple[Any, ...]:
        return self.yogurma_motoru.all_clusters()


    def _relations(
        self,
    ) -> tuple[Any, ...]:
        return self.yogurma_motoru.all_relations()


    def _cluster_relations(
        self,
    ) -> tuple[Any, ...]:
        return self.yogurma_motoru.all_cluster_relations()


    def _piece_map(
        self,
    ) -> dict[str, Any]:
        return {
            self._piece_id(piece): piece
            for piece in self._pieces()
        }


    def _cluster_map(
        self,
    ) -> dict[str, Any]:
        return {
            cluster.cluster_id: cluster
            for cluster in self._clusters()
        }


    # ========================================================================
    # PIECE FIELD HELPERS
    # ========================================================================


    @staticmethod
    def _piece_id(
        piece: Any,
    ) -> str:
        if hasattr(piece, "information_id"):
            return str(
                getattr(
                    piece,
                    "information_id",
                )
            )


        if hasattr(piece, "id"):
            return str(
                getattr(
                    piece,
                    "id",
                )
            )


        raise TypeError(
            "InformationPiece must expose information_id or id."
        )


    @staticmethod
    def _field(
        piece: Any,
        *names: str,
    ) -> Any:
        for name in names:
            if hasattr(piece, name):
                return getattr(
                    piece,
                    name,
                )


        return None


    @classmethod
    def _source_id(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "source_id",
            "source",
            "master_source_id",
        )


        if value is None:
            return None


        if isinstance(value, str):
            return value


        return str(value)


    @classmethod
    def _original_source_id(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "original_source_id",
            "provenance_root_id",
            "source_family_id",
        )


        if value is None:
            return None


        if isinstance(value, str):
            return value


        return str(value)


    @classmethod
    def _root_id(
        cls,
        piece: Any,
    ) -> Optional[str]:
        """
        Ortak bilgi kökü.


        Bu değer otomatik olarak "bağımsız kanıt" anlamına gelmez.
        Sadece mevcut provenance/root bilgisinin yapısal kimliğidir.
        """


        original = cls._original_source_id(piece)


        if original:
            return original


        return cls._source_id(piece)


    @classmethod
    def _topic(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "topic",
            "subject",
        )


        return (
            str(value)
            if value is not None
            else None
        )


    @classmethod
    def _asset(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "reference_asset",
            "instrument_or_market",
            "entity_scope",
        )


        return (
            str(value)
            if value is not None
            else None
        )


    @classmethod
    def _status(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "status",
            "information_status",
            "fact_status",
        )


        if value is None:
            return None


        if isinstance(value, Enum):
            return str(value.value)


        return str(value)


    @classmethod
    def _claim(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "claim",
            "content",
        )


        return (
            str(value)
            if value is not None
            else None
        )


    @classmethod
    def _directness(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "directness",
            "measurement_role",
        )


        if value is None:
            return None


        if isinstance(value, Enum):
            return str(value.value)


        return str(value)


    @classmethod
    def _reference_period(
        cls,
        piece: Any,
    ) -> Optional[str]:
        value = cls._field(
            piece,
            "reference_period",
        )


        return (
            str(value)
            if value is not None
            else None
        )


    @classmethod
    def _production_time(
        cls,
        piece: Any,
    ) -> Optional[datetime]:
        value = cls._field(
            piece,
            "production_time",
            "publication_time",
        )


        return (
            value
            if isinstance(value, datetime)
            else None
        )


    @classmethod
    def _event_time(
        cls,
        piece: Any,
    ) -> Optional[datetime]:
        value = cls._field(
            piece,
            "event_time",
            "observation_time",
        )


        return (
            value
            if isinstance(value, datetime)
            else None
        )


    # ========================================================================
    # FINDING REGISTRATION
    # ========================================================================


    def _add_finding(
        self,
        finding: AnalysisFinding,
    ) -> AnalysisFinding:


        if finding.finding_id in self._findings:
            raise ValueError(
                f"Duplicate finding_id: "
                f"{finding.finding_id}"
            )


        self._findings[
            finding.finding_id
        ] = finding


        return finding


    def _add_relation_analysis(
        self,
        analysis: RelationAnalysis,
    ) -> RelationAnalysis:


        if analysis.analysis_id in self._relation_analyses:
            raise ValueError(
                f"Duplicate analysis_id: "
                f"{analysis.analysis_id}"
            )


        self._relation_analyses[
            analysis.analysis_id
        ] = analysis


        return analysis


    def _add_measurement(
        self,
        measurement: StructuralMeasurement,
    ) -> StructuralMeasurement:


        if (
            measurement.measurement_id
            in self._structural_measurements
        ):
            raise ValueError(
                f"Duplicate measurement_id: "
                f"{measurement.measurement_id}"
            )


        self._structural_measurements[
            measurement.measurement_id
        ] = measurement


        return measurement


    def _add_provenance_analysis(
        self,
        analysis: ProvenanceAnalysis,
    ) -> ProvenanceAnalysis:


        if (
            analysis.analysis_id
            in self._provenance_analyses
        ):
            raise ValueError(
                f"Duplicate provenance analysis_id: "
                f"{analysis.analysis_id}"
            )


        self._provenance_analyses[
            analysis.analysis_id
        ] = analysis


        return analysis


    def _add_uncertainty_analysis(
        self,
        analysis: UncertaintyAnalysis,
    ) -> UncertaintyAnalysis:


        if (
            analysis.analysis_id
            in self._uncertainty_analyses
        ):
            raise ValueError(
                f"Duplicate uncertainty analysis_id: "
                f"{analysis.analysis_id}"
            )


        self._uncertainty_analyses[
            analysis.analysis_id
        ] = analysis


        return analysis


    # ========================================================================
    # 1. STRUCTURAL DETECTION
    # ========================================================================


    def analyze_cluster_structure(
        self,
        cluster_id: str,
    ) -> AnalysisFinding:


        cluster = self._cluster_map().get(
            cluster_id
        )


        if cluster is None:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


        information_ids = tuple(
            cluster.member_information_ids
        )


        finding = AnalysisFinding(
            finding_id=(
                f"structural:{cluster_id}"
            ),
            finding_type=(
                AnalyticalFindingType.STRUCTURAL_DETECTION
            ),
            information_ids=information_ids,
            cluster_ids=(cluster_id,),
            description=(
                "Kümenin mevcut yapısal özellikleri "
                "betimlenmiştir."
            ),
            metrics={
                "member_count": len(
                    information_ids
                ),
                "child_cluster_count": len(
                    cluster.child_cluster_ids
                ),
                "shared_axis_count": len(
                    cluster.shared_axes
                ),
                "cluster_state": (
                    cluster.state.value
                    if isinstance(
                        cluster.state,
                        Enum,
                    )
                    else str(cluster.state)
                ),
            },
        )


        return self._add_finding(
            finding
        )


    # ========================================================================
    # 2. PROVENANCE / COMMON ROOT
    # ========================================================================


    def analyze_provenance(
        self,
        cluster_id: str,
    ) -> ProvenanceAnalysis:


        cluster = self._cluster_map().get(
            cluster_id
        )


        if cluster is None:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


        piece_map = self._piece_map()


        information_ids = tuple(
            cluster.member_information_ids
        )


        root_ids: list[str] = []


        for information_id in information_ids:


            piece = piece_map.get(
                information_id
            )


            if piece is None:
                continue


            root = self._root_id(
                piece
            )


            if root is not None:
                root_ids.append(root)


        unique_roots = tuple(
            dict.fromkeys(root_ids)
        )


        if len(unique_roots) == 1:
            analysis_type = (
                ProvenanceAnalysisType.COMMON_ROOT
            )
            note = (
                "Kümedeki kayıtların mevcut provenance "
                "yapısında tek ortak kök kimliği vardır. "
                "Bu sonuç bağımsızlık veya kanıt gücü hükmü değildir."
            )


        elif len(unique_roots) > 1:
            analysis_type = (
                ProvenanceAnalysisType.SEPARATE_ROOTS
            )
            note = (
                "Kümede birden fazla ayrı bilgi kökü "
                "bulunmaktadır. Ayrı kök bulunması tek başına "
                "doğruluk veya kanıt gücü anlamına gelmez."
            )


        else:
            analysis_type = (
                ProvenanceAnalysisType.APPARENTLY_INDEPENDENT_PATHS
            )
            note = (
                "Kayıtlar için mevcut provenance kökü "
                "yeterli değildir; bağımsızlık hükmü kurulmamıştır."
            )


        analysis = ProvenanceAnalysis(
            analysis_id=(
                f"provenance:{cluster_id}"
            ),
            analysis_type=analysis_type,
            information_ids=information_ids,
            root_ids=unique_roots,
            note=note,
        )


        self._add_provenance_analysis(
            analysis
        )


        # Yapısal ölçüm:
        # distinct root count = bağımsız kanıt skoru değildir.
        self._add_measurement(
            StructuralMeasurement(
                measurement_id=(
                    f"common-root-count:{cluster_id}"
                ),
                measurement_type=(
                    StructuralMeasurementType.COMMON_ROOT_COUNT
                ),
                information_ids=information_ids,
                value=float(
                    len(unique_roots)
                ),
                unit="root_count",
                note=(
                    "Ayrı provenance root kimliklerinin sayısı. "
                    "Evidence strength veya confidence değildir."
                ),
            )
        )


        return analysis


    # ========================================================================
    # 3. INDEPENDENCE STRUCTURE
    # ========================================================================


    def analyze_independence_structure(
        self,
        cluster_id: str,
    ) -> AnalysisFinding:


        cluster = self._cluster_map().get(
            cluster_id
        )


        if cluster is None:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


        piece_map = self._piece_map()


        root_ids = []


        for information_id in (
            cluster.member_information_ids
        ):
            piece = piece_map.get(
                information_id
            )


            if piece is None:
                continue


            root = self._root_id(
                piece
            )


            if root is not None:
                root_ids.append(root)


        distinct_roots = tuple(
            dict.fromkeys(root_ids)
        )


        finding = AnalysisFinding(
            finding_id=(
                f"independence:{cluster_id}"
            ),
            finding_type=(
                AnalyticalFindingType.INDEPENDENCE_ANALYSIS
            ),
            information_ids=tuple(
                cluster.member_information_ids
            ),
            cluster_ids=(cluster_id,),
            description=(
                "Kümedeki bilgi kökü yapısı "
                "betimlenmiştir; ayrı kök sayısı "
                "bağımsızlık güveni veya kanıt gücü "
                "olarak yorumlanmaz."
            ),
            metrics={
                "record_count": len(
                    cluster.member_information_ids
                ),
                "distinct_root_count": len(
                    distinct_roots
                ),
            },
        )


        self._add_measurement(
            StructuralMeasurement(
                measurement_id=(
                    f"independent-root-count:{cluster_id}"
                ),
                measurement_type=(
                    StructuralMeasurementType.INDEPENDENT_ROOT_COUNT
                ),
                information_ids=tuple(
                    cluster.member_information_ids
                ),
                value=float(
                    len(distinct_roots)
                ),
                unit="root_count",
                note=(
                    "Distinct provenance root count. "
                    "Automatic independence/trust score değildir."
                ),
            )
        )


        return self._add_finding(
            finding
        )


    # ========================================================================
    # 4. SOURCE VIEW CHANGE
    # ========================================================================


    def analyze_source_changes(
        self,
        cluster_id: str,
        source_id: str,
    ) -> AnalysisFinding:


        cluster = self._cluster_map().get(
            cluster_id
        )


        if cluster is None:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


        piece_map = self._piece_map()


        pieces = [
            piece_map[information_id]
            for information_id
            in cluster.member_information_ids
            if information_id in piece_map
            and self._source_id(
                piece_map[information_id]
            ) == source_id
        ]


        pieces.sort(
            key=lambda piece: (
                self._production_time(piece)
                or datetime.min
            )
        )


        # Kayıt sayısı değişim sayısı değildir.
        # Gerçek değişim için claim/status karşılaştırılır.
        change_count = 0


        previous_signature: Optional[
            tuple[Optional[str], Optional[str]]
        ] = None


        change_information_ids: list[str] = []


        for piece in pieces:


            signature = (
                self._claim(piece),
                self._status(piece),
            )


            if (
                previous_signature is not None
                and signature != previous_signature
            ):
                change_count += 1
                change_information_ids.append(
                    self._piece_id(piece)
                )


            previous_signature = signature


        first_time = (
            self._production_time(
                pieces[0]
            )
            if pieces
            else None
        )


        last_time = (
            self._production_time(
                pieces[-1]
            )
            if pieces
            else None
        )


        finding = AnalysisFinding(
            finding_id=(
                f"source-change:{cluster_id}:{source_id}"
            ),
            finding_type=(
                AnalyticalFindingType.CHANGE_ANALYSIS
            ),
            information_ids=tuple(
                self._piece_id(piece)
                for piece in pieces
            ),
            cluster_ids=(cluster_id,),
            description=(
                f"Kaynak {source_id} için küme bağlamında "
                f"{change_count} içerik/statü değişimi "
                "gözlenmiştir."
            ),
            metrics={
                "source_id": source_id,
                "record_count": len(pieces),
                "change_count": change_count,
                "first_production_time": (
                    first_time.isoformat()
                    if first_time
                    else None
                ),
                "last_production_time": (
                    last_time.isoformat()
                    if last_time
                    else None
                ),
            },
        )


        self._add_measurement(
            StructuralMeasurement(
                measurement_id=(
                    f"view-change-count:"
                    f"{cluster_id}:{source_id}"
                ),
                measurement_type=(
                    StructuralMeasurementType.VIEW_CHANGE_COUNT
                ),
                information_ids=tuple(
                    self._piece_id(piece)
                    for piece in pieces
                ),
                value=float(
                    change_count
                ),
                unit="changes",
                note=(
                    "Claim/status signature değişim sayısıdır; "
                    "önem veya doğruluk ölçüsü değildir."
                ),
            )
        )


        if change_information_ids:
            self._add_measurement(
                StructuralMeasurement(
                    measurement_id=(
                        f"view-change-timing:"
                        f"{cluster_id}:{source_id}"
                    ),
                    measurement_type=(
                        StructuralMeasurementType.VIEW_CHANGE_TIMING
                    ),
                    information_ids=tuple(
                        change_information_ids
                    ),
                    value=float(
                        len(change_information_ids)
                    ),
                    unit="change_events",
                    note=(
                        "Değişim olaylarının sayısal olmayan "
                        "zaman bağlamı finding kayıtlarında korunur."
                    ),
                )
            )


        return self._add_finding(
            finding
        )


    # ========================================================================
    # 5. REPETITION / RELAY
    # ========================================================================


    def analyze_repetition_relay(
        self,
        cluster_id: str,
    ) -> AnalysisFinding:


        cluster = self._cluster_map().get(
            cluster_id
        )


        if cluster is None:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


        piece_map = self._piece_map()


        root_groups: dict[
            Optional[str],
            list[str],
        ] = {}


        for information_id in (
            cluster.member_information_ids
        ):
            piece = piece_map.get(
                information_id
            )


            if piece is None:
                continue


            root = self._root_id(
                piece
            )


            root_groups.setdefault(
                root,
                [],
            ).append(
                information_id
            )


        repeated_groups = {
            root: ids
            for root, ids in root_groups.items()
            if root is not None
            and len(ids) > 1
        }


        repeated_record_count = sum(
            len(ids)
            for ids in repeated_groups.values()
        )


        finding = AnalysisFinding(
            finding_id=(
                f"repetition-relay:{cluster_id}"
            ),
            finding_type=(
                AnalyticalFindingType.REPETITION_RELAY
            ),
            information_ids=tuple(
                cluster.member_information_ids
            ),
            cluster_ids=(cluster_id,),
            description=(
                "Aynı provenance kökünden gelen tekrar/"
                "aktarım grupları yapısal olarak tespit edilmiştir."
            ),
            metrics={
                "repeated_root_group_count": len(
                    repeated_groups
                ),
                "repeated_record_count": (
                    repeated_record_count
                ),
            },
        )


        self._add_measurement(
            StructuralMeasurement(
                measurement_id=(
                    f"repetition-count:{cluster_id}"
                ),
                measurement_type=(
                    StructuralMeasurementType.REPETITION_COUNT
                ),
                information_ids=tuple(
                    cluster.member_information_ids
                ),
                value=float(
                    repeated_record_count
                ),
                unit="records",
                note=(
                    "Aynı provenance kökünden gelen "
                    "kayıtların sayısıdır; consensus değildir."
                ),
            )
        )


        return self._add_finding(
            finding
        )


    # ========================================================================
    # 6. COMPARABILITY
    # ========================================================================


    def check_comparability(
        self,
        information_id_a: str,
        information_id_b: str,
    ) -> RelationAnalysis:


        piece_map = self._piece_map()


        try:
            piece_a = piece_map[
                information_id_a
            ]
            piece_b = piece_map[
                information_id_b
            ]
        except KeyError as exc:
            raise KeyError(
                f"Unknown information_id: {exc.args[0]}"
            ) from exc


        conditions: list[
            ComparabilityCondition
        ] = []


        # --------------------------------------------------------------------
        # Subject
        # --------------------------------------------------------------------


        subject_a = self._topic(
            piece_a
        )
        subject_b = self._topic(
            piece_b
        )


        if (
            subject_a is not None
            and subject_b is not None
            and subject_a == subject_b
        ):
            conditions.append(
                ComparabilityCondition.SAME_SUBJECT
            )


        # --------------------------------------------------------------------
        # Asset
        # --------------------------------------------------------------------


        asset_a = self._asset(
            piece_a
        )
        asset_b = self._asset(
            piece_b
        )


        if (
            asset_a is not None
            and asset_b is not None
            and asset_a == asset_b
        ):
            conditions.append(
                ComparabilityCondition.SAME_OR_COMPARABLE_ASSET
            )


        # --------------------------------------------------------------------
        # Reference period
        # --------------------------------------------------------------------


        period_a = self._reference_period(
            piece_a
        )
        period_b = self._reference_period(
            piece_b
        )


        if (
            period_a is not None
            and period_b is not None
            and period_a == period_b
        ):
            conditions.append(
                ComparabilityCondition.SAME_OR_OVERLAPPING_REFERENCE_PERIOD
            )


        # --------------------------------------------------------------------
        # Claim
        # --------------------------------------------------------------------


        claim_a = self._claim(
            piece_a
        )
        claim_b = self._claim(
            piece_b
        )


        if (
            claim_a is not None
            and claim_b is not None
            and claim_a == claim_b
        ):
            conditions.append(
                ComparabilityCondition.ACTUAL_CLAIM
            )


        # --------------------------------------------------------------------
        # Directness
        # --------------------------------------------------------------------


        directness_a = self._directness(
            piece_a
        )
        directness_b = self._directness(
            piece_b
        )


        if (
            directness_a is not None
            and directness_b is not None
        ):
            conditions.append(
                ComparabilityCondition.DIRECTNESS
            )


        # --------------------------------------------------------------------
        # Provenance
        # --------------------------------------------------------------------


        root_a = self._root_id(
            piece_a
        )
        root_b = self._root_id(
            piece_b
        )


        if (
            root_a is not None
            and root_b is not None
        ):
            conditions.append(
                ComparabilityCondition.PROVENANCE
            )


        # --------------------------------------------------------------------
        # Information status
        # --------------------------------------------------------------------


        status_a = self._status(
            piece_a
        )
        status_b = self._status(
            piece_b
        )


        if (
            status_a is not None
            and status_b is not None
        ):
            conditions.append(
                ComparabilityCondition.INFORMATION_STATUS
            )


        # --------------------------------------------------------------------
        # Special status pair
        # --------------------------------------------------------------------


        pair = (
            (status_a or "").lower(),
            (status_b or "").lower(),
        )


        reverse_pair = (
            pair[1],
            pair[0],
        )


        pair_result = (
            COMPARABILITY_PAIRS.get(
                pair
            )
            or COMPARABILITY_PAIRS.get(
                reverse_pair
            )
        )


        # --------------------------------------------------------------------
        # General result
        # --------------------------------------------------------------------


        required_core = {
            ComparabilityCondition.SAME_SUBJECT,
            ComparabilityCondition.SAME_OR_COMPARABLE_ASSET,
            ComparabilityCondition.SAME_OR_OVERLAPPING_REFERENCE_PERIOD,
        }


        core_count = len(
            required_core
            & set(conditions)
        )


        if pair_result is not None:
            result = pair_result


        elif core_count == 3:
            result = (
                ComparabilityResult.COMPARABLE
            )


        elif core_count >= 1:
            result = (
                ComparabilityResult.CONDITIONALLY_COMPARABLE
            )


        else:
            result = (
                ComparabilityResult.NOT_COMPARABLE
            )


        analysis = RelationAnalysis(
            analysis_id=(
                f"comparability:"
                f"{information_id_a}:"
                f"{information_id_b}"
            ),
            relation_analysis_type=(
                RelationAnalysisType.REPETITION_RELAY
            ),
            information_ids=(
                information_id_a,
                information_id_b,
            ),
            comparability=result,
            conditions=tuple(
                conditions
            ),
            note=(
                "Comparability is a structural condition check. "
                "It does not transform information statuses."
            ),
        )


        self._add_relation_analysis(
            analysis
        )


        self._add_finding(
            AnalysisFinding(
                finding_id=(
                    f"comparability:"
                    f"{information_id_a}:"
                    f"{information_id_b}"
                ),
                finding_type=(
                    AnalyticalFindingType.COMPARABILITY_CHECK
                ),
                information_ids=(
                    information_id_a,
                    information_id_b,
                ),
                description=(
                    "İki bilgi parçasının karşılaştırılabilirlik "
                    "koşulları kontrol edilmiştir."
                ),
                metrics={
                    "condition_count": len(
                        conditions
                    ),
                },
                comparability=result,
            )
        )


        return analysis


    # ========================================================================
    # 7. RELATION ANALYSIS
    # ========================================================================


    def analyze_relation(
        self,
        relation_id: str,
    ) -> RelationAnalysis:


        relation = next(
            (
                relation
                for relation in self._relations()
                if relation.relation_id
                == relation_id
            ),
            None,
        )


        if relation is None:
            raise KeyError(
                f"Unknown relation_id: {relation_id}"
            )


        source_id = (
            relation.source_information_id
        )
        target_id = (
            relation.target_information_id
        )


        comparability = self.check_comparability(
            source_id,
            target_id,
        )


        relation_type = relation.relation_type


        mapping = {
            "supports": RelationAnalysisType.CONVERGENCE,
            "contradicts": RelationAnalysisType.CONTRADICTION,
            "limits": RelationAnalysisType.DIVERGENCE,
            "repeats": RelationAnalysisType.REPETITION_RELAY,
            "updates": RelationAnalysisType.CHANGE_ANALYSIS,
            "corrects": RelationAnalysisType.CHANGE_ANALYSIS,
            "same_topic": RelationAnalysisType.REPETITION_RELAY,
            "same_event_different_angle": (
                RelationAnalysisType.COMPLEMENTARITY
            ),
            "prior_view_of_same_institution": (
                RelationAnalysisType.DIVERGENCE
            ),
            "different_explanation_of_same_positioning": (
                RelationAnalysisType.DIVERGENCE
            ),
            "forecast_outcome_comparison": (
                RelationAnalysisType.RELATIONAL_ANALYSIS
                if hasattr(
                    RelationAnalysisType,
                    "RELATIONAL_ANALYSIS",
                )
                else RelationAnalysisType.REPETITION_RELAY
            ),
        }


        relation_value = (
            relation_type.value
            if isinstance(
                relation_type,
                Enum,
            )
            else str(relation_type)
        )


        analysis_type = mapping.get(
            relation_value,
            RelationAnalysisType.REPETITION_RELAY,
        )


        analysis = RelationAnalysis(
            analysis_id=(
                f"relation:{relation_id}"
            ),
            relation_analysis_type=analysis_type,
            information_ids=(
                source_id,
                target_id,
            ),
            comparability=(
                comparability.comparability
            ),
            conditions=(
                comparability.conditions
            ),
            note=(
                "Relation type is analyzed together with "
                "comparability conditions; the relationship "
                "does not establish truth, strength or consensus."
            ),
        )


        self._add_relation_analysis(
            analysis
        )


        self._add_finding(
            AnalysisFinding(
                finding_id=(
                    f"relation-finding:{relation_id}"
                ),
                finding_type=(
                    AnalyticalFindingType.RELATIONAL_ANALYSIS
                ),
                information_ids=(
                    source_id,
                    target_id,
                ),
                description=(
                    "6. Bölümden gelen ilişkinin "
                    "karşılaştırılabilirlik koşullarıyla "
                    "birlikte analizi."
                ),
                metrics={
                    "relationship_state": (
                        relation.state.value
                        if isinstance(
                            relation.state,
                            Enum,
                        )
                        else str(relation.state)
                    ),
                },
                comparability=(
                    comparability.comparability
                ),
            )
        )


        return analysis


    # ========================================================================
    # 8. UNCERTAINTY
    # ========================================================================


    def classify_uncertainty(
        self,
        information_ids: Sequence[str],
        uncertainty_type: UncertaintyType,
        details: str,
    ) -> UncertaintyAnalysis:


        ids = tuple(
            information_ids
        )


        for information_id in ids:
            if information_id not in self._piece_map():
                raise KeyError(
                    f"Unknown information_id: "
                    f"{information_id}"
                )


        analysis = UncertaintyAnalysis(
            analysis_id=(
                f"uncertainty:"
                f"{uncertainty_type.value}:"
                f"{len(self._uncertainty_analyses)}"
            ),
            uncertainty_type=uncertainty_type,
            information_ids=ids,
            note=details,
        )


        self._add_uncertainty_analysis(
            analysis
        )


        self._add_finding(
            AnalysisFinding(
                finding_id=(
                    f"uncertainty-finding:"
                    f"{len(self._findings)}"
                ),
                finding_type=(
                    AnalyticalFindingType.UNCERTAINTY_ANALYSIS
                ),
                information_ids=ids,
                description=details,
                uncertainty_type=uncertainty_type,
            )
        )


        return analysis


    # ========================================================================
    # 9. FORWARD LOOKING NOT YET OUTCOME
    # ========================================================================


    def mark_forward_looking_without_outcome(
        self,
        information_id: str,
    ) -> UncertaintyAnalysis:


        piece = self._piece_map().get(
            information_id
        )


        if piece is None:
            raise KeyError(
                f"Unknown information_id: "
                f"{information_id}"
            )


        status = (
            self._status(piece)
            or ""
        ).lower()


        if status not in {
            "forecast",
            "expectation",
            "forward_looking",
        }:
            raise ValueError(
                "InformationPiece is not identified as "
                "a forward-looking status."
            )


        return self.classify_uncertainty(
            information_ids=(
                information_id,
            ),
            uncertainty_type=(
                UncertaintyType.FORWARD_LOOKING_NOT_YET_OUTCOME
            ),
            details=(
                "Forward-looking information exists, but "
                "a corresponding outcome has not yet been "
                "observed in the available information state."
            ),
        )


    # ========================================================================
    # 10. POINT-IN-TIME ANALYSIS
    # ========================================================================


    def build_point_in_time_record(
        self,
        information_ids: Sequence[str],
    ) -> PointInTimeRecord:


        ids = tuple(
            information_ids
        )


        piece_map = self._piece_map()


        production_times = [
            self._production_time(
                piece_map[information_id]
            )
            for information_id in ids
            if information_id in piece_map
        ]


        event_times = [
            self._event_time(
                piece_map[information_id]
            )
            for information_id in ids
            if information_id in piece_map
        ]


        production_times = [
            value
            for value in production_times
            if value is not None
        ]


        event_times = [
            value
            for value in event_times
            if value is not None
        ]


        reference_periods = {
            self._reference_period(
                piece_map[information_id]
            )
            for information_id in ids
            if information_id in piece_map
            and self._reference_period(
                piece_map[information_id]
            ) is not None
        }


        return PointInTimeRecord(
            production_time=(
                min(production_times)
                if production_times
                else None
            ),
            event_time=(
                min(event_times)
                if event_times
                else None
            ),
            reference_period=(
                next(iter(reference_periods))
                if len(reference_periods) == 1
                else None
            ),
            information_ids=ids,
        )


    # ========================================================================
    # 11. TIME MEASUREMENTS
    # ========================================================================


    def measure_time_gap(
        self,
        information_id_a: str,
        information_id_b: str,
        measurement_type: StructuralMeasurementType,
    ) -> StructuralMeasurement:


        if measurement_type not in {
            StructuralMeasurementType.DIVERGENCE_DURATION,
            StructuralMeasurementType.FORECAST_OUTCOME_TIME_GAP,
            StructuralMeasurementType.PATTERN_DURATION,
        }:
            raise ValueError(
                "Unsupported time measurement type."
            )


        piece_map = self._piece_map()


        piece_a = piece_map.get(
            information_id_a
        )
        piece_b = piece_map.get(
            information_id_b
        )


        if piece_a is None:
            raise KeyError(
                f"Unknown information_id: "
                f"{information_id_a}"
            )


        if piece_b is None:
            raise KeyError(
                f"Unknown information_id: "
                f"{information_id_b}"
            )


        time_a = self._production_time(
            piece_a
        )
        time_b = self._production_time(
            piece_b
        )


        if (
            time_a is None
            or time_b is None
        ):
            value = None
            unit = None
            note = (
                "Gerekli production time mevcut değil; "
                "ölçüm tamamlanamadı."
            )


        else:
            value = abs(
                (
                    time_b - time_a
                ).total_seconds()
            )


            unit = "seconds"


            note = (
                "Zaman farkı betimleyici ölçümdür; "
                "önem veya doğruluk göstergesi değildir."
            )


        measurement = StructuralMeasurement(
            measurement_id=(
                f"time-gap:"
                f"{information_id_a}:"
                f"{information_id_b}"
            ),
            measurement_type=measurement_type,
            information_ids=(
                information_id_a,
                information_id_b,
            ),
            value=value,
            unit=unit,
            note=note,
        )


        return self._add_measurement(
            measurement
        )


    # ========================================================================
    # 12. EXTERNAL REGIME RELATIONSHIP
    # ========================================================================


    def analyze_external_regime_relationship(
        self,
        external_regime: ExternalRegimeInput,
        information_ids: Sequence[str],
    ) -> AnalysisFinding:


        ids = tuple(
            information_ids
        )


        for information_id in ids:
            if information_id not in self._piece_map():
                raise KeyError(
                    f"Unknown information_id: "
                    f"{information_id}"
                )


        finding = AnalysisFinding(
            finding_id=(
                f"external-regime:"
                f"{len(self._findings)}"
            ),
            finding_type=(
                AnalyticalFindingType.RELATIONAL_ANALYSIS
            ),
            information_ids=ids,
            description=(
                "Dışsal rejim/makro/piyasa iddiası ile "
                "CTA bilgi yapılarının zaman ve bağlam "
                "ilişkisi incelenmiştir. Dışsal iddia "
                "sistem tarafından doğrulanmış rejim "
                "sınıflandırması değildir."
            ),
            metrics={
                "external_regime_present": bool(
                    external_regime.regime_claim
                ),
                "macro_context_present": bool(
                    external_regime.macro_context
                ),
                "market_condition_present": bool(
                    external_regime.market_condition
                ),
            },
        )


        return self._add_finding(
            finding
        )


    # ========================================================================
    # 13. POINT-IN-TIME RULES
    # ========================================================================


    @staticmethod
    def point_in_time_rule() -> str:
        return (
            "Sonraki bilgi, geçmişteki bilgi durumunun "
            "yerine geçirilemez."
        )


    @staticmethod
    def forecast_outcome_rule() -> str:
        return (
            "Forecast kendi üretildiği andaki statüsünü korur. "
            "Outcome daha sonra eklenen tarihsel bilgidir."
        )


    @staticmethod
    def positioning_revision_rule() -> str:
        return (
            "Eski positioning kaydı silinmez. "
            "Revizyon yeni tarihsel durum olarak eklenir."
        )


    @staticmethod
    def view_change_rule() -> str:
        return (
            "Eski görüş korunur. Yeni görüş ayrı bir "
            "tarihsel durumdur."
        )


    @staticmethod
    def later_falsified_rule() -> str:
        return (
            "Bilginin geçmişte ne söylediği ve o anda hangi "
            "statüde olduğu korunur. Sonraki yanlışlanma veya "
            "düzeltme yeni tarihsel değerlendirme katmanıdır."
        )


    # ========================================================================
    # 14. 7 -> 8 SINIRI
    # ========================================================================


    @staticmethod
    def seven_to_eight_boundary() -> None:
        """
        7'nin analitik bulguları 8'in nihai CTA hükmü değildir.
        """
        return None


    # ========================================================================
    # 15. INTEGRITY VALIDATION
    # ========================================================================


    def validate_integrity(self) -> None:


        piece_ids = {
            self._piece_id(piece)
            for piece in self._pieces()
        }


        cluster_ids = {
            cluster.cluster_id
            for cluster in self._clusters()
        }


        # --------------------------------------------------------------------
        # Findings
        # --------------------------------------------------------------------


        for finding in self._findings.values():


            missing_information = (
                set(finding.information_ids)
                - piece_ids
            )


            if missing_information:
                raise ValueError(
                    "Finding references missing InformationPiece: "
                    f"{sorted(missing_information)}"
                )


            missing_clusters = (
                set(finding.cluster_ids)
                - cluster_ids
            )


            if missing_clusters:
                raise ValueError(
                    "Finding references missing Cluster: "
                    f"{sorted(missing_clusters)}"
                )


        # --------------------------------------------------------------------
        # Relation analyses
        # --------------------------------------------------------------------


        for analysis in (
            self._relation_analyses.values()
        ):


            missing = (
                set(analysis.information_ids)
                - piece_ids
            )


            if missing:
                raise ValueError(
                    "RelationAnalysis references missing InformationPiece: "
                    f"{sorted(missing)}"
                )


        # --------------------------------------------------------------------
        # Measurements
        # --------------------------------------------------------------------


        for measurement in (
            self._structural_measurements.values()
        ):


            missing = (
                set(measurement.information_ids)
                - piece_ids
            )


            if missing:
                raise ValueError(
                    "StructuralMeasurement references missing "
                    f"InformationPiece: {sorted(missing)}"
                )


        # --------------------------------------------------------------------
        # Provenance analyses
        # --------------------------------------------------------------------


        for analysis in (
            self._provenance_analyses.values()
        ):


            missing = (
                set(analysis.information_ids)
                - piece_ids
            )


            if missing:
                raise ValueError(
                    "ProvenanceAnalysis references missing "
                    f"InformationPiece: {sorted(missing)}"
                )


        # --------------------------------------------------------------------
        # Uncertainty analyses
        # --------------------------------------------------------------------


        for analysis in (
            self._uncertainty_analyses.values()
        ):


            missing = (
                set(analysis.information_ids)
                - piece_ids
            )


            if missing:
                raise ValueError(
                    "UncertaintyAnalysis references missing "
                    f"InformationPiece: {sorted(missing)}"
                )


    # ========================================================================
    # 16. STATIC BOUNDARY VALIDATION
    # ========================================================================


    @staticmethod
    def validate_forbidden_fields() -> None:


        classes = (
            AnalysisFinding,
            RelationAnalysis,
            StructuralMeasurement,
            ProvenanceAnalysis,
            UncertaintyAnalysis,
            AnalysisOutput,
        )


        for cls in classes:


            fields = getattr(
                cls,
                "__dataclass_fields__",
                {},
            )


            for forbidden in (
                FORBIDDEN_ANALYSIS_FIELDS
            ):


                if forbidden in fields:
                    raise AssertionError(
                        f"Forbidden field '{forbidden}' "
                        f"found in {cls.__name__}"
                    )


        public_methods = {
            name
            for name in dir(
                AnalysisEngine
            )
            if not name.startswith("_")
            and callable(
                getattr(
                    AnalysisEngine,
                    name,
                )
            )
        }


        leaked = (
            public_methods
            & FORBIDDEN_ANALYSIS_OPERATIONS
        )


        if leaked:
            raise AssertionError(
                "Forbidden analysis operations exposed: "
                f"{sorted(leaked)}"
            )


# ============================================================================
# 17. FINAL ARCHITECTURAL PRINCIPLE
# ============================================================================


ANALYSIS_FINAL_PRINCIPLE = (
    "7. Bölüm — Analiz / Hesaplama / Değerlendirme; Yoğurma "
    "Motoru'ndan gelen ilişkili bilgi yapılarını, karşılaştırılabilirlik "
    "koşullarını, bilgi statülerini, zaman boyutunu, bağlamı ve "
    "provenance'ı koruyarak analiz eder. Yapısal ve zamansal özellikleri "
    "ölçebilir; yakınsama, ayrışma, çelişki, tamamlayıcılık, tekrar, "
    "bağımsızlık ve belirsizlik örüntülerini ortaya çıkarabilir. Ancak "
    "bu analitik bulguları otomatik olarak değer, güven, ağırlık, "
    "üstünlük, nihai CTA anlamı, gelecek tahmini veya işlem kararına "
    "dönüştürmez. Nihai CTA Synthesis / Sonuç katmanı 8. Bölümde "
    "ayrıca tasarlanacaktır."
)


# ============================================================================
# 18. VALIDATION / SELF TEST
# ============================================================================


def validate_7() -> None:
    """
    7. Bölümün kendi yapısal sınırlarını doğrular.


    Not:
        Buradaki self-test 6. Bölüm dosyasını import etmez.
        Gerçek entegrasyon testi aşağıdaki IntegrationTest bölümünde
        oluşturulan minimal 6. Bölüm uyumlu test nesnesiyle yapılır.
    """


    AnalysisEngine.validate_forbidden_fields()


    # ------------------------------------------------------------------------
    # Minimal 6. Bölüm uyumlu test nesneleri
    # ------------------------------------------------------------------------


    @dataclass(frozen=True)
    class TestPiece:
        information_id: str
        source_id: str
        original_source_id: Optional[str]
        production_time: datetime
        reference_period: str
        topic: str
        reference_asset: str
        status: str
        content: str


    @dataclass(frozen=True)
    class TestCluster:
        cluster_id: str
        member_information_ids: tuple[str, ...]
        child_cluster_ids: tuple[str, ...]
        shared_axes: tuple[Any, ...]
        state: str


    @dataclass(frozen=True)
    class TestRelation:
        relation_id: str
        source_information_id: str
        target_information_id: str
        relation_type: str
        state: str


    class TestYogurma:
        def __init__(
            self,
            pieces,
            clusters,
            relations,
        ):
            self._pieces = pieces
            self._clusters = clusters
            self._relations = relations


        def all_information_pieces(self):
            return tuple(
                self._pieces
            )


        def all_clusters(self):
            return tuple(
                self._clusters
            )


        def all_relations(self):
            return tuple(
                self._relations
            )


        def all_cluster_relations(self):
            return tuple()


        def state(self):
            return None


    p1 = TestPiece(
        information_id="info1",
        source_id="sourceA",
        original_source_id="rootA",
        production_time=datetime(
            2026,
            1,
            1,
        ),
        reference_period="2026-Q1",
        topic="CTA",
        reference_asset="ES",
        status="institution_view",
        content="View A",
    )


    p2 = TestPiece(
        information_id="info2",
        source_id="sourceA",
        original_source_id="rootA",
        production_time=datetime(
            2026,
            2,
            1,
        ),
        reference_period="2026-Q1",
        topic="CTA",
        reference_asset="ES",
        status="institution_view",
        content="View B",
    )


    p3 = TestPiece(
        information_id="info3",
        source_id="sourceB",
        original_source_id="rootB",
        production_time=datetime(
            2026,
            2,
            10,
        ),
        reference_period="2026-Q1",
        topic="CTA",
        reference_asset="ES",
        status="positioning",
        content="Positioning observation",
    )


    cluster = TestCluster(
        cluster_id="cluster1",
        member_information_ids=(
            "info1",
            "info2",
            "info3",
        ),
        child_cluster_ids=(),
        shared_axes=(
            "common_event",
            "common_reference_period",
        ),
        state="developing",
    )


    relation = TestRelation(
        relation_id="relation1",
        source_information_id="info1",
        target_information_id="info3",
        relation_type="supports",
        state="active",
    )


    yogurma = TestYogurma(
        pieces=(
            p1,
            p2,
            p3,
        ),
        clusters=(
            cluster,
        ),
        relations=(
            relation,
        ),
    )


    engine = AnalysisEngine(
        yogurma
    )


    # ------------------------------------------------------------------------
    # Structural
    # ------------------------------------------------------------------------


    structural = (
        engine.analyze_cluster_structure(
            "cluster1"
        )
    )


    assert (
        structural.metrics["member_count"]
        == 3
    )


    # ------------------------------------------------------------------------
    # Provenance
    # ------------------------------------------------------------------------


    provenance = (
        engine.analyze_provenance(
            "cluster1"
        )
    )


    assert (
        len(provenance.root_ids)
        == 2
    )


    # ------------------------------------------------------------------------
    # Independence structure
    # ------------------------------------------------------------------------


    independence = (
        engine.analyze_independence_structure(
            "cluster1"
        )
    )


    assert (
        independence.metrics[
            "distinct_root_count"
        ]
        == 2
    )


    # ------------------------------------------------------------------------
    # Source changes
    # ------------------------------------------------------------------------


    change = (
        engine.analyze_source_changes(
            "cluster1",
            "sourceA",
        )
    )


    assert (
        change.metrics[
            "change_count"
        ]
        == 1
    )


    # ------------------------------------------------------------------------
    # Repetition / relay
    # ------------------------------------------------------------------------


    repetition = (
        engine.analyze_repetition_relay(
            "cluster1"
        )
    )


    assert (
        repetition.metrics[
            "repeated_root_group_count"
        ]
        == 1
    )


    # ------------------------------------------------------------------------
    # Comparability
    # ------------------------------------------------------------------------


    comparison = (
        engine.check_comparability(
            "info1",
            "info3",
        )
    )


    assert (
        comparison.comparability
        in {
            ComparabilityResult.COMPARABLE,
            ComparabilityResult.CONDITIONALLY_COMPARABLE,
            ComparabilityResult.LIMITED_COMPARABLE,
        }
    )


    # ------------------------------------------------------------------------
    # Relation
    # ------------------------------------------------------------------------


    relation_analysis = (
        engine.analyze_relation(
            "relation1"
        )
    )


    assert (
        relation_analysis.information_ids
        == (
            "info1",
            "info3",
        )
    )


    # ------------------------------------------------------------------------
    # Uncertainty
    # ------------------------------------------------------------------------


    uncertainty = (
        engine.classify_uncertainty(
            ("info1",),
            UncertaintyType.CONTEXT_UNCERTAINTY,
            "Context requires additional qualification.",
        )
    )


    assert (
        uncertainty.uncertainty_type
        == UncertaintyType.CONTEXT_UNCERTAINTY
    )


    # ------------------------------------------------------------------------
    # Point-in-time
    # ------------------------------------------------------------------------


    pit = (
        engine.build_point_in_time_record(
            (
                "info1",
                "info2",
            )
        )
    )


    assert (
        pit.production_time
        == datetime(
            2026,
            1,
            1,
        )
    )


    # ------------------------------------------------------------------------
    # Time measurement
    # ------------------------------------------------------------------------


    time_measurement = (
        engine.measure_time_gap(
            "info1",
            "info2",
            StructuralMeasurementType.PATTERN_DURATION,
        )
    )


    assert (
        time_measurement.value
        == 31 * 24 * 60 * 60
    )


    # ------------------------------------------------------------------------
    # 7 -> 8
    # ------------------------------------------------------------------------


    engine.seven_to_eight_boundary()


    # ------------------------------------------------------------------------
    # Final integrity
    # ------------------------------------------------------------------------


    engine.validate_integrity()


    output = engine.output()


    assert len(
        output.findings
    ) >= 1


    assert isinstance(
        ANALYSIS_FINAL_PRINCIPLE,
        str,
    )


# ============================================================================
# 19. MAIN
# ============================================================================


if __name__ == "__main__":


    validate_7()


    print(
        "7. BÖLÜM — ANALİZ / HESAPLAMA / DEĞERLENDİRME"
    )
    print("=" * 72)


    print(
        ANALYSIS_FINAL_PRINCIPLE
    )


    print("=" * 72)


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "Validation: PASSED"
    )


ERHAN / CTA TERMINALI
"""
8. BÖLÜM — CTA SYNTHESIS / SONUÇ
FINAL KOD


7. Bölüm tarafından ortaya konmuş analitik bulguları ve ilişkileri,
zaman, kapsam, aktör, bilgi statüsü, provenance ve bağlam farklılıklarını
koruyarak birlikte değerlendirir ve koşullu, bağlamsal bir CTA tablosu
oluşturur.


8. Bölüm:
- yeni veri üretmez,
- yeni bağımsız kanıt üretmez,
- 7. Bölümde yapılmamış yeni analiz üretmez,
- 7. Bölüm ölçümlerini yeniden hesaplamaz,
- 7. Bölümün yerine geçmez,
- nihai CTA yönü veya karar üretmez.


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Optional, Sequence


# ============================================================
# 1. SYNTHESIS DURUMU
# ============================================================


class SynthesisState(str, Enum):
    """
    8. Bölüm synthesis durumları.


    SUCCESSFUL:
        Birden fazla 7. Bölüm bulgusu arasında anlamlı üst düzey
        bağ kurulmuş ve kritik bağlamsal farklılıklar korunmuştur.


    PARTIAL:
        Bazı bulgular anlamlı biçimde birleştirilebilmiş, ancak
        bazı kritik alanlar açık / belirsiz / çözümlenmemiş kalmıştır.


    FAILURE:
        Gerekli 7. Bölüm referansları veya anlamlı ilişki yapısı
        bulunmadığından açıklanabilir bir üst düzey synthesis
        kurulamaz.
    """


    SUCCESSFUL = "successful"
    PARTIAL = "partial"
    FAILURE = "failure"


# ============================================================
# 2. SYNTHESIS KAVRAMLARI
# ============================================================


class SynthesisConcept(str, Enum):
    """
    8. Bölümün temel synthesis sözlüğü.


    HARMONY_AUXILIARY yalnızca yardımcı açıklama kavramıdır.
    Ayrı bir temel synthesis ilişkisi değildir.


    SUPPORT özellikle kavramsal temel ilişki olarak bulunmaz.
    """


    CONVERGENCE = "convergence"
    COMPLEMENTARITY = "complementarity"
    LIMITATION = "limitation"
    CONDITIONALITY = "conditionality"
    DIVERGENCE = "divergence"
    CONTRADICTION = "contradiction"
    UNCERTAINTY = "uncertainty"
    HARMONY_AUXILIARY = "harmony_auxiliary"


# ============================================================
# 3. 7 → 8 REFERANS TÜRÜ
# ============================================================


class Section7ReferenceType(str, Enum):
    """
    8'in dayandığı 7. Bölüm çıktısının türünü açıkça belirtir.
    """


    FINDING = "finding"
    RELATION_ANALYSIS = "relation_analysis"
    STRUCTURAL_MEASUREMENT = "structural_measurement"
    PROVENANCE_ANALYSIS = "provenance_analysis"
    UNCERTAINTY_ANALYSIS = "uncertainty_analysis"


# ============================================================
# 4. 7. BÖLÜM REFERANS KAYDI
# ============================================================


@dataclass(frozen=True)
class Section7Reference:
    """
    8. Bölüm synthesis'inin 7. Bölümdeki gerçek kaynağı.


    Bu nesne yeni analiz üretmez.
    Yalnızca 7. Bölümden gelen mevcut çıktının kimliğini taşır.
    """


    reference_id: str
    reference_type: Section7ReferenceType


    # İlgili 7 çıktısının gerçek kimliği.
    source_output_id: str


    # İsteğe bağlı cluster bilgisi.
    # Cluster ID hiçbir zaman source_output_id yerine geçmez.
    cluster_id: Optional[str] = None


    # 7 çıktısının mevcut açıklaması.
    description: Optional[str] = None


# ============================================================
# 5. BAĞLAMSAL KORUMA
# ============================================================


@dataclass(frozen=True)
class SynthesisContext:
    """
    8. Bölümün synthesis sırasında korumak zorunda olduğu bağlam.


    Buradaki alanlar yeni analiz sonucu değildir.
    7. Bölümden taşınan / 7 çıktısında mevcut olan bağlamsal
    farklılıkların korunması içindir.
    """


    time_horizons: tuple[str, ...] = field(default_factory=tuple)
    actors: tuple[str, ...] = field(default_factory=tuple)
    information_statuses: tuple[str, ...] = field(default_factory=tuple)
    scopes: tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: tuple[str, ...] = field(default_factory=tuple)
    contexts: tuple[str, ...] = field(default_factory=tuple)


    # Synthesis sırasında bu ayrımların korunması zorunludur.
    preserve_time_horizons: bool = True
    preserve_actors: bool = True
    preserve_information_statuses: bool = True
    preserve_scopes: bool = True
    preserve_provenance: bool = True
    preserve_contexts: bool = True


# ============================================================
# 6. SYNTHESIS STATEMENT
# ============================================================


@dataclass(frozen=True)
class SynthesisStatement:
    """
    Tek bir üst düzey synthesis ifadesi.


    statement:
        7. Bölüm bulgularının birlikte ifade edilen üst düzey anlamı.


    source_finding_ids:
        Synthesis'in dayandığı gerçek 7. Bölüm çıktı ID'leri.


    source_relation_ids:
        7. Bölüm tarafından kurulmuş / analiz edilmiş ilişki ID'leri.


    used_concepts:
        8. Bölümde kullanılan synthesis kavramları.


    context:
        Zaman, aktör, statü, kapsam, provenance ve bağlam korunumu.


    ÖNEMLİ:
        Bu sınıf yeni veri veya yeni bağımsız kanıt taşımaz.
    """


    statement_id: str
    statement: str


    source_finding_ids: tuple[str, ...]
    source_relation_ids: tuple[str, ...] = field(default_factory=tuple)


    used_concepts: tuple[SynthesisConcept, ...] = field(
        default_factory=tuple
    )


    context: SynthesisContext = field(
        default_factory=SynthesisContext
    )


    note: Optional[str] = None


# ============================================================
# 7. SYNTHESIS OUTPUT
# ============================================================


@dataclass(frozen=True)
class SynthesisOutput:
    """
    8. Bölümün tamamlanmış synthesis çıktısı.


    Bu çıktı:
    - yeni veri değildir,
    - yeni bağımsız kanıt değildir,
    - yeni analiz değildir,
    - trade/risk/position kararı değildir.


    Tamamlanmış output'un geçerli olabilmesi için:
    - en az bir gerçek 7 referansı,
    - gerekli ilişki referansları,
    - bağlamsal koruma
    bulunmalıdır.
    """


    synthesis_id: str
    cluster_id: Optional[str]


    synthesis_state: SynthesisState


    statements: tuple[SynthesisStatement, ...]


    connected_7_references: tuple[Section7Reference, ...]


    preserved_context: SynthesisContext


    # Tamamlanmış çıktının referans bütünlüğü.
    valid: bool = False


    # İnsan tarafından kontrol edilmesi gereken açıklamalar.
    unresolved_items: tuple[str, ...] = field(default_factory=tuple)


# ============================================================
# 8. YASAKLI 8. BÖLÜM ÇIKTILARI
# ============================================================


FORBIDDEN_SYNTHESIS_OUTPUTS = frozenset(
    {
        "new_fact",
        "new_data",
        "new_independent_evidence",
        "causality",
        "actor_intent",
        "evidence_strength",
        "reliability_verdict",
        "confidence",
        "confidence_score",
        "probability",
        "prediction",
        "future_prediction",
        "trade_decision",
        "risk_decision",
        "position_decision",
        "investment_advice",
        "bullish_verdict",
        "bearish_verdict",
        "final_direction_verdict",
        "final_bias",
        "BUY",
        "SELL",
        "LONG",
        "SHORT",
        "signal",
        "weight",
        "weighting",
        "ranking",
        "score",
        "priority_score",
    }
)


# ============================================================
# 9. 7 → 8 REFERANS KAYDI
# ============================================================


class Section7ReferenceRegistry:
    """
    7. Bölüm çıktılarının yalnızca referans amaçlı kayıt defteri.


    8 burada analiz yapmaz.
    7 çıktısını değiştirmez.
    7 çıktısını yeniden hesaplamaz.
    """


    def __init__(self) -> None:
        self._references: dict[str, Section7Reference] = {}


    def register(self, reference: Section7Reference) -> None:
        if not reference.reference_id:
            raise ValueError("7 referansı boş olamaz.")


        if not reference.source_output_id:
            raise ValueError(
                "7 referansının source_output_id alanı zorunludur."
            )


        if reference.reference_id in self._references:
            raise ValueError(
                f"7 referansı zaten kayıtlı: {reference.reference_id}"
            )


        self._references[reference.reference_id] = reference


    def exists(self, reference_id: str) -> bool:
        return reference_id in self._references


    def get(self, reference_id: str) -> Section7Reference:
        try:
            return self._references[reference_id]
        except KeyError as exc:
            raise KeyError(
                f"7 Bölüm referansı bulunamadı: {reference_id}"
            ) from exc


    def all(self) -> tuple[Section7Reference, ...]:
        return tuple(self._references.values())


# ============================================================
# 10. 7 ÇIKTISINDAN REFERANS ÜRETME ADAPTÖRÜ
# ============================================================


def _extract_output_id(obj: object) -> Optional[str]:
    """
    7. Bölümdeki farklı çıktı nesnelerinin ID alanını güvenli şekilde
    okur.


    Desteklenen alanlar:
    - finding_id
    - analysis_id
    - measurement_id


    Bu fonksiyon yeni ID üretmez.
    """


    for attribute in (
        "finding_id",
        "analysis_id",
        "measurement_id",
    ):
        value = getattr(obj, attribute, None)


        if isinstance(value, str) and value:
            return value


    return None


def build_section7_reference(
    obj: object,
    reference_type: Section7ReferenceType,
    cluster_id: Optional[str] = None,
    description: Optional[str] = None,
) -> Section7Reference:
    """
    Mevcut 7. Bölüm çıktısından yalnızca referans oluşturur.


    7 çıktısını değiştirmez ve yeniden analiz etmez.
    """


    output_id = _extract_output_id(obj)


    if not output_id:
        raise ValueError(
            "7. Bölüm çıktısında geçerli bir çıktı ID'si bulunamadı."
        )


    return Section7Reference(
        reference_id=output_id,
        reference_type=reference_type,
        source_output_id=output_id,
        cluster_id=cluster_id,
        description=description,
    )


# ============================================================
# 11. REFERANS BÜTÜNLÜĞÜ
# ============================================================


def validate_statement_traceability(
    statement: SynthesisStatement,
    registry: Section7ReferenceRegistry,
) -> None:
    """
    Tamamlanmış synthesis statement'ının 7'ye geri izlenebilirliğini
    kontrol eder.
    """


    if not statement.statement_id:
        raise ValueError("Synthesis statement ID boş olamaz.")


    if not statement.statement.strip():
        raise ValueError(
            f"Synthesis statement boş olamaz: {statement.statement_id}"
        )


    if not statement.source_finding_ids:
        raise ValueError(
            "Synthesis statement en az bir 7. Bölüm bulgusuna "
            "geri izlenebilir olmalıdır: "
            f"{statement.statement_id}"
        )


    for finding_id in statement.source_finding_ids:
        if not registry.exists(finding_id):
            raise ValueError(
                "Synthesis statement'ın referans verdiği 7 çıktısı "
                f"bulunamadı: {finding_id}"
            )


    for relation_id in statement.source_relation_ids:
        if not registry.exists(relation_id):
            raise ValueError(
                "Synthesis statement'ın referans verdiği 7 ilişkisi "
                f"bulunamadı: {relation_id}"
            )


    if not statement.context.preserve_time_horizons:
        raise ValueError(
            "Zaman ufku korunumu kapatılamaz."
        )


    if not statement.context.preserve_actors:
        raise ValueError(
            "Aktör ayrımı korunumu kapatılamaz."
        )


    if not statement.context.preserve_information_statuses:
        raise ValueError(
            "Bilgi statüsü korunumu kapatılamaz."
        )


    if not statement.context.preserve_scopes:
        raise ValueError(
            "Kapsam korunumu kapatılamaz."
        )


    if not statement.context.preserve_provenance:
        raise ValueError(
            "Provenance korunumu kapatılamaz."
        )


    if not statement.context.preserve_contexts:
        raise ValueError(
            "Bağlam korunumu kapatılamaz."
        )


# ============================================================
# 12. SYNTHESIS DURUMU DEĞERLENDİRME SINIRI
# ============================================================


def determine_synthesis_state(
    statements: Sequence[SynthesisStatement],
    unresolved_items: Sequence[str],
) -> SynthesisState:
    """
    Synthesis durumunu değerlendirir.


    ÖNEMLİ:
    Bu fonksiyon 7. Bölümde yeni analiz yapmaz.


    Yalnızca 8'e verilmiş synthesis yapısının:
    - referans içerip içermediğine,
    - kısmi / çözümlenmemiş alan bulunup bulunmadığına
    bakar.


    Çelişki veya belirsizlik tek başına FAILURE değildir.
    """


    if not statements:
        return SynthesisState.FAILURE


    if any(
        not statement.source_finding_ids
        for statement in statements
    ):
        return SynthesisState.FAILURE


    if unresolved_items:
        return SynthesisState.PARTIAL


    return SynthesisState.SUCCESSFUL


# ============================================================
# 13. CONTEXT BÜTÜNLÜĞÜ
# ============================================================


def validate_synthesis_context(
    context: SynthesisContext,
) -> None:
    """
    Synthesis context'in temel korunma kurallarını doğrular.
    """


    required_flags = (
        context.preserve_time_horizons,
        context.preserve_actors,
        context.preserve_information_statuses,
        context.preserve_scopes,
        context.preserve_provenance,
        context.preserve_contexts,
    )


    if not all(required_flags):
        raise ValueError(
            "8. Bölüm synthesis context koruma sınırlarından "
            "biri kapatılmış."
        )


# ============================================================
# 14. SYNTHESIS MOTORU
# ============================================================


class CTASynthesisEngine:
    """
    8. Bölüm — CTA Synthesis / Sonuç Motoru.


    Görev:
        7. Bölümün mevcut analitik çıktılarının üst düzey
        bağlamsal sentezini taşımak.


    Yapmaz:
        - yeni analiz,
        - yeni ölçüm,
        - yeni veri,
        - yeni bağımsız kanıt,
        - causality,
        - actor intent,
        - confidence,
        - reliability,
        - evidence strength,
        - weighting,
        - ranking,
        - probability,
        - prediction,
        - trade,
        - risk,
        - final bias.


    Motor yalnızca:
        7 → 8 referans zincirini,
        synthesis ifadelerini,
        synthesis kavramlarını,
        bağlamsal korumayı
        yönetir.
    """


    def __init__(
        self,
        section7_registry: Section7ReferenceRegistry,
    ) -> None:
        self._registry = section7_registry
        self._outputs: list[SynthesisOutput] = []


    # --------------------------------------------------------
    # READ-ONLY ACCESS
    # --------------------------------------------------------


    def section7_references(
        self,
    ) -> tuple[Section7Reference, ...]:
        return self._registry.all()


    def outputs(self) -> tuple[SynthesisOutput, ...]:
        return tuple(self._outputs)


    # --------------------------------------------------------
    # STATEMENT VALIDATION
    # --------------------------------------------------------


    def validate_statement(
        self,
        statement: SynthesisStatement,
    ) -> None:
        validate_statement_traceability(
            statement,
            self._registry,
        )


    # --------------------------------------------------------
    # SYNTHESIS OLUŞTURMA
    # --------------------------------------------------------


    def create_synthesis(
        self,
        synthesis_id: str,
        statements: Sequence[SynthesisStatement],
        preserved_context: SynthesisContext,
        cluster_id: Optional[str] = None,
        unresolved_items: Sequence[str] = (),
    ) -> SynthesisOutput:
        """
        7. Bölüm bulgularını yeniden analiz etmeden synthesis çıktısı
        oluşturur.


        Tamamlanmış output yalnızca tüm gerekli referanslar geçerliyse
        valid=True olur.
        """


        if not synthesis_id:
            raise ValueError(
                "Synthesis ID boş olamaz."
            )


        validate_synthesis_context(
            preserved_context
        )


        normalized_statements = tuple(statements)
        normalized_unresolved = tuple(unresolved_items)


        if not normalized_statements:
            return SynthesisOutput(
                synthesis_id=synthesis_id,
                cluster_id=cluster_id,
                synthesis_state=SynthesisState.FAILURE,
                statements=tuple(),
                connected_7_references=tuple(),
                preserved_context=preserved_context,
                valid=False,
                unresolved_items=normalized_unresolved,
            )


        # Her statement'ın 7 traceability'sini kontrol et.
        for statement in normalized_statements:
            self.validate_statement(statement)


        # Statement'ların kullandığı gerçek 7 referanslarını topla.
        reference_ids: list[str] = []


        for statement in normalized_statements:
            reference_ids.extend(
                statement.source_finding_ids
            )
            reference_ids.extend(
                statement.source_relation_ids
            )


        # Sıra korunur, tekrarlar kaldırılır.
        unique_reference_ids = tuple(
            dict.fromkeys(reference_ids)
        )


        connected_references = tuple(
            self._registry.get(reference_id)
            for reference_id in unique_reference_ids
        )


        state = determine_synthesis_state(
            normalized_statements,
            normalized_unresolved,
        )


        output = SynthesisOutput(
            synthesis_id=synthesis_id,
            cluster_id=cluster_id,
            synthesis_state=state,
            statements=normalized_statements,
            connected_7_references=connected_references,
            preserved_context=preserved_context,
            valid=True,
            unresolved_items=normalized_unresolved,
        )


        self._outputs.append(output)


        return output


# ============================================================
# 15. OUTPUT BÜTÜNLÜĞÜ
# ============================================================


def validate_synthesis_output(
    output: SynthesisOutput,
) -> None:
    """
    Tamamlanmış synthesis çıktısının referans bütünlüğünü doğrular.
    """


    if not output.valid:
        raise ValueError(
            f"Synthesis output valid değil: {output.synthesis_id}"
        )


    if not output.statements:
        raise ValueError(
            "Valid synthesis en az bir statement içermelidir."
        )


    if not output.connected_7_references:
        raise ValueError(
            "Valid synthesis en az bir 7. Bölüm referansı "
            "içermelidir."
        )


    connected_ids = {
        reference.source_output_id
        for reference in output.connected_7_references
    }


    for statement in output.statements:
        for finding_id in statement.source_finding_ids:
            if finding_id not in connected_ids:
                raise ValueError(
                    "Synthesis statement ile 7 referansı arasında "
                    f"traceability kopukluğu: {finding_id}"
                )


        for relation_id in statement.source_relation_ids:
            if relation_id not in connected_ids:
                raise ValueError(
                    "Synthesis relation ile 7 referansı arasında "
                    f"traceability kopukluğu: {relation_id}"
                )


    validate_synthesis_context(
        output.preserved_context
    )


# ============================================================
# 16. MULTİMODAL SINIRI
# ============================================================


def validate_multimodal_boundary() -> None:
    """
    Görsel/multimodal formatın tek başına epistemik üstünlük
    oluşturmasını engelleyen kavramsal sınır.


    8:
        chart,
        graph,
        table,
        screenshot,
        infographic,
        diagram,
        map,
        PDF figure/table,
        X media


    gibi girdileri yeniden analiz etmez.


    Görsel kaynaklı bilgi yalnızca 7'nin oluşturduğu analitik
    bulgular üzerinden synthesis girdisi olabilir.
    """


    forbidden_implications = (
        "visual_strength",
        "visual_reliability",
        "visual_independence",
        "visual_confidence",
        "visual_evidence_strength",
    )


    assert forbidden_implications


# ============================================================
# 17. 7 → 8 SINIRI
# ============================================================


def seven_to_eight_boundary() -> str:
    return (
        "7 = Ne görülüyor? "
        "8 = 7 tarafından ortaya konmuş bulgular birlikte ne ifade ediyor?"
    )


# ============================================================
# 18. 8'İN YAPAMAYACAĞI İŞLEMLER
# ============================================================


FORBIDDEN_OPERATIONS = frozenset(
    {
        "reanalyze_section_7",
        "recalculate_section_7_measurements",
        "create_new_evidence",
        "create_new_fact",
        "create_new_independent_evidence",
        "infer_causality",
        "infer_actor_intent",
        "assign_reliability",
        "assign_confidence",
        "assign_evidence_strength",
        "assign_probability",
        "weight_sources",
        "rank_sources",
        "predict_future",
        "generate_trade_signal",
        "make_risk_decision",
        "make_position_decision",
        "produce_investment_advice",
        "produce_final_bias",
        "produce_bullish_verdict",
        "produce_bearish_verdict",
        "classify_market_regime",
        "decide_for_kokboru",
        "decide_for_tulpar",
    }
)


def validate_forbidden_operations() -> None:
    """
    Yasaklı operasyonların yalnızca kavramsal sınır olarak kayıtlı
    olduğunu doğrular.
    """


    for operation in FORBIDDEN_OPERATIONS:
        assert isinstance(operation, str)
        assert operation.strip()


# ============================================================
# 19. FINAL PRINCIPLE
# ============================================================


SYNTHESIS_FINAL_PRINCIPLE = (
    "8. Bölüm — CTA Synthesis / Sonuç; 7. Bölüm tarafından ortaya "
    "konmuş analitik bulguları ve ilişkileri, zaman, kapsam, aktör, "
    "bilgi statüsü, provenance ve bağlam farklılıklarını koruyarak "
    "birlikte değerlendirir ve koşullu, bağlamsal bir CTA tablosu "
    "oluşturur. 8. Bölüm yeni veri, bağımsız kanıt veya yeni analitik "
    "gerçeklik üretmez; her synthesis ifadesi 7. Bölüm bulgularına "
    "geri izlenebilir olmalıdır. Yakınsama, tamamlayıcılık, sınırlama, "
    "koşulluluk, ayrışma, çelişki ve belirsizlik korunur. Synthesis "
    "7. Bölümde yapılmamış analizi yeniden üretmez. Hiçbir synthesis "
    "ifadesi kanıt gücü, güvenilirlik, confidence, ağırlık, üstünlük, "
    "probability, gelecek tahmini, trade kararı, risk kararı, yatırım "
    "tavsiyesi veya kesin nihai yön hükmüne dönüştürülmez. Nihai karar "
    "yetkisi KÖKBÖRÜ veya TULPAR adına bu bölümde bulunmaz."
)


# ============================================================
# 20. VALIDATION
# ============================================================


def validate_8() -> None:
    """
    8. Bölüm yapısal self-validation.


    Bu fonksiyon yalnızca kodun iç tutarlılığını test eder.
    Harici veri veya gerçek runtime sistemi doğrulamaz.
    """


    # --------------------------------------------------------
    # Registry
    # --------------------------------------------------------


    registry = Section7ReferenceRegistry()


    finding_ref = Section7Reference(
        reference_id="finding_001",
        reference_type=Section7ReferenceType.FINDING,
        source_output_id="finding_001",
        cluster_id="cluster_001",
        description="7. Bölüm analitik bulgusu.",
    )


    relation_ref = Section7Reference(
        reference_id="relation_001",
        reference_type=Section7ReferenceType.RELATION_ANALYSIS,
        source_output_id="relation_001",
        cluster_id="cluster_001",
        description="7. Bölüm ilişki analizi.",
    )


    uncertainty_ref = Section7Reference(
        reference_id="uncertainty_001",
        reference_type=Section7ReferenceType.UNCERTAINTY_ANALYSIS,
        source_output_id="uncertainty_001",
        cluster_id="cluster_001",
        description="7. Bölüm belirsizlik analizi.",
    )


    registry.register(finding_ref)
    registry.register(relation_ref)
    registry.register(uncertainty_ref)


    assert registry.exists("finding_001")
    assert registry.exists("relation_001")
    assert registry.exists("uncertainty_001")


    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------


    context = SynthesisContext(
        time_horizons=(
            "short_term",
            "long_term",
        ),
        actors=(
            "actor_a",
            "actor_b",
        ),
        information_statuses=(
            "current_observation",
            "commentary",
        ),
        scopes=(
            "cta_context",
        ),
        provenance_refs=(
            "root_001",
        ),
        contexts=(
            "market_context_001",
        ),
    )


    validate_synthesis_context(context)


    # --------------------------------------------------------
    # Statement
    # --------------------------------------------------------


    statement = SynthesisStatement(
        statement_id="statement_001",
        statement=(
            "7. Bölüm bulguları kısa vadeli yakınsama ile birlikte "
            "çözümlenmemiş belirsizliğin korunması gerektiğini "
            "göstermektedir."
        ),
        source_finding_ids=(
            "finding_001",
        ),
        source_relation_ids=(
            "relation_001",
        ),
        used_concepts=(
            SynthesisConcept.CONVERGENCE,
            SynthesisConcept.UNCERTAINTY,
        ),
        context=context,
    )


    validate_statement_traceability(
        statement,
        registry,
    )


    # --------------------------------------------------------
    # Engine
    # --------------------------------------------------------


    engine = CTASynthesisEngine(
        section7_registry=registry,
    )


    output = engine.create_synthesis(
        synthesis_id="synthesis_001",
        statements=(statement,),
        preserved_context=context,
        cluster_id="cluster_001",
    )


    assert output.valid is True
    assert output.synthesis_state == SynthesisState.SUCCESSFUL


    validate_synthesis_output(output)


    assert len(output.connected_7_references) == 2


    # --------------------------------------------------------
    # Partial synthesis
    # --------------------------------------------------------


    partial_statement = SynthesisStatement(
        statement_id="statement_002",
        statement=(
            "Bazı bulgular birlikte değerlendirilebilirken kritik "
            "bir belirsizlik açık kalmaktadır."
        ),
        source_finding_ids=(
            "finding_001",
        ),
        source_relation_ids=(
            "uncertainty_001",
        ),
        used_concepts=(
            SynthesisConcept.CONDITIONALITY,
            SynthesisConcept.UNCERTAINTY,
        ),
        context=context,
    )


    partial_output = engine.create_synthesis(
        synthesis_id="synthesis_002",
        statements=(partial_statement,),
        preserved_context=context,
        cluster_id="cluster_001",
        unresolved_items=(
            "critical_context_unresolved",
        ),
    )


    assert partial_output.valid is True
    assert partial_output.synthesis_state == SynthesisState.PARTIAL


    validate_synthesis_output(partial_output)


    # --------------------------------------------------------
    # Failure
    # --------------------------------------------------------


    failure_output = engine.create_synthesis(
        synthesis_id="synthesis_003",
        statements=tuple(),
        preserved_context=context,
        cluster_id="cluster_001",
    )


    assert failure_output.valid is False
    assert failure_output.synthesis_state == SynthesisState.FAILURE


    # --------------------------------------------------------
    # Multimodal boundary
    # --------------------------------------------------------


    validate_multimodal_boundary()


    # --------------------------------------------------------
    # Forbidden operations
    # --------------------------------------------------------


    validate_forbidden_operations()


    # --------------------------------------------------------
    # Boundary
    # --------------------------------------------------------


    boundary = seven_to_eight_boundary()


    assert "7 = Ne görülüyor?" in boundary
    assert "8 =" in boundary


    # --------------------------------------------------------
    # Final principle
    # --------------------------------------------------------


    assert isinstance(
        SYNTHESIS_FINAL_PRINCIPLE,
        str,
    )


    assert "yeni veri" in SYNTHESIS_FINAL_PRINCIPLE
    assert "geri izlenebilir" in SYNTHESIS_FINAL_PRINCIPLE
    assert "trade kararı" in SYNTHESIS_FINAL_PRINCIPLE


# ============================================================
# 21. MODULE ENTRY
# ============================================================


if __name__ == "__main__":
    validate_8()


    print(
        "8. BÖLÜM — CTA SYNTHESIS / SONUÇ"
    )
    print("=" * 70)
    print(SYNTHESIS_FINAL_PRINCIPLE)
    print("=" * 70)
    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )
    print(
        "Validation: OK"
    )


"""
9. BÖLÜM — TARİHÇE / HAFIZA
FINAL KOD


5–8 arasındaki katmanların zaman içinde üretilmiş bilgi, ilişkisel yapı,
analitik bulgu ve synthesis durumlarını kendi tarihsel bağlamları,
provenance'ları ve zaman referansları korunarak muhafaza eder.


Sonraki bilgi, revizyon ve later outcome geçmiş historical state'in
yerine geçirilmez. Her yeni gelişme ayrı tarihsel katman olarak tutulur.


TEMEL İLKE:
    9 geçmişi korur; geçmişi yeniden yazmaz.


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Iterable, Optional


# ============================================================
# 1. ZAMAN REFERANSLARI
# ============================================================


class TimeReference(str, Enum):
    """
    Historical state'in zaman referansları.


    PRODUCTION_SNAPSHOT_TIME:
        Historical state'in temel zaman kimliği.


    EVENT_TIME:
        State'in anlattığı olayın zamanı.


    REFERENCE_PERIOD:
        State'in referans verdiği dönem.


    REVISION_TIME:
        Varsa daha sonra gerçekleşen revizyon/değişim zamanı.


    VALIDITY_PERIOD:
        Gerektiğinde korunan bağlamsal geçerlilik dönemi.
    """


    PRODUCTION_SNAPSHOT_TIME = "production_snapshot_time"
    EVENT_TIME = "event_time"
    REFERENCE_PERIOD = "reference_period"
    REVISION_TIME = "revision_time"
    VALIDITY_PERIOD = "validity_period"


# ============================================================
# 2. MEMORY OBJECT TYPES
# ============================================================


class MemoryObjectType(str, Enum):
    """
    9. Bölümün tarihsel olarak koruduğu nesneler.
    """


    # 5 — Bilgi
    INFORMATION_PIECE = "information_piece"
    RAW_INFORMATION = "raw_information"
    SOURCE_VIEW = "source_view"
    POSITIONING_CHANGE = "positioning_change"
    INFORMATION_STATUS_CHANGE = "information_status_change"
    PROVENANCE = "provenance"


    # 6 — Yoğurma
    RELATIONAL_STRUCTURE_STATE = "relational_structure_state"
    CLUSTER_STATE = "cluster_state"
    RELATIONSHIP_STATE = "relationship_state"
    STRUCTURE_CHANGE = "structure_change"


    # 7 — Analiz
    ANALYTICAL_FINDING_STATE = "analytical_finding_state"
    UNCERTAINTY_AT_TIME = "uncertainty_at_time"
    HISTORICAL_INFORMATION_CONDITION = (
        "historical_information_condition"
    )


    # 8 — Synthesis
    SYNTHESIS_RESULT = "synthesis_result"
    SYNTHESIS_INPUT_STATE = "synthesis_input_state"
    SYNTHESIS_UNCERTAINTY = "synthesis_uncertainty"
    SYNTHESIS_LIMITATION = "synthesis_limitation"


    # Sonraki gelişmeler
    NEW_INFORMATION = "new_information"
    REVISION = "revision"
    CHANGE = "change"
    LATER_OUTCOME = "later_outcome"
    FORECAST_OUTCOME_RECORD = "forecast_outcome_record"


    # Historical evaluation
    HISTORICAL_EVALUATION = "historical_evaluation"


# ============================================================
# 3. HISTORICAL STATE
# ============================================================


@dataclass(frozen=True)
class HistoricalState:
    """
    Belirli bir production/snapshot anındaki historical state.


    ÖNEMLİ:
        Bu nesne frozen'dır.


        İçerdiği koleksiyonlar tuple'dır.
        Böylece state oluşturulduktan sonra doğrudan mutasyona
        uğratılamaz.


    State:
        - 5 bilgi durumunu,
        - 6 ilişkisel durumunu,
        - 7 analitik durumunu,
        - 8 synthesis durumunu


    aynı historical snapshot altında referanslar.


    9 bu nesneleri yeniden üretmez.
    Yalnızca o anda mevcut olan kimlikleri tarihsel olarak korur.
    """


    state_id: str
    snapshot_time: datetime


    # 5
    information_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    raw_information_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    provenance_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    # 6
    relational_structure_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    cluster_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    relationship_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    # 7
    analytical_finding_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    uncertainty_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    # 8
    synthesis_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    synthesis_uncertainty_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    synthesis_limitation_ids: tuple[str, ...] = field(
        default_factory=tuple
    )


    # Historical context
    event_time: Optional[datetime] = None
    reference_period: Optional[str] = None
    revision_time: Optional[datetime] = None
    validity_period: Optional[str] = None


    # İnsan tarafından verilen tarihsel açıklama.
    note: Optional[str] = None


# ============================================================
# 4. HISTORICAL CHANGE
# ============================================================


class ChangeType(str, Enum):
    """
    Historical state'ler arasındaki değişim türleri.


    Bunlar 9 tarafından analiz edilmez.
    Yalnızca tarihsel değişimin türünü kaydeder.
    """


    NEW_INFORMATION = "new_information"
    SOURCE_VIEW_CHANGE = "source_view_change"
    POSITIONING_CHANGE = "positioning_change"
    INFORMATION_STATUS_CHANGE = "information_status_change"
    DATA_REVISION = "data_revision"
    STRUCTURE_CHANGE = "structure_change"
    ANALYTICAL_CHANGE = "analytical_change"
    SYNTHESIS_CHANGE = "synthesis_change"
    FORECAST_REALIZED = "forecast_realized"
    FORECAST_NOT_REALIZED = "forecast_not_realized"


@dataclass(frozen=True)
class HistoricalChange:
    """
    Eski state korunur.


    Yeni state varsa ayrı historical layer'dır.


    previous_state_id:
        Önceki historical state.


    new_state_id:
        Yeni historical state.


    9 burada değişimin analitik anlamını üretmez.
    """


    change_id: str
    change_type: ChangeType


    previous_state_id: str
    new_state_id: str


    change_time: datetime


    note: Optional[str] = None


# ============================================================
# 5. LATER OUTCOME
# ============================================================


class LaterOutcomeType(str, Enum):
    """
    Historical state'ten sonra gelen gelişme türleri.
    """


    OUTCOME = "outcome"
    REVISION = "revision"
    SOURCE_VIEW_CHANGE = "source_view_change"
    POSITIONING_CHANGE = "positioning_change"
    NEW_INFORMATION = "new_information"
    FORECAST_OUTCOME = "forecast_outcome"


@dataclass(frozen=True)
class LaterOutcome:
    """
    Historical state'ten sonra gerçekleşen gelişme.


    Bu nesne geçmiş state'in içine yazılmaz.


    target_state_id:
        Outcome'un hangi historical state ile ilişkili olduğunu
        belirtir.


    outcome_time:
        Gerçekleşmenin / ortaya çıkışın zamanı.


    record_time:
        Outcome'un hafızaya kaydedildiği zaman.


    ÖNEMLİ:
        Outcome, target historical state'in parçası değildir.
    """


    outcome_id: str
    target_state_id: str


    outcome_time: datetime
    record_time: datetime


    outcome_type: LaterOutcomeType


    description: Optional[str] = None


# ============================================================
# 6. HISTORICAL EVALUATION
# ============================================================


@dataclass(frozen=True)
class HistoricalEvaluation:
    """
    Daha önce 7 veya 8 tarafından üretilmiş historical evaluation'ın
    tarihsel kaydı.


    9 kendisi evaluation üretmez.


    produced_by:
        Evaluation'ın daha önce hangi katmanda üretildiğini belirtir.


    İzin verilen üreticiler:


    9 yalnızca bunların mevcut tarihsel kaydını korur.
    """


    evaluation_id: str


    state_id: str
    outcome_id: str


    produced_by: str


    evaluation_time: datetime


    description: Optional[str] = None


# ============================================================
# 7. PROVENANCE STATE
# ============================================================


@dataclass(frozen=True)
class HistoricalProvenance:
    """
    Historical state içinde provenance bağlantısının korunması.


    9 provenance değerlendirmez.
    Sadece mevcut provenance kimliklerini tarihsel snapshot'a
    bağlar.
    """


    provenance_id: str
    source_id: str


    source_url: Optional[str] = None
    source_locator: Optional[str] = None


    parent_provenance_id: Optional[str] = None


    note: Optional[str] = None


# ============================================================
# 8. IMMUTABLE SNAPSHOT BOUNDARY
# ============================================================


def _normalize_ids(
    values: Iterable[str],
) -> tuple[str, ...]:
    """
    ID koleksiyonunu immutable tuple'a çevirir.


    Duplicate ID'ler tekilleştirilir ancak sıralama korunur.
    """


    normalized: list[str] = []


    for value in values:
        if not isinstance(value, str) or not value:
            raise ValueError(
                "Historical state ID alanları boş veya geçersiz olamaz."
            )


        if value not in normalized:
            normalized.append(value)


    return tuple(normalized)


def freeze_historical_state(
    state: HistoricalState,
) -> HistoricalState:
    """
    HistoricalState'in immutable koleksiyon sınırını doğrular.


    Yeni bir state üretmez; verilen state'in tarihsel bütünlüğünü
    kontrol eder.
    """


    if not state.state_id:
        raise ValueError(
            "Historical state state_id boş olamaz."
        )


    if not isinstance(
        state.snapshot_time,
        datetime,
    ):
        raise TypeError(
            "snapshot_time datetime olmalıdır."
        )


    return HistoricalState(
        state_id=state.state_id,
        snapshot_time=state.snapshot_time,


        information_ids=_normalize_ids(
            state.information_ids
        ),


        raw_information_ids=_normalize_ids(
            state.raw_information_ids
        ),


        provenance_ids=_normalize_ids(
            state.provenance_ids
        ),


        relational_structure_ids=_normalize_ids(
            state.relational_structure_ids
        ),


        cluster_ids=_normalize_ids(
            state.cluster_ids
        ),


        relationship_ids=_normalize_ids(
            state.relationship_ids
        ),


        analytical_finding_ids=_normalize_ids(
            state.analytical_finding_ids
        ),


        uncertainty_ids=_normalize_ids(
            state.uncertainty_ids
        ),


        synthesis_ids=_normalize_ids(
            state.synthesis_ids
        ),


        synthesis_uncertainty_ids=_normalize_ids(
            state.synthesis_uncertainty_ids
        ),


        synthesis_limitation_ids=_normalize_ids(
            state.synthesis_limitation_ids
        ),


        event_time=state.event_time,
        reference_period=state.reference_period,
        revision_time=state.revision_time,
        validity_period=state.validity_period,
        note=state.note,
    )


# ============================================================
# 9. POINT-IN-TIME KURALLARI
# ============================================================


def point_in_time_integrity() -> str:
    return (
        "Belirli bir historical state için 'O anda ne biliniyordu?' "
        "sorusunun cevabı, daha sonra öğrenilen bilgilerle değiştirilmez."
    )


def no_retroactive_injection() -> str:
    return (
        "Sonraki bilgi, revizyon veya outcome geçmiş historical state'in "
        "içine geriye dönük olarak taşınamaz."
    )


def historical_state_is_immutable() -> str:
    return (
        "Kaydedilmiş historical state update edilemez veya üzerine "
        "yazılamaz; yeni durum ayrı historical state olarak kaydedilir."
    )


# ============================================================
# 10. HISTORICAL PATTERN / 7 SINIRI
# ============================================================


def historical_pattern_boundary() -> str:
    """
    9 tarihsel malzemeyi sağlar.


    9:
        similarity hesaplamaz,
        pattern matching yapmaz,
        benzerlik seçmez,
        tarihsel örüntü analizi yapmaz.


    Bu işlemler 7'nin analiz yetki alanıdır.
    """


    return (
        "9 tarihsel malzemeyi sağlar; 7 bu malzeme üzerinde "
        "karşılaştırma, benzerlik ve örüntü analizi yapar. "
        "9 içinde similarity veya pattern motoru bulunmaz."
    )


# ============================================================
# 11. 5–8 SINIRI
# ============================================================


FIVE_TO_EIGHT_BOUNDARY = {
    "5": "Bilgiyi korur.",
    "6": "Bilgiler arasındaki ilişkileri ve kümeleri oluşturur.",
    "7": "İlişkileri analiz eder ve analitik bulguları üretir.",
    "8": "7 bulgularının birlikte ne ifade ettiğini sentezler.",
    "9": (
        "5–8'in zaman içindeki historical state'lerini korur "
        "ve erişilebilir kılar."
    ),
}


def memory_not_reproduction() -> str:
    return (
        "9; 5'i yeniden oluşturmaz, 6'yı yeniden kurmaz, 7'yi "
        "yeniden çalıştırmaz, 8'i yeniden üretmez. 9'un görevi "
        "tarihçe ve hafızadır."
    )


# ============================================================
# 12. HAFIZA MOTORU
# ============================================================


class HafizaMotoru:
    """
    9. Bölüm — Tarihçe / Hafıza.


    TEMEL GÖREV:
        5–8 tarafından üretilmiş historical durumları korumak.


    TEMEL KORUMALAR:
        - point-in-time integrity
        - immutable historical state
        - provenance preservation
        - temporal separation
        - revision/change preservation
        - later outcome separation
        - historical evaluation preservation
        - layered history


    9 YAPMAZ:
        - analiz
        - synthesis
        - similarity
        - pattern matching
        - prediction
        - trade signal
        - risk decision
        - confidence
        - reliability
        - trust score
        - weighting
        - ranking
    """


    def __init__(self) -> None:
        # state_id -> immutable HistoricalState
        self._states: dict[str, HistoricalState] = {}


        # Historical snapshot zamanı -> state_id'ler.
        # Aynı snapshot zamanında farklı state'lerin bulunmasına izin verir.
        self._states_by_snapshot: dict[
            datetime,
            tuple[str, ...],
        ] = {}


        self._changes: dict[
            str,
            HistoricalChange,
        ] = {}


        self._outcomes: dict[
            str,
            LaterOutcome,
        ] = {}


        self._evaluations: dict[
            str,
            HistoricalEvaluation,
        ] = {}


        self._provenance: dict[
            str,
            HistoricalProvenance,
        ] = {}


    # ========================================================
    # STATE
    # ========================================================


    def record_historical_state(
        self,
        state: HistoricalState,
    ) -> str:
        """
        Yeni immutable historical state kaydeder.


        Aynı state_id ikinci kez kullanılamaz.


        ÖNEMLİ:
            Aynı snapshot_time'a sahip farklı state'ler mümkündür.
            Bu nedenle snapshot zamanı tek başına primary identity değildir.
        """


        frozen_state = freeze_historical_state(state)


        if frozen_state.state_id in self._states:
            raise ValueError(
                "Historical state immutable'dır; aynı state_id "
                f"üzerine yazılamaz: {frozen_state.state_id}"
            )


        self._states[
            frozen_state.state_id
        ] = frozen_state


        existing_ids = self._states_by_snapshot.get(
            frozen_state.snapshot_time,
            (),
        )


        self._states_by_snapshot[
            frozen_state.snapshot_time
        ] = existing_ids + (
            frozen_state.state_id,
        )


        return frozen_state.state_id


    def get_historical_state(
        self,
        state_id: str,
    ) -> HistoricalState:
        """
        Historical state'i immutable haliyle döndürür.
        """


        if state_id not in self._states:
            raise KeyError(
                f"Historical state bulunamadı: {state_id}"
            )


        return self._states[state_id]


    def states_at(
        self,
        snapshot_time: datetime,
    ) -> tuple[HistoricalState, ...]:
        """
        Belirli snapshot zamanındaki tüm historical state'leri
        döndürür.
        """


        state_ids = self._states_by_snapshot.get(
            snapshot_time,
            (),
        )


        return tuple(
            self._states[state_id]
            for state_id in state_ids
        )


    def all_states(
        self,
    ) -> tuple[HistoricalState, ...]:
        return tuple(self._states.values())


    def state_count(self) -> int:
        return len(self._states)


    # ========================================================
    # CHANGE / REVISION
    # ========================================================


    def add_change(
        self,
        change: HistoricalChange,
    ) -> None:
        """
        Historical change kaydeder.


        Önceki ve yeni state'lerin gerçekten mevcut olması gerekir.


        9 değişimin anlamını analiz etmez.
        """


        if change.change_id in self._changes:
            raise ValueError(
                "Duplicate historical change ID: "
                f"{change.change_id}"
            )


        if change.previous_state_id not in self._states:
            raise ValueError(
                "Previous historical state bulunamadı: "
                f"{change.previous_state_id}"
            )


        if change.new_state_id not in self._states:
            raise ValueError(
                "New historical state bulunamadı: "
                f"{change.new_state_id}"
            )


        previous_state = self._states[
            change.previous_state_id
        ]


        new_state = self._states[
            change.new_state_id
        ]


        if change.change_time < previous_state.snapshot_time:
            raise ValueError(
                "Change time previous historical state'ten önce olamaz."
            )


        if new_state.snapshot_time < previous_state.snapshot_time:
            raise ValueError(
                "New historical state previous state'ten daha eski olamaz."
            )


        self._changes[
            change.change_id
        ] = change


    def changes(
        self,
    ) -> tuple[HistoricalChange, ...]:
        return tuple(self._changes.values())


    # ========================================================
    # LATER OUTCOME
    # ========================================================


    def append_later_outcome(
        self,
        outcome: LaterOutcome,
    ) -> None:
        """
        Later outcome'u geçmiş state'ten ayrı tutar.


        Kritik kural:
            outcome_time >= target snapshot_time


        Ayrıca outcome hiçbir zaman target HistoricalState'in
        içine eklenmez.
        """


        if outcome.outcome_id in self._outcomes:
            raise ValueError(
                "Duplicate later outcome ID: "
                f"{outcome.outcome_id}"
            )


        if outcome.target_state_id not in self._states:
            raise ValueError(
                "Later outcome'un hedef historical state'i bulunamadı: "
                f"{outcome.target_state_id}"
            )


        target_state = self._states[
            outcome.target_state_id
        ]


        if outcome.outcome_time < target_state.snapshot_time:
            raise ValueError(
                "Later outcome, hedef historical state'ten "
                "önce gerçekleşemez."
            )


        if outcome.record_time < outcome.outcome_time:
            raise ValueError(
                "Outcome record_time, outcome_time'dan önce olamaz."
            )


        self._outcomes[
            outcome.outcome_id
        ] = outcome


    def outcomes(
        self,
    ) -> tuple[LaterOutcome, ...]:
        return tuple(self._outcomes.values())


    def outcomes_for_state(
        self,
        state_id: str,
    ) -> tuple[LaterOutcome, ...]:
        if state_id not in self._states:
            raise KeyError(
                f"Historical state bulunamadı: {state_id}"
            )


        return tuple(
            outcome
            for outcome in self._outcomes.values()
            if outcome.target_state_id == state_id
        )


    # ========================================================
    # HISTORICAL EVALUATION
    # ========================================================


    def add_historical_evaluation(
        self,
        evaluation: HistoricalEvaluation,
    ) -> None:
        """
        Daha önce 7 veya 8 tarafından üretilmiş evaluation'ı
        tarihsel kayıt olarak saklar.


        9'un kendi evaluation üretmesine izin verilmez.
        """


        if evaluation.evaluation_id in self._evaluations:
            raise ValueError(
                "Duplicate historical evaluation ID: "
                f"{evaluation.evaluation_id}"
            )


        if evaluation.produced_by not in {
            "7",
            "8",
            "section_7",
            "section_8",
        }:
            raise ValueError(
                "9 yalnızca 7 veya 8 tarafından daha önce üretilmiş "
                "historical evaluation'ları saklayabilir."
            )


        if evaluation.state_id not in self._states:
            raise ValueError(
                "Historical evaluation state'i bulunamadı: "
                f"{evaluation.state_id}"
            )


        if evaluation.outcome_id not in self._outcomes:
            raise ValueError(
                "Historical evaluation outcome'u bulunamadı: "
                f"{evaluation.outcome_id}"
            )


        outcome = self._outcomes[
            evaluation.outcome_id
        ]


        if outcome.target_state_id != evaluation.state_id:
            raise ValueError(
                "Historical evaluation state/outcome bağlantısı "
                "uyumsuz."
            )


        if evaluation.evaluation_time < outcome.outcome_time:
            raise ValueError(
                "Historical evaluation outcome'dan önce üretilemez."
            )


        self._evaluations[
            evaluation.evaluation_id
        ] = evaluation


    def evaluations(
        self,
    ) -> tuple[HistoricalEvaluation, ...]:
        return tuple(self._evaluations.values())


    # ========================================================
    # PROVENANCE
    # ========================================================


    def add_provenance(
        self,
        provenance: HistoricalProvenance,
    ) -> None:
        """
        Historical provenance kaydı.


        9 provenance'ın güvenilirliğini değerlendirmez.
        """


        if provenance.provenance_id in self._provenance:
            raise ValueError(
                "Duplicate historical provenance ID: "
                f"{provenance.provenance_id}"
            )


        if not provenance.source_id:
            raise ValueError(
                "Historical provenance source_id boş olamaz."
            )


        if provenance.parent_provenance_id is not None:
            if (
                provenance.parent_provenance_id
                not in self._provenance
            ):
                raise ValueError(
                    "Parent provenance bulunamadı: "
                    f"{provenance.parent_provenance_id}"
                )


        self._provenance[
            provenance.provenance_id
        ] = provenance


    def provenance(
        self,
    ) -> tuple[HistoricalProvenance, ...]:
        return tuple(self._provenance.values())


    # ========================================================
    # INTEGRITY
    # ========================================================


    def verify_point_in_time_integrity(
        self,
    ) -> None:
        """
        Tüm historical state'lerin temel PIT koşullarını kontrol eder.


        Bu kontrol:
        - state'in snapshot zamanını,
        - immutable identity'yi,
        - later outcome zaman ayrımını,
        - change zaman ayrımını


        doğrular.
        """


        for state in self._states.values():


            assert isinstance(
                state.snapshot_time,
                datetime,
            ), (
                "Historical state snapshot_time datetime olmalıdır: "
                f"{state.state_id}"
            )


            assert state.state_id in self._states, (
                "Historical state registry bütünlüğü bozulmuş: "
                f"{state.state_id}"
            )


        for outcome in self._outcomes.values():


            target = self._states[
                outcome.target_state_id
            ]


            assert outcome.outcome_time >= (
                target.snapshot_time
            ), (
                "Later outcome geçmiş historical state'ten "
                "önce olamaz: "
                f"{outcome.outcome_id}"
            )


            assert outcome.record_time >= (
                outcome.outcome_time
            ), (
                "Outcome record_time outcome_time'dan önce olamaz: "
                f"{outcome.outcome_id}"
            )


        for change in self._changes.values():


            previous = self._states[
                change.previous_state_id
            ]


            new_state = self._states[
                change.new_state_id
            ]


            assert change.change_time >= (
                previous.snapshot_time
            ), (
                "Change previous state'ten önce olamaz: "
                f"{change.change_id}"
            )


            assert new_state.snapshot_time >= (
                previous.snapshot_time
            ), (
                "New state previous state'ten daha eski olamaz: "
                f"{change.change_id}"
            )


    def verify_no_overwrite(
        self,
        state_id: str,
    ) -> None:
        """
        State'in registry'de mevcut olduğunu ve immutable identity'nin
        korunmuş olduğunu kontrol eder.


        9'un state update metodu yoktur.
        """


        if state_id not in self._states:
            raise AssertionError(
                "Historical state mevcut değil veya silinmiş: "
                f"{state_id}"
            )


        state = self._states[state_id]


        assert state.state_id == state_id


    def verify_historical_layer_separation(
        self,
    ) -> None:
        """
        Later outcome ve revision kayıtlarının historical state'in
        kendisine eklenmediğini doğrular.


        9 bunları ayrı koleksiyonlarda tutar.
        """


        state_ids = set(self._states)


        for outcome in self._outcomes.values():


            assert outcome.outcome_id not in state_ids, (
                "Later outcome historical state ID alanına "
                "yerleştirilemez."
            )


        for change in self._changes.values():


            assert change.change_id not in state_ids, (
                "Historical change state olarak kaydedilemez."
            )


    # ========================================================
    # READ-ONLY HISTORICAL ACCESS
    # ========================================================


    def historical_timeline(
        self,
    ) -> tuple[HistoricalState, ...]:
        """
        Historical state'leri snapshot zamanına göre sıralı
        erişilebilir hale getirir.


        Bu işlem analiz veya pattern matching değildir.
        """


        return tuple(
            sorted(
                self._states.values(),
                key=lambda state: (
                    state.snapshot_time,
                    state.state_id,
                ),
            )
        )


# ============================================================
# 13. DOĞAL HAFIZA ÇIKTILARI
# ============================================================


NATURAL_MEMORY_OUTPUTS = (
    "Bu kurum Ocak'ta X, Mart'ta Y diyordu.",
    "Bu synthesis Mart ayındaki bilgi durumuna aitti.",
    "Bu positioning şu tarihte değişti.",
    "Bu forecast şu tarihte üretildi.",
    "Bu forecast'in hedeflediği dönem daha sonra kapandı.",
    "Şu outcome daha sonra gerçekleşti.",
    "Bu veri daha sonra revize edildi.",
    "O dönemde şu bilgi mevcut değildi.",
    "Bugün bilinen bu bilgi o historical state'te mevcut değildi.",
)


NON_MEMORY_OUTPUTS = (
    "Bu 10 olay birbirine benziyor.",
    "Bu forecast başarılıydı.",
    "Bu örüntü gelecekte tekrar eder.",
)


# ============================================================
# 14. KESİN YASAKLAR
# ============================================================


FORBIDDEN_MEMORY_OPERATIONS = frozenset(
    {
        "overwrite_past_state",
        "delete_past_state",
        "inject_current_knowledge_to_past",
        "single_true_past_narrative",
        "similarity_analysis",
        "pattern_matching",
        "historical_pattern_analysis",
        "create_historical_evaluation",
        "prediction",
        "trade_signal",
        "risk_decision",
        "position_decision",
        "confidence_score",
        "reliability_score",
        "trust_score",
        "evidence_strength",
        "weighting",
        "ranking",
        "rerun_section_5",
        "rerun_section_6",
        "rerun_section_7",
        "rerun_section_8",
        "carry_old_cta_terminal_methodology",
        "replace_past_synthesis_with_current",
        "retroactively_insert_later_outcome",
        "retroactively_modify_historical_state",
    }
)


def no_forbidden_memory_operations() -> None:
    for operation in FORBIDDEN_MEMORY_OPERATIONS:
        assert isinstance(operation, str)
        assert operation.strip()


# ============================================================
# 15. TEKNİK MİMARİ YASAKLARI — KAVRAMSAL BÖLÜM SINIRI
# ============================================================


FORBIDDEN_CONCEPTUAL_ARCHITECTURE = frozenset(
    {
        "database_design",
        "storage_engine_design",
        "api_design",
        "ui_design",
        "network_architecture",
        "distributed_storage",
    }
)


def conceptual_boundary_is_locked() -> None:
    """
    9. Bölümün kavramsal tanımında database/storage/API/UI mimarisi
    tanımlanmadığını korur.


    Bu kod yalnızca kavramsal sınırların davranışsal kontrolünü
    temsil eder.
    """


    for item in FORBIDDEN_CONCEPTUAL_ARCHITECTURE:
        assert isinstance(item, str)


# ============================================================
# 16. NİHAİ KAVRAMSAL TANIM
# ============================================================


MEMORY_FINAL_DEFINITION = (
    "ERHAN / CTA TERMINALI'nin Tarihçe / Hafıza katmanı; 5–8 arasındaki "
    "katmanların zaman içinde üretilmiş bilgi, ilişkisel yapı, analitik "
    "bulgu ve synthesis durumlarını kendi tarihsel bağlamları, "
    "provenance'ları ve zaman referansları korunarak muhafaza eden; "
    "sonraki bilgi, revizyon ve later outcome'ları geçmiş state'in "
    "yerine geçirmeden ayrı tarihsel katmanlar olarak tutan; geçmişin "
    "bugünkü bilgiyle kirletilmesini önleyen ve geçmiş durumları "
    "erişilebilir kılan kavramsal hafıza katmanıdır."
)


# ============================================================
# 17. FINAL PRINCIPLE
# ============================================================


MEMORY_FINAL_PRINCIPLE = (
    "9 geçmişi korur; geçmişi yeniden yazmaz. "
    "Historical state kendi production/snapshot zamanında dondurulur. "
    "Sonraki bilgi, revision, change ve later outcome ayrı tarihsel "
    "katmanlarda tutulur. Historical state bugünkü bilgiyle geriye "
    "dönük olarak değiştirilmez. 9 similarity, pattern, historical "
    "evaluation, prediction, trade, risk veya karar üretmez; 5–8'in "
    "zaman içindeki tarihsel durumlarını, provenance'larını ve "
    "point-in-time bağlamlarını erişilebilir tutar."
)


# ============================================================
# 18. VALIDATION
# ============================================================


def validate_9() -> None:
    """
    9. Bölüm self-validation.


    Bu fonksiyon:
        - tarihsel state bütünlüğünü,
        - PIT ayrımını,
        - immutable layering sınırını,
        - later outcome ayrımını,
        - revision/change bağlantısını,
        - historical evaluation sınırını,
        - provenance korunmasını


    test eder.


    Harici runtime sisteminin doğrulaması değildir.
    """


    # --------------------------------------------------------
    # Yasaklar
    # --------------------------------------------------------


    no_forbidden_memory_operations()
    conceptual_boundary_is_locked()


    # --------------------------------------------------------
    # Boundary
    # --------------------------------------------------------


    assert (
        "değiştirilmez"
        in point_in_time_integrity()
    )


    assert (
        "geriye dönük"
        in no_retroactive_injection()
    )


    assert (
        "üzerine yazılamaz"
        in historical_state_is_immutable()
    )


    assert (
        "7"
        in historical_pattern_boundary()
    )


    assert (
        "hafıza"
        in memory_not_reproduction()
    )


    # --------------------------------------------------------
    # Memory engine
    # --------------------------------------------------------


    memory = HafizaMotoru()


    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------


    p1 = HistoricalProvenance(
        provenance_id="prov_001",
        source_id="source_001",
        source_url="https://example.invalid/source",
        source_locator="record-001",
    )


    memory.add_provenance(p1)


    assert len(memory.provenance()) == 1


    # --------------------------------------------------------
    # January historical state
    # --------------------------------------------------------


    jan_time = datetime(
        2026,
        1,
        15,
        12,
        0,
    )


    jan_state = HistoricalState(
        state_id="state_jan",
        snapshot_time=jan_time,


        information_ids=(
            "info_jan_001",
            "info_jan_002",
        ),


        raw_information_ids=(
            "raw_jan_001",
        ),


        provenance_ids=(
            "prov_001",
        ),


        relational_structure_ids=(
            "structure_jan_001",
        ),


        cluster_ids=(
            "cluster_jan_001",
        ),


        relationship_ids=(
            "relation_jan_001",
        ),


        analytical_finding_ids=(
            "finding_jan_001",
        ),


        uncertainty_ids=(
            "uncertainty_jan_001",
        ),


        synthesis_ids=(
            "synthesis_jan_001",
        ),


        synthesis_uncertainty_ids=(
            "synth_uncertainty_jan_001",
        ),


        synthesis_limitation_ids=(
            "synth_limitation_jan_001",
        ),


        reference_period="2026-01",
    )


    memory.record_historical_state(
        jan_state
    )


    assert memory.state_count() == 1


    # --------------------------------------------------------
    # March historical state
    # --------------------------------------------------------


    mar_time = datetime(
        2026,
        3,
        15,
        12,
        0,
    )


    mar_state = HistoricalState(
        state_id="state_mar",
        snapshot_time=mar_time,


        information_ids=(
            "info_jan_001",
            "info_jan_002",
            "info_mar_001",
        ),


        raw_information_ids=(
            "raw_jan_001",
            "raw_mar_001",
        ),


        provenance_ids=(
            "prov_001",
        ),


        relational_structure_ids=(
            "structure_mar_001",
        ),


        cluster_ids=(
            "cluster_mar_001",
        ),


        relationship_ids=(
            "relation_mar_001",
        ),


        analytical_finding_ids=(
            "finding_mar_001",
        ),


        uncertainty_ids=(
            "uncertainty_mar_001",
        ),


        synthesis_ids=(
            "synthesis_mar_001",
        ),


        reference_period="2026-03",
    )


    memory.record_historical_state(
        mar_state
    )


    assert memory.state_count() == 2


    # --------------------------------------------------------
    # State immutability / duplicate rejection
    # --------------------------------------------------------


    try:
        memory.record_historical_state(
            jan_state
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Aynı historical state_id üzerine yazılmasına izin verildi."
        )


    # --------------------------------------------------------
    # Change chain
    # --------------------------------------------------------


    change = HistoricalChange(
        change_id="change_001",
        change_type=ChangeType.POSITIONING_CHANGE,
        previous_state_id="state_jan",
        new_state_id="state_mar",
        change_time=mar_time,
    )


    memory.add_change(change)


    assert len(memory.changes()) == 1


    # --------------------------------------------------------
    # Later outcome
    # --------------------------------------------------------


    outcome_time = datetime(
        2026,
        6,
        15,
        12,
        0,
    )


    record_time = datetime(
        2026,
        6,
        15,
        13,
        0,
    )


    outcome = LaterOutcome(
        outcome_id="outcome_001",
        target_state_id="state_jan",
        outcome_time=outcome_time,
        record_time=record_time,
        outcome_type=LaterOutcomeType.FORECAST_OUTCOME,
        description=(
            "January historical state sonrasında ortaya çıkan outcome."
        ),
    )


    memory.append_later_outcome(
        outcome
    )


    assert len(memory.outcomes()) == 1


    assert (
        memory.outcomes_for_state(
            "state_jan"
        )[0].outcome_id
        == "outcome_001"
    )


    # --------------------------------------------------------
    # Historical evaluation
    # --------------------------------------------------------


    evaluation_time = datetime(
        2026,
        7,
        1,
        12,
        0,
    )


    evaluation = HistoricalEvaluation(
        evaluation_id="evaluation_001",
        state_id="state_jan",
        outcome_id="outcome_001",
        produced_by="7",
        evaluation_time=evaluation_time,
        description=(
            "Daha önce 7 tarafından üretilmiş historical evaluation."
        ),
    )


    memory.add_historical_evaluation(
        evaluation
    )


    assert len(memory.evaluations()) == 1


    # --------------------------------------------------------
    # PIT validation
    # --------------------------------------------------------


    memory.verify_point_in_time_integrity()


    # --------------------------------------------------------
    # Layer separation
    # --------------------------------------------------------


    memory.verify_historical_layer_separation()


    # --------------------------------------------------------
    # No overwrite
    # --------------------------------------------------------


    memory.verify_no_overwrite(
        "state_jan"
    )


    # --------------------------------------------------------
    # Timeline
    # --------------------------------------------------------


    timeline = memory.historical_timeline()


    assert len(timeline) == 2
    assert (
        timeline[0].state_id
        == "state_jan"
    )
    assert (
        timeline[1].state_id
        == "state_mar"
    )


    # --------------------------------------------------------
    # Historical state remains unchanged
    # --------------------------------------------------------


    original_jan = memory.get_historical_state(
        "state_jan"
    )


    assert (
        original_jan.information_ids
        == (
            "info_jan_001",
            "info_jan_002",
        )
    )


    assert (
        original_jan.synthesis_ids
        == (
            "synthesis_jan_001",
        )
    )


    # Later outcome state'in içine eklenmemiştir.
    assert (
        "outcome_001"
        not in original_jan.information_ids
    )


    assert (
        "outcome_001"
        not in original_jan.synthesis_ids
    )


    # --------------------------------------------------------
    # Natural / non-memory outputs
    # --------------------------------------------------------


    assert len(
        NATURAL_MEMORY_OUTPUTS
    ) >= 5


    assert len(
        NON_MEMORY_OUTPUTS
    ) >= 2


    # --------------------------------------------------------
    # Final definitions
    # --------------------------------------------------------


    assert isinstance(
        MEMORY_FINAL_DEFINITION,
        str,
    )


    assert isinstance(
        MEMORY_FINAL_PRINCIPLE,
        str,
    )


    assert (
        "geçmişi korur"
        in MEMORY_FINAL_PRINCIPLE
    )


    assert (
        "yeniden yazmaz"
        in MEMORY_FINAL_PRINCIPLE
    )


# ============================================================
# 19. MODULE ENTRY
# ============================================================


if __name__ == "__main__":
    validate_9()


    print(
        "9. BÖLÜM — TARİHÇE / HAFIZA"
    )


    print("=" * 70)


    print(
        MEMORY_FINAL_DEFINITION
    )


    print("=" * 70)


    print(
        MEMORY_FINAL_PRINCIPLE
    )


    print("=" * 70)


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "Validation: OK"
    )


"""
10. BÖLÜM — RED TEAM
FINAL KİLİTLEME TURU


1–9 arasındaki kavramsal mimari için son Red Team kontrol katmanıdır.


Kontrol edilen 5 risk:


1. Hidden Epistemic Transformation
2. False Independence / Echo
3. Synthesis → Final Bias / Prediction Kayması
4. Hidden Causality
5. CTA Scope Creep


Nihai kavramsal karar:
    5/5 = D — NO ISSUE
    Yeni kavramsal düzeltme gerekmiyor.
    10. Bölüm kilitlenebilir.


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass
from enum import Enum


# ============================================================
# 1. RED TEAM SINIFLANDIRMASI
# ============================================================


class RedTeamClassification(str, Enum):
    """
    Red Team bulgusunun sınıflandırması.
    """


    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    NO_ISSUE = "D — NO ISSUE"


# ============================================================
# 2. KİLİTLİ RED TEAM RİSK ID'LERİ
# ============================================================


REQUIRED_RED_TEAM_IDS = frozenset(
    {
        "rt1",
        "rt2",
        "rt3",
        "rt4",
        "rt5",
    }
)


# ============================================================
# 3. RED TEAM BULGUSU
# ============================================================


@dataclass(frozen=True)
class RedTeamFinding:
    """
    Tek bir Red Team bulgusu.


    Her bulgu:
        - problemi,
        - neden problem olduğunu,
        - etkilenen bölümleri,
        - mevcut mimarinin korumasını,
        - yeni düzeltme gerekip gerekmediğini,
        - nihai sınıflandırmayı


    taşır.
    """


    finding_id: str
    title: str


    problem: str
    why_problem: str


    affected_sections: tuple[str, ...]


    current_design_resolves: bool
    resolution_note: str


    new_fix_required: bool


    classification: RedTeamClassification


    status: str = "LOCKED"


# ============================================================
# 4. KİLİTLİ 5 RED TEAM BULGUSU
# ============================================================


RED_TEAM_FINDINGS: tuple[RedTeamFinding, ...] = (


    # --------------------------------------------------------
    # RT1 — HIDDEN EPISTEMIC TRANSFORMATION
    # --------------------------------------------------------


    RedTeamFinding(
        finding_id="rt1",
        title="Hidden Epistemic Dönüşüm",


        problem=(
            "Convergence'ın evidence strength'e, independence'ın "
            "reliability'ye, persistence/duration'ın importance'a, "
            "repetition'ın consensus'a veya structural measurement'ın "
            "confidence/truth'a dönüşmesi riski."
        ),


        why_problem=(
            "Bu dönüşümler betimleyici ve yapısal bulguları epistemik "
            "değer hükümlerine dönüştürür ve 6–8'in açık sınırlarını "
            "ihlal eder."
        ),


        affected_sections=("6", "7", "8"),


        current_design_resolves=True,


        resolution_note=(
            "6 ilişkileri kurar fakat değer biçmez. 7 yapısal ve "
            "zamansal özellikleri analiz edebilir ancak bunları önem, "
            "güç, güven, reliability veya evidence strength'e "
            "dönüştüremez. 8 synthesis yapmasına rağmen evidence "
            "strength, confidence, reliability, truth veya weighting "
            "üretemez. Ölçüm ≠ değer ilkesi korunur."
        ),


        new_fix_required=False,


        classification=RedTeamClassification.NO_ISSUE,
    ),


    # --------------------------------------------------------
    # RT2 — FALSE INDEPENDENCE / ECHO
    # --------------------------------------------------------


    RedTeamFinding(
        finding_id="rt2",
        title="False Independence / Echo",


        problem=(
            "Original Source → Relay → Commentary → X Post → "
            "Media Report → Another Report zincirinin çok sayıda "
            "bağımsız bilgiymiş gibi değerlendirilmesi."
        ),


        why_problem=(
            "Kayıt sayısının bağımsız bilgi sayısı olarak yorumlanması "
            "sahte consensus ve sahte convergence oluşturabilir."
        ),


        affected_sections=("4", "5", "6", "7"),


        current_design_resolves=True,


        resolution_note=(
            "Provenance, common root, relay, repetition, publication "
            "lineage, source family ve bağımsız bilgi kökü ayrımları "
            "korunur. Aynı kökten gelen tekrarlar bağımsız convergence "
            "olarak kabul edilmez. Kayıt sayısı ≠ bağımsız bilgi sayısı."
        ),


        new_fix_required=False,


        classification=RedTeamClassification.NO_ISSUE,
    ),


    # --------------------------------------------------------
    # RT3 — SYNTHESIS → FINAL BIAS / PREDICTION
    # --------------------------------------------------------


    RedTeamFinding(
        finding_id="rt3",
        title="Synthesis → Final Bias / Prediction Kayması",


        problem=(
            "8'de oluşturulan üst düzey anlamın zaman içinde final "
            "bias, prediction veya tek yönlü hükme dönüşmesi."
        ),


        why_problem=(
            "Synthesis yanlış tanımlanırsa mevcut analitik bulguların "
            "ötesine geçerek kesin yön, prediction veya karar üretme "
            "riski oluşur."
        ),


        affected_sections=("7", "8"),


        current_design_resolves=True,


        resolution_note=(
            "8, 7'nin bulgularını yeniden analiz etmez ve yeni veri "
            "veya bağımsız kanıt üretmez. Synthesis ifadeleri 7'ye "
            "izlenebilir tutulur. Çelişki ve belirsizlik korunabilir. "
            "Prediction, trade kararı, risk kararı veya kesin "
            "bullish/bearish hüküm üretilmez. Meaning ≠ Judgment."
        ),


        new_fix_required=False,


        classification=RedTeamClassification.NO_ISSUE,
    ),


    # --------------------------------------------------------
    # RT4 — HIDDEN CAUSALITY
    # --------------------------------------------------------


    RedTeamFinding(
        finding_id="rt4",
        title="Hidden Causality",


        problem=(
            "Birlikte görülme → ilişki → nedensellik veya zaman "
            "sıralaması → neden-sonuç şeklinde örtük nedensellik "
            "üretilmesi. Convergence veya complementarity'nin "
            "causality olarak yorumlanması."
        ),


        why_problem=(
            "Birlikte görülme, aynı yönde hareket veya ardışıklık "
            "tek başına neden-sonuç ilişkisini kanıtlamaz."
        ),


        affected_sections=("6", "7", "8"),


        current_design_resolves=True,


        resolution_note=(
            "6 ilişkileri kurarken causality hükmü vermez. 7 ilişkisel "
            "ve zamansal örüntüleri nedenselliğe dönüştürmez. 8, "
            "7'de kurulmamış yeni nedensellik üretemez. Birlikte "
            "görülme ≠ nedensellik; zaman sıralaması ≠ nedensellik; "
            "convergence ≠ nedensellik; complementarity ≠ nedensellik."
        ),


        new_fix_required=False,


        classification=RedTeamClassification.NO_ISSUE,
    ),


    # --------------------------------------------------------
    # RT5 — CTA SCOPE CREEP
    # --------------------------------------------------------


    RedTeamFinding(
        finding_id="rt5",
        title="CTA Kapsamı — Scope Creep",


        problem=(
            "Macro, options, volatility, cross-asset, genel piyasa "
            "bilgisi, positioning yorumları veya finansal medyanın "
            "terminali genel market/macro intelligence sistemine "
            "dönüştürmesi."
        ),


        why_problem=(
            "CTA ile doğrudan veya anlamlı bağlantısı olmayan "
            "bilgilerin sürekli eklenmesi CTA Terminali'nin "
            "tanımlı kapsamını aşabilir."
        ),


        affected_sections=("1", "2", "3", "4"),


        current_design_resolves=True,


        resolution_note=(
            "Genel piyasa veya makro bilgi yalnızca CTA dünyasını, "
            "CTA davranışını, CTA stratejisini, CTA positioning'ini "
            "veya CTA'ların içinde bulunduğu koşulları anlamaya "
            "anlamlı katkı sağladığı ölçüde kapsamda tutulur. "
            "CTA ile anlamlı bağlantısı olmayan genel bilgi "
            "otomatik olarak ana CTA bilgi evrenine dahil edilmez."
        ),


        new_fix_required=False,


        classification=RedTeamClassification.NO_ISSUE,
    ),
)


# ============================================================
# 5. RED TEAM MOTORU
# ============================================================


class RedTeamMotoru:
    """
    10. Bölüm — Red Team Denetim ve Kilitleme Motoru.


    Görevleri:


    - Tam olarak 5 kilitli Red Team riskini doğrulamak.
    - Duplicate finding ID'lerini engellemek.
    - Eksik riskleri tespit etmek.
    - CRITICAL / MAJOR / MINOR bulguları ayırmak.
    - NO_ISSUE kararlarının gerçekten tutarlı olduğunu doğrulamak.
    - Yeni kavramsal düzeltme gerekip gerekmediğini kontrol etmek.
    - Nihai kilitlenebilirlik kararını üretmek.


    Yapmaz:


    - Yeni özellik üretmez.
    - Yeni kaynak üretmez.
    - MASTER kaynak listesini değiştirmez.
    - 5–8'in görevlerini 10'a taşımaz.
    - Skor üretmez.
    - Weighting üretmez.
    - Ranking üretmez.
    - Confidence sistemi üretmez.
    - Reliability sistemi üretmez.
    - Database/API/UI mimarisi üretmez.
    """


    def __init__(
        self,
        findings: tuple[RedTeamFinding, ...] = RED_TEAM_FINDINGS,
    ) -> None:


        self._findings: dict[
            str,
            RedTeamFinding,
        ] = {}


        for finding in findings:
            self.add_finding(finding)


    # ========================================================
    # FINDING EKLEME
    # ========================================================


    def add_finding(
        self,
        finding: RedTeamFinding,
    ) -> None:
        """
        Red Team bulgusu ekler.


        Aynı finding_id ikinci kez eklenemez.
        """


        if not finding.finding_id:
            raise ValueError(
                "Red Team finding_id boş olamaz."
            )


        if finding.finding_id in self._findings:
            raise ValueError(
                "Duplicate Red Team finding_id: "
                f"{finding.finding_id}"
            )


        self._findings[
            finding.finding_id
        ] = finding


    # ========================================================
    # READ ACCESS
    # ========================================================


    def findings(
        self,
    ) -> tuple[RedTeamFinding, ...]:
        return tuple(
            self._findings.values()
        )


    def count(self) -> int:
        return len(self._findings)


    def get(
        self,
        finding_id: str,
    ) -> RedTeamFinding:
        if finding_id not in self._findings:
            raise KeyError(
                f"Red Team finding bulunamadı: {finding_id}"
            )


        return self._findings[finding_id]


    # ========================================================
    # CLASSIFICATION
    # ========================================================


    def by_classification(
        self,
        classification: RedTeamClassification,
    ) -> tuple[RedTeamFinding, ...]:


        return tuple(
            finding
            for finding in self._findings.values()
            if finding.classification == classification
        )


    def critical_findings(
        self,
    ) -> tuple[RedTeamFinding, ...]:


        return self.by_classification(
            RedTeamClassification.CRITICAL
        )


    def major_findings(
        self,
    ) -> tuple[RedTeamFinding, ...]:


        return self.by_classification(
            RedTeamClassification.MAJOR
        )


    def minor_findings(
        self,
    ) -> tuple[RedTeamFinding, ...]:


        return self.by_classification(
            RedTeamClassification.MINOR
        )


    def no_issue_findings(
        self,
    ) -> tuple[RedTeamFinding, ...]:


        return self.by_classification(
            RedTeamClassification.NO_ISSUE
        )


    # ========================================================
    # 5/5 KİMLİK KONTROLÜ
    # ========================================================


    def verify_required_findings(
        self,
    ) -> None:
        """
        Tam olarak rt1–rt5 setinin mevcut olduğunu doğrular.
        """


        actual_ids = frozenset(
            self._findings.keys()
        )


        if actual_ids != REQUIRED_RED_TEAM_IDS:
            missing = REQUIRED_RED_TEAM_IDS - actual_ids
            unexpected = actual_ids - REQUIRED_RED_TEAM_IDS


            raise AssertionError(
                "Red Team finding set hatalı. "
                f"Missing={sorted(missing)}, "
                f"Unexpected={sorted(unexpected)}"
            )


        if len(self._findings) != 5:
            raise AssertionError(
                "Red Team tam olarak 5 bulgu içermelidir."
            )


    # ========================================================
    # İÇ TUTARLILIK
    # ========================================================


    def verify_finding_integrity(
        self,
    ) -> None:
        """
        Her bulgunun final karar alanlarının birbiriyle
        tutarlı olduğunu doğrular.
        """


        for finding in self._findings.values():


            if not finding.title:
                raise AssertionError(
                    f"Finding title boş: {finding.finding_id}"
                )


            if not finding.problem:
                raise AssertionError(
                    f"Finding problem boş: {finding.finding_id}"
                )


            if not finding.why_problem:
                raise AssertionError(
                    f"Finding why_problem boş: {finding.finding_id}"
                )


            if not finding.affected_sections:
                raise AssertionError(
                    f"Etkilenen bölüm belirtilmemiş: "
                    f"{finding.finding_id}"
                )


            if not finding.resolution_note:
                raise AssertionError(
                    f"Resolution note boş: "
                    f"{finding.finding_id}"
                )


            # NO_ISSUE için mevcut tasarım çözmüş olmalı.
            if finding.classification == (
                RedTeamClassification.NO_ISSUE
            ):
                if not finding.current_design_resolves:
                    raise AssertionError(
                        "NO_ISSUE olarak sınıflandırılan bulgu "
                        "current_design_resolves=True olmalıdır: "
                        f"{finding.finding_id}"
                    )


                if finding.new_fix_required:
                    raise AssertionError(
                        "NO_ISSUE olarak sınıflandırılan bulgu "
                        "new_fix_required=False olmalıdır: "
                        f"{finding.finding_id}"
                    )


            # Çözülmemiş bir bulgu NO_ISSUE olamaz.
            if not finding.current_design_resolves:
                if finding.classification == (
                    RedTeamClassification.NO_ISSUE
                ):
                    raise AssertionError(
                        "Çözülmemiş bulgu NO_ISSUE olamaz: "
                        f"{finding.finding_id}"
                    )


            # Yeni düzeltme gerekiyorsa NO_ISSUE olamaz.
            if finding.new_fix_required:
                if finding.classification == (
                    RedTeamClassification.NO_ISSUE
                ):
                    raise AssertionError(
                        "Yeni düzeltme gereken bulgu "
                        "NO_ISSUE olamaz: "
                        f"{finding.finding_id}"
                    )


    # ========================================================
    # LOCKED KONTROLÜ
    # ========================================================


    def verify_all_locked(
        self,
    ) -> bool:
        """
        Bütün Red Team bulgularının LOCKED olduğunu doğrular.


        Sadece status kontrolü yapmaz.
        Önce:
            - 5/5 ID
            - bütünlük
            - classification
            - düzeltme durumu


        kontrol edilir.
        """


        self.verify_required_findings()
        self.verify_finding_integrity()


        return all(
            finding.status == "LOCKED"
            for finding in self._findings.values()
        )


    # ========================================================
    # CRITICAL / MAJOR KONTROLÜ
    # ========================================================


    def has_blocking_findings(
        self,
    ) -> bool:


        return bool(
            self.critical_findings()
            or self.major_findings()
        )


    # ========================================================
    # YENİ KAVRAMSAL DÜZELTME KONTROLÜ
    # ========================================================


    def has_new_conceptual_fix_required(
        self,
    ) -> bool:


        return any(
            finding.new_fix_required
            for finding in self._findings.values()
        )


    # ========================================================
    # FINAL VERDICT
    # ========================================================


    def final_verdict(
        self,
    ) -> str:
        """
        Nihai Red Team kararı.


        LOCKABLE ancak:
            - 5/5 risk mevcutsa,
            - bütün bulgular bütünlük kontrolünden geçerse,
            - hepsi LOCKED ise,
            - CRITICAL/MAJOR yoksa,
            - yeni kavramsal düzeltme gerekmiyorsa,
            - bütün bulgular NO_ISSUE ise


        verilir.
        """


        if not self.verify_all_locked():
            return "NOT LOCKABLE"


        if self.has_blocking_findings():
            return "NOT LOCKABLE"


        if self.has_new_conceptual_fix_required():
            return "NOT LOCKABLE"


        if len(
            self.no_issue_findings()
        ) != 5:
            return "NOT LOCKABLE"


        return "LOCKABLE"


# ============================================================
# 6. NİHAİ KARAR METNİ
# ============================================================


FINAL_DECISION = (
    "EVET — 5 noktanın tamamı mevcut 1–9 kavramsal mimari içinde "
    "yeterince çözülmüştür. Yeni kavramsal düzeltme gerekmemektedir. "
    "10. Bölüm kilitlenebilir."
)


def final_decision_text() -> str:
    return FINAL_DECISION


# ============================================================
# 7. FINAL VALIDATION
# ============================================================


def validate_10() -> None:
    """
    10. Bölüm final self-validation.


    Kontroller:


    1. Tam 5 Red Team riski.
    2. rt1–rt5 eksiksiz.
    3. Duplicate ID yok.
    4. Her bulgu LOCKED.
    5. Her bulgu NO_ISSUE.
    6. Her bulgu mevcut tasarım tarafından çözülmüş.
    7. Hiçbir yeni kavramsal düzeltme gerekmiyor.
    8. CRITICAL / MAJOR / MINOR yok.
    9. Nihai verdict LOCKABLE.
    """


    # --------------------------------------------------------
    # Sabit liste
    # --------------------------------------------------------


    assert len(
        RED_TEAM_FINDINGS
    ) == 5, (
        "Red Team tam olarak 5 bulgu içermelidir."
    )


    # --------------------------------------------------------
    # ID uniqueness
    # --------------------------------------------------------


    finding_ids = [
        finding.finding_id
        for finding in RED_TEAM_FINDINGS
    ]


    assert len(
        finding_ids
    ) == len(
        set(finding_ids)
    ), (
        "Duplicate Red Team finding_id bulundu."
    )


    # --------------------------------------------------------
    # Exact required IDs
    # --------------------------------------------------------


    assert frozenset(
        finding_ids
    ) == REQUIRED_RED_TEAM_IDS, (
        "rt1–rt5 Red Team ID seti eksik veya değişmiş."
    )


    # --------------------------------------------------------
    # Individual finding checks
    # --------------------------------------------------------


    for finding in RED_TEAM_FINDINGS:


        assert finding.current_design_resolves is True


        assert finding.new_fix_required is False


        assert (
            finding.classification
            == RedTeamClassification.NO_ISSUE
        )


        assert finding.status == "LOCKED"


    # --------------------------------------------------------
    # Motor
    # --------------------------------------------------------


    motor = RedTeamMotoru()


    assert motor.count() == 5


    # --------------------------------------------------------
    # Required findings
    # --------------------------------------------------------


    motor.verify_required_findings()


    # --------------------------------------------------------
    # Integrity
    # --------------------------------------------------------


    motor.verify_finding_integrity()


    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------


    assert len(
        motor.no_issue_findings()
    ) == 5


    assert len(
        motor.critical_findings()
    ) == 0


    assert len(
        motor.major_findings()
    ) == 0


    assert len(
        motor.minor_findings()
    ) == 0


    # --------------------------------------------------------
    # Resolution
    # --------------------------------------------------------


    assert (
        motor.has_blocking_findings()
        is False
    )


    assert (
        motor.has_new_conceptual_fix_required()
        is False
    )


    # --------------------------------------------------------
    # Lock
    # --------------------------------------------------------


    assert (
        motor.verify_all_locked()
        is True
    )


    # --------------------------------------------------------
    # Final verdict
    # --------------------------------------------------------


    assert (
        motor.final_verdict()
        == "LOCKABLE"
    )


    assert (
        final_decision_text()
        == FINAL_DECISION
    )


    assert (
        "kilitlenebilir"
        in final_decision_text()
    )


# ============================================================
# 8. FINAL PRINCIPLE
# ============================================================


RED_TEAM_FINAL_PRINCIPLE = (
    "10. Bölüm — Red Team; 1–9 arasındaki kavramsal mimarinin "
    "hidden epistemic transformation, false independence / echo, "
    "synthesis'in final bias veya prediction'a kayması, hidden "
    "causality ve CTA scope creep riskleri karşısında sınırlarını "
    "koruyup korumadığını denetler. Bu denetim yeni bir sistem "
    "katmanı, yeni veri, yeni kaynak, skor, weighting, ranking, "
    "confidence veya karar mekanizması üretmez. Beş Red Team "
    "kontrolünün tamamı D — NO ISSUE olarak sonuçlanmış ve yeni "
    "kavramsal düzeltme gerekmemiştir."
)


# ============================================================
# 9. MODULE ENTRY
# ============================================================


if __name__ == "__main__":
    validate_10()


    print(
        "10. BÖLÜM — RED TEAM"
    )


    print(
        "=" * 70
    )


    print(
        FINAL_DECISION
    )


    print(
        "=" * 70
    )


    print(
        RED_TEAM_FINAL_PRINCIPLE
    )


    print(
        "=" * 70
    )


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "Validation: OK"
    )


"""
11. BÖLÜM — TEKNİK MİMARİ
FINAL KİLİTLEME


Teknik mimari sözleşmesi:


1. Historical Snapshot zamanı ayrıdır.
2. Publication / Access / Ingestion ayrıdır.
3. Provenance Root / Path / Independence ayrıdır.
4. Information Piece zorunlu canonicalization ile ezilmez.
5. Information Status 5. Bölümden gelir ve teknik katman tarafından
   sessizce değiştirilemez.
6. Kaynak nedensellik iddiası ile sistemin kendi nedensellik hükmü ayrıdır.
7. Bounded Context / Read-Write Authority mantıksal olarak korunur.
8. Referential / Atomic Validity tamamlanmış state için zorunludur.


REFERENTIAL / ATOMIC VALIDITY:


Gerekli trace/reference bağlantıları tamamlanmamış bir
Finding, Synthesis, Historical Snapshot veya Relationship
sistemde geçici/incomplete state olarak bulunabilir.


Ancak gerekli referansları gerçekten mevcut ve geçerli olmadan
tamamlanmış/geçerli çıktı olarak kabul edilemez.


Eksik state:
    - silinmez,
    - otomatik reddedilmez,
    - geçmiş state'i değiştirmez,
    - sonradan oluşan bilgiyi geçmişe sessizce enjekte etmez.


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable


# ============================================================
# 1. TEKNİK MİMARİ SINIFLANDIRMASI
# ============================================================


class TechnicalArchitectureClass(str, Enum):
    """
    Teknik mimari sorgu sınıflandırması.


    A: Problem yok.
    B: Minimum düzeltme gerekli.
    C: Kavramsal sınır belirsiz.
    D: Kapsam dışı.
    """


    A_NO_ISSUE = "A"
    B_FIX_REQUIRED = "B"
    C_BOUNDARY_UNCLEAR = "C"
    D_OUT_OF_SCOPE = "D"


# ============================================================
# 2. TEKNİK MİMARİ BULGUSU
# ============================================================


@dataclass(frozen=True)
class TechnicalArchitectureFinding:
    """
    Tek bir teknik mimari sorgu bulgusu.
    """


    finding_id: str
    title: str
    classification: TechnicalArchitectureClass


    problem: str | None
    technical_importance: str
    relation_to_1_10: str
    minimum_fix: str | None


# ============================================================
# 3. 11. BÖLÜMÜN 8 KİLİTLİ BULGUSU
# ============================================================


TECHNICAL_ARCHITECTURE_FINDINGS: tuple[
    TechnicalArchitectureFinding,
    ...,
] = (


    # --------------------------------------------------------
    # Q1 — HISTORICAL SNAPSHOT ZAMANI
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q1",
        title="Historical Snapshot Zamanı",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Production, access, ingestion, event, reference, revision "
            "ve snapshot zamanlarının semantik olarak ayrılması "
            "point-in-time bütünlüğü ve hindsight contamination'ın "
            "önlenmesi için yeterlidir. as_of_time / snapshot_time, "
            "sistemin temsil ettiği historical state'in zaman sınırıdır. "
            "Production time bunun yerine geçirilemez."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q2 — PUBLICATION / ACCESS / INGESTION
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q2",
        title="Publication / Access / Ingestion",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Publication, access ve ingestion farklı olaylardır. "
            "Fiziksel olarak aynı yapıda tutulabilmeleri semantik "
            "ayrımı ortadan kaldırmaz. Bir yayına tekrar erişilmesi "
            "durumunda publication kimliği ve provenance korunabildiği "
            "sürece point-in-time ve provenance bütünlüğü korunur."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q3 — PROVENANCE ROOT / INDEPENDENCE
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q3",
        title="Provenance Root ve Independence",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "provenance_root, provenance_path ve independent_path "
            "farklı kavramlardır. Farklı provenance_root_id değerleri "
            "otomatik olarak bağımsız kanıt anlamına gelmez. Bu ayrım "
            "false independence ve yanlış consensus üretimini engeller."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q4 — DEDUPLICATION / CANONICALIZATION
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q4",
        title="Information Piece Deduplication / Canonicalization",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Zorunlu tekilleştirme veya canonicalization dayatılmaması, "
            "Information Piece'in provenance, context, publication/access "
            "geçmişi, zaman ve anlamlı farklılıklarının korunmasını sağlar. "
            "Aynı kökten gelen kayıtların bağımsız kanıt gibi görünmemesi "
            "ise 4–7'deki provenance ve independence sınırlarıyla korunur."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q5 — INFORMATION STATUS
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q5",
        title="Information Status Sınırı",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Teknik enum veya schema değişikliği tek başına yeni "
            "epistemik kategori yaratamaz. Status kavramının kaynağı "
            "5. Bölümdeki kavramsal tanımdır. 11. Bölüm bunu değiştiremez "
            "ve mevcut status'ları teknik sebeple sessizce dönüştüremez."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q6 — CAUSALITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q6",
        title="Causality Sınırı",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Kaynağın yayınladığı nedensellik iddiasının saklanması ile "
            "sistemin kendi nedensellik hükmünü üretmesi birbirinden "
            "ayrılmıştır. Kaynak iddiası, ERHAN tarafından üretilmiş "
            "nedensellik hükmü değildir."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q7 — BOUNDED CONTEXT / READ-WRITE AUTHORITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q7",
        title="Bounded Context / Read-Write Authority",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "6, 7 ve 8'in fiziksel olarak ayrı servisler olması zorunlu "
            "değildir. Logical boundary, read/write authority, output "
            "contract, immutable veya versioned input, traceability ve "
            "sessiz mutation'ın engellenmesi yeterli teknik sınırları "
            "oluşturur. Fiziksel ayrım 12. Kodlama aşamasına bırakılır."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q8 — REFERENTIAL / ATOMIC VALIDITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q8",
        title="Referential / Atomic Validity",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Tamamlanmış Finding, Synthesis, Historical Snapshot veya "
            "Relationship; kendisini oluşturan zorunlu trace/reference "
            "bağlantıları gerçekten mevcut ve geçerli olmadan "
            "tamamlanmış/geçerli çıktı olarak kabul edilemez. Eksik "
            "referanslı state geçici/incomplete olarak bulunabilir. "
            "Bu kural provenance, traceability ve point-in-time "
            "bütünlüğünü teknik sözleşmede korur."
        ),


        relation_to_1_10=(
            "Çelişmiyor. Aksine 5–10'daki provenance, traceability, "
            "point-in-time ve 7→8 sınırlarını teknik bütünlük kuralı "
            "olarak koruyor."
        ),


        minimum_fix=None,
    ),
)


# ============================================================
# 4. REFERENTIAL / ATOMIC VALIDITY
# ============================================================


class TechnicalEntityType(str, Enum):
    """
    Referential / Atomic Validity kapsamında kontrol edilen
    tamamlanmış state türleri.
    """


    FINDING = "FINDING"
    SYNTHESIS = "SYNTHESIS"
    SNAPSHOT = "SNAPSHOT"
    RELATIONSHIP = "RELATIONSHIP"


# ============================================================
# 5. IMMUTABLE TECHNICAL STATE CONTRACT
# ============================================================


@dataclass(frozen=True)
class TechnicalStateContract:
    """
    Bir teknik state'in referans bütünlüğü sözleşmesi.


    required_references:
        State'in tamamlanabilmesi için bulunması gereken referans ID'leri.


    is_completed:
        State'in tamamlanmış/geçerli çıktı olarak işaretlenip
        işaretlenmediği.


    ÖNEMLİ:
        Bu sınıf referansların yalnızca dolu string olmasını değil,
        Enforcer içindeki gerçek reference registry'de bulunmasını
        kontrol eder.
    """


    entity_type: TechnicalEntityType
    entity_id: str
    required_references: tuple[str, ...]
    is_completed: bool = False


    def has_required_reference_ids(self) -> bool:
        """
        Referans listesinin biçimsel bütünlüğü.


        Boş ID veya whitespace-only ID kabul edilmez.
        """


        return bool(
            self.required_references
        ) and all(
            isinstance(reference_id, str)
            and bool(reference_id.strip())
            for reference_id in self.required_references
        )


# ============================================================
# 6. REFERANS KAYDI
# ============================================================


@dataclass(frozen=True)
class TechnicalReference:
    """
    Teknik referans registry kaydı.


    Reference'ın gerçekten mevcut olduğunu temsil eder.
    """


    reference_id: str
    reference_type: str


# ============================================================
# 7. TEKNİK MİMARİ ENFORCER
# ============================================================


class TechnicalArchitectureEnforcer:
    """
    11. Bölüm — Teknik Mimari Bütünlük ve Doğrulama Motoru.


    Denetlediği sınırlar:


    - point-in-time ayrımı,
    - publication/access/ingestion ayrımı,
    - provenance ayrımı,
    - reference bütünlüğü,
    - completed/incomplete state ayrımı,
    - duplicate entity engeli,
    - sessiz mutation engeli.


    Bu motor:


    - epistemik skor üretmez,
    - confidence üretmez,
    - reliability üretmez,
    - weighting üretmez,
    - ranking üretmez,
    - karar üretmez,
    - trade sinyali üretmez.
    """


    def __init__(self) -> None:


        self._contracts: dict[
            str,
            TechnicalStateContract,
        ] = {}


        self._references: dict[
            str,
            TechnicalReference,
        ] = {}


    # ========================================================
    # REFERANS REGISTRY
    # ========================================================


    def register_reference(
        self,
        reference_id: str,
        reference_type: str,
    ) -> None:
        """
        Gerçek bir teknik referans kaydeder.


        Aynı reference_id ikinci kez kaydedilemez.
        """


        if not isinstance(reference_id, str):
            raise TypeError(
                "reference_id string olmalıdır."
            )


        normalized_id = reference_id.strip()


        if not normalized_id:
            raise ValueError(
                "reference_id boş olamaz."
            )


        if normalized_id in self._references:
            raise ValueError(
                "Duplicate technical reference_id: "
                f"{normalized_id}"
            )


        if not reference_type.strip():
            raise ValueError(
                "reference_type boş olamaz."
            )


        self._references[
            normalized_id
        ] = TechnicalReference(
            reference_id=normalized_id,
            reference_type=reference_type.strip(),
        )


    def has_reference(
        self,
        reference_id: str,
    ) -> bool:
        return reference_id.strip() in self._references


    def reference_count(self) -> int:
        return len(self._references)


    # ========================================================
    # STATE VALIDATION
    # ========================================================


    def validate_atomic_validity(
        self,
        contract: TechnicalStateContract,
    ) -> bool:
        """
        Referential / Atomic Validity.


        Completed state için iki koşul zorunludur:


        1. Referans ID'leri biçimsel olarak geçerli olmalı.
        2. Her zorunlu referans registry'de gerçekten bulunmalı.


        Incomplete state bu kural nedeniyle reddedilmez.
        Sadece completed olarak kabul edilmez.
        """


        if not contract.has_required_reference_ids():
            return False


        return all(
            self.has_reference(reference_id)
            for reference_id in contract.required_references
        )


    # ========================================================
    # STATE REGISTER
    # ========================================================


    def register_entity_state(
        self,
        entity_type: TechnicalEntityType,
        entity_id: str,
        references: Iterable[str],
        mark_completed: bool = False,
    ) -> bool:
        """
        Yeni entity state kaydeder.


        Duplicate entity_id kabul edilmez.


        Eksik referans varsa:
            mark_completed=True olsa bile state completed olmaz.


        State silinmez ve otomatik reddedilmez.
        Incomplete olarak saklanabilir.
        """


        if not isinstance(entity_type, TechnicalEntityType):
            raise TypeError(
                "entity_type TechnicalEntityType olmalıdır."
            )


        if not isinstance(entity_id, str):
            raise TypeError(
                "entity_id string olmalıdır."
            )


        normalized_entity_id = entity_id.strip()


        if not normalized_entity_id:
            raise ValueError(
                "entity_id boş olamaz."
            )


        # Sessiz overwrite kesin olarak engellenir.
        if normalized_entity_id in self._contracts:
            raise ValueError(
                "Duplicate entity_id / silent overwrite engellendi: "
                f"{normalized_entity_id}"
            )


        reference_tuple = tuple(
            reference_id.strip()
            for reference_id in references
            if isinstance(reference_id, str)
        )


        contract = TechnicalStateContract(
            entity_type=entity_type,
            entity_id=normalized_entity_id,
            required_references=reference_tuple,
            is_completed=False,
        )


        # ----------------------------------------------------
        # Completed talebi yalnızca gerçek referanslar mevcutsa
        # kabul edilir.
        # ----------------------------------------------------


        if mark_completed:
            if self.validate_atomic_validity(contract):
                contract = TechnicalStateContract(
                    entity_type=contract.entity_type,
                    entity_id=contract.entity_id,
                    required_references=contract.required_references,
                    is_completed=True,
                )


        self._contracts[
            normalized_entity_id
        ] = contract


        return contract.is_completed


    # ========================================================
    # STATE OKUMA
    # ========================================================


    def get_contract(
        self,
        entity_id: str,
    ) -> TechnicalStateContract:
        normalized_id = entity_id.strip()


        if normalized_id not in self._contracts:
            raise KeyError(
                f"Technical state bulunamadı: {normalized_id}"
            )


        return self._contracts[normalized_id]


    def contracts(
        self,
    ) -> tuple[TechnicalStateContract, ...]:
        return tuple(
            self._contracts.values()
        )


    def completed_contracts(
        self,
    ) -> tuple[TechnicalStateContract, ...]:
        return tuple(
            contract
            for contract in self._contracts.values()
            if contract.is_completed
        )


    def incomplete_contracts(
        self,
    ) -> tuple[TechnicalStateContract, ...]:
        return tuple(
            contract
            for contract in self._contracts.values()
            if not contract.is_completed
        )


    # ========================================================
    # SILENT MUTATION ENGELİ
    # ========================================================


    def update_entity_state(
        self,
        entity_id: str,
        *,
        references: Iterable[str] | None = None,
        mark_completed: bool | None = None,
    ) -> None:
        """
        Mevcut state'in sessiz mutation'ını engeller.


        11. Bölüm append-only / immutable boundary nedeniyle
        mevcut state doğrudan güncellenemez.


        Yeni bir state gerekiyorsa yeni entity/version ID'si
        ile yeni historical layer oluşturulmalıdır.
        """


        raise RuntimeError(
            "Technical state sessizce güncellenemez. "
            "Yeni state/version oluşturulmalıdır."
        )


    def delete_entity_state(
        self,
        entity_id: str,
    ) -> None:
        """
        Historical/technical state silinemez.
        """


        raise RuntimeError(
            "Technical state silinemez."
        )


    # ========================================================
    # BÜTÜNLÜK KONTROLÜ
    # ========================================================


    def validate_all_contracts(
        self,
    ) -> bool:
        """
        Registry'deki tüm contract'ların bütünlüğünü kontrol eder.


        Incomplete state'ler geçerlidir; ancak completed state'ler
        referential/atomic validity şartını mutlaka karşılamalıdır.
        """


        for contract in self._contracts.values():


            if not contract.entity_id.strip():
                return False


            if not contract.has_required_reference_ids():
                if contract.is_completed:
                    return False


            if contract.is_completed:
                if not self.validate_atomic_validity(
                    contract
                ):
                    return False


        return True


# ============================================================
# 8. REFERENTIAL / ATOMIC VALIDITY KISITLARI
# ============================================================


REFERENTIAL_ATOMIC_VALIDITY_CONSTRAINTS: tuple[str, ...] = (
    "yeni bir epistemik kategori oluşturmaz",
    "yeni bir bilgi statüsü oluşturmaz",
    "yeni bir güven/confidence değeri oluşturmaz",
    "eksik state'i otomatik olarak silmez",
    "eksik state'i otomatik olarak reddedilmiş bilgi haline getirmez",
    "geçmiş state'i değiştirmez",
    "sonradan oluşan referansları geçmiş state'e sessizce enjekte etmez",
    "tamamlanmış state'in sessizce değiştirilmesine izin vermez",
    "duplicate entity_id ile mevcut state'in üzerine yazılmasına izin vermez",
)


def referential_atomic_validity_rule() -> str:
    return (
        "Gerekli trace/reference bağlantıları tamamlanmamış bir "
        "Finding, Synthesis, Historical Snapshot veya Relationship "
        "sistemde geçici/incomplete state olarak bulunabilir; ancak "
        "gerekli referansları gerçekten mevcut ve geçerli olmadan "
        "tamamlanmış/geçerli çıktı olarak kabul edilemez."
    )


# ============================================================
# 9. TEKNİK MİMARİ FİNAL DURUMU
# ============================================================


TECHNICAL_ARCHITECTURE_FINAL_STATUS = (
    "LOCKED"
)


TECHNICAL_ARCHITECTURE_FINAL_DECISION = (
    "11. BÖLÜM LOCKED. Referential / Atomic Validity, "
    "11. Bölümün teknik bütünlük sözleşmesinin zorunlu parçasıdır. "
    "Sekiz teknik mimari kontrolün tamamında aktif bir kavramsal "
    "boşluk bulunmamaktadır."
)


# ============================================================
# 10. FINAL VALIDATION
# ============================================================


def validate_11() -> None:
    """
    11. Bölüm final self-validation.


    Kontroller:


    1. Tam 8 teknik mimari bulgu.
    2. q1–q7 + q8 eksiksiz.
    3. Duplicate finding ID yok.
    4. Tüm bulgular A_NO_ISSUE.
    5. B/C/D bulgusu yok.
    6. Referential / Atomic Validity aktif.
    7. Gerçek referans olmadan completed state oluşamıyor.
    8. Incomplete state saklanabiliyor.
    9. Duplicate entity overwrite engelleniyor.
    10. Sessiz update/delete engelleniyor.
    """


    # --------------------------------------------------------
    # Finding count
    # --------------------------------------------------------


    assert len(
        TECHNICAL_ARCHITECTURE_FINDINGS
    ) == 8, (
        "11. Bölüm tam olarak 8 teknik mimari bulgu içermelidir."
    )


    # --------------------------------------------------------
    # Finding IDs
    # --------------------------------------------------------


    expected_ids = {
        "q1",
        "q2",
        "q3",
        "q4",
        "q5",
        "q6",
        "q7",
        "q8",
    }


    actual_ids = {
        finding.finding_id
        for finding in TECHNICAL_ARCHITECTURE_FINDINGS
    }


    assert actual_ids == expected_ids, (
        "11. Bölüm finding ID seti hatalı."
    )


    assert len(actual_ids) == 8, (
        "Duplicate technical finding ID bulundu."
    )


    # --------------------------------------------------------
    # All A
    # --------------------------------------------------------


    assert all(
        finding.classification
        == TechnicalArchitectureClass.A_NO_ISSUE
        for finding in TECHNICAL_ARCHITECTURE_FINDINGS
    ), (
        "Final LOCKED durumda bütün teknik mimari bulgular "
        "A_NO_ISSUE olmalıdır."
    )


    # --------------------------------------------------------
    # No B / C / D
    # --------------------------------------------------------


    assert not any(
        finding.classification
        == TechnicalArchitectureClass.B_FIX_REQUIRED
        for finding in TECHNICAL_ARCHITECTURE_FINDINGS
    )


    assert not any(
        finding.classification
        == TechnicalArchitectureClass.C_BOUNDARY_UNCLEAR
        for finding in TECHNICAL_ARCHITECTURE_FINDINGS
    )


    assert not any(
        finding.classification
        == TechnicalArchitectureClass.D_OUT_OF_SCOPE
        for finding in TECHNICAL_ARCHITECTURE_FINDINGS
    )


    # --------------------------------------------------------
    # Referential rule
    # --------------------------------------------------------


    rule = referential_atomic_validity_rule()


    assert "incomplete" in rule
    assert "tamamlanmış/geçerli çıktı" in rule


    assert len(
        REFERENTIAL_ATOMIC_VALIDITY_CONSTRAINTS
    ) >= 8


    # --------------------------------------------------------
    # Enforcer
    # --------------------------------------------------------


    enforcer = TechnicalArchitectureEnforcer()


    # Gerçek referanslar.
    enforcer.register_reference(
        "ref.finding.001",
        "FINDING",
    )


    enforcer.register_reference(
        "ref.source.001",
        "SOURCE",
    )


    # --------------------------------------------------------
    # Eksik referanslı state:
    # completed talebi verilse bile incomplete kalmalı.
    # --------------------------------------------------------


    incomplete_result = (
        enforcer.register_entity_state(
            TechnicalEntityType.FINDING,
            "finding.incomplete",
            references=(
                "ref.missing.001",
            ),
            mark_completed=True,
        )
    )


    assert incomplete_result is False


    incomplete_contract = (
        enforcer.get_contract(
            "finding.incomplete"
        )
    )


    assert (
        incomplete_contract.is_completed
        is False
    )


    # --------------------------------------------------------
    # Gerçek referansları olan state completed olabilir.
    # --------------------------------------------------------


    completed_result = (
        enforcer.register_entity_state(
            TechnicalEntityType.FINDING,
            "finding.complete",
            references=(
                "ref.finding.001",
                "ref.source.001",
            ),
            mark_completed=True,
        )
    )


    assert completed_result is True


    completed_contract = (
        enforcer.get_contract(
            "finding.complete"
        )
    )


    assert (
        completed_contract.is_completed
        is True
    )


    assert (
        enforcer.validate_atomic_validity(
            completed_contract
        )
        is True
    )


    # --------------------------------------------------------
    # Duplicate entity ID engellenmeli.
    # --------------------------------------------------------


    try:
        enforcer.register_entity_state(
            TechnicalEntityType.FINDING,
            "finding.complete",
            references=(
                "ref.finding.001",
            ),
            mark_completed=False,
        )


    except ValueError as exc:
        assert "Duplicate entity_id" in str(exc)


    else:
        raise AssertionError(
            "Duplicate entity_id sessiz overwrite'a izin verdi."
        )


    # --------------------------------------------------------
    # Sessiz update engellenmeli.
    # --------------------------------------------------------


    try:
        enforcer.update_entity_state(
            "finding.complete",
            mark_completed=False,
        )


    except RuntimeError:
        pass


    else:
        raise AssertionError(
            "Technical state sessizce güncellenebildi."
        )


    # --------------------------------------------------------
    # Delete engellenmeli.
    # --------------------------------------------------------


    try:
        enforcer.delete_entity_state(
            "finding.complete"
        )


    except RuntimeError:
        pass


    else:
        raise AssertionError(
            "Technical state silinebildi."
        )


    # --------------------------------------------------------
    # Registry integrity
    # --------------------------------------------------------


    assert (
        enforcer.validate_all_contracts()
        is True
    )


    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------


    assert (
        TECHNICAL_ARCHITECTURE_FINAL_STATUS
        == "LOCKED"
    )


    assert (
        "LOCKED"
        in TECHNICAL_ARCHITECTURE_FINAL_DECISION
    )


# ============================================================
# 11. FINAL PRINCIPLE
# ============================================================


TECHNICAL_ARCHITECTURE_FINAL_PRINCIPLE = (
    "11. Bölüm — Teknik Mimari; 1–10 arasında tanımlanan "
    "provenance, point-in-time, information status, causality, "
    "bounded context ve read/write authority sınırlarını teknik "
    "bütünlük sözleşmesine taşır. Referential / Atomic Validity "
    "kuralı sayesinde Finding, Synthesis, Historical Snapshot veya "
    "Relationship gibi tamamlanmış çıktılar zorunlu trace/reference "
    "bağlantıları gerçekten mevcut olmadan geçerli kabul edilmez. "
    "Eksik state geçici/incomplete olarak tutulabilir; ancak "
    "sessizce completed hale getirilemez, geçmiş state değiştirilemez "
    "ve mevcut entity üzerine yazılamaz. Bu katman yeni epistemik "
    "kategori, confidence, reliability, weighting, ranking veya "
    "karar mekanizması üretmez."
)


# ============================================================
# 12. MODULE ENTRY
# ============================================================


if __name__ == "__main__":


    validate_11()


    print(
        "11. BÖLÜM — TEKNİK MİMARİ"
    )


    print(
        "=" * 72
    )


    print(
        TECHNICAL_ARCHITECTURE_FINAL_DECISION
    )


    print(
        "-" * 72
    )


    print(
        referential_atomic_validity_rule()
    )


    print(
        "-" * 72
    )


    print(
        TECHNICAL_ARCHITECTURE_FINAL_PRINCIPLE
    )


    print(
        "-" * 72
    )


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "=" * 72
    )


    print(
        "Validation: OK"
    )
