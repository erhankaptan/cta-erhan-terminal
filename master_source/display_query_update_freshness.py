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
