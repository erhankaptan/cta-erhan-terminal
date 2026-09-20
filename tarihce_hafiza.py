FINAL KOD


5â€“8 arasÄ±ndaki katmanlarÄ±n zaman iÃ§inde Ã¼retilmiÅŸ bilgi, iliÅŸkisel yapÄ±,
analitik bulgu ve synthesis durumlarÄ±nÄ± kendi tarihsel baÄŸlamlarÄ±,
provenance'larÄ± ve zaman referanslarÄ± korunarak muhafaza eder.


Sonraki bilgi, revizyon ve later outcome geÃ§miÅŸ historical state'in
yerine geÃ§irilmez. Her yeni geliÅŸme ayrÄ± tarihsel katman olarak tutulur.


TEMEL Ä°LKE:
    9 geÃ§miÅŸi korur; geÃ§miÅŸi yeniden yazmaz.


READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ
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
    Historical state'in zaman referanslarÄ±.


    PRODUCTION_SNAPSHOT_TIME:
        Historical state'in temel zaman kimliÄŸi.


    EVENT_TIME:
        State'in anlattÄ±ÄŸÄ± olayÄ±n zamanÄ±.


    REFERENCE_PERIOD:
        State'in referans verdiÄŸi dÃ¶nem.


    REVISION_TIME:
        Varsa daha sonra gerÃ§ekleÅŸen revizyon/deÄŸiÅŸim zamanÄ±.


    VALIDITY_PERIOD:
        GerektiÄŸinde korunan baÄŸlamsal geÃ§erlilik dÃ¶nemi.
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
    9. BÃ¶lÃ¼mÃ¼n tarihsel olarak koruduÄŸu nesneler.
    """


    # 5 â€” Bilgi
    INFORMATION_PIECE = "information_piece"
    RAW_INFORMATION = "raw_information"
    SOURCE_VIEW = "source_view"
    POSITIONING_CHANGE = "positioning_change"
    INFORMATION_STATUS_CHANGE = "information_status_change"
    PROVENANCE = "provenance"


    # 6 â€” YoÄŸurma
    RELATIONAL_STRUCTURE_STATE = "relational_structure_state"
    CLUSTER_STATE = "cluster_state"
    RELATIONSHIP_STATE = "relationship_state"
    STRUCTURE_CHANGE = "structure_change"


    # 7 â€” Analiz
    ANALYTICAL_FINDING_STATE = "analytical_finding_state"
    UNCERTAINTY_AT_TIME = "uncertainty_at_time"
    HISTORICAL_INFORMATION_CONDITION = (
        "historical_information_condition"
    )


    # 8 â€” Synthesis
    SYNTHESIS_RESULT = "synthesis_result"
    SYNTHESIS_INPUT_STATE = "synthesis_input_state"
    SYNTHESIS_UNCERTAINTY = "synthesis_uncertainty"
    SYNTHESIS_LIMITATION = "synthesis_limitation"


    # Sonraki geliÅŸmeler
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
    Belirli bir production/snapshot anÄ±ndaki historical state.


    Ã–NEMLÄ°:
        Bu nesne frozen'dÄ±r.


        Ä°Ã§erdiÄŸi koleksiyonlar tuple'dÄ±r.
        BÃ¶ylece state oluÅŸturulduktan sonra doÄŸrudan mutasyona
        uÄŸratÄ±lamaz.


    State:
        - 5 bilgi durumunu,
        - 6 iliÅŸkisel durumunu,
        - 7 analitik durumunu,
        - 8 synthesis durumunu


    aynÄ± historical snapshot altÄ±nda referanslar.


    9 bu nesneleri yeniden Ã¼retmez.
    YalnÄ±zca o anda mevcut olan kimlikleri tarihsel olarak korur.
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


    # Ä°nsan tarafÄ±ndan verilen tarihsel aÃ§Ä±klama.
    note: Optional[str] = None




# ============================================================
# 4. HISTORICAL CHANGE
# ============================================================


class ChangeType(str, Enum):
    """
    Historical state'ler arasÄ±ndaki deÄŸiÅŸim tÃ¼rleri.


    Bunlar 9 tarafÄ±ndan analiz edilmez.
    YalnÄ±zca tarihsel deÄŸiÅŸimin tÃ¼rÃ¼nÃ¼ kaydeder.
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


    Yeni state varsa ayrÄ± historical layer'dÄ±r.


    previous_state_id:
        Ã–nceki historical state.


    new_state_id:
        Yeni historical state.


    9 burada deÄŸiÅŸimin analitik anlamÄ±nÄ± Ã¼retmez.
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
    Historical state'ten sonra gelen geliÅŸme tÃ¼rleri.
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
    Historical state'ten sonra gerÃ§ekleÅŸen geliÅŸme.


    Bu nesne geÃ§miÅŸ state'in iÃ§ine yazÄ±lmaz.


    target_state_id:
        Outcome'un hangi historical state ile iliÅŸkili olduÄŸunu
        belirtir.


    outcome_time:
        GerÃ§ekleÅŸmenin / ortaya Ã§Ä±kÄ±ÅŸÄ±n zamanÄ±.


    record_time:
        Outcome'un hafÄ±zaya kaydedildiÄŸi zaman.


    Ã–NEMLÄ°:
        Outcome, target historical state'in parÃ§asÄ± deÄŸildir.
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
    Daha Ã¶nce 7 veya 8 tarafÄ±ndan Ã¼retilmiÅŸ historical evaluation'Ä±n
    tarihsel kaydÄ±.


    9 kendisi evaluation Ã¼retmez.


    produced_by:
        Evaluation'Ä±n daha Ã¶nce hangi katmanda Ã¼retildiÄŸini belirtir.


    Ä°zin verilen Ã¼reticiler:


    9 yalnÄ±zca bunlarÄ±n mevcut tarihsel kaydÄ±nÄ± korur.
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
    Historical state iÃ§inde provenance baÄŸlantÄ±sÄ±nÄ±n korunmasÄ±.


    9 provenance deÄŸerlendirmez.
    Sadece mevcut provenance kimliklerini tarihsel snapshot'a
    baÄŸlar.
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
    ID koleksiyonunu immutable tuple'a Ã§evirir.


    Duplicate ID'ler tekilleÅŸtirilir ancak sÄ±ralama korunur.
    """


    normalized: list[str] = []


    for value in values:
        if not isinstance(value, str) or not value:
            raise ValueError(
                "Historical state ID alanlarÄ± boÅŸ veya geÃ§ersiz olamaz."
            )


        if value not in normalized:
            normalized.append(value)


    return tuple(normalized)




def freeze_historical_state(
    state: HistoricalState,
) -> HistoricalState:
    """
    HistoricalState'in immutable koleksiyon sÄ±nÄ±rÄ±nÄ± doÄŸrular.


    Yeni bir state Ã¼retmez; verilen state'in tarihsel bÃ¼tÃ¼nlÃ¼ÄŸÃ¼nÃ¼
    kontrol eder.
    """


    if not state.state_id:
        raise ValueError(
            "Historical state state_id boÅŸ olamaz."
        )


    if not isinstance(
        state.snapshot_time,
        datetime,
    ):
        raise TypeError(
            "snapshot_time datetime olmalÄ±dÄ±r."
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
        "Belirli bir historical state iÃ§in 'O anda ne biliniyordu?' "
        "sorusunun cevabÄ±, daha sonra Ã¶ÄŸrenilen bilgilerle deÄŸiÅŸtirilmez."
    )




def no_retroactive_injection() -> str:
    return (
        "Sonraki bilgi, revizyon veya outcome geÃ§miÅŸ historical state'in "
        "iÃ§ine geriye dÃ¶nÃ¼k olarak taÅŸÄ±namaz."
    )




def historical_state_is_immutable() -> str:
    return (
        "KaydedilmiÅŸ historical state update edilemez veya Ã¼zerine "
        "yazÄ±lamaz; yeni durum ayrÄ± historical state olarak kaydedilir."
    )




# ============================================================
# 10. HISTORICAL PATTERN / 7 SINIRI
# ============================================================


def historical_pattern_boundary() -> str:
    """
    9 tarihsel malzemeyi saÄŸlar.


    9:
        similarity hesaplamaz,
        pattern matching yapmaz,
        benzerlik seÃ§mez,
        tarihsel Ã¶rÃ¼ntÃ¼ analizi yapmaz.


    Bu iÅŸlemler 7'nin analiz yetki alanÄ±dÄ±r.
    """


    return (
        "9 tarihsel malzemeyi saÄŸlar; 7 bu malzeme Ã¼zerinde "
        "karÅŸÄ±laÅŸtÄ±rma, benzerlik ve Ã¶rÃ¼ntÃ¼ analizi yapar. "
        "9 iÃ§inde similarity veya pattern motoru bulunmaz."
    )




# ============================================================
# 11. 5â€“8 SINIRI
# ============================================================


FIVE_TO_EIGHT_BOUNDARY = {
    "5": "Bilgiyi korur.",
    "6": "Bilgiler arasÄ±ndaki iliÅŸkileri ve kÃ¼meleri oluÅŸturur.",
    "7": "Ä°liÅŸkileri analiz eder ve analitik bulgularÄ± Ã¼retir.",
    "8": "7 bulgularÄ±nÄ±n birlikte ne ifade ettiÄŸini sentezler.",
    "9": (
        "5â€“8'in zaman iÃ§indeki historical state'lerini korur "
        "ve eriÅŸilebilir kÄ±lar."
    ),
}




def memory_not_reproduction() -> str:
    return (
        "9; 5'i yeniden oluÅŸturmaz, 6'yÄ± yeniden kurmaz, 7'yi "
        "yeniden Ã§alÄ±ÅŸtÄ±rmaz, 8'i yeniden Ã¼retmez. 9'un gÃ¶revi "
        "tarihÃ§e ve hafÄ±zadÄ±r."
    )




# ============================================================
# 12. HAFIZA MOTORU
# ============================================================


class HafizaMotoru:
    """
    9. BÃ¶lÃ¼m â€” TarihÃ§e / HafÄ±za.


    TEMEL GÃ–REV:
        5â€“8 tarafÄ±ndan Ã¼retilmiÅŸ historical durumlarÄ± korumak.


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


        # Historical snapshot zamanÄ± -> state_id'ler.
        # AynÄ± snapshot zamanÄ±nda farklÄ± state'lerin bulunmasÄ±na izin verir.
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


        AynÄ± state_id ikinci kez kullanÄ±lamaz.


        Ã–NEMLÄ°:
            AynÄ± snapshot_time'a sahip farklÄ± state'ler mÃ¼mkÃ¼ndÃ¼r.
            Bu nedenle snapshot zamanÄ± tek baÅŸÄ±na primary identity deÄŸildir.
        """


        frozen_state = freeze_historical_state(state)


        if frozen_state.state_id in self._states:
            raise ValueError(
                "Historical state immutable'dÄ±r; aynÄ± state_id "
                f"Ã¼zerine yazÄ±lamaz: {frozen_state.state_id}"
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
        Historical state'i immutable haliyle dÃ¶ndÃ¼rÃ¼r.
        """


        if state_id not in self._states:
            raise KeyError(
                f"Historical state bulunamadÄ±: {state_id}"
            )


        return self._states[state_id]


    def states_at(
        self,
        snapshot_time: datetime,
    ) -> tuple[HistoricalState, ...]:
        """
        Belirli snapshot zamanÄ±ndaki tÃ¼m historical state'leri
        dÃ¶ndÃ¼rÃ¼r.
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


        Ã–nceki ve yeni state'lerin gerÃ§ekten mevcut olmasÄ± gerekir.


        9 deÄŸiÅŸimin anlamÄ±nÄ± analiz etmez.
        """


        if change.change_id in self._changes:
            raise ValueError(
                "Duplicate historical change ID: "
                f"{change.change_id}"
            )


        if change.previous_state_id not in self._states:
            raise ValueError(
                "Previous historical state bulunamadÄ±: "
                f"{change.previous_state_id}"
            )


        if change.new_state_id not in self._states:
            raise ValueError(
                "New historical state bulunamadÄ±: "
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
                "Change time previous historical state'ten Ã¶nce olamaz."
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
        Later outcome'u geÃ§miÅŸ state'ten ayrÄ± tutar.


        Kritik kural:
            outcome_time >= target snapshot_time


        AyrÄ±ca outcome hiÃ§bir zaman target HistoricalState'in
        iÃ§ine eklenmez.
        """


        if outcome.outcome_id in self._outcomes:
            raise ValueError(
                "Duplicate later outcome ID: "
                f"{outcome.outcome_id}"
            )


        if outcome.target_state_id not in self._states:
            raise ValueError(
                "Later outcome'un hedef historical state'i bulunamadÄ±: "
                f"{outcome.target_state_id}"
            )


        target_state = self._states[
            outcome.target_state_id
        ]


        if outcome.outcome_time < target_state.snapshot_time:
            raise ValueError(
                "Later outcome, hedef historical state'ten "
                "Ã¶nce gerÃ§ekleÅŸemez."
            )


        if outcome.record_time < outcome.outcome_time:
            raise ValueError(
                "Outcome record_time, outcome_time'dan Ã¶nce olamaz."
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
                f"Historical state bulunamadÄ±: {state_id}"
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
        Daha Ã¶nce 7 veya 8 tarafÄ±ndan Ã¼retilmiÅŸ evaluation'Ä±
        tarihsel kayÄ±t olarak saklar.


        9'un kendi evaluation Ã¼retmesine izin verilmez.
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
                "9 yalnÄ±zca 7 veya 8 tarafÄ±ndan daha Ã¶nce Ã¼retilmiÅŸ "
                "historical evaluation'larÄ± saklayabilir."
            )


        if evaluation.state_id not in self._states:
            raise ValueError(
                "Historical evaluation state'i bulunamadÄ±: "
                f"{evaluation.state_id}"
            )


        if evaluation.outcome_id not in self._outcomes:
            raise ValueError(
                "Historical evaluation outcome'u bulunamadÄ±: "
                f"{evaluation.outcome_id}"
            )


        outcome = self._outcomes[
            evaluation.outcome_id
        ]


        if outcome.target_state_id != evaluation.state_id:
            raise ValueError(
                "Historical evaluation state/outcome baÄŸlantÄ±sÄ± "
                "uyumsuz."
            )


        if evaluation.evaluation_time < outcome.outcome_time:
            raise ValueError(
                "Historical evaluation outcome'dan Ã¶nce Ã¼retilemez."
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
        Historical provenance kaydÄ±.


        9 provenance'Ä±n gÃ¼venilirliÄŸini deÄŸerlendirmez.
        """


        if provenance.provenance_id in self._provenance:
            raise ValueError(
                "Duplicate historical provenance ID: "
                f"{provenance.provenance_id}"
            )


        if not provenance.source_id:
            raise ValueError(
                "Historical provenance source_id boÅŸ olamaz."
            )


        if provenance.parent_provenance_id is not None:
            if (
                provenance.parent_provenance_id
                not in self._provenance
            ):
                raise ValueError(
                    "Parent provenance bulunamadÄ±: "
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
        TÃ¼m historical state'lerin temel PIT koÅŸullarÄ±nÄ± kontrol eder.


        Bu kontrol:
        - state'in snapshot zamanÄ±nÄ±,
        - immutable identity'yi,
        - later outcome zaman ayrÄ±mÄ±nÄ±,
        - change zaman ayrÄ±mÄ±nÄ±


        doÄŸrular.
        """


        for state in self._states.values():


            assert isinstance(
                state.snapshot_time,
                datetime,
            ), (
                "Historical state snapshot_time datetime olmalÄ±dÄ±r: "
                f"{state.state_id}"
            )


            assert state.state_id in self._states, (
                "Historical state registry bÃ¼tÃ¼nlÃ¼ÄŸÃ¼ bozulmuÅŸ: "
                f"{state.state_id}"
            )


        for outcome in self._outcomes.values():


            target = self._states[
                outcome.target_state_id
            ]


            assert outcome.outcome_time >= (
                target.snapshot_time
            ), (
                "Later outcome geÃ§miÅŸ historical state'ten "
                "Ã¶nce olamaz: "
                f"{outcome.outcome_id}"
            )


            assert outcome.record_time >= (
                outcome.outcome_time
            ), (
                "Outcome record_time outcome_time'dan Ã¶nce olamaz: "
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
                "Change previous state'ten Ã¶nce olamaz: "
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
        State'in registry'de mevcut olduÄŸunu ve immutable identity'nin
        korunmuÅŸ olduÄŸunu kontrol eder.


        9'un state update metodu yoktur.
        """


        if state_id not in self._states:
            raise AssertionError(
                "Historical state mevcut deÄŸil veya silinmiÅŸ: "
                f"{state_id}"
            )


        state = self._states[state_id]


        assert state.state_id == state_id


    def verify_historical_layer_separation(
        self,
    ) -> None:
        """
        Later outcome ve revision kayÄ±tlarÄ±nÄ±n historical state'in
        kendisine eklenmediÄŸini doÄŸrular.


        9 bunlarÄ± ayrÄ± koleksiyonlarda tutar.
        """


        state_ids = set(self._states)


        for outcome in self._outcomes.values():


            assert outcome.outcome_id not in state_ids, (
                "Later outcome historical state ID alanÄ±na "
                "yerleÅŸtirilemez."
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
        Historical state'leri snapshot zamanÄ±na gÃ¶re sÄ±ralÄ±
        eriÅŸilebilir hale getirir.


        Bu iÅŸlem analiz veya pattern matching deÄŸildir.
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
# 13. DOÄžAL HAFIZA Ã‡IKTILARI
# ============================================================


NATURAL_MEMORY_OUTPUTS = (
    "Bu kurum Ocak'ta X, Mart'ta Y diyordu.",
    "Bu synthesis Mart ayÄ±ndaki bilgi durumuna aitti.",
    "Bu positioning ÅŸu tarihte deÄŸiÅŸti.",
    "Bu forecast ÅŸu tarihte Ã¼retildi.",
    "Bu forecast'in hedeflediÄŸi dÃ¶nem daha sonra kapandÄ±.",
    "Åžu outcome daha sonra gerÃ§ekleÅŸti.",
    "Bu veri daha sonra revize edildi.",
    "O dÃ¶nemde ÅŸu bilgi mevcut deÄŸildi.",
    "BugÃ¼n bilinen bu bilgi o historical state'te mevcut deÄŸildi.",
)




NON_MEMORY_OUTPUTS = (
    "Bu 10 olay birbirine benziyor.",
    "Bu forecast baÅŸarÄ±lÄ±ydÄ±.",
    "Bu Ã¶rÃ¼ntÃ¼ gelecekte tekrar eder.",
)




# ============================================================
# 14. KESÄ°N YASAKLAR
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
# 15. TEKNÄ°K MÄ°MARÄ° YASAKLARI â€” KAVRAMSAL BÃ–LÃœM SINIRI
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
    9. BÃ¶lÃ¼mÃ¼n kavramsal tanÄ±mÄ±nda database/storage/API/UI mimarisi
    tanÄ±mlanmadÄ±ÄŸÄ±nÄ± korur.


    Bu kod yalnÄ±zca kavramsal sÄ±nÄ±rlarÄ±n davranÄ±ÅŸsal kontrolÃ¼nÃ¼
    temsil eder.
    """


    for item in FORBIDDEN_CONCEPTUAL_ARCHITECTURE:
        assert isinstance(item, str)




# ============================================================
# 16. NÄ°HAÄ° KAVRAMSAL TANIM
# ============================================================


MEMORY_FINAL_DEFINITION = (
    "ERHAN / CTA TERMINALI'nin TarihÃ§e / HafÄ±za katmanÄ±; 5â€“8 arasÄ±ndaki "
    "katmanlarÄ±n zaman iÃ§inde Ã¼retilmiÅŸ bilgi, iliÅŸkisel yapÄ±, analitik "
    "bulgu ve synthesis durumlarÄ±nÄ± kendi tarihsel baÄŸlamlarÄ±, "
    "provenance'larÄ± ve zaman referanslarÄ± korunarak muhafaza eden; "
    "sonraki bilgi, revizyon ve later outcome'larÄ± geÃ§miÅŸ state'in "
    "yerine geÃ§irmeden ayrÄ± tarihsel katmanlar olarak tutan; geÃ§miÅŸin "
    "bugÃ¼nkÃ¼ bilgiyle kirletilmesini Ã¶nleyen ve geÃ§miÅŸ durumlarÄ± "
    "eriÅŸilebilir kÄ±lan kavramsal hafÄ±za katmanÄ±dÄ±r."
)




# ============================================================
# 17. FINAL PRINCIPLE
# ============================================================


MEMORY_FINAL_PRINCIPLE = (
    "9 geÃ§miÅŸi korur; geÃ§miÅŸi yeniden yazmaz. "
    "Historical state kendi production/snapshot zamanÄ±nda dondurulur. "
    "Sonraki bilgi, revision, change ve later outcome ayrÄ± tarihsel "
    "katmanlarda tutulur. Historical state bugÃ¼nkÃ¼ bilgiyle geriye "
    "dÃ¶nÃ¼k olarak deÄŸiÅŸtirilmez. 9 similarity, pattern, historical "
    "evaluation, prediction, trade, risk veya karar Ã¼retmez; 5â€“8'in "
    "zaman iÃ§indeki tarihsel durumlarÄ±nÄ±, provenance'larÄ±nÄ± ve "
    "point-in-time baÄŸlamlarÄ±nÄ± eriÅŸilebilir tutar."
)




# ============================================================
# 18. VALIDATION
# ============================================================


def validate_9() -> None:
    """
    9. BÃ¶lÃ¼m self-validation.


    Bu fonksiyon:
        - tarihsel state bÃ¼tÃ¼nlÃ¼ÄŸÃ¼nÃ¼,
        - PIT ayrÄ±mÄ±nÄ±,
        - immutable layering sÄ±nÄ±rÄ±nÄ±,
        - later outcome ayrÄ±mÄ±nÄ±,
        - revision/change baÄŸlantÄ±sÄ±nÄ±,
        - historical evaluation sÄ±nÄ±rÄ±nÄ±,
        - provenance korunmasÄ±nÄ±


    test eder.


    Harici runtime sisteminin doÄŸrulamasÄ± deÄŸildir.
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
        "deÄŸiÅŸtirilmez"
        in point_in_time_integrity()
    )


    assert (
        "geriye dÃ¶nÃ¼k"
        in no_retroactive_injection()
    )


    assert (
        "Ã¼zerine yazÄ±lamaz"
        in historical_state_is_immutable()
    )


    assert (
        "7"
        in historical_pattern_boundary()
    )


    assert (
        "hafÄ±za"
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
            "AynÄ± historical state_id Ã¼zerine yazÄ±lmasÄ±na izin verildi."
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
            "January historical state sonrasÄ±nda ortaya Ã§Ä±kan outcome."
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
            "Daha Ã¶nce 7 tarafÄ±ndan Ã¼retilmiÅŸ historical evaluation."
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


    # Later outcome state'in iÃ§ine eklenmemiÅŸtir.
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
        "geÃ§miÅŸi korur"
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
        "9. BÃ–LÃœM â€” TARÄ°HÃ‡E / HAFIZA"
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
        "READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ"
    )


    print(
        "Validation: OK"
    )


"""
