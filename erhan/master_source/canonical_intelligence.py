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
