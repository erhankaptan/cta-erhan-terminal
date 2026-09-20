FINAL KÄ°LÄ°TLEME


Teknik mimari sÃ¶zleÅŸmesi:


1. Historical Snapshot zamanÄ± ayrÄ±dÄ±r.
2. Publication / Access / Ingestion ayrÄ±dÄ±r.
3. Provenance Root / Path / Independence ayrÄ±dÄ±r.
4. Information Piece zorunlu canonicalization ile ezilmez.
5. Information Status 5. BÃ¶lÃ¼mden gelir ve teknik katman tarafÄ±ndan
   sessizce deÄŸiÅŸtirilemez.
6. Kaynak nedensellik iddiasÄ± ile sistemin kendi nedensellik hÃ¼kmÃ¼ ayrÄ±dÄ±r.
7. Bounded Context / Read-Write Authority mantÄ±ksal olarak korunur.
8. Referential / Atomic Validity tamamlanmÄ±ÅŸ state iÃ§in zorunludur.


REFERENTIAL / ATOMIC VALIDITY:


Gerekli trace/reference baÄŸlantÄ±larÄ± tamamlanmamÄ±ÅŸ bir
Finding, Synthesis, Historical Snapshot veya Relationship
sistemde geÃ§ici/incomplete state olarak bulunabilir.


Ancak gerekli referanslarÄ± gerÃ§ekten mevcut ve geÃ§erli olmadan
tamamlanmÄ±ÅŸ/geÃ§erli Ã§Ä±ktÄ± olarak kabul edilemez.


Eksik state:
    - silinmez,
    - otomatik reddedilmez,
    - geÃ§miÅŸ state'i deÄŸiÅŸtirmez,
    - sonradan oluÅŸan bilgiyi geÃ§miÅŸe sessizce enjekte etmez.


READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable




# ============================================================
# 1. TEKNÄ°K MÄ°MARÄ° SINIFLANDIRMASI
# ============================================================


class TechnicalArchitectureClass(str, Enum):
    """
    Teknik mimari sorgu sÄ±nÄ±flandÄ±rmasÄ±.


    A: Problem yok.
    B: Minimum dÃ¼zeltme gerekli.
    C: Kavramsal sÄ±nÄ±r belirsiz.
    D: Kapsam dÄ±ÅŸÄ±.
    """


    A_NO_ISSUE = "A"
    B_FIX_REQUIRED = "B"
    C_BOUNDARY_UNCLEAR = "C"
    D_OUT_OF_SCOPE = "D"




# ============================================================
# 2. TEKNÄ°K MÄ°MARÄ° BULGUSU
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
# 3. 11. BÃ–LÃœMÃœN 8 KÄ°LÄ°TLÄ° BULGUSU
# ============================================================


