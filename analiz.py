"""
ERHAN / CTA TERMINAL
7. BÃ–LÃœM â€” ANALÄ°Z / HESAPLAMA / DEÄžERLENDÄ°RME
FINAL CODE


READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ


6. BÃ¶lÃ¼m â€” YoÄŸurma Motoru'ndan gelen iliÅŸkili ve baÄŸlamsal bilgi
yapÄ±larÄ±nÄ± analiz eder.


7. BÃ¶lÃ¼mÃ¼n gÃ¶revi:
    - yapÄ±sal tespit,
    - iliÅŸkisel analiz,
    - Ã¶rÃ¼ntÃ¼ analizi,
    - zaman analizi,
    - provenance analizi,
    - karÅŸÄ±laÅŸtÄ±rÄ±labilirlik kontrolÃ¼,
    - convergence / divergence / contradiction /
      complementarity / repetition-relay analizi,
    - baÄŸÄ±msÄ±zlÄ±k yapÄ±sÄ±nÄ±n analizi,
    - belirsizlik tÃ¼rlerinin analizi,
    - izin verilen yapÄ±sal ve zamansal Ã¶lÃ§Ã¼mlerdir.


7. BÃ¶lÃ¼m:
    - nihai CTA hÃ¼kmÃ¼ Ã¼retmez,
    - bullish / bearish nihai yÃ¶n Ã¼retmez,
    - final bias Ã¼retmez,
    - trade sinyali Ã¼retmez,
    - risk / pozisyon kararÄ± Ã¼retmez,
    - gelecek tahmini Ã¼retmez,
    - confidence / reliability / trust Ã¼retmez,
    - evidence strength Ã¼retmez,
    - weighting / ranking yapmaz,
    - kendi baÅŸÄ±na piyasa rejimi sÄ±nÄ±flandÄ±rmaz.


6 -> 7:
    YoÄŸurma Motoru iliÅŸkileri ve yapÄ±larÄ± oluÅŸturur.


7 -> 8:
    Analiz Motoru analitik bulgular Ã¼retir.
    Bu bulgular 8. BÃ¶lÃ¼m CTA Synthesis / SonuÃ§ katmanÄ±na devredilir.


Ã–NEMLÄ°:
    Bu dosya 6. BÃ¶lÃ¼mÃ¼n InformationPiece, Cluster, Relation,
    ClusterRelation ve Membership sÄ±nÄ±flarÄ±nÄ± yeniden tanÄ±mlamaz.
    GerÃ§ek 6. BÃ¶lÃ¼m YoÄŸurma Motoru ile Ã§alÄ±ÅŸÄ±r.
"""


from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Sequence




# ============================================================================
# 1. ANALÄ°TÄ°K BULGU TÃœRLERÄ°
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
# 2. KARÅžILAÅžTIRILABÄ°LÄ°RLÄ°K
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
# 3. Ä°LÄ°ÅžKÄ° ANALÄ°Z TÃœRLERÄ°
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
# 4. YAPISAL / ZAMANSAL Ã–LÃ‡ÃœMLER
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


    # Ã–lÃ§Ã¼m sonucu betimleyici deÄŸerdir.
    # DeÄŸer hiÃ§bir ÅŸekilde score/confidence/ranking anlamÄ± taÅŸÄ±maz.
    value: Optional[float] = None


    unit: Optional[str] = None


    # Ä°htiyaÃ§ halinde Ã¶lÃ§Ã¼mÃ¼n metinsel aÃ§Ä±klamasÄ±.
    note: Optional[str] = None




# ============================================================================
# 5. PROVENANCE ANALÄ°ZÄ°
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
# 6. BELÄ°RSÄ°ZLÄ°K
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
# 7. DIÅžSAL REJÄ°M GÄ°RDÄ°SÄ°
# ============================================================================




