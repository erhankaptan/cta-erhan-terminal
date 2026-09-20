FINAL KOD


7. BÃ¶lÃ¼m tarafÄ±ndan ortaya konmuÅŸ analitik bulgularÄ± ve iliÅŸkileri,
zaman, kapsam, aktÃ¶r, bilgi statÃ¼sÃ¼, provenance ve baÄŸlam farklÄ±lÄ±klarÄ±nÄ±
koruyarak birlikte deÄŸerlendirir ve koÅŸullu, baÄŸlamsal bir CTA tablosu
oluÅŸturur.


8. BÃ¶lÃ¼m:
- yeni veri Ã¼retmez,
- yeni baÄŸÄ±msÄ±z kanÄ±t Ã¼retmez,
- 7. BÃ¶lÃ¼mde yapÄ±lmamÄ±ÅŸ yeni analiz Ã¼retmez,
- 7. BÃ¶lÃ¼m Ã¶lÃ§Ã¼mlerini yeniden hesaplamaz,
- 7. BÃ¶lÃ¼mÃ¼n yerine geÃ§mez,
- nihai CTA yÃ¶nÃ¼ veya karar Ã¼retmez.


READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ
"""


from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Optional, Sequence




# ============================================================
# 1. SYNTHESIS DURUMU
# ============================================================


class SynthesisState(str, Enum):
    """
    8. BÃ¶lÃ¼m synthesis durumlarÄ±.


    SUCCESSFUL:
        Birden fazla 7. BÃ¶lÃ¼m bulgusu arasÄ±nda anlamlÄ± Ã¼st dÃ¼zey
        baÄŸ kurulmuÅŸ ve kritik baÄŸlamsal farklÄ±lÄ±klar korunmuÅŸtur.


    PARTIAL:
        BazÄ± bulgular anlamlÄ± biÃ§imde birleÅŸtirilebilmiÅŸ, ancak
        bazÄ± kritik alanlar aÃ§Ä±k / belirsiz / Ã§Ã¶zÃ¼mlenmemiÅŸ kalmÄ±ÅŸtÄ±r.


    FAILURE:
        Gerekli 7. BÃ¶lÃ¼m referanslarÄ± veya anlamlÄ± iliÅŸki yapÄ±sÄ±
        bulunmadÄ±ÄŸÄ±ndan aÃ§Ä±klanabilir bir Ã¼st dÃ¼zey synthesis
        kurulamaz.
    """


    SUCCESSFUL = "successful"
    PARTIAL = "partial"
    FAILURE = "failure"




# ============================================================
# 2. SYNTHESIS KAVRAMLARI
# ============================================================


class SynthesisConcept(str, Enum):
    """
    8. BÃ¶lÃ¼mÃ¼n temel synthesis sÃ¶zlÃ¼ÄŸÃ¼.


    HARMONY_AUXILIARY yalnÄ±zca yardÄ±mcÄ± aÃ§Ä±klama kavramÄ±dÄ±r.
    AyrÄ± bir temel synthesis iliÅŸkisi deÄŸildir.


    SUPPORT Ã¶zellikle kavramsal temel iliÅŸki olarak bulunmaz.
    """


    CONVERGENCE = "convergence"
    COMPLEMENTARITY = "complementarity"
    LIMITATION = "limitation"
    CONDITIONALITY = "conditionality"
    DIVERGENCE = "divergence"
    CONTRADICTION = "contradiction"
    UNCERTAINTY = "uncertainty"
    HARMONY_AUXILIARY = "harmony_auxiliary"




# ============================================================
# 3. 7 â†’ 8 REFERANS TÃœRÃœ
# ============================================================


class Section7ReferenceType(str, Enum):
    """
    8'in dayandÄ±ÄŸÄ± 7. BÃ¶lÃ¼m Ã§Ä±ktÄ±sÄ±nÄ±n tÃ¼rÃ¼nÃ¼ aÃ§Ä±kÃ§a belirtir.
    """


    FINDING = "finding"
    RELATION_ANALYSIS = "relation_analysis"
    STRUCTURAL_MEASUREMENT = "structural_measurement"
    PROVENANCE_ANALYSIS = "provenance_analysis"
    UNCERTAINTY_ANALYSIS = "uncertainty_analysis"




# ============================================================
# 4. 7. BÃ–LÃœM REFERANS KAYDI
# ============================================================


@dataclass(frozen=True)
class Section7Reference:
    """
    8. BÃ¶lÃ¼m synthesis'inin 7. BÃ¶lÃ¼mdeki gerÃ§ek kaynaÄŸÄ±.


    Bu nesne yeni analiz Ã¼retmez.
    YalnÄ±zca 7. BÃ¶lÃ¼mden gelen mevcut Ã§Ä±ktÄ±nÄ±n kimliÄŸini taÅŸÄ±r.
    """


    reference_id: str
    reference_type: Section7ReferenceType


    # Ä°lgili 7 Ã§Ä±ktÄ±sÄ±nÄ±n gerÃ§ek kimliÄŸi.
    source_output_id: str


    # Ä°steÄŸe baÄŸlÄ± cluster bilgisi.
    # Cluster ID hiÃ§bir zaman source_output_id yerine geÃ§mez.
    cluster_id: Optional[str] = None


    # 7 Ã§Ä±ktÄ±sÄ±nÄ±n mevcut aÃ§Ä±klamasÄ±.
    description: Optional[str] = None




# ============================================================
# 5. BAÄžLAMSAL KORUMA
# ============================================================


@dataclass(frozen=True)
class SynthesisContext:
    """
    8. BÃ¶lÃ¼mÃ¼n synthesis sÄ±rasÄ±nda korumak zorunda olduÄŸu baÄŸlam.


    Buradaki alanlar yeni analiz sonucu deÄŸildir.
    7. BÃ¶lÃ¼mden taÅŸÄ±nan / 7 Ã§Ä±ktÄ±sÄ±nda mevcut olan baÄŸlamsal
    farklÄ±lÄ±klarÄ±n korunmasÄ± iÃ§indir.
    """


    time_horizons: tuple[str, ...] = field(default_factory=tuple)
    actors: tuple[str, ...] = field(default_factory=tuple)
    information_statuses: tuple[str, ...] = field(default_factory=tuple)
    scopes: tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: tuple[str, ...] = field(default_factory=tuple)
    contexts: tuple[str, ...] = field(default_factory=tuple)


    # Synthesis sÄ±rasÄ±nda bu ayrÄ±mlarÄ±n korunmasÄ± zorunludur.
    preserve_time_horizons: bool = True
    preserve_actors: bool = True
    preserve_information_statuses: bool = True
    preserve_scopes: bool = True
    preserve_provenance: bool = True
    preserve_contexts: bool = True




# ============================================================
# 6. SYNTHESIS STATEMENT
# ============================================================


@dataclass(frozen=True)
class SynthesisStatement:
    """
    Tek bir Ã¼st dÃ¼zey synthesis ifadesi.


    statement:
        7. BÃ¶lÃ¼m bulgularÄ±nÄ±n birlikte ifade edilen Ã¼st dÃ¼zey anlamÄ±.


    source_finding_ids:
        Synthesis'in dayandÄ±ÄŸÄ± gerÃ§ek 7. BÃ¶lÃ¼m Ã§Ä±ktÄ± ID'leri.


    source_relation_ids:
        7. BÃ¶lÃ¼m tarafÄ±ndan kurulmuÅŸ / analiz edilmiÅŸ iliÅŸki ID'leri.


    used_concepts:
        8. BÃ¶lÃ¼mde kullanÄ±lan synthesis kavramlarÄ±.


    context:
        Zaman, aktÃ¶r, statÃ¼, kapsam, provenance ve baÄŸlam korunumu.


    Ã–NEMLÄ°:
        Bu sÄ±nÄ±f yeni veri veya yeni baÄŸÄ±msÄ±z kanÄ±t taÅŸÄ±maz.
    """


    statement_id: str
    statement: str


    source_finding_ids: tuple[str, ...]
    source_relation_ids: tuple[str, ...] = field(default_factory=tuple)


    used_concepts: tuple[SynthesisConcept, ...] = field(
        default_factory=tuple
    )


    context: SynthesisContext = field(
        default_factory=SynthesisContext
    )


    note: Optional[str] = None




# ============================================================
# 7. SYNTHESIS OUTPUT
# ============================================================


@dataclass(frozen=True)
class SynthesisOutput:
    """
    8. BÃ¶lÃ¼mÃ¼n tamamlanmÄ±ÅŸ synthesis Ã§Ä±ktÄ±sÄ±.


    Bu Ã§Ä±ktÄ±:
    - yeni veri deÄŸildir,
    - yeni baÄŸÄ±msÄ±z kanÄ±t deÄŸildir,
    - yeni analiz deÄŸildir,
    - trade/risk/position kararÄ± deÄŸildir.


    TamamlanmÄ±ÅŸ output'un geÃ§erli olabilmesi iÃ§in:
    - en az bir gerÃ§ek 7 referansÄ±,
    - gerekli iliÅŸki referanslarÄ±,
    - baÄŸlamsal koruma
    bulunmalÄ±dÄ±r.
    """


    synthesis_id: str
    cluster_id: Optional[str]


    synthesis_state: SynthesisState


    statements: tuple[SynthesisStatement, ...]


    connected_7_references: tuple[Section7Reference, ...]


    preserved_context: SynthesisContext


    # TamamlanmÄ±ÅŸ Ã§Ä±ktÄ±nÄ±n referans bÃ¼tÃ¼nlÃ¼ÄŸÃ¼.
    valid: bool = False


    # Ä°nsan tarafÄ±ndan kontrol edilmesi gereken aÃ§Ä±klamalar.
    unresolved_items: tuple[str, ...] = field(default_factory=tuple)




# ============================================================
# 8. YASAKLI 8. BÃ–LÃœM Ã‡IKTILARI
# ============================================================


FORBIDDEN_SYNTHESIS_OUTPUTS = frozenset(
    {
        "new_fact",
        "new_data",
        "new_independent_evidence",
        "causality",
        "actor_intent",
        "evidence_strength",
        "reliability_verdict",
        "confidence",
        "confidence_score",
        "probability",
        "prediction",
        "future_prediction",
        "trade_decision",
        "risk_decision",
        "position_decision",
        "investment_advice",
        "bullish_verdict",
        "bearish_verdict",
        "final_direction_verdict",
        "final_bias",
        "BUY",
        "SELL",
        "LONG",
        "SHORT",
        "signal",
        "weight",
        "weighting",
        "ranking",
        "score",
        "priority_score",
    }
)




# ============================================================
# 9. 7 â†’ 8 REFERANS KAYDI
# ============================================================


class Section7ReferenceRegistry:
    """
    7. BÃ¶lÃ¼m Ã§Ä±ktÄ±larÄ±nÄ±n yalnÄ±zca referans amaÃ§lÄ± kayÄ±t defteri.


    8 burada analiz yapmaz.
    7 Ã§Ä±ktÄ±sÄ±nÄ± deÄŸiÅŸtirmez.
    7 Ã§Ä±ktÄ±sÄ±nÄ± yeniden hesaplamaz.
    """


    def __init__(self) -> None:
        self._references: dict[str, Section7Reference] = {}


    def register(self, reference: Section7Reference) -> None:
        if not reference.reference_id:
            raise ValueError("7 referansÄ± boÅŸ olamaz.")


        if not reference.source_output_id:
            raise ValueError(
                "7 referansÄ±nÄ±n source_output_id alanÄ± zorunludur."
            )


        if reference.reference_id in self._references:
            raise ValueError(
                f"7 referansÄ± zaten kayÄ±tlÄ±: {reference.reference_id}"
            )


        self._references[reference.reference_id] = reference


    def exists(self, reference_id: str) -> bool:
        return reference_id in self._references


    def get(self, reference_id: str) -> Section7Reference:
        try:
            return self._references[reference_id]
        except KeyError as exc:
            raise KeyError(
                f"7 BÃ¶lÃ¼m referansÄ± bulunamadÄ±: {reference_id}"
            ) from exc


    def all(self) -> tuple[Section7Reference, ...]:
        return tuple(self._references.values())




# ============================================================
# 10. 7 Ã‡IKTISINDAN REFERANS ÃœRETME ADAPTÃ–RÃœ
# ============================================================


def _extract_output_id(obj: object) -> Optional[str]:
    """
    7. BÃ¶lÃ¼mdeki farklÄ± Ã§Ä±ktÄ± nesnelerinin ID alanÄ±nÄ± gÃ¼venli ÅŸekilde
    okur.


    Desteklenen alanlar:
    - finding_id
    - analysis_id
    - measurement_id


    Bu fonksiyon yeni ID Ã¼retmez.
    """


    for attribute in (
        "finding_id",
        "analysis_id",
        "measurement_id",
    ):
        value = getattr(obj, attribute, None)


        if isinstance(value, str) and value:
            return value


    return None




def build_section7_reference(
    obj: object,
    reference_type: Section7ReferenceType,
    cluster_id: Optional[str] = None,
    description: Optional[str] = None,
) -> Section7Reference:
    """
    Mevcut 7. BÃ¶lÃ¼m Ã§Ä±ktÄ±sÄ±ndan yalnÄ±zca referans oluÅŸturur.


    7 Ã§Ä±ktÄ±sÄ±nÄ± deÄŸiÅŸtirmez ve yeniden analiz etmez.
    """


    output_id = _extract_output_id(obj)


    if not output_id:
        raise ValueError(
            "7. BÃ¶lÃ¼m Ã§Ä±ktÄ±sÄ±nda geÃ§erli bir Ã§Ä±ktÄ± ID'si bulunamadÄ±."
        )


    return Section7Reference(
        reference_id=output_id,
        reference_type=reference_type,
        source_output_id=output_id,
        cluster_id=cluster_id,
        description=description,
    )




# ============================================================
# 11. REFERANS BÃœTÃœNLÃœÄžÃœ
# ============================================================


def validate_statement_traceability(
    statement: SynthesisStatement,
    registry: Section7ReferenceRegistry,
) -> None:
    """
    TamamlanmÄ±ÅŸ synthesis statement'Ä±nÄ±n 7'ye geri izlenebilirliÄŸini
    kontrol eder.
    """


    if not statement.statement_id:
        raise ValueError("Synthesis statement ID boÅŸ olamaz.")


    if not statement.statement.strip():
        raise ValueError(
            f"Synthesis statement boÅŸ olamaz: {statement.statement_id}"
        )


    if not statement.source_finding_ids:
        raise ValueError(
            "Synthesis statement en az bir 7. BÃ¶lÃ¼m bulgusuna "
            "geri izlenebilir olmalÄ±dÄ±r: "
            f"{statement.statement_id}"
        )


    for finding_id in statement.source_finding_ids:
        if not registry.exists(finding_id):
            raise ValueError(
                "Synthesis statement'Ä±n referans verdiÄŸi 7 Ã§Ä±ktÄ±sÄ± "
                f"bulunamadÄ±: {finding_id}"
            )


    for relation_id in statement.source_relation_ids:
        if not registry.exists(relation_id):
            raise ValueError(
                "Synthesis statement'Ä±n referans verdiÄŸi 7 iliÅŸkisi "
                f"bulunamadÄ±: {relation_id}"
            )


    if not statement.context.preserve_time_horizons:
        raise ValueError(
            "Zaman ufku korunumu kapatÄ±lamaz."
        )


    if not statement.context.preserve_actors:
        raise ValueError(
            "AktÃ¶r ayrÄ±mÄ± korunumu kapatÄ±lamaz."
        )


    if not statement.context.preserve_information_statuses:
        raise ValueError(
            "Bilgi statÃ¼sÃ¼ korunumu kapatÄ±lamaz."
        )


    if not statement.context.preserve_scopes:
        raise ValueError(
            "Kapsam korunumu kapatÄ±lamaz."
        )


    if not statement.context.preserve_provenance:
        raise ValueError(
            "Provenance korunumu kapatÄ±lamaz."
        )


    if not statement.context.preserve_contexts:
        raise ValueError(
            "BaÄŸlam korunumu kapatÄ±lamaz."
        )




# ============================================================
# 12. SYNTHESIS DURUMU DEÄžERLENDÄ°RME SINIRI
# ============================================================


def determine_synthesis_state(
    statements: Sequence[SynthesisStatement],
    unresolved_items: Sequence[str],
) -> SynthesisState:
    """
    Synthesis durumunu deÄŸerlendirir.


    Ã–NEMLÄ°:
    Bu fonksiyon 7. BÃ¶lÃ¼mde yeni analiz yapmaz.


    YalnÄ±zca 8'e verilmiÅŸ synthesis yapÄ±sÄ±nÄ±n:
    - referans iÃ§erip iÃ§ermediÄŸine,
    - kÄ±smi / Ã§Ã¶zÃ¼mlenmemiÅŸ alan bulunup bulunmadÄ±ÄŸÄ±na
    bakar.


    Ã‡eliÅŸki veya belirsizlik tek baÅŸÄ±na FAILURE deÄŸildir.
    """


    if not statements:
        return SynthesisState.FAILURE


    if any(
        not statement.source_finding_ids
        for statement in statements
    ):
        return SynthesisState.FAILURE


    if unresolved_items:
        return SynthesisState.PARTIAL


    return SynthesisState.SUCCESSFUL




# ============================================================
# 13. CONTEXT BÃœTÃœNLÃœÄžÃœ
# ============================================================


def validate_synthesis_context(
    context: SynthesisContext,
) -> None:
    """
    Synthesis context'in temel korunma kurallarÄ±nÄ± doÄŸrular.
    """


    required_flags = (
        context.preserve_time_horizons,
        context.preserve_actors,
        context.preserve_information_statuses,
        context.preserve_scopes,
        context.preserve_provenance,
        context.preserve_contexts,
    )


    if not all(required_flags):
        raise ValueError(
            "8. BÃ¶lÃ¼m synthesis context koruma sÄ±nÄ±rlarÄ±ndan "
            "biri kapatÄ±lmÄ±ÅŸ."
        )




# ============================================================
# 14. SYNTHESIS MOTORU
# ============================================================


class CTASynthesisEngine:
    """
    8. BÃ¶lÃ¼m â€” CTA Synthesis / SonuÃ§ Motoru.


    GÃ¶rev:
        7. BÃ¶lÃ¼mÃ¼n mevcut analitik Ã§Ä±ktÄ±larÄ±nÄ±n Ã¼st dÃ¼zey
        baÄŸlamsal sentezini taÅŸÄ±mak.


    Yapmaz:
        - yeni analiz,
        - yeni Ã¶lÃ§Ã¼m,
        - yeni veri,
        - yeni baÄŸÄ±msÄ±z kanÄ±t,
        - causality,
        - actor intent,
        - confidence,
        - reliability,
        - evidence strength,
        - weighting,
        - ranking,
        - probability,
        - prediction,
        - trade,
        - risk,
        - final bias.


    Motor yalnÄ±zca:
        7 â†’ 8 referans zincirini,
        synthesis ifadelerini,
        synthesis kavramlarÄ±nÄ±,
        baÄŸlamsal korumayÄ±
        yÃ¶netir.
    """


    def __init__(
        self,
        section7_registry: Section7ReferenceRegistry,
    ) -> None:
        self._registry = section7_registry
        self._outputs: list[SynthesisOutput] = []


    # --------------------------------------------------------
    # READ-ONLY ACCESS
    # --------------------------------------------------------


    def section7_references(
        self,
    ) -> tuple[Section7Reference, ...]:
        return self._registry.all()


    def outputs(self) -> tuple[SynthesisOutput, ...]:
        return tuple(self._outputs)


    # --------------------------------------------------------
    # STATEMENT VALIDATION
    # --------------------------------------------------------


    def validate_statement(
        self,
        statement: SynthesisStatement,
    ) -> None:
        validate_statement_traceability(
            statement,
            self._registry,
        )


    # --------------------------------------------------------
    # SYNTHESIS OLUÅžTURMA
    # --------------------------------------------------------


    def create_synthesis(
        self,
        synthesis_id: str,
        statements: Sequence[SynthesisStatement],
        preserved_context: SynthesisContext,
        cluster_id: Optional[str] = None,
        unresolved_items: Sequence[str] = (),
    ) -> SynthesisOutput:
        """
        7. BÃ¶lÃ¼m bulgularÄ±nÄ± yeniden analiz etmeden synthesis Ã§Ä±ktÄ±sÄ±
        oluÅŸturur.


        TamamlanmÄ±ÅŸ output yalnÄ±zca tÃ¼m gerekli referanslar geÃ§erliyse
        valid=True olur.
        """


        if not synthesis_id:
            raise ValueError(
                "Synthesis ID boÅŸ olamaz."
            )


        validate_synthesis_context(
            preserved_context
        )


        normalized_statements = tuple(statements)
        normalized_unresolved = tuple(unresolved_items)


        if not normalized_statements:
            return SynthesisOutput(
                synthesis_id=synthesis_id,
                cluster_id=cluster_id,
                synthesis_state=SynthesisState.FAILURE,
                statements=tuple(),
                connected_7_references=tuple(),
                preserved_context=preserved_context,
                valid=False,
                unresolved_items=normalized_unresolved,
            )


        # Her statement'Ä±n 7 traceability'sini kontrol et.
        for statement in normalized_statements:
            self.validate_statement(statement)


        # Statement'larÄ±n kullandÄ±ÄŸÄ± gerÃ§ek 7 referanslarÄ±nÄ± topla.
        reference_ids: list[str] = []


        for statement in normalized_statements:
            reference_ids.extend(
                statement.source_finding_ids
            )
            reference_ids.extend(
                statement.source_relation_ids
            )


        # SÄ±ra korunur, tekrarlar kaldÄ±rÄ±lÄ±r.
        unique_reference_ids = tuple(
            dict.fromkeys(reference_ids)
        )


        connected_references = tuple(
            self._registry.get(reference_id)
            for reference_id in unique_reference_ids
        )


        state = determine_synthesis_state(
            normalized_statements,
            normalized_unresolved,
        )


        output = SynthesisOutput(
            synthesis_id=synthesis_id,
            cluster_id=cluster_id,
            synthesis_state=state,
            statements=normalized_statements,
            connected_7_references=connected_references,
            preserved_context=preserved_context,
            valid=True,
            unresolved_items=normalized_unresolved,
        )


        self._outputs.append(output)


        return output




# ============================================================
# 15. OUTPUT BÃœTÃœNLÃœÄžÃœ
# ============================================================


def validate_synthesis_output(
    output: SynthesisOutput,
) -> None:
    """
    TamamlanmÄ±ÅŸ synthesis Ã§Ä±ktÄ±sÄ±nÄ±n referans bÃ¼tÃ¼nlÃ¼ÄŸÃ¼nÃ¼ doÄŸrular.
    """


    if not output.valid:
        raise ValueError(
            f"Synthesis output valid deÄŸil: {output.synthesis_id}"
        )


    if not output.statements:
        raise ValueError(
            "Valid synthesis en az bir statement iÃ§ermelidir."
        )


    if not output.connected_7_references:
        raise ValueError(
            "Valid synthesis en az bir 7. BÃ¶lÃ¼m referansÄ± "
            "iÃ§ermelidir."
        )


    connected_ids = {
        reference.source_output_id
        for reference in output.connected_7_references
    }


    for statement in output.statements:
        for finding_id in statement.source_finding_ids:
            if finding_id not in connected_ids:
                raise ValueError(
                    "Synthesis statement ile 7 referansÄ± arasÄ±nda "
                    f"traceability kopukluÄŸu: {finding_id}"
                )


        for relation_id in statement.source_relation_ids:
            if relation_id not in connected_ids:
                raise ValueError(
                    "Synthesis relation ile 7 referansÄ± arasÄ±nda "
                    f"traceability kopukluÄŸu: {relation_id}"
                )


    validate_synthesis_context(
        output.preserved_context
    )




# ============================================================
# 16. MULTÄ°MODAL SINIRI
# ============================================================


def validate_multimodal_boundary() -> None:
    """
    GÃ¶rsel/multimodal formatÄ±n tek baÅŸÄ±na epistemik Ã¼stÃ¼nlÃ¼k
    oluÅŸturmasÄ±nÄ± engelleyen kavramsal sÄ±nÄ±r.


    8:
        chart,
        graph,
        table,
        screenshot,
        infographic,
        diagram,
        map,
        PDF figure/table,
        X media


    gibi girdileri yeniden analiz etmez.


    GÃ¶rsel kaynaklÄ± bilgi yalnÄ±zca 7'nin oluÅŸturduÄŸu analitik
    bulgular Ã¼zerinden synthesis girdisi olabilir.
    """


    forbidden_implications = (
        "visual_strength",
        "visual_reliability",
        "visual_independence",
        "visual_confidence",
        "visual_evidence_strength",
    )


    assert forbidden_implications




# ============================================================
# 17. 7 â†’ 8 SINIRI
# ============================================================


def seven_to_eight_boundary() -> str:
    return (
        "7 = Ne gÃ¶rÃ¼lÃ¼yor? "
        "8 = 7 tarafÄ±ndan ortaya konmuÅŸ bulgular birlikte ne ifade ediyor?"
    )




# ============================================================
# 18. 8'Ä°N YAPAMAYACAÄžI Ä°ÅžLEMLER
# ============================================================


FORBIDDEN_OPERATIONS = frozenset(
    {
        "reanalyze_section_7",
        "recalculate_section_7_measurements",
        "create_new_evidence",
        "create_new_fact",
        "create_new_independent_evidence",
        "infer_causality",
        "infer_actor_intent",
        "assign_reliability",
        "assign_confidence",
        "assign_evidence_strength",
        "assign_probability",
        "weight_sources",
        "rank_sources",
        "predict_future",
        "generate_trade_signal",
        "make_risk_decision",
        "make_position_decision",
        "produce_investment_advice",
        "produce_final_bias",
        "produce_bullish_verdict",
        "produce_bearish_verdict",
        "classify_market_regime",
        "decide_for_kokboru",
        "decide_for_tulpar",
    }
)




def validate_forbidden_operations() -> None:
    """
    YasaklÄ± operasyonlarÄ±n yalnÄ±zca kavramsal sÄ±nÄ±r olarak kayÄ±tlÄ±
    olduÄŸunu doÄŸrular.
    """


    for operation in FORBIDDEN_OPERATIONS:
        assert isinstance(operation, str)
        assert operation.strip()




# ============================================================
# 19. FINAL PRINCIPLE
# ============================================================


SYNTHESIS_FINAL_PRINCIPLE = (
    "8. BÃ¶lÃ¼m â€” CTA Synthesis / SonuÃ§; 7. BÃ¶lÃ¼m tarafÄ±ndan ortaya "
    "konmuÅŸ analitik bulgularÄ± ve iliÅŸkileri, zaman, kapsam, aktÃ¶r, "
    "bilgi statÃ¼sÃ¼, provenance ve baÄŸlam farklÄ±lÄ±klarÄ±nÄ± koruyarak "
    "birlikte deÄŸerlendirir ve koÅŸullu, baÄŸlamsal bir CTA tablosu "
    "oluÅŸturur. 8. BÃ¶lÃ¼m yeni veri, baÄŸÄ±msÄ±z kanÄ±t veya yeni analitik "
    "gerÃ§eklik Ã¼retmez; her synthesis ifadesi 7. BÃ¶lÃ¼m bulgularÄ±na "
    "geri izlenebilir olmalÄ±dÄ±r. YakÄ±nsama, tamamlayÄ±cÄ±lÄ±k, sÄ±nÄ±rlama, "
    "koÅŸulluluk, ayrÄ±ÅŸma, Ã§eliÅŸki ve belirsizlik korunur. Synthesis "
    "7. BÃ¶lÃ¼mde yapÄ±lmamÄ±ÅŸ analizi yeniden Ã¼retmez. HiÃ§bir synthesis "
    "ifadesi kanÄ±t gÃ¼cÃ¼, gÃ¼venilirlik, confidence, aÄŸÄ±rlÄ±k, Ã¼stÃ¼nlÃ¼k, "
    "probability, gelecek tahmini, trade kararÄ±, risk kararÄ±, yatÄ±rÄ±m "
    "tavsiyesi veya kesin nihai yÃ¶n hÃ¼kmÃ¼ne dÃ¶nÃ¼ÅŸtÃ¼rÃ¼lmez. Nihai karar "
    "yetkisi KÃ–KBÃ–RÃœ veya TULPAR adÄ±na bu bÃ¶lÃ¼mde bulunmaz."
)




# ============================================================
# 20. VALIDATION
# ============================================================


def validate_8() -> None:
    """
    8. BÃ¶lÃ¼m yapÄ±sal self-validation.


    Bu fonksiyon yalnÄ±zca kodun iÃ§ tutarlÄ±lÄ±ÄŸÄ±nÄ± test eder.
    Harici veri veya gerÃ§ek runtime sistemi doÄŸrulamaz.
    """


    # --------------------------------------------------------
    # Registry
    # --------------------------------------------------------


    registry = Section7ReferenceRegistry()


    finding_ref = Section7Reference(
        reference_id="finding_001",
        reference_type=Section7ReferenceType.FINDING,
        source_output_id="finding_001",
        cluster_id="cluster_001",
        description="7. BÃ¶lÃ¼m analitik bulgusu.",
    )


    relation_ref = Section7Reference(
        reference_id="relation_001",
        reference_type=Section7ReferenceType.RELATION_ANALYSIS,
        source_output_id="relation_001",
        cluster_id="cluster_001",
        description="7. BÃ¶lÃ¼m iliÅŸki analizi.",
    )


    uncertainty_ref = Section7Reference(
        reference_id="uncertainty_001",
        reference_type=Section7ReferenceType.UNCERTAINTY_ANALYSIS,
        source_output_id="uncertainty_001",
        cluster_id="cluster_001",
        description="7. BÃ¶lÃ¼m belirsizlik analizi.",
    )


    registry.register(finding_ref)
    registry.register(relation_ref)
    registry.register(uncertainty_ref)


    assert registry.exists("finding_001")
    assert registry.exists("relation_001")
    assert registry.exists("uncertainty_001")


    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------


    context = SynthesisContext(
        time_horizons=(
            "short_term",
            "long_term",
        ),
        actors=(
            "actor_a",
            "actor_b",
        ),
        information_statuses=(
            "current_observation",
            "commentary",
        ),
        scopes=(
            "cta_context",
        ),
        provenance_refs=(
            "root_001",
        ),
        contexts=(
            "market_context_001",
        ),
    )


    validate_synthesis_context(context)


    # --------------------------------------------------------
    # Statement
    # --------------------------------------------------------


    statement = SynthesisStatement(
        statement_id="statement_001",
        statement=(
            "7. BÃ¶lÃ¼m bulgularÄ± kÄ±sa vadeli yakÄ±nsama ile birlikte "
            "Ã§Ã¶zÃ¼mlenmemiÅŸ belirsizliÄŸin korunmasÄ± gerektiÄŸini "
            "gÃ¶stermektedir."
        ),
        source_finding_ids=(
            "finding_001",
        ),
        source_relation_ids=(
            "relation_001",
        ),
        used_concepts=(
            SynthesisConcept.CONVERGENCE,
            SynthesisConcept.UNCERTAINTY,
        ),
        context=context,
    )


    validate_statement_traceability(
        statement,
        registry,
    )


    # --------------------------------------------------------
    # Engine
    # --------------------------------------------------------


    engine = CTASynthesisEngine(
        section7_registry=registry,
    )


    output = engine.create_synthesis(
        synthesis_id="synthesis_001",
        statements=(statement,),
        preserved_context=context,
        cluster_id="cluster_001",
    )


    assert output.valid is True
    assert output.synthesis_state == SynthesisState.SUCCESSFUL


    validate_synthesis_output(output)


    assert len(output.connected_7_references) == 2


    # --------------------------------------------------------
    # Partial synthesis
    # --------------------------------------------------------


    partial_statement = SynthesisStatement(
        statement_id="statement_002",
        statement=(
            "BazÄ± bulgular birlikte deÄŸerlendirilebilirken kritik "
            "bir belirsizlik aÃ§Ä±k kalmaktadÄ±r."
        ),
        source_finding_ids=(
            "finding_001",
        ),
        source_relation_ids=(
            "uncertainty_001",
        ),
        used_concepts=(
            SynthesisConcept.CONDITIONALITY,
            SynthesisConcept.UNCERTAINTY,
        ),
        context=context,
    )


    partial_output = engine.create_synthesis(
        synthesis_id="synthesis_002",
        statements=(partial_statement,),
        preserved_context=context,
        cluster_id="cluster_001",
        unresolved_items=(
            "critical_context_unresolved",
        ),
    )


    assert partial_output.valid is True
    assert partial_output.synthesis_state == SynthesisState.PARTIAL


    validate_synthesis_output(partial_output)


    # --------------------------------------------------------
    # Failure
    # --------------------------------------------------------


    failure_output = engine.create_synthesis(
        synthesis_id="synthesis_003",
        statements=tuple(),
        preserved_context=context,
        cluster_id="cluster_001",
    )


    assert failure_output.valid is False
    assert failure_output.synthesis_state == SynthesisState.FAILURE


    # --------------------------------------------------------
    # Multimodal boundary
    # --------------------------------------------------------


    validate_multimodal_boundary()


    # --------------------------------------------------------
    # Forbidden operations
    # --------------------------------------------------------


    validate_forbidden_operations()


    # --------------------------------------------------------
    # Boundary
    # --------------------------------------------------------


    boundary = seven_to_eight_boundary()


    assert "7 = Ne gÃ¶rÃ¼lÃ¼yor?" in boundary
    assert "8 =" in boundary


    # --------------------------------------------------------
    # Final principle
    # --------------------------------------------------------


    assert isinstance(
        SYNTHESIS_FINAL_PRINCIPLE,
        str,
    )


    assert "yeni veri" in SYNTHESIS_FINAL_PRINCIPLE
    assert "geri izlenebilir" in SYNTHESIS_FINAL_PRINCIPLE
    assert "trade kararÄ±" in SYNTHESIS_FINAL_PRINCIPLE




# ============================================================
# 21. MODULE ENTRY
# ============================================================


if __name__ == "__main__":
    validate_8()


    print(
        "8. BÃ–LÃœM â€” CTA SYNTHESIS / SONUÃ‡"
    )
    print("=" * 70)
    print(SYNTHESIS_FINAL_PRINCIPLE)
    print("=" * 70)
    print(
        "READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ"
    )
    print(
        "Validation: OK"
    )


"""
