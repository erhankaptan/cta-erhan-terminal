8. BÖLÜM — CTA SYNTHESIS / SONUÇ
FINAL KOD


7. Bölüm tarafından ortaya konmuş analitik bulguları ve ilişkileri,
zaman, kapsam, aktör, bilgi statüsü, provenance ve bağlam farklılıklarını
koruyarak birlikte değerlendirir ve koşullu, bağlamsal bir CTA tablosu
oluşturur.


8. Bölüm:
- yeni veri üretmez,
- yeni bağımsız kanıt üretmez,
- 7. Bölümde yapılmamış yeni analiz üretmez,
- 7. Bölüm ölçümlerini yeniden hesaplamaz,
- 7. Bölümün yerine geçmez,
- nihai CTA yönü veya karar üretmez.


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ
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
    8. Bölüm synthesis durumları.


    SUCCESSFUL:
        Birden fazla 7. Bölüm bulgusu arasında anlamlı üst düzey
        bağ kurulmuş ve kritik bağlamsal farklılıklar korunmuştur.


    PARTIAL:
        Bazı bulgular anlamlı biçimde birleştirilebilmiş, ancak
        bazı kritik alanlar açık / belirsiz / çözümlenmemiş kalmıştır.


    FAILURE:
        Gerekli 7. Bölüm referansları veya anlamlı ilişki yapısı
        bulunmadığından açıklanabilir bir üst düzey synthesis
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
    8. Bölümün temel synthesis sözlüğü.


    HARMONY_AUXILIARY yalnızca yardımcı açıklama kavramıdır.
    Ayrı bir temel synthesis ilişkisi değildir.


    SUPPORT özellikle kavramsal temel ilişki olarak bulunmaz.
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
# 3. 7 → 8 REFERANS TÜRÜ
# ============================================================


class Section7ReferenceType(str, Enum):
    """
    8'in dayandığı 7. Bölüm çıktısının türünü açıkça belirtir.
    """


    FINDING = "finding"
    RELATION_ANALYSIS = "relation_analysis"
    STRUCTURAL_MEASUREMENT = "structural_measurement"
    PROVENANCE_ANALYSIS = "provenance_analysis"
    UNCERTAINTY_ANALYSIS = "uncertainty_analysis"




# ============================================================
# 4. 7. BÖLÜM REFERANS KAYDI
# ============================================================


@dataclass(frozen=True)
class Section7Reference:
    """
    8. Bölüm synthesis'inin 7. Bölümdeki gerçek kaynağı.


    Bu nesne yeni analiz üretmez.
    Yalnızca 7. Bölümden gelen mevcut çıktının kimliğini taşır.
    """


    reference_id: str
    reference_type: Section7ReferenceType


    # İlgili 7 çıktısının gerçek kimliği.
    source_output_id: str


    # İsteğe bağlı cluster bilgisi.
    # Cluster ID hiçbir zaman source_output_id yerine geçmez.
    cluster_id: Optional[str] = None


    # 7 çıktısının mevcut açıklaması.
    description: Optional[str] = None




# ============================================================
# 5. BAĞLAMSAL KORUMA
# ============================================================


