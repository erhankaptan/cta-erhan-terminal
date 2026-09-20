

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


BÃ–LÃœM 6 owns clustering / relationship evaluation.
BÃ–LÃœM 7 owns analysis / calculation / evaluation.
BÃ–LÃœM 8 owns synthesis.


This module is intentionally a preservation / traceability layer.
"""


from __future__ import annotations


from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple
from uuid import uuid4




# ============================================================================
# ENUMS â€” 5. BÃ–LÃœM KAVRAMSAL SINIRLAR
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
    """Raised when a 5. BÃ¶lÃ¼m invariant is violated."""




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
    BÃ–LÃœM 4. No new MASTER source is created here.
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
    5. BÃ–LÃœM â€” BÄ°LGÄ° HAVUZU


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
# EXPLICITLY FORBIDDEN 5. BÃ–LÃœM OPERATIONS
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
    Static architectural validation for BÃ–LÃœM 5.


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
            f"Forbidden BÃ–LÃœM 5 operations exposed: {sorted(leaked)}"
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
    print("BÃ–LÃœM 5 â€” BÄ°LGÄ° HAVUZU: VALIDATION PASSED")


