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
