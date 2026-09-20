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