TECHNICAL_ARCHITECTURE_FINDINGS: tuple[
    TechnicalArchitectureFinding,
    ...,
] = (


    # --------------------------------------------------------
    # Q1 â€” HISTORICAL SNAPSHOT ZAMANI
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q1",
        title="Historical Snapshot ZamanÄ±",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Production, access, ingestion, event, reference, revision "
            "ve snapshot zamanlarÄ±nÄ±n semantik olarak ayrÄ±lmasÄ± "
            "point-in-time bÃ¼tÃ¼nlÃ¼ÄŸÃ¼ ve hindsight contamination'Ä±n "
            "Ã¶nlenmesi iÃ§in yeterlidir. as_of_time / snapshot_time, "
            "sistemin temsil ettiÄŸi historical state'in zaman sÄ±nÄ±rÄ±dÄ±r. "
            "Production time bunun yerine geÃ§irilemez."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q2 â€” PUBLICATION / ACCESS / INGESTION
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q2",
        title="Publication / Access / Ingestion",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Publication, access ve ingestion farklÄ± olaylardÄ±r. "
            "Fiziksel olarak aynÄ± yapÄ±da tutulabilmeleri semantik "
            "ayrÄ±mÄ± ortadan kaldÄ±rmaz. Bir yayÄ±na tekrar eriÅŸilmesi "
            "durumunda publication kimliÄŸi ve provenance korunabildiÄŸi "
            "sÃ¼rece point-in-time ve provenance bÃ¼tÃ¼nlÃ¼ÄŸÃ¼ korunur."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q3 â€” PROVENANCE ROOT / INDEPENDENCE
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q3",
        title="Provenance Root ve Independence",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "provenance_root, provenance_path ve independent_path "
            "farklÄ± kavramlardÄ±r. FarklÄ± provenance_root_id deÄŸerleri "
            "otomatik olarak baÄŸÄ±msÄ±z kanÄ±t anlamÄ±na gelmez. Bu ayrÄ±m "
            "false independence ve yanlÄ±ÅŸ consensus Ã¼retimini engeller."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q4 â€” DEDUPLICATION / CANONICALIZATION
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q4",
        title="Information Piece Deduplication / Canonicalization",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Zorunlu tekilleÅŸtirme veya canonicalization dayatÄ±lmamasÄ±, "
            "Information Piece'in provenance, context, publication/access "
            "geÃ§miÅŸi, zaman ve anlamlÄ± farklÄ±lÄ±klarÄ±nÄ±n korunmasÄ±nÄ± saÄŸlar. "
            "AynÄ± kÃ¶kten gelen kayÄ±tlarÄ±n baÄŸÄ±msÄ±z kanÄ±t gibi gÃ¶rÃ¼nmemesi "
            "ise 4â€“7'deki provenance ve independence sÄ±nÄ±rlarÄ±yla korunur."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q5 â€” INFORMATION STATUS
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q5",
        title="Information Status SÄ±nÄ±rÄ±",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Teknik enum veya schema deÄŸiÅŸikliÄŸi tek baÅŸÄ±na yeni "
            "epistemik kategori yaratamaz. Status kavramÄ±nÄ±n kaynaÄŸÄ± "
            "5. BÃ¶lÃ¼mdeki kavramsal tanÄ±mdÄ±r. 11. BÃ¶lÃ¼m bunu deÄŸiÅŸtiremez "
            "ve mevcut status'larÄ± teknik sebeple sessizce dÃ¶nÃ¼ÅŸtÃ¼remez."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q6 â€” CAUSALITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q6",
        title="Causality SÄ±nÄ±rÄ±",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "KaynaÄŸÄ±n yayÄ±nladÄ±ÄŸÄ± nedensellik iddiasÄ±nÄ±n saklanmasÄ± ile "
            "sistemin kendi nedensellik hÃ¼kmÃ¼nÃ¼ Ã¼retmesi birbirinden "
            "ayrÄ±lmÄ±ÅŸtÄ±r. Kaynak iddiasÄ±, ERHAN tarafÄ±ndan Ã¼retilmiÅŸ "
            "nedensellik hÃ¼kmÃ¼ deÄŸildir."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q7 â€” BOUNDED CONTEXT / READ-WRITE AUTHORITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q7",
        title="Bounded Context / Read-Write Authority",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "6, 7 ve 8'in fiziksel olarak ayrÄ± servisler olmasÄ± zorunlu "
            "deÄŸildir. Logical boundary, read/write authority, output "
            "contract, immutable veya versioned input, traceability ve "
            "sessiz mutation'Ä±n engellenmesi yeterli teknik sÄ±nÄ±rlarÄ± "
            "oluÅŸturur. Fiziksel ayrÄ±m 12. Kodlama aÅŸamasÄ±na bÄ±rakÄ±lÄ±r."
        ),


        relation_to_1_10="Ã‡eliÅŸmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q8 â€” REFERENTIAL / ATOMIC VALIDITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q8",
        title="Referential / Atomic Validity",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "TamamlanmÄ±ÅŸ Finding, Synthesis, Historical Snapshot veya "
            "Relationship; kendisini oluÅŸturan zorunlu trace/reference "
            "baÄŸlantÄ±larÄ± gerÃ§ekten mevcut ve geÃ§erli olmadan "
            "tamamlanmÄ±ÅŸ/geÃ§erli Ã§Ä±ktÄ± olarak kabul edilemez. Eksik "
            "referanslÄ± state geÃ§ici/incomplete olarak bulunabilir. "
            "Bu kural provenance, traceability ve point-in-time "
            "bÃ¼tÃ¼nlÃ¼ÄŸÃ¼nÃ¼ teknik sÃ¶zleÅŸmede korur."
        ),


        relation_to_1_10=(
            "Ã‡eliÅŸmiyor. Aksine 5â€“10'daki provenance, traceability, "
            "point-in-time ve 7â†’8 sÄ±nÄ±rlarÄ±nÄ± teknik bÃ¼tÃ¼nlÃ¼k kuralÄ± "
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
    Referential / Atomic Validity kapsamÄ±nda kontrol edilen
    tamamlanmÄ±ÅŸ state tÃ¼rleri.
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
    Bir teknik state'in referans bÃ¼tÃ¼nlÃ¼ÄŸÃ¼ sÃ¶zleÅŸmesi.


    required_references:
        State'in tamamlanabilmesi iÃ§in bulunmasÄ± gereken referans ID'leri.


    is_completed:
        State'in tamamlanmÄ±ÅŸ/geÃ§erli Ã§Ä±ktÄ± olarak iÅŸaretlenip
        iÅŸaretlenmediÄŸi.


    Ã–NEMLÄ°:
        Bu sÄ±nÄ±f referanslarÄ±n yalnÄ±zca dolu string olmasÄ±nÄ± deÄŸil,
        Enforcer iÃ§indeki gerÃ§ek reference registry'de bulunmasÄ±nÄ±
        kontrol eder.
    """


    entity_type: TechnicalEntityType
    entity_id: str
    required_references: tuple[str, ...]
    is_completed: bool = False


    def has_required_reference_ids(self) -> bool:
        """
        Referans listesinin biÃ§imsel bÃ¼tÃ¼nlÃ¼ÄŸÃ¼.


        BoÅŸ ID veya whitespace-only ID kabul edilmez.
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
    Teknik referans registry kaydÄ±.


    Reference'Ä±n gerÃ§ekten mevcut olduÄŸunu temsil eder.
    """


    reference_id: str
    reference_type: str




# ============================================================
# 7. TEKNÄ°K MÄ°MARÄ° ENFORCER
# ============================================================


class TechnicalArchitectureEnforcer:
    """
    11. BÃ¶lÃ¼m â€” Teknik Mimari BÃ¼tÃ¼nlÃ¼k ve DoÄŸrulama Motoru.


    DenetlediÄŸi sÄ±nÄ±rlar:


    - point-in-time ayrÄ±mÄ±,
    - publication/access/ingestion ayrÄ±mÄ±,
    - provenance ayrÄ±mÄ±,
    - reference bÃ¼tÃ¼nlÃ¼ÄŸÃ¼,
    - completed/incomplete state ayrÄ±mÄ±,
    - duplicate entity engeli,
    - sessiz mutation engeli.


    Bu motor:


    - epistemik skor Ã¼retmez,
    - confidence Ã¼retmez,
    - reliability Ã¼retmez,
    - weighting Ã¼retmez,
    - ranking Ã¼retmez,
    - karar Ã¼retmez,
    - trade sinyali Ã¼retmez.
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
        GerÃ§ek bir teknik referans kaydeder.


        AynÄ± reference_id ikinci kez kaydedilemez.
        """


        if not isinstance(reference_id, str):
            raise TypeError(
                "reference_id string olmalÄ±dÄ±r."
            )


        normalized_id = reference_id.strip()


        if not normalized_id:
            raise ValueError(
                "reference_id boÅŸ olamaz."
            )


        if normalized_id in self._references:
            raise ValueError(
                "Duplicate technical reference_id: "
                f"{normalized_id}"
            )


        if not reference_type.strip():
            raise ValueError(
                "reference_type boÅŸ olamaz."
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


        Completed state iÃ§in iki koÅŸul zorunludur:


        1. Referans ID'leri biÃ§imsel olarak geÃ§erli olmalÄ±.
        2. Her zorunlu referans registry'de gerÃ§ekten bulunmalÄ±.


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
                "entity_type TechnicalEntityType olmalÄ±dÄ±r."
            )


        if not isinstance(entity_id, str):
            raise TypeError(
                "entity_id string olmalÄ±dÄ±r."
            )


        normalized_entity_id = entity_id.strip()


        if not normalized_entity_id:
            raise ValueError(
                "entity_id boÅŸ olamaz."
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
        # Completed talebi yalnÄ±zca gerÃ§ek referanslar mevcutsa
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
                f"Technical state bulunamadÄ±: {normalized_id}"
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
    # SILENT MUTATION ENGELÄ°
    # ========================================================


    def update_entity_state(
        self,
        entity_id: str,
        *,
        references: Iterable[str] | None = None,
        mark_completed: bool | None = None,
    ) -> None:
        """
        Mevcut state'in sessiz mutation'Ä±nÄ± engeller.


        11. BÃ¶lÃ¼m append-only / immutable boundary nedeniyle
        mevcut state doÄŸrudan gÃ¼ncellenemez.


        Yeni bir state gerekiyorsa yeni entity/version ID'si
        ile yeni historical layer oluÅŸturulmalÄ±dÄ±r.
        """


        raise RuntimeError(
            "Technical state sessizce gÃ¼ncellenemez. "
            "Yeni state/version oluÅŸturulmalÄ±dÄ±r."
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
    # BÃœTÃœNLÃœK KONTROLÃœ
    # ========================================================


    def validate_all_contracts(
        self,
    ) -> bool:
        """
        Registry'deki tÃ¼m contract'larÄ±n bÃ¼tÃ¼nlÃ¼ÄŸÃ¼nÃ¼ kontrol eder.


        Incomplete state'ler geÃ§erlidir; ancak completed state'ler
        referential/atomic validity ÅŸartÄ±nÄ± mutlaka karÅŸÄ±lamalÄ±dÄ±r.
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
    "yeni bir epistemik kategori oluÅŸturmaz",
    "yeni bir bilgi statÃ¼sÃ¼ oluÅŸturmaz",
    "yeni bir gÃ¼ven/confidence deÄŸeri oluÅŸturmaz",
    "eksik state'i otomatik olarak silmez",
    "eksik state'i otomatik olarak reddedilmiÅŸ bilgi haline getirmez",
    "geÃ§miÅŸ state'i deÄŸiÅŸtirmez",
    "sonradan oluÅŸan referanslarÄ± geÃ§miÅŸ state'e sessizce enjekte etmez",
    "tamamlanmÄ±ÅŸ state'in sessizce deÄŸiÅŸtirilmesine izin vermez",
    "duplicate entity_id ile mevcut state'in Ã¼zerine yazÄ±lmasÄ±na izin vermez",
)




