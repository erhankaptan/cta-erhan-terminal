11. BÖLÜM — TEKNİK MİMARİ
FINAL KİLİTLEME


Teknik mimari sözleşmesi:


1. Historical Snapshot zamanı ayrıdır.
2. Publication / Access / Ingestion ayrıdır.
3. Provenance Root / Path / Independence ayrıdır.
4. Information Piece zorunlu canonicalization ile ezilmez.
5. Information Status 5. Bölümden gelir ve teknik katman tarafından
   sessizce değiştirilemez.
6. Kaynak nedensellik iddiası ile sistemin kendi nedensellik hükmü ayrıdır.
7. Bounded Context / Read-Write Authority mantıksal olarak korunur.
8. Referential / Atomic Validity tamamlanmış state için zorunludur.


REFERENTIAL / ATOMIC VALIDITY:


Gerekli trace/reference bağlantıları tamamlanmamış bir
Finding, Synthesis, Historical Snapshot veya Relationship
sistemde geçici/incomplete state olarak bulunabilir.


Ancak gerekli referansları gerçekten mevcut ve geçerli olmadan
tamamlanmış/geçerli çıktı olarak kabul edilemez.


Eksik state:
    - silinmez,
    - otomatik reddedilmez,
    - geçmiş state'i değiştirmez,
    - sonradan oluşan bilgiyi geçmişe sessizce enjekte etmez.


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable




# ============================================================
# 1. TEKNİK MİMARİ SINIFLANDIRMASI
# ============================================================


class TechnicalArchitectureClass(str, Enum):
    """
    Teknik mimari sorgu sınıflandırması.


    A: Problem yok.
    B: Minimum düzeltme gerekli.
    C: Kavramsal sınır belirsiz.
    D: Kapsam dışı.
    """


    A_NO_ISSUE = "A"
    B_FIX_REQUIRED = "B"
    C_BOUNDARY_UNCLEAR = "C"
    D_OUT_OF_SCOPE = "D"




# ============================================================
# 2. TEKNİK MİMARİ BULGUSU
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
# 3. 11. BÖLÜMÜN 8 KİLİTLİ BULGUSU
# ============================================================