@dataclass(frozen=True)
class ExternalRegimeInput:
    """
    DÄ±ÅŸarÄ±dan gelen rejim / makro / piyasa baÄŸlamÄ±.


    Bu nesne rejimi doÄŸrulamaz ve kendi baÅŸÄ±na yeni rejim
    sÄ±nÄ±flandÄ±rmasÄ± Ã¼retmez.
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
# 9. ANALÄ°Z BULGUSU
# ============================================================================




@dataclass(frozen=True)
class AnalysisFinding:
    """
    7. BÃ¶lÃ¼mÃ¼n temel Ã§Ä±ktÄ± nesnesi.


    AnalysisFinding:
        - gÃ¶zlemi,
        - yapÄ±sal bulguyu,
        - Ã¶lÃ§Ã¼mÃ¼,
        - iliÅŸki analizini


    taÅŸÄ±r.


    Nihai anlam / karar taÅŸÄ±maz.
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
# 10. 7 -> 8 Ã‡IKTI
# ============================================================================




@dataclass(frozen=True)
class AnalysisOutput:
    """
    8. BÃ¶lÃ¼me devredilecek analitik Ã§Ä±ktÄ±.


    Burada final CTA hÃ¼kmÃ¼ yoktur.
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
# 12. ANALÄ°Z MOTORU
# ============================================================================




class AnalysisEngine:
    """
    7. BÃ¶lÃ¼m â€” Analiz / Hesaplama / DeÄŸerlendirme Motoru.


    Girdi:
        6. BÃ¶lÃ¼m YogurmaMotoru.


    Ã‡Ä±ktÄ±:
        Analitik bulgular.


    Motor:
        - 6. BÃ¶lÃ¼mdeki InformationPiece'leri deÄŸiÅŸtirmez.
        - 6. BÃ¶lÃ¼m kÃ¼melerini deÄŸiÅŸtirmez.
        - 6. BÃ¶lÃ¼m iliÅŸkilerini deÄŸiÅŸtirmez.
        - geÃ§miÅŸ bilgi durumlarÄ±nÄ± overwrite etmez.


    Motorun iÅŸi analizdir.
    Nihai CTA synthesis 8. BÃ¶lÃ¼me aittir.
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
        6. BÃ¶lÃ¼m final motorunun gerekli public arayÃ¼zÃ¼nÃ¼ kontrol eder.
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
                    "7. BÃ¶lÃ¼m requires 6. BÃ¶lÃ¼m YogurmaMotoru "
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
        Ortak bilgi kÃ¶kÃ¼.


        Bu deÄŸer otomatik olarak "baÄŸÄ±msÄ±z kanÄ±t" anlamÄ±na gelmez.
        Sadece mevcut provenance/root bilgisinin yapÄ±sal kimliÄŸidir.
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
                "KÃ¼menin mevcut yapÄ±sal Ã¶zellikleri "
                "betimlenmiÅŸtir."
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
                "KÃ¼medeki kayÄ±tlarÄ±n mevcut provenance "
                "yapÄ±sÄ±nda tek ortak kÃ¶k kimliÄŸi vardÄ±r. "
                "Bu sonuÃ§ baÄŸÄ±msÄ±zlÄ±k veya kanÄ±t gÃ¼cÃ¼ hÃ¼kmÃ¼ deÄŸildir."
            )


        elif len(unique_roots) > 1:
            analysis_type = (
                ProvenanceAnalysisType.SEPARATE_ROOTS
            )
            note = (
                "KÃ¼mede birden fazla ayrÄ± bilgi kÃ¶kÃ¼ "
                "bulunmaktadÄ±r. AyrÄ± kÃ¶k bulunmasÄ± tek baÅŸÄ±na "
                "doÄŸruluk veya kanÄ±t gÃ¼cÃ¼ anlamÄ±na gelmez."
            )


        else:
            analysis_type = (
                ProvenanceAnalysisType.APPARENTLY_INDEPENDENT_PATHS
            )
            note = (
                "KayÄ±tlar iÃ§in mevcut provenance kÃ¶kÃ¼ "
                "yeterli deÄŸildir; baÄŸÄ±msÄ±zlÄ±k hÃ¼kmÃ¼ kurulmamÄ±ÅŸtÄ±r."
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


        # YapÄ±sal Ã¶lÃ§Ã¼m:
        # distinct root count = baÄŸÄ±msÄ±z kanÄ±t skoru deÄŸildir.
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
                    "AyrÄ± provenance root kimliklerinin sayÄ±sÄ±. "
                    "Evidence strength veya confidence deÄŸildir."
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
                "KÃ¼medeki bilgi kÃ¶kÃ¼ yapÄ±sÄ± "
                "betimlenmiÅŸtir; ayrÄ± kÃ¶k sayÄ±sÄ± "
                "baÄŸÄ±msÄ±zlÄ±k gÃ¼veni veya kanÄ±t gÃ¼cÃ¼ "
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
                    "Automatic independence/trust score deÄŸildir."
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


        # KayÄ±t sayÄ±sÄ± deÄŸiÅŸim sayÄ±sÄ± deÄŸildir.
        # GerÃ§ek deÄŸiÅŸim iÃ§in claim/status karÅŸÄ±laÅŸtÄ±rÄ±lÄ±r.
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
                f"Kaynak {source_id} iÃ§in kÃ¼me baÄŸlamÄ±nda "
                f"{change_count} iÃ§erik/statÃ¼ deÄŸiÅŸimi "
                "gÃ¶zlenmiÅŸtir."
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
                    "Claim/status signature deÄŸiÅŸim sayÄ±sÄ±dÄ±r; "
                    "Ã¶nem veya doÄŸruluk Ã¶lÃ§Ã¼sÃ¼ deÄŸildir."
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
                        "DeÄŸiÅŸim olaylarÄ±nÄ±n sayÄ±sal olmayan "
                        "zaman baÄŸlamÄ± finding kayÄ±tlarÄ±nda korunur."
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
                "AynÄ± provenance kÃ¶kÃ¼nden gelen tekrar/"
                "aktarÄ±m gruplarÄ± yapÄ±sal olarak tespit edilmiÅŸtir."
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
                    "AynÄ± provenance kÃ¶kÃ¼nden gelen "
                    "kayÄ±tlarÄ±n sayÄ±sÄ±dÄ±r; consensus deÄŸildir."
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
                    "Ä°ki bilgi parÃ§asÄ±nÄ±n karÅŸÄ±laÅŸtÄ±rÄ±labilirlik "
                    "koÅŸullarÄ± kontrol edilmiÅŸtir."
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
                    "6. BÃ¶lÃ¼mden gelen iliÅŸkinin "
                    "karÅŸÄ±laÅŸtÄ±rÄ±labilirlik koÅŸullarÄ±yla "
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
                "Gerekli production time mevcut deÄŸil; "
                "Ã¶lÃ§Ã¼m tamamlanamadÄ±."
            )


        else:
            value = abs(
                (
                    time_b - time_a
                ).total_seconds()
            )


            unit = "seconds"


            note = (
                "Zaman farkÄ± betimleyici Ã¶lÃ§Ã¼mdÃ¼r; "
                "Ã¶nem veya doÄŸruluk gÃ¶stergesi deÄŸildir."
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
                "DÄ±ÅŸsal rejim/makro/piyasa iddiasÄ± ile "
                "CTA bilgi yapÄ±larÄ±nÄ±n zaman ve baÄŸlam "
                "iliÅŸkisi incelenmiÅŸtir. DÄ±ÅŸsal iddia "
                "sistem tarafÄ±ndan doÄŸrulanmÄ±ÅŸ rejim "
                "sÄ±nÄ±flandÄ±rmasÄ± deÄŸildir."
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
            "Sonraki bilgi, geÃ§miÅŸteki bilgi durumunun "
            "yerine geÃ§irilemez."
        )


    @staticmethod
    def forecast_outcome_rule() -> str:
        return (
            "Forecast kendi Ã¼retildiÄŸi andaki statÃ¼sÃ¼nÃ¼ korur. "
            "Outcome daha sonra eklenen tarihsel bilgidir."
        )


    @staticmethod
    def positioning_revision_rule() -> str:
        return (
            "Eski positioning kaydÄ± silinmez. "
            "Revizyon yeni tarihsel durum olarak eklenir."
        )


    @staticmethod
    def view_change_rule() -> str:
        return (
            "Eski gÃ¶rÃ¼ÅŸ korunur. Yeni gÃ¶rÃ¼ÅŸ ayrÄ± bir "
            "tarihsel durumdur."
        )


    @staticmethod
    def later_falsified_rule() -> str:
        return (
            "Bilginin geÃ§miÅŸte ne sÃ¶ylediÄŸi ve o anda hangi "
            "statÃ¼de olduÄŸu korunur. Sonraki yanlÄ±ÅŸlanma veya "
            "dÃ¼zeltme yeni tarihsel deÄŸerlendirme katmanÄ±dÄ±r."
        )


    # ========================================================================
    # 14. 7 -> 8 SINIRI
    # ========================================================================


    @staticmethod
    def seven_to_eight_boundary() -> None:
        """
        7'nin analitik bulgularÄ± 8'in nihai CTA hÃ¼kmÃ¼ deÄŸildir.
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
    "7. BÃ¶lÃ¼m â€” Analiz / Hesaplama / DeÄŸerlendirme; YoÄŸurma "
    "Motoru'ndan gelen iliÅŸkili bilgi yapÄ±larÄ±nÄ±, karÅŸÄ±laÅŸtÄ±rÄ±labilirlik "
    "koÅŸullarÄ±nÄ±, bilgi statÃ¼lerini, zaman boyutunu, baÄŸlamÄ± ve "
    "provenance'Ä± koruyarak analiz eder. YapÄ±sal ve zamansal Ã¶zellikleri "
    "Ã¶lÃ§ebilir; yakÄ±nsama, ayrÄ±ÅŸma, Ã§eliÅŸki, tamamlayÄ±cÄ±lÄ±k, tekrar, "
    "baÄŸÄ±msÄ±zlÄ±k ve belirsizlik Ã¶rÃ¼ntÃ¼lerini ortaya Ã§Ä±karabilir. Ancak "
    "bu analitik bulgularÄ± otomatik olarak deÄŸer, gÃ¼ven, aÄŸÄ±rlÄ±k, "
    "Ã¼stÃ¼nlÃ¼k, nihai CTA anlamÄ±, gelecek tahmini veya iÅŸlem kararÄ±na "
    "dÃ¶nÃ¼ÅŸtÃ¼rmez. Nihai CTA Synthesis / SonuÃ§ katmanÄ± 8. BÃ¶lÃ¼mde "
    "ayrÄ±ca tasarlanacaktÄ±r."
)




# ============================================================================
# 18. VALIDATION / SELF TEST
# ============================================================================




def validate_7() -> None:
    """
    7. BÃ¶lÃ¼mÃ¼n kendi yapÄ±sal sÄ±nÄ±rlarÄ±nÄ± doÄŸrular.


    Not:
        Buradaki self-test 6. BÃ¶lÃ¼m dosyasÄ±nÄ± import etmez.
        GerÃ§ek entegrasyon testi aÅŸaÄŸÄ±daki IntegrationTest bÃ¶lÃ¼mÃ¼nde
        oluÅŸturulan minimal 6. BÃ¶lÃ¼m uyumlu test nesnesiyle yapÄ±lÄ±r.
    """


    AnalysisEngine.validate_forbidden_fields()


    # ------------------------------------------------------------------------
    # Minimal 6. BÃ¶lÃ¼m uyumlu test nesneleri
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
        "7. BÃ–LÃœM â€” ANALÄ°Z / HESAPLAMA / DEÄžERLENDÄ°RME"
    )
    print("=" * 72)


    print(
        ANALYSIS_FINAL_PRINCIPLE
    )


    print("=" * 72)


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ"
    )


    print(
        "Validation: PASSED"
    )