@dataclass(frozen=True)
class SynthesisContext:
    """
    8. Bölümün synthesis sırasında korumak zorunda olduğu bağlam.


    Buradaki alanlar yeni analiz sonucu değildir.
    7. Bölümden taşınan / 7 çıktısında mevcut olan bağlamsal
    farklılıkların korunması içindir.
    """


    time_horizons: tuple[str, ...] = field(default_factory=tuple)
    actors: tuple[str, ...] = field(default_factory=tuple)
    information_statuses: tuple[str, ...] = field(default_factory=tuple)
    scopes: tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: tuple[str, ...] = field(default_factory=tuple)
    contexts: tuple[str, ...] = field(default_factory=tuple)


    # Synthesis sırasında bu ayrımların korunması zorunludur.
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
    Tek bir üst düzey synthesis ifadesi.


    statement:
        7. Bölüm bulgularının birlikte ifade edilen üst düzey anlamı.


    source_finding_ids:
        Synthesis'in dayandığı gerçek 7. Bölüm çıktı ID'leri.


    source_relation_ids:
        7. Bölüm tarafından kurulmuş / analiz edilmiş ilişki ID'leri.


    used_concepts:
        8. Bölümde kullanılan synthesis kavramları.


    context:
        Zaman, aktör, statü, kapsam, provenance ve bağlam korunumu.


    ÖNEMLİ:
        Bu sınıf yeni veri veya yeni bağımsız kanıt taşımaz.
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
    8. Bölümün tamamlanmış synthesis çıktısı.


    Bu çıktı:
    - yeni veri değildir,
    - yeni bağımsız kanıt değildir,
    - yeni analiz değildir,
    - trade/risk/position kararı değildir.


    Tamamlanmış output'un geçerli olabilmesi için:
    - en az bir gerçek 7 referansı,
    - gerekli ilişki referansları,
    - bağlamsal koruma
    bulunmalıdır.
    """


    synthesis_id: str
    cluster_id: Optional[str]


    synthesis_state: SynthesisState


    statements: tuple[SynthesisStatement, ...]


    connected_7_references: tuple[Section7Reference, ...]


    preserved_context: SynthesisContext


    # Tamamlanmış çıktının referans bütünlüğü.
    valid: bool = False


    # İnsan tarafından kontrol edilmesi gereken açıklamalar.
    unresolved_items: tuple[str, ...] = field(default_factory=tuple)




# ============================================================
# 8. YASAKLI 8. BÖLÜM ÇIKTILARI
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
# 9. 7 → 8 REFERANS KAYDI
# ============================================================


class Section7ReferenceRegistry:
    """
    7. Bölüm çıktılarının yalnızca referans amaçlı kayıt defteri.


    8 burada analiz yapmaz.
    7 çıktısını değiştirmez.
    7 çıktısını yeniden hesaplamaz.
    """


    def __init__(self) -> None:
        self._references: dict[str, Section7Reference] = {}


    def register(self, reference: Section7Reference) -> None:
        if not reference.reference_id:
            raise ValueError("7 referansı boş olamaz.")


        if not reference.source_output_id:
            raise ValueError(
                "7 referansının source_output_id alanı zorunludur."
            )


        if reference.reference_id in self._references:
            raise ValueError(
                f"7 referansı zaten kayıtlı: {reference.reference_id}"
            )


        self._references[reference.reference_id] = reference


    def exists(self, reference_id: str) -> bool:
        return reference_id in self._references


    def get(self, reference_id: str) -> Section7Reference:
        try:
            return self._references[reference_id]
        except KeyError as exc:
            raise KeyError(
                f"7 Bölüm referansı bulunamadı: {reference_id}"
            ) from exc


    def all(self) -> tuple[Section7Reference, ...]:
        return tuple(self._references.values())




# ============================================================
# 10. 7 ÇIKTISINDAN REFERANS ÜRETME ADAPTÖRÜ
# ============================================================


def _extract_output_id(obj: object) -> Optional[str]:
    """
    7. Bölümdeki farklı çıktı nesnelerinin ID alanını güvenli şekilde
    okur.


    Desteklenen alanlar:
    - finding_id
    - analysis_id
    - measurement_id


    Bu fonksiyon yeni ID üretmez.
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
    Mevcut 7. Bölüm çıktısından yalnızca referans oluşturur.


    7 çıktısını değiştirmez ve yeniden analiz etmez.
    """


    output_id = _extract_output_id(obj)


    if not output_id:
        raise ValueError(
            "7. Bölüm çıktısında geçerli bir çıktı ID'si bulunamadı."
        )


    return Section7Reference(
        reference_id=output_id,
        reference_type=reference_type,
        source_output_id=output_id,
        cluster_id=cluster_id,
        description=description,
    )




# ============================================================
# 11. REFERANS BÜTÜNLÜĞÜ
# ============================================================


def validate_statement_traceability(
    statement: SynthesisStatement,
    registry: Section7ReferenceRegistry,
) -> None:
    """
    Tamamlanmış synthesis statement'ının 7'ye geri izlenebilirliğini
    kontrol eder.
    """


    if not statement.statement_id:
        raise ValueError("Synthesis statement ID boş olamaz.")


    if not statement.statement.strip():
        raise ValueError(
            f"Synthesis statement boş olamaz: {statement.statement_id}"
        )


    if not statement.source_finding_ids:
        raise ValueError(
            "Synthesis statement en az bir 7. Bölüm bulgusuna "
            "geri izlenebilir olmalıdır: "
            f"{statement.statement_id}"
        )


    for finding_id in statement.source_finding_ids:
        if not registry.exists(finding_id):
            raise ValueError(
                "Synthesis statement'ın referans verdiği 7 çıktısı "
                f"bulunamadı: {finding_id}"
            )


    for relation_id in statement.source_relation_ids:
        if not registry.exists(relation_id):
            raise ValueError(
                "Synthesis statement'ın referans verdiği 7 ilişkisi "
                f"bulunamadı: {relation_id}"
            )


    if not statement.context.preserve_time_horizons:
        raise ValueError(
            "Zaman ufku korunumu kapatılamaz."
        )


    if not statement.context.preserve_actors:
        raise ValueError(
            "Aktör ayrımı korunumu kapatılamaz."
        )


    if not statement.context.preserve_information_statuses:
        raise ValueError(
            "Bilgi statüsü korunumu kapatılamaz."
        )


    if not statement.context.preserve_scopes:
        raise ValueError(
            "Kapsam korunumu kapatılamaz."
        )


    if not statement.context.preserve_provenance:
        raise ValueError(
            "Provenance korunumu kapatılamaz."
        )


    if not statement.context.preserve_contexts:
        raise ValueError(
            "Bağlam korunumu kapatılamaz."
        )




# ============================================================
# 12. SYNTHESIS DURUMU DEĞERLENDİRME SINIRI
# ============================================================


def determine_synthesis_state(
    statements: Sequence[SynthesisStatement],
    unresolved_items: Sequence[str],
) -> SynthesisState:
    """
    Synthesis durumunu değerlendirir.


    ÖNEMLİ:
    Bu fonksiyon 7. Bölümde yeni analiz yapmaz.


    Yalnızca 8'e verilmiş synthesis yapısının:
    - referans içerip içermediğine,
    - kısmi / çözümlenmemiş alan bulunup bulunmadığına
    bakar.


    Çelişki veya belirsizlik tek başına FAILURE değildir.
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
# 13. CONTEXT BÜTÜNLÜĞÜ
# ============================================================