def referential_atomic_validity_rule() -> str:
    return (
        "Gerekli trace/reference baÄŸlantÄ±larÄ± tamamlanmamÄ±ÅŸ bir "
        "Finding, Synthesis, Historical Snapshot veya Relationship "
        "sistemde geÃ§ici/incomplete state olarak bulunabilir; ancak "
        "gerekli referanslarÄ± gerÃ§ekten mevcut ve geÃ§erli olmadan "
        "tamamlanmÄ±ÅŸ/geÃ§erli Ã§Ä±ktÄ± olarak kabul edilemez."
    )




# ============================================================
# 9. TEKNÄ°K MÄ°MARÄ° FÄ°NAL DURUMU
# ============================================================


TECHNICAL_ARCHITECTURE_FINAL_STATUS = (
    "LOCKED"
)


TECHNICAL_ARCHITECTURE_FINAL_DECISION = (
    "11. BÃ–LÃœM LOCKED. Referential / Atomic Validity, "
    "11. BÃ¶lÃ¼mÃ¼n teknik bÃ¼tÃ¼nlÃ¼k sÃ¶zleÅŸmesinin zorunlu parÃ§asÄ±dÄ±r. "
    "Sekiz teknik mimari kontrolÃ¼n tamamÄ±nda aktif bir kavramsal "
    "boÅŸluk bulunmamaktadÄ±r."
)




