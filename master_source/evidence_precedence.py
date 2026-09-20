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
