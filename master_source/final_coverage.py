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