def validate_synthesis_context(
    context: SynthesisContext,
) -> None:
    """
    Synthesis context'in temel korunma kurallarını doğrular.
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
            "8. Bölüm synthesis context koruma sınırlarından "
            "biri kapatılmış."
        )




# ============================================================
# 14. SYNTHESIS MOTORU
# ============================================================


class CTASynthesisEngine:
    """
    8. Bölüm — CTA Synthesis / Sonuç Motoru.


    Görev:
        7. Bölümün mevcut analitik çıktılarının üst düzey
        bağlamsal sentezini taşımak.


    Yapmaz:
        - yeni analiz,
        - yeni ölçüm,
        - yeni veri,
        - yeni bağımsız kanıt,
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


    Motor yalnızca:
        7 → 8 referans zincirini,
        synthesis ifadelerini,
        synthesis kavramlarını,
        bağlamsal korumayı
        yönetir.
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
    # SYNTHESIS OLUŞTURMA
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
        7. Bölüm bulgularını yeniden analiz etmeden synthesis çıktısı
        oluşturur.


        Tamamlanmış output yalnızca tüm gerekli referanslar geçerliyse
        valid=True olur.
        """


        if not synthesis_id:
            raise ValueError(
                "Synthesis ID boş olamaz."
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


        # Her statement'ın 7 traceability'sini kontrol et.
        for statement in normalized_statements:
            self.validate_statement(statement)


        # Statement'ların kullandığı gerçek 7 referanslarını topla.
        reference_ids: list[str] = []


        for statement in normalized_statements:
            reference_ids.extend(
                statement.source_finding_ids
            )
            reference_ids.extend(
                statement.source_relation_ids
            )


        # Sıra korunur, tekrarlar kaldırılır.
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
# 15. OUTPUT BÜTÜNLÜĞÜ
# ============================================================


def validate_synthesis_output(
    output: SynthesisOutput,
) -> None:
    """
    Tamamlanmış synthesis çıktısının referans bütünlüğünü doğrular.
    """


    if not output.valid:
        raise ValueError(
            f"Synthesis output valid değil: {output.synthesis_id}"
        )


    if not output.statements:
        raise ValueError(
            "Valid synthesis en az bir statement içermelidir."
        )


    if not output.connected_7_references:
        raise ValueError(
            "Valid synthesis en az bir 7. Bölüm referansı "
            "içermelidir."
        )


    connected_ids = {
        reference.source_output_id
        for reference in output.connected_7_references
    }


    for statement in output.statements:
        for finding_id in statement.source_finding_ids:
            if finding_id not in connected_ids:
                raise ValueError(
                    "Synthesis statement ile 7 referansı arasında "
                    f"traceability kopukluğu: {finding_id}"
                )


        for relation_id in statement.source_relation_ids:
            if relation_id not in connected_ids:
                raise ValueError(
                    "Synthesis relation ile 7 referansı arasında "
                    f"traceability kopukluğu: {relation_id}"
                )


    validate_synthesis_context(
        output.preserved_context
    )




# ============================================================
# 16. MULTİMODAL SINIRI
# ============================================================


def validate_multimodal_boundary() -> None:
    """
    Görsel/multimodal formatın tek başına epistemik üstünlük
    oluşturmasını engelleyen kavramsal sınır.


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


    Görsel kaynaklı bilgi yalnızca 7'nin oluşturduğu analitik
    bulgular üzerinden synthesis girdisi olabilir.
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
# 17. 7 → 8 SINIRI
# ============================================================