# ============================================================
# 10. FINAL VALIDATION
# ============================================================


def validate_11() -> None:
    """
    11. BÃ¶lÃ¼m final self-validation.


    Kontroller:


    1. Tam 8 teknik mimari bulgu.
    2. q1â€“q7 + q8 eksiksiz.
    3. Duplicate finding ID yok.
    4. TÃ¼m bulgular A_NO_ISSUE.
    5. B/C/D bulgusu yok.
    6. Referential / Atomic Validity aktif.
    7. GerÃ§ek referans olmadan completed state oluÅŸamÄ±yor.
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
        "11. BÃ¶lÃ¼m tam olarak 8 teknik mimari bulgu iÃ§ermelidir."
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
        "11. BÃ¶lÃ¼m finding ID seti hatalÄ±."
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
        "Final LOCKED durumda bÃ¼tÃ¼n teknik mimari bulgular "
        "A_NO_ISSUE olmalÄ±dÄ±r."
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
    assert "tamamlanmÄ±ÅŸ/geÃ§erli Ã§Ä±ktÄ±" in rule


    assert len(
        REFERENTIAL_ATOMIC_VALIDITY_CONSTRAINTS
    ) >= 8


    # --------------------------------------------------------
    # Enforcer
    # --------------------------------------------------------


    enforcer = TechnicalArchitectureEnforcer()


    # GerÃ§ek referanslar.
    enforcer.register_reference(
        "ref.finding.001",
        "FINDING",
    )


    enforcer.register_reference(
        "ref.source.001",
        "SOURCE",
    )


    # --------------------------------------------------------
    # Eksik referanslÄ± state:
    # completed talebi verilse bile incomplete kalmalÄ±.
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
    # GerÃ§ek referanslarÄ± olan state completed olabilir.
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
            "Technical state sessizce gÃ¼ncellenebildi."
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
    "11. BÃ¶lÃ¼m â€” Teknik Mimari; 1â€“10 arasÄ±nda tanÄ±mlanan "
    "provenance, point-in-time, information status, causality, "
    "bounded context ve read/write authority sÄ±nÄ±rlarÄ±nÄ± teknik "
    "bÃ¼tÃ¼nlÃ¼k sÃ¶zleÅŸmesine taÅŸÄ±r. Referential / Atomic Validity "
    "kuralÄ± sayesinde Finding, Synthesis, Historical Snapshot veya "
    "Relationship gibi tamamlanmÄ±ÅŸ Ã§Ä±ktÄ±lar zorunlu trace/reference "
    "baÄŸlantÄ±larÄ± gerÃ§ekten mevcut olmadan geÃ§erli kabul edilmez. "
    "Eksik state geÃ§ici/incomplete olarak tutulabilir; ancak "
    "sessizce completed hale getirilemez, geÃ§miÅŸ state deÄŸiÅŸtirilemez "
    "ve mevcut entity Ã¼zerine yazÄ±lamaz. Bu katman yeni epistemik "
    "kategori, confidence, reliability, weighting, ranking veya "
    "karar mekanizmasÄ± Ã¼retmez."
)




# ============================================================
# 12. MODULE ENTRY
# ============================================================


if __name__ == "__main__":


    validate_11()


    print(
        "11. BÃ–LÃœM â€” TEKNÄ°K MÄ°MARÄ°"
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
        "READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ"
    )


    print(
        "=" * 72
    )


    print(
        "Validation: OK"
    )