TECHNICAL_ARCHITECTURE_FINDINGS: tuple[
    TechnicalArchitectureFinding,
    ...,
] = (


    # --------------------------------------------------------
    # Q1 — HISTORICAL SNAPSHOT ZAMANI
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q1",
        title="Historical Snapshot Zamanı",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Production, access, ingestion, event, reference, revision "
            "ve snapshot zamanlarının semantik olarak ayrılması "
            "point-in-time bütünlüğü ve hindsight contamination'ın "
            "önlenmesi için yeterlidir. as_of_time / snapshot_time, "
            "sistemin temsil ettiği historical state'in zaman sınırıdır. "
            "Production time bunun yerine geçirilemez."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q2 — PUBLICATION / ACCESS / INGESTION
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q2",
        title="Publication / Access / Ingestion",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Publication, access ve ingestion farklı olaylardır. "
            "Fiziksel olarak aynı yapıda tutulabilmeleri semantik "
            "ayrımı ortadan kaldırmaz. Bir yayına tekrar erişilmesi "
            "durumunda publication kimliği ve provenance korunabildiği "
            "sürece point-in-time ve provenance bütünlüğü korunur."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q3 — PROVENANCE ROOT / INDEPENDENCE
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q3",
        title="Provenance Root ve Independence",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "provenance_root, provenance_path ve independent_path "
            "farklı kavramlardır. Farklı provenance_root_id değerleri "
            "otomatik olarak bağımsız kanıt anlamına gelmez. Bu ayrım "
            "false independence ve yanlış consensus üretimini engeller."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q4 — DEDUPLICATION / CANONICALIZATION
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q4",
        title="Information Piece Deduplication / Canonicalization",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Zorunlu tekilleştirme veya canonicalization dayatılmaması, "
            "Information Piece'in provenance, context, publication/access "
            "geçmişi, zaman ve anlamlı farklılıklarının korunmasını sağlar. "
            "Aynı kökten gelen kayıtların bağımsız kanıt gibi görünmemesi "
            "ise 4–7'deki provenance ve independence sınırlarıyla korunur."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q5 — INFORMATION STATUS
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q5",
        title="Information Status Sınırı",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Teknik enum veya schema değişikliği tek başına yeni "
            "epistemik kategori yaratamaz. Status kavramının kaynağı "
            "5. Bölümdeki kavramsal tanımdır. 11. Bölüm bunu değiştiremez "
            "ve mevcut status'ları teknik sebeple sessizce dönüştüremez."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q6 — CAUSALITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q6",
        title="Causality Sınırı",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Kaynağın yayınladığı nedensellik iddiasının saklanması ile "
            "sistemin kendi nedensellik hükmünü üretmesi birbirinden "
            "ayrılmıştır. Kaynak iddiası, ERHAN tarafından üretilmiş "
            "nedensellik hükmü değildir."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q7 — BOUNDED CONTEXT / READ-WRITE AUTHORITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q7",
        title="Bounded Context / Read-Write Authority",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "6, 7 ve 8'in fiziksel olarak ayrı servisler olması zorunlu "
            "değildir. Logical boundary, read/write authority, output "
            "contract, immutable veya versioned input, traceability ve "
            "sessiz mutation'ın engellenmesi yeterli teknik sınırları "
            "oluşturur. Fiziksel ayrım 12. Kodlama aşamasına bırakılır."
        ),


        relation_to_1_10="Çelişmiyor.",


        minimum_fix=None,
    ),


    # --------------------------------------------------------
    # Q8 — REFERENTIAL / ATOMIC VALIDITY
    # --------------------------------------------------------


    TechnicalArchitectureFinding(
        finding_id="q8",
        title="Referential / Atomic Validity",
        classification=TechnicalArchitectureClass.A_NO_ISSUE,


        problem=None,


        technical_importance=(
            "Tamamlanmış Finding, Synthesis, Historical Snapshot veya "
            "Relationship; kendisini oluşturan zorunlu trace/reference "
            "bağlantıları gerçekten mevcut ve geçerli olmadan "
            "tamamlanmış/geçerli çıktı olarak kabul edilemez. Eksik "
            "referanslı state geçici/incomplete olarak bulunabilir. "
            "Bu kural provenance, traceability ve point-in-time "
            "bütünlüğünü teknik sözleşmede korur."
        ),


        relation_to_1_10=(
            "Çelişmiyor. Aksine 5–10'daki provenance, traceability, "
            "point-in-time ve 7→8 sınırlarını teknik bütünlük kuralı "
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
    Referential / Atomic Validity kapsamında kontrol edilen
    tamamlanmış state türleri.
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
    Bir teknik state'in referans bütünlüğü sözleşmesi.


    required_references:
        State'in tamamlanabilmesi için bulunması gereken referans ID'leri.


    is_completed:
        State'in tamamlanmış/geçerli çıktı olarak işaretlenip
        işaretlenmediği.


    ÖNEMLİ:
        Bu sınıf referansların yalnızca dolu string olmasını değil,
        Enforcer içindeki gerçek reference registry'de bulunmasını
        kontrol eder.
    """


    entity_type: TechnicalEntityType
    entity_id: str
    required_references: tuple[str, ...]
    is_completed: bool = False


    def has_required_reference_ids(self) -> bool:
        """
        Referans listesinin biçimsel bütünlüğü.


        Boş ID veya whitespace-only ID kabul edilmez.
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
    Teknik referans registry kaydı.


    Reference'ın gerçekten mevcut olduğunu temsil eder.
    """


    reference_id: str
    reference_type: str




# ============================================================
# 7. TEKNİK MİMARİ ENFORCER
# ============================================================


class TechnicalArchitectureEnforcer:
    """
    11. Bölüm — Teknik Mimari Bütünlük ve Doğrulama Motoru.


    Denetlediği sınırlar:


    - point-in-time ayrımı,
    - publication/access/ingestion ayrımı,
    - provenance ayrımı,
    - reference bütünlüğü,
    - completed/incomplete state ayrımı,
    - duplicate entity engeli,
    - sessiz mutation engeli.


    Bu motor:


    - epistemik skor üretmez,
    - confidence üretmez,
    - reliability üretmez,
    - weighting üretmez,
    - ranking üretmez,
    - karar üretmez,
    - trade sinyali üretmez.
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
        Gerçek bir teknik referans kaydeder.


        Aynı reference_id ikinci kez kaydedilemez.
        """


        if not isinstance(reference_id, str):
            raise TypeError(
                "reference_id string olmalıdır."
            )


        normalized_id = reference_id.strip()


        if not normalized_id:
            raise ValueError(
                "reference_id boş olamaz."
            )


        if normalized_id in self._references:
            raise ValueError(
                "Duplicate technical reference_id: "
                f"{normalized_id}"
            )


        if not reference_type.strip():
            raise ValueError(
                "reference_type boş olamaz."
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


        Completed state için iki koşul zorunludur:


        1. Referans ID'leri biçimsel olarak geçerli olmalı.
        2. Her zorunlu referans registry'de gerçekten bulunmalı.


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
                "entity_type TechnicalEntityType olmalıdır."
            )


        if not isinstance(entity_id, str):
            raise TypeError(
                "entity_id string olmalıdır."
            )


        normalized_entity_id = entity_id.strip()


        if not normalized_entity_id:
            raise ValueError(
                "entity_id boş olamaz."
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
        # Completed talebi yalnızca gerçek referanslar mevcutsa
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
                f"Technical state bulunamadı: {normalized_id}"
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
    # SILENT MUTATION ENGELİ
    # ========================================================


    def update_entity_state(
        self,
        entity_id: str,
        *,
        references: Iterable[str] | None = None,
        mark_completed: bool | None = None,
    ) -> None:
        """
        Mevcut state'in sessiz mutation'ını engeller.


        11. Bölüm append-only / immutable boundary nedeniyle
        mevcut state doğrudan güncellenemez.


        Yeni bir state gerekiyorsa yeni entity/version ID'si
        ile yeni historical layer oluşturulmalıdır.
        """


        raise RuntimeError(
            "Technical state sessizce güncellenemez. "
            "Yeni state/version oluşturulmalıdır."
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
    # BÜTÜNLÜK KONTROLÜ
    # ========================================================


    def validate_all_contracts(
        self,
    ) -> bool:
        """
        Registry'deki tüm contract'ların bütünlüğünü kontrol eder.


        Incomplete state'ler geçerlidir; ancak completed state'ler
        referential/atomic validity şartını mutlaka karşılamalıdır.
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
    "yeni bir epistemik kategori oluşturmaz",
    "yeni bir bilgi statüsü oluşturmaz",
    "yeni bir güven/confidence değeri oluşturmaz",
    "eksik state'i otomatik olarak silmez",
    "eksik state'i otomatik olarak reddedilmiş bilgi haline getirmez",
    "geçmiş state'i değiştirmez",
    "sonradan oluşan referansları geçmiş state'e sessizce enjekte etmez",
    "tamamlanmış state'in sessizce değiştirilmesine izin vermez",
    "duplicate entity_id ile mevcut state'in üzerine yazılmasına izin vermez",
)




def referential_atomic_validity_rule() -> str:
    return (
        "Gerekli trace/reference bağlantıları tamamlanmamış bir "
        "Finding, Synthesis, Historical Snapshot veya Relationship "
        "sistemde geçici/incomplete state olarak bulunabilir; ancak "
        "gerekli referansları gerçekten mevcut ve geçerli olmadan "
        "tamamlanmış/geçerli çıktı olarak kabul edilemez."
    )




# ============================================================
# 9. TEKNİK MİMARİ FİNAL DURUMU
# ============================================================


TECHNICAL_ARCHITECTURE_FINAL_STATUS = (
    "LOCKED"
)


TECHNICAL_ARCHITECTURE_FINAL_DECISION = (
    "11. BÖLÜM LOCKED. Referential / Atomic Validity, "
    "11. Bölümün teknik bütünlük sözleşmesinin zorunlu parçasıdır. "
    "Sekiz teknik mimari kontrolün tamamında aktif bir kavramsal "
    "boşluk bulunmamaktadır."
)




# ============================================================
# 10. FINAL VALIDATION
# ============================================================


def validate_11() -> None:
    """
    11. Bölüm final self-validation.


    Kontroller:


    1. Tam 8 teknik mimari bulgu.
    2. q1–q7 + q8 eksiksiz.
    3. Duplicate finding ID yok.
    4. Tüm bulgular A_NO_ISSUE.
    5. B/C/D bulgusu yok.
    6. Referential / Atomic Validity aktif.
    7. Gerçek referans olmadan completed state oluşamıyor.
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
        "11. Bölüm tam olarak 8 teknik mimari bulgu içermelidir."
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
        "11. Bölüm finding ID seti hatalı."
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
        "Final LOCKED durumda bütün teknik mimari bulgular "
        "A_NO_ISSUE olmalıdır."
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
    assert "tamamlanmış/geçerli çıktı" in rule


    assert len(
        REFERENTIAL_ATOMIC_VALIDITY_CONSTRAINTS
    ) >= 8


    # --------------------------------------------------------
    # Enforcer
    # --------------------------------------------------------


    enforcer = TechnicalArchitectureEnforcer()


    # Gerçek referanslar.
    enforcer.register_reference(
        "ref.finding.001",
        "FINDING",
    )


    enforcer.register_reference(
        "ref.source.001",
        "SOURCE",
    )


    # --------------------------------------------------------
    # Eksik referanslı state:
    # completed talebi verilse bile incomplete kalmalı.
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
    # Gerçek referansları olan state completed olabilir.
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
            "Technical state sessizce güncellenebildi."
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
    "11. Bölüm — Teknik Mimari; 1–10 arasında tanımlanan "
    "provenance, point-in-time, information status, causality, "
    "bounded context ve read/write authority sınırlarını teknik "
    "bütünlük sözleşmesine taşır. Referential / Atomic Validity "
    "kuralı sayesinde Finding, Synthesis, Historical Snapshot veya "
    "Relationship gibi tamamlanmış çıktılar zorunlu trace/reference "
    "bağlantıları gerçekten mevcut olmadan geçerli kabul edilmez. "
    "Eksik state geçici/incomplete olarak tutulabilir; ancak "
    "sessizce completed hale getirilemez, geçmiş state değiştirilemez "
    "ve mevcut entity üzerine yazılamaz. Bu katman yeni epistemik "
    "kategori, confidence, reliability, weighting, ranking veya "
    "karar mekanizması üretmez."
)




# ============================================================
# 12. MODULE ENTRY
# ============================================================


if __name__ == "__main__":


    validate_11()


    print(
        "11. BÖLÜM — TEKNİK MİMARİ"
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
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "=" * 72
    )


    print(
        "Validation: OK"
    )