def seven_to_eight_boundary() -> str:
    return (
        "7 = Ne görülüyor? "
        "8 = 7 tarafından ortaya konmuş bulgular birlikte ne ifade ediyor?"
    )




# ============================================================
# 18. 8'İN YAPAMAYACAĞI İŞLEMLER
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
    Yasaklı operasyonların yalnızca kavramsal sınır olarak kayıtlı
    olduğunu doğrular.
    """


    for operation in FORBIDDEN_OPERATIONS:
        assert isinstance(operation, str)
        assert operation.strip()




# ============================================================
# 19. FINAL PRINCIPLE
# ============================================================


SYNTHESIS_FINAL_PRINCIPLE = (
    "8. Bölüm — CTA Synthesis / Sonuç; 7. Bölüm tarafından ortaya "
    "konmuş analitik bulguları ve ilişkileri, zaman, kapsam, aktör, "
    "bilgi statüsü, provenance ve bağlam farklılıklarını koruyarak "
    "birlikte değerlendirir ve koşullu, bağlamsal bir CTA tablosu "
    "oluşturur. 8. Bölüm yeni veri, bağımsız kanıt veya yeni analitik "
    "gerçeklik üretmez; her synthesis ifadesi 7. Bölüm bulgularına "
    "geri izlenebilir olmalıdır. Yakınsama, tamamlayıcılık, sınırlama, "
    "koşulluluk, ayrışma, çelişki ve belirsizlik korunur. Synthesis "
    "7. Bölümde yapılmamış analizi yeniden üretmez. Hiçbir synthesis "
    "ifadesi kanıt gücü, güvenilirlik, confidence, ağırlık, üstünlük, "
    "probability, gelecek tahmini, trade kararı, risk kararı, yatırım "
    "tavsiyesi veya kesin nihai yön hükmüne dönüştürülmez. Nihai karar "
    "yetkisi KÖKBÖRÜ veya TULPAR adına bu bölümde bulunmaz."
)




# ============================================================
# 20. VALIDATION
# ============================================================


def validate_8() -> None:
    """
    8. Bölüm yapısal self-validation.


    Bu fonksiyon yalnızca kodun iç tutarlılığını test eder.
    Harici veri veya gerçek runtime sistemi doğrulamaz.
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
        description="7. Bölüm analitik bulgusu.",
    )


    relation_ref = Section7Reference(
        reference_id="relation_001",
        reference_type=Section7ReferenceType.RELATION_ANALYSIS,
        source_output_id="relation_001",
        cluster_id="cluster_001",
        description="7. Bölüm ilişki analizi.",
    )


    uncertainty_ref = Section7Reference(
        reference_id="uncertainty_001",
        reference_type=Section7ReferenceType.UNCERTAINTY_ANALYSIS,
        source_output_id="uncertainty_001",
        cluster_id="cluster_001",
        description="7. Bölüm belirsizlik analizi.",
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
            "7. Bölüm bulguları kısa vadeli yakınsama ile birlikte "
            "çözümlenmemiş belirsizliğin korunması gerektiğini "
            "göstermektedir."
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
            "Bazı bulgular birlikte değerlendirilebilirken kritik "
            "bir belirsizlik açık kalmaktadır."
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


    assert "7 = Ne görülüyor?" in boundary
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
    assert "trade kararı" in SYNTHESIS_FINAL_PRINCIPLE




# ============================================================
# 21. MODULE ENTRY
# ============================================================


if __name__ == "__main__":
    validate_8()


    print(
        "8. BÖLÜM — CTA SYNTHESIS / SONUÇ"
    )
    print("=" * 70)
    print(SYNTHESIS_FINAL_PRINCIPLE)
    print("=" * 70)
    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )
    print(
        "Validation: OK"
    )


"""
