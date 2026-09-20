6. BÖLÜM — YOĞURMA MOTORU
ERHAN / CTA TERMINALI


"""
ERHAN / CTA TERMINAL
6. BÖLÜM — YOĞURMA MOTORU
FINAL CODE


READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ


Amaç
-----
5. Bölüm — Bilgi Havuzu içinde korunmuş InformationPiece kayıtlarını:


- anlamlı bağlamsal kümeler halinde yapılandırmak,
- çoklu üyeliği korumak,
- ana / alt küme ilişkilerini korumak,
- yatay ilişkili kümeleri korumak,
- bilgi parçaları arasındaki ilişkileri yapılandırmak,
- provenance / bilgi kökünü korumak,
- zaman ve bağlam sürekliliğini korumak,
- ilişki ve küme yaşam döngüsü geçmişini korumak,
- 7. Bölüm için analize hazır yapılar üretmek


amacıyla kullanır.


Bu modül:


- analiz yapmaz,
- hesaplama yapmaz,
- değerlendirme yapmaz,
- confidence üretmez,
- trust score üretmez,
- truth score üretmez,
- evidence strength üretmez,
- weighting yapmaz,
- ranking yapmaz,
- consensus üretmez,
- forecast üretmez,
- prediction üretmez,
- piyasa yönü tahmin etmez,
- BUY / SELL üretmez,
- trade signal üretmez,
- final CTA bias üretmez,
- risk kararı üretmez,
- kullanıcı adına nihai karar vermez.


ÖNEMLİ
-------
Bu modül 5. Bölüm'deki InformationPiece sınıfını yeniden tanımlamaz.
5. Bölümden gelen bilgi nesnelerini doğrudan kullanır.


6. Bölümde küme sınırı "yeni bir tahmin/puanlama metodolojisi"
ile hesaplanmaz. Küme üyeliği, sağlanan bağlamsal süreklilik
eksenlerinin kaydedilmesi ve korunması üzerinden yapılandırılır.


7. Bölüm:
    Analiz / Hesaplama / Değerlendirme


8. Bölüm:
    CTA Synthesis / Sonuç


9. Bölüm:
    Tarihçe / Hafıza
"""


from __future__ import annotations


from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Tuple




# ============================================================================
# 1. İLİŞKİ DURUMLARI
# ============================================================================




class RelationState(str, Enum):
    """
    İlişkinin mevcut / tarihsel durumu.


    Bunlar:
        - confidence
        - trust
        - truth
        - reliability
        - evidence strength


    değildir.
    """


    ACTIVE = "active"
    UNCERTAIN = "uncertain"
    DISPUTED = "disputed"
    WEAKENED = "weakened"
    INVALIDATED = "invalidated"
    UNRESOLVED = "unresolved"




# ============================================================================
# 2. KÜME YAŞAM DÖNGÜSÜ
# ============================================================================




class ClusterState(str, Enum):
    """
    Kümenin yaşam döngüsü.
    """


    FORMING = "forming"
    DEVELOPING = "developing"
    UPDATED = "updated"
    CLOSED = "closed"
    REOPENED = "reopened"




# ============================================================================
# 3. KÜME SINIRI EKSENLERİ
# ============================================================================




class ClusterAxis(str, Enum):
    """
    Anlamlı bağlamsal süreklilik eksenleri.


    Bu eksenlerin bulunması, kümenin önemini veya doğruluğunu
    göstermez.


    Kelime benzerliği bu enum içinde bilinçli olarak bulunmaz.
    """


    COMMON_SUBJECT = "common_subject"
    COMMON_EVENT = "common_event"
    COMMON_THEME = "common_theme"
    COMMON_REFERENCE_PERIOD = "common_reference_period"
    COMMON_ACTOR = "common_actor"
    COMMON_INSTITUTION = "common_institution"
    COMMON_ASSET = "common_asset"
    COMMON_INFORMATION_ROOT = "common_information_root"
    COMMON_EVENT_CONTEXT = "common_event_context"




# ============================================================================
# 4. İLİŞKİ TİPLERİ
# ============================================================================




class RelationType(str, Enum):
    """
    6. Bölümde korunabilecek ilişki türleri.


    İlişkinin varlığı ile ilişkinin analitik anlamı birbirinden
    ayrıdır. Analitik değerlendirme 7. Bölüme aittir.
    """


    SAME_TOPIC = "same_topic"
    SAME_EVENT_DIFFERENT_ANGLE = "same_event_different_angle"
    SUPPORTS = "supports"
    LIMITS = "limits"
    CONTRADICTS = "contradicts"
    UPDATES = "updates"
    CORRECTS = "corrects"
    REPEATS = "repeats"
    PRIOR_VIEW_OF_SAME_INSTITUTION = "prior_view_of_same_institution"
    DIFFERENT_EXPLANATION_OF_SAME_POSITIONING = (
        "different_explanation_of_same_positioning"
    )
    FORECAST_OUTCOME_COMPARISON = "forecast_outcome_comparison"




# ============================================================================
# 5. KÜME İLİŞKİ TİPLERİ
# ============================================================================




class ClusterRelationType(str, Enum):
    """
    Hiyerarşik olmayan kümeler arasındaki yatay ilişki.


    Ana/alt ilişkisi değildir.
    """


    RELATED = "related"
    CONTINUATION = "continuation"
    DIFFERENT_ANGLE = "different_angle"
    CONNECTED_EVENT = "connected_event"
    RELATED_CONTEXT = "related_context"




# ============================================================================
# 6. KÜME YAŞAM DÖNGÜSÜ GEÇMİŞİ
# ============================================================================




@dataclass(frozen=True)
class ClusterLifecycleEvent:
    """
    Kümenin yaşam döngüsündeki tarihsel bir durum değişimi.


    Eski durum silinmez.
    """


    event_id: str
    cluster_id: str


    previous_state: Optional[ClusterState]
    new_state: ClusterState


    occurred_at: datetime
    reason: Optional[str] = None




# ============================================================================
# 7. İLİŞKİ DURUM GEÇMİŞİ
# ============================================================================




@dataclass(frozen=True)
class RelationStateEvent:
    """
    Bir ilişkinin durum değişiminin tarihsel kaydı.
    """


    event_id: str
    relation_id: str


    previous_state: Optional[RelationState]
    new_state: RelationState


    occurred_at: datetime
    reason: Optional[str] = None




# ============================================================================
# 8. BİLGİ PARÇASI İLİŞKİSİ
# ============================================================================




@dataclass(frozen=True)
class Relation:
    """
    İki InformationPiece arasındaki ilişkisel bağ.


    Burada yalnızca ilişki ve onun tarihsel durumu korunur.


    İlişkinin:
        - gücü,
        - doğruluğu,
        - güvenilirliği,
        - önemi,
        - ağırlığı


    hesaplanmaz.
    """


    relation_id: str


    source_information_id: str
    target_information_id: str


    relation_type: RelationType


    state: RelationState = RelationState.ACTIVE


    context_note: Optional[str] = None


    created_at: Optional[datetime] = None


    state_history: Tuple[RelationStateEvent, ...] = field(
        default_factory=tuple
    )




# ============================================================================
# 9. KÜME İLİŞKİSİ
# ============================================================================




@dataclass(frozen=True)
class ClusterRelation:
    """
    İki küme arasındaki yatay ilişki.


    Bu ilişki ana/alt hiyerarşi değildir.


    Hiyerarşik olmayan ilişkili kümeleri zorla ana/alt yapıya
    sokmamak için kullanılır.
    """


    relation_id: str


    source_cluster_id: str
    target_cluster_id: str


    relation_type: ClusterRelationType


    state: RelationState = RelationState.ACTIVE


    context_note: Optional[str] = None


    created_at: Optional[datetime] = None


    state_history: Tuple[RelationStateEvent, ...] = field(
        default_factory=tuple
    )




# ============================================================================
# 10. KÜME
# ============================================================================




@dataclass(frozen=True)
class Cluster:
    """
    6. Bölüm bilgi kümesi.


    Küme:
        - bağlamsal süreklilik taşır,
        - InformationPiece ID'lerini referanslar,
        - çoklu üyeliği destekler,
        - ana/alt yapıyı destekler,
        - yatay ilişkileri destekler,
        - yaşam döngüsü geçmişini korur.


    Küme bir önem, doğruluk veya güven sıralaması değildir.
    """


    cluster_id: str


    cluster_type: str


    state: ClusterState = ClusterState.FORMING


    member_information_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )


    parent_cluster_id: Optional[str] = None


    child_cluster_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )


    shared_axes: Tuple[ClusterAxis, ...] = field(
        default_factory=tuple
    )


    context_note: Optional[str] = None


    created_at: Optional[datetime] = None


    lifecycle_history: Tuple[ClusterLifecycleEvent, ...] = field(
        default_factory=tuple
    )




# ============================================================================
# 11. ÇOKLU ÜYELİK
# ============================================================================




@dataclass(frozen=True)
class Membership:
    """
    InformationPiece -> Cluster üyeliği.


    Aynı InformationPiece birden fazla Cluster içinde bulunabilir.


    InformationPiece kopyalanmaz.
    """


    information_id: str
    cluster_id: str


    assigned_at: Optional[datetime] = None


    context_note: Optional[str] = None




# ============================================================================
# 12. YOĞURMA DURUMU
# ============================================================================




@dataclass(frozen=True)
class YogurmaState:
    """
    Yoğurma Motoru'nun mevcut yapısal durumu.


    Buradaki nesneler analiz sonucu değildir.
    """


    clusters: Tuple[Cluster, ...] = field(
        default_factory=tuple
    )


    relations: Tuple[Relation, ...] = field(
        default_factory=tuple
    )


    cluster_relations: Tuple[ClusterRelation, ...] = field(
        default_factory=tuple
    )


    memberships: Tuple[Membership, ...] = field(
        default_factory=tuple
    )




# ============================================================================
# 13. YOĞURMA MOTORU
# ============================================================================




class YogurmaMotoru:
    """
    6. Bölüm — Yoğurma Motoru.


    5. Bölümdeki InformationPiece nesnelerini doğrudan referanslar.


    Sorumlulukları:
        - bağlamsal kümeler,
        - çoklu üyelik,
        - ana/alt kümeler,
        - yatay ilişkili kümeler,
        - bilgi parçaları arası ilişkiler,
        - provenance referanslarının korunması,
        - ilişki geçmişi,
        - küme yaşam döngüsü.


    Sorumlulukları DEĞİLDİR:
        - analiz,
        - hesaplama,
        - değerlendirme,
        - skor,
        - ağırlık,
        - ranking,
        - confidence,
        - trust,
        - truth,
        - prediction,
        - forecast,
        - trade,
        - risk,
        - final CTA bias.
    """


    def __init__(self) -> None:
        # 5. Bölümden gelen gerçek bilgi parçaları.
        #
        # Burada InformationPiece yeniden tanımlanmaz.
        self._pieces: dict[str, Any] = {}


        self._clusters: dict[str, Cluster] = {}


        self._relations: dict[str, Relation] = {}


        self._cluster_relations: dict[
            str,
            ClusterRelation,
        ] = {}


        self._memberships: set[tuple[str, str]] = set()


    # ========================================================================
    # INFORMATION PIECES — 5 -> 6
    # ========================================================================


    def register_information_piece(
        self,
        piece: Any,
    ) -> None:
        """
        5. Bölüm InformationPiece nesnesini 6. Bölüme bağlar.


        Aynı information ID ikinci kez gelirse eski kayıt sessizce
        ezilmez.


        Bu modül InformationPiece içeriğini değiştirmez.
        """


        information_id = self._extract_information_id(piece)


        if information_id in self._pieces:
            existing = self._pieces[information_id]


            if existing is piece:
                return


            raise ValueError(
                f"Duplicate information_id in 6. Bölüm: "
                f"{information_id}"
            )


        self._pieces[information_id] = piece


    def register_information_pieces(
        self,
        pieces: Iterable[Any],
    ) -> None:
        """
        Birden fazla 5. Bölüm InformationPiece kaydını ekler.
        """


        for piece in pieces:
            self.register_information_piece(piece)


    def get_information_piece(
        self,
        information_id: str,
    ) -> Any:
        """
        Kayıtlı InformationPiece döndürür.
        """


        try:
            return self._pieces[information_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown information_id: {information_id}"
            ) from exc


    def information_piece_exists(
        self,
        information_id: str,
    ) -> bool:
        return information_id in self._pieces


    def all_information_pieces(
        self,
    ) -> Tuple[Any, ...]:
        return tuple(self._pieces.values())


    # ========================================================================
    # CLUSTER CREATION
    # ========================================================================


    def create_cluster(
        self,
        cluster_id: str,
        cluster_type: str,
        *,
        shared_axes: Iterable[ClusterAxis] = (),
        parent_cluster_id: Optional[str] = None,
        context_note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> Cluster:
        """
        Yeni küme oluşturur.


        parent_cluster_id verilmişse parent'ın gerçekten mevcut olması
        gerekir.


        Bu metod yalnızca sağlanan bağlamsal eksenleri kaydeder.
        Kelime benzerliğine dayalı otomatik kümeleme yapmaz.
        """


        if not cluster_id.strip():
            raise ValueError("cluster_id cannot be empty.")


        if not cluster_type.strip():
            raise ValueError("cluster_type cannot be empty.")


        if cluster_id in self._clusters:
            raise ValueError(
                f"Duplicate cluster_id: {cluster_id}"
            )


        if parent_cluster_id == cluster_id:
            raise ValueError(
                "A cluster cannot be its own parent."
            )


        if (
            parent_cluster_id is not None
            and parent_cluster_id not in self._clusters
        ):
            raise ValueError(
                f"Unknown parent_cluster_id: {parent_cluster_id}"
            )


        normalized_axes = tuple(dict.fromkeys(shared_axes))


        cluster = Cluster(
            cluster_id=cluster_id,
            cluster_type=cluster_type,
            state=ClusterState.FORMING,
            member_information_ids=(),
            parent_cluster_id=parent_cluster_id,
            child_cluster_ids=(),
            shared_axes=normalized_axes,
            context_note=context_note,
            created_at=created_at,
            lifecycle_history=(),
        )


        self._clusters[cluster_id] = cluster


        if parent_cluster_id is not None:
            parent = self._clusters[parent_cluster_id]


            if cluster_id not in parent.child_cluster_ids:
                updated_parent = replace(
                    parent,
                    child_cluster_ids=(
                        *parent.child_cluster_ids,
                        cluster_id,
                    ),
                )


                self._clusters[parent_cluster_id] = updated_parent


        return cluster


    # ========================================================================
    # CLUSTER ACCESS
    # ========================================================================


    def get_cluster(
        self,
        cluster_id: str,
    ) -> Cluster:
        try:
            return self._clusters[cluster_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            ) from exc


    def cluster_exists(
        self,
        cluster_id: str,
    ) -> bool:
        return cluster_id in self._clusters


    def all_clusters(
        self,
    ) -> Tuple[Cluster, ...]:
        return tuple(self._clusters.values())


    def cluster_count(self) -> int:
        return len(self._clusters)


    # ========================================================================
    # MULTI MEMBERSHIP
    # ========================================================================


    def assign_information_to_cluster(
        self,
        information_id: str,
        cluster_id: str,
        *,
        assigned_at: Optional[datetime] = None,
        context_note: Optional[str] = None,
    ) -> Membership:
        """
        InformationPiece'i kümeye bağlar.


        Aynı InformationPiece farklı kümelere bağlanabilir.


        Aynı information_id + cluster_id çifti ikinci kez eklenmez.
        """


        self._require_information(information_id)
        self._require_cluster(cluster_id)


        membership_key = (
            information_id,
            cluster_id,
        )


        if membership_key in self._memberships:
            raise ValueError(
                "Duplicate membership: "
                f"{information_id} -> {cluster_id}"
            )


        membership = Membership(
            information_id=information_id,
            cluster_id=cluster_id,
            assigned_at=assigned_at,
            context_note=context_note,
        )


        self._memberships.add(membership_key)


        cluster = self._clusters[cluster_id]


        if information_id not in cluster.member_information_ids:
            updated_cluster = replace(
                cluster,
                member_information_ids=(
                    *cluster.member_information_ids,
                    information_id,
                ),
            )


            self._clusters[cluster_id] = updated_cluster


        return membership


    def memberships_of(
        self,
        information_id: str,
    ) -> Tuple[Membership, ...]:
        """
        Bir InformationPiece'in tüm küme üyeliklerini döndürür.
        """


        return tuple(
            Membership(
                information_id=piece_id,
                cluster_id=cluster_id,
            )
            for piece_id, cluster_id in self._memberships
            if piece_id == information_id
        )


    def memberships_in_cluster(
        self,
        cluster_id: str,
    ) -> Tuple[Membership, ...]:
        self._require_cluster(cluster_id)


        return tuple(
            Membership(
                information_id=piece_id,
                cluster_id=cluster_id,
            )
            for piece_id, membership_cluster_id
            in self._memberships
            if membership_cluster_id == cluster_id
        )


    def clusters_for_information(
        self,
        information_id: str,
    ) -> Tuple[Cluster, ...]:
        """
        Bir InformationPiece'in ait olduğu tüm kümeler.
        """


        self._require_information(information_id)


        cluster_ids = {
            cluster_id
            for piece_id, cluster_id in self._memberships
            if piece_id == information_id
        }


        return tuple(
            self._clusters[cluster_id]
            for cluster_id in cluster_ids
        )


    # ========================================================================
    # INFORMATION RELATIONS
    # ========================================================================


    def add_relation(
        self,
        relation_id: str,
        source_information_id: str,
        target_information_id: str,
        relation_type: RelationType,
        *,
        state: RelationState = RelationState.ACTIVE,
        context_note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> Relation:
        """
        InformationPiece'ler arasındaki ilişkiyi kaydeder.


        Kaynak ve hedef bilgi parçaları gerçekten mevcut olmalıdır.


        Bu metod ilişkinin doğruluğunu veya gücünü değerlendirmez.
        """


        if not relation_id.strip():
            raise ValueError("relation_id cannot be empty.")


        if relation_id in self._relations:
            raise ValueError(
                f"Duplicate relation_id: {relation_id}"
            )


        self._require_information(source_information_id)
        self._require_information(target_information_id)


        if source_information_id == target_information_id:
            raise ValueError(
                "A relation cannot connect an information piece to itself."
            )


        relation = Relation(
            relation_id=relation_id,
            source_information_id=source_information_id,
            target_information_id=target_information_id,
            relation_type=relation_type,
            state=state,
            context_note=context_note,
            created_at=created_at,
            state_history=(),
        )


        self._relations[relation_id] = relation


        return relation


    def get_relation(
        self,
        relation_id: str,
    ) -> Relation:
        try:
            return self._relations[relation_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown relation_id: {relation_id}"
            ) from exc


    def all_relations(
        self,
    ) -> Tuple[Relation, ...]:
        return tuple(self._relations.values())


    def relations_for_information(
        self,
        information_id: str,
    ) -> Tuple[Relation, ...]:
        self._require_information(information_id)


        return tuple(
            relation
            for relation in self._relations.values()
            if (
                relation.source_information_id == information_id
                or relation.target_information_id == information_id
            )
        )


    def relation_count(self) -> int:
        return len(self._relations)


    # ========================================================================
    # RELATION STATE HISTORY
    # ========================================================================


    def update_relation_state(
        self,
        relation_id: str,
        new_state: RelationState,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Relation:
        """
        İlişki durumunu değiştirir.


        Önceki durum silinmez.
        """


        relation = self.get_relation(relation_id)


        if relation.state == new_state:
            return relation


        event = RelationStateEvent(
            event_id=self._next_event_id(
                "relation-state"
            ),
            relation_id=relation_id,
            previous_state=relation.state,
            new_state=new_state,
            occurred_at=(
                changed_at
                if changed_at is not None
                else datetime.utcnow()
            ),
            reason=reason,
        )


        updated = replace(
            relation,
            state=new_state,
            state_history=(
                *relation.state_history,
                event,
            ),
        )


        self._relations[relation_id] = updated


        return updated


    # ========================================================================
    # CLUSTER LIFECYCLE
    # ========================================================================


    def update_cluster_lifecycle(
        self,
        cluster_id: str,
        new_state: ClusterState,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Cluster:
        """
        Kümenin yaşam döngüsünü değiştirir.


        Önceki durum silinmez.


        CLOSED:
            Küme silinmez.


        REOPENED:
            Kapanmış bir kümenin yeniden aktif bağlama alınmasını
            temsil eder.


        Bu işlem hiçbir analitik önem veya değer anlamı taşımaz.
        """


        cluster = self.get_cluster(cluster_id)


        if cluster.state == new_state:
            return cluster


        event = ClusterLifecycleEvent(
            event_id=self._next_event_id(
                "cluster-state"
            ),
            cluster_id=cluster_id,
            previous_state=cluster.state,
            new_state=new_state,
            occurred_at=(
                changed_at
                if changed_at is not None
                else datetime.utcnow()
            ),
            reason=reason,
        )


        updated = replace(
            cluster,
            state=new_state,
            lifecycle_history=(
                *cluster.lifecycle_history,
                event,
            ),
        )


        self._clusters[cluster_id] = updated


        return updated


    def close_cluster(
        self,
        cluster_id: str,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Cluster:
        return self.update_cluster_lifecycle(
            cluster_id,
            ClusterState.CLOSED,
            changed_at=changed_at,
            reason=reason,
        )


    def reopen_cluster(
        self,
        cluster_id: str,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Cluster:
        return self.update_cluster_lifecycle(
            cluster_id,
            ClusterState.REOPENED,
            changed_at=changed_at,
            reason=reason,
        )


    # ========================================================================
    # CLUSTER RELATIONS — YATAY YAPILAR
    # ========================================================================


    def add_cluster_relation(
        self,
        relation_id: str,
        source_cluster_id: str,
        target_cluster_id: str,
        relation_type: ClusterRelationType,
        *,
        state: RelationState = RelationState.ACTIVE,
        context_note: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> ClusterRelation:
        """
        Hiyerarşik olmayan iki küme arasındaki ilişkiyi kaydeder.


        İlişkili kümeler zorla ana/alt yapıya sokulmaz.
        """


        if not relation_id.strip():
            raise ValueError(
                "cluster relation_id cannot be empty."
            )


        if relation_id in self._cluster_relations:
            raise ValueError(
                f"Duplicate cluster relation_id: {relation_id}"
            )


        self._require_cluster(source_cluster_id)
        self._require_cluster(target_cluster_id)


        if source_cluster_id == target_cluster_id:
            raise ValueError(
                "A cluster cannot be related to itself."
            )


        relation = ClusterRelation(
            relation_id=relation_id,
            source_cluster_id=source_cluster_id,
            target_cluster_id=target_cluster_id,
            relation_type=relation_type,
            state=state,
            context_note=context_note,
            created_at=created_at,
            state_history=(),
        )


        self._cluster_relations[relation_id] = relation


        return relation


    def get_cluster_relation(
        self,
        relation_id: str,
    ) -> ClusterRelation:
        try:
            return self._cluster_relations[relation_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown cluster relation_id: {relation_id}"
            ) from exc


    def all_cluster_relations(
        self,
    ) -> Tuple[ClusterRelation, ...]:
        return tuple(self._cluster_relations.values())


    def update_cluster_relation_state(
        self,
        relation_id: str,
        new_state: RelationState,
        *,
        changed_at: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> ClusterRelation:
        """
        Küme ilişkisinin durumunu değiştirir.


        Önceki durum korunur.
        """


        relation = self.get_cluster_relation(
            relation_id
        )


        if relation.state == new_state:
            return relation


        event = RelationStateEvent(
            event_id=self._next_event_id(
                "cluster-relation-state"
            ),
            relation_id=relation_id,
            previous_state=relation.state,
            new_state=new_state,
            occurred_at=(
                changed_at
                if changed_at is not None
                else datetime.utcnow()
            ),
            reason=reason,
        )


        updated = replace(
            relation,
            state=new_state,
            state_history=(
                *relation.state_history,
                event,
            ),
        )


        self._cluster_relations[relation_id] = updated


        return updated


    # ========================================================================
    # CONTEXTUAL CONTINUITY
    # ========================================================================


    def record_cluster_axes(
        self,
        cluster_id: str,
        axes: Iterable[ClusterAxis],
    ) -> Cluster:
        """
        Küme için mevcut bağlamsal süreklilik eksenlerini kaydeder.


        Bu metod yeni bir analiz veya skor üretmez.
        Sadece sağlanan bağlamsal yapıyı korur.


        Kelime benzerliği burada kullanılmaz.
        """


        cluster = self.get_cluster(cluster_id)


        merged = tuple(
            dict.fromkeys(
                (
                    *cluster.shared_axes,
                    *tuple(axes),
                )
            )
        )


        updated = replace(
            cluster,
            shared_axes=merged,
        )


        self._clusters[cluster_id] = updated


        return updated


    def has_contextual_continuity(
        self,
        cluster_id: str,
    ) -> bool:
        """
        Kümeye kaydedilmiş en az bir anlamlı bağlamsal süreklilik
        ekseni bulunup bulunmadığını kontrol eder.


        Bu bir güven / önem / doğruluk skoru değildir.
        """


        cluster = self.get_cluster(cluster_id)


        return bool(cluster.shared_axes)


    # ========================================================================
    # PROVENANCE PRESERVATION
    # ========================================================================


    def provenance_for_information(
        self,
        information_id: str,
    ) -> Mapping[str, Any]:
        """
        5. Bölüm InformationPiece içindeki provenance / source
        bilgilerini değiştirmeden dışarı verir.


        Farklı 5. Bölüm modellerinin isimleri için güvenli erişim
        yardımcıları kullanılır.


        Burada provenance hakkında yeni yorum üretilmez.
        """


        piece = self.get_information_piece(
            information_id
        )


        result: dict[str, Any] = {
            "information_id": information_id,
        }


        for attribute in (
            "source",
            "provenance",
            "source_id",
            "original_source_id",
            "channel",
            "production_time",
            "reference_period",
        ):
            if hasattr(piece, attribute):
                result[attribute] = getattr(
                    piece,
                    attribute,
                )


        return result


    # ========================================================================
    # 6 -> 7 OUTPUT
    # ========================================================================


    def state(self) -> YogurmaState:
        """
        7. Bölüme devredilecek analize hazır ilişkisel yapı.


        Bu metod:
            - analiz yapmaz,
            - hesaplama yapmaz,
            - değerlendirme yapmaz,
            - ağırlıklandırma yapmaz,
            - ranking yapmaz.
        """


        return YogurmaState(
            clusters=tuple(
                self._clusters.values()
            ),
            relations=tuple(
                self._relations.values()
            ),
            cluster_relations=tuple(
                self._cluster_relations.values()
            ),
            memberships=tuple(
                Membership(
                    information_id=information_id,
                    cluster_id=cluster_id,
                )
                for information_id, cluster_id
                in self._memberships
            ),
        )


    # ========================================================================
    # INTEGRITY VALIDATION
    # ========================================================================


    def validate_integrity(self) -> None:
        """
        Yapısal bütünlük kontrolü.


        Bu kontrol:
            - truth,
            - confidence,
            - reliability,
            - evidence strength,
            - ranking,
            - weighting


        hesaplamaz.


        Yalnızca referansların ve yapıların tamamlığını kontrol eder.
        """


        # --------------------------------------------------------------------
        # Cluster integrity
        # --------------------------------------------------------------------


        for cluster in self._clusters.values():


            if (
                cluster.parent_cluster_id is not None
                and cluster.parent_cluster_id
                not in self._clusters
            ):
                raise ValueError(
                    "Cluster references missing parent: "
                    f"{cluster.cluster_id}"
                )


            if cluster.cluster_id in cluster.child_cluster_ids:
                raise ValueError(
                    "Cluster cannot contain itself as child: "
                    f"{cluster.cluster_id}"
                )


            for child_id in cluster.child_cluster_ids:


                if child_id not in self._clusters:
                    raise ValueError(
                        "Cluster references missing child: "
                        f"{child_id}"
                    )


                child = self._clusters[child_id]


                if child.parent_cluster_id != cluster.cluster_id:
                    raise ValueError(
                        "Parent/child cluster reference mismatch: "
                        f"{cluster.cluster_id} -> {child_id}"
                    )


            for information_id in cluster.member_information_ids:


                if information_id not in self._pieces:
                    raise ValueError(
                        "Cluster references missing InformationPiece: "
                        f"{information_id}"
                    )


                if (
                    information_id,
                    cluster.cluster_id,
                ) not in self._memberships:
                    raise ValueError(
                        "Cluster membership is missing reverse reference: "
                        f"{information_id} -> {cluster.cluster_id}"
                    )


        # --------------------------------------------------------------------
        # Membership integrity
        # --------------------------------------------------------------------


        for information_id, cluster_id in self._memberships:


            if information_id not in self._pieces:
                raise ValueError(
                    "Membership references missing InformationPiece: "
                    f"{information_id}"
                )


            if cluster_id not in self._clusters:
                raise ValueError(
                    "Membership references missing Cluster: "
                    f"{cluster_id}"
                )


            if (
                information_id
                not in self._clusters[
                    cluster_id
                ].member_information_ids
            ):
                raise ValueError(
                    "Membership reverse reference missing: "
                    f"{information_id} -> {cluster_id}"
                )


        # --------------------------------------------------------------------
        # Information relation integrity
        # --------------------------------------------------------------------


        for relation in self._relations.values():


            if relation.source_information_id not in self._pieces:
                raise ValueError(
                    "Relation references missing source InformationPiece: "
                    f"{relation.relation_id}"
                )


            if relation.target_information_id not in self._pieces:
                raise ValueError(
                    "Relation references missing target InformationPiece: "
                    f"{relation.relation_id}"
                )


            if (
                relation.source_information_id
                == relation.target_information_id
            ):
                raise ValueError(
                    "Relation cannot self-reference: "
                    f"{relation.relation_id}"
                )


            for event in relation.state_history:


                if event.relation_id != relation.relation_id:
                    raise ValueError(
                        "Relation state history reference mismatch: "
                        f"{relation.relation_id}"
                    )


                if event.new_state is None:
                    raise ValueError(
                        "Relation state history contains empty state: "
                        f"{relation.relation_id}"
                    )


        # --------------------------------------------------------------------
        # Cluster relation integrity
        # --------------------------------------------------------------------


        for relation in self._cluster_relations.values():


            if relation.source_cluster_id not in self._clusters:
                raise ValueError(
                    "Cluster relation references missing source Cluster: "
                    f"{relation.relation_id}"
                )


            if relation.target_cluster_id not in self._clusters:
                raise ValueError(
                    "Cluster relation references missing target Cluster: "
                    f"{relation.relation_id}"
                )


            if (
                relation.source_cluster_id
                == relation.target_cluster_id
            ):
                raise ValueError(
                    "Cluster relation cannot self-reference: "
                    f"{relation.relation_id}"
                )


        # --------------------------------------------------------------------
        # Lifecycle history integrity
        # --------------------------------------------------------------------


        for cluster in self._clusters.values():


            for event in cluster.lifecycle_history:


                if event.cluster_id != cluster.cluster_id:
                    raise ValueError(
                        "Cluster lifecycle history reference mismatch: "
                        f"{cluster.cluster_id}"
                    )


                if event.new_state is None:
                    raise ValueError(
                        "Cluster lifecycle event has no new state: "
                        f"{cluster.cluster_id}"
                    )


    # ========================================================================
    # INTERNAL VALIDATION HELPERS
    # ========================================================================


    def _require_information(
        self,
        information_id: str,
    ) -> None:
        if information_id not in self._pieces:
            raise KeyError(
                f"Unknown information_id: {information_id}"
            )


    def _require_cluster(
        self,
        cluster_id: str,
    ) -> None:
        if cluster_id not in self._clusters:
            raise KeyError(
                f"Unknown cluster_id: {cluster_id}"
            )


    @staticmethod
    def _extract_information_id(
        piece: Any,
    ) -> str:
        """
        5. Bölümdeki InformationPiece'in ID alanını okur.


        Desteklenen ana biçimler:
            information_id
            id


        Burada yeni bilgi üretilmez.
        """


        if hasattr(piece, "information_id"):
            information_id = getattr(
                piece,
                "information_id",
            )


        elif hasattr(piece, "id"):
            information_id = getattr(
                piece,
                "id",
            )


        else:
            raise TypeError(
                "5. Bölüm InformationPiece must expose "
                "'information_id' or 'id'."
            )


        if not isinstance(
            information_id,
            str,
        ) or not information_id.strip():
            raise ValueError(
                "InformationPiece ID must be a non-empty string."
            )


        return information_id


    @staticmethod
    def _next_event_id(
        prefix: str,
    ) -> str:
        """
        Deterministik olmayan fakat yalnızca tarihsel olay kaydı için
        kullanılan lokal ID üretimi.


        Bu ID herhangi bir epistemik anlam taşımaz.
        """


        import uuid


        return f"{prefix}:{uuid.uuid4().hex}"




# ============================================================================
# 14. YASAKLI 6. BÖLÜM SORUMLULUKLARI
# ============================================================================




FORBIDDEN_YOGURMA_FIELDS = frozenset(
    {
        "trust_score",
        "truth_score",
        "confidence",
        "reliability",
        "evidence_strength",
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
        "trade_decision",
        "risk_decision",
        "forecast",
        "prediction",
        "consensus",
    }
)




FORBIDDEN_YOGURMA_OPERATIONS = frozenset(
    {
        "score",
        "calculate_confidence",
        "calculate_reliability",
        "calculate_truth",
        "calculate_weight",
        "rank",
        "predict",
        "forecast",
        "decide",
        "generate_signal",
        "generate_bias",
    }
)




# ============================================================================
# 15. STATIC BOUNDARY VALIDATION
# ============================================================================




def validate_6_boundary() -> None:
    """
    6. Bölümün karar üretmeyen sınırını doğrular.


    Bu fonksiyon analiz yapmaz.
    """


    dataclasses_to_check = (
        Cluster,
        Relation,
        ClusterRelation,
        Membership,
    )


    for cls in dataclasses_to_check:


        fields = getattr(
            cls,
            "__dataclass_fields__",
            {},
        )


        for forbidden in FORBIDDEN_YOGURMA_FIELDS:


            if forbidden in fields:
                raise AssertionError(
                    f"Forbidden 6. Bölüm field found in "
                    f"{cls.__name__}: {forbidden}"
                )


    motor_methods = {
        name
        for name in dir(YogurmaMotoru)
        if not name.startswith("_")
        and callable(
            getattr(
                YogurmaMotoru,
                name,
            )
        )
    }


    leaked_operations = (
        motor_methods
        & FORBIDDEN_YOGURMA_OPERATIONS
    )


    if leaked_operations:
        raise AssertionError(
            "Forbidden 6. Bölüm operations exposed: "
            f"{sorted(leaked_operations)}"
        )




# ============================================================================
# 16. SELF TEST
# ============================================================================




def validate_6() -> None:
    """
    6. Bölüm yapısal validation.


    Testler yalnızca yapısal bütünlüğü kontrol eder.
    """


    validate_6_boundary()


    motor = YogurmaMotoru()


    # ------------------------------------------------------------------------
    # 5. Bölümden örnek InformationPiece yerine basit test nesnesi.
    #
    # Gerçek çalışma sırasında 5. Bölüm InformationPiece nesnesi doğrudan
    # register_information_piece() ile kullanılacaktır.
    # ------------------------------------------------------------------------


    @dataclass(frozen=True)
    class TestInformationPiece:
        information_id: str
        content: str


    info1 = TestInformationPiece(
        information_id="info-001",
        content="CTA information A",
    )


    info2 = TestInformationPiece(
        information_id="info-002",
        content="CTA information B",
    )


    info3 = TestInformationPiece(
        information_id="info-003",
        content="CTA information C",
    )


    motor.register_information_piece(info1)
    motor.register_information_piece(info2)
    motor.register_information_piece(info3)


    assert (
        len(motor.all_information_pieces())
        == 3
    )


    # ------------------------------------------------------------------------
    # Ana küme
    # ------------------------------------------------------------------------


    root = motor.create_cluster(
        cluster_id="cluster-root",
        cluster_type="event",
        shared_axes=(
            ClusterAxis.COMMON_EVENT,
            ClusterAxis.COMMON_REFERENCE_PERIOD,
        ),
        created_at=datetime(
            2026,
            1,
            1,
        ),
    )


    assert root.state == ClusterState.FORMING


    # ------------------------------------------------------------------------
    # Alt küme
    # ------------------------------------------------------------------------


    child = motor.create_cluster(
        cluster_id="cluster-child",
        cluster_type="event_phase",
        shared_axes=(
            ClusterAxis.COMMON_EVENT,
            ClusterAxis.COMMON_ACTOR,
        ),
        parent_cluster_id="cluster-root",
        created_at=datetime(
            2026,
            1,
            2,
        ),
    )


    assert (
        child.parent_cluster_id
        == "cluster-root"
    )


    assert (
        "cluster-child"
        in motor.get_cluster(
            "cluster-root"
        ).child_cluster_ids
    )


    # ------------------------------------------------------------------------
    # Çoklu üyelik
    # ------------------------------------------------------------------------


    motor.assign_information_to_cluster(
        "info-001",
        "cluster-root",
    )


    motor.assign_information_to_cluster(
        "info-001",
        "cluster-child",
    )


    motor.assign_information_to_cluster(
        "info-002",
        "cluster-root",
    )


    assert len(
        motor.clusters_for_information(
            "info-001"
        )
    ) == 2


    # ------------------------------------------------------------------------
    # İlişki
    # ------------------------------------------------------------------------


    relation = motor.add_relation(
        relation_id="relation-001",
        source_information_id="info-001",
        target_information_id="info-002",
        relation_type=RelationType.SAME_EVENT_DIFFERENT_ANGLE,
        state=RelationState.ACTIVE,
        context_note="Same event, different angle.",
        created_at=datetime(
            2026,
            1,
            3,
        ),
    )


    assert (
        relation.state
        == RelationState.ACTIVE
    )


    # ------------------------------------------------------------------------
    # İlişki durum değişikliği
    # ------------------------------------------------------------------------


    updated_relation = motor.update_relation_state(
        "relation-001",
        RelationState.DISPUTED,
        changed_at=datetime(
            2026,
            1,
            4,
        ),
        reason="Relationship became disputed.",
    )


    assert (
        updated_relation.state
        == RelationState.DISPUTED
    )


    assert len(
        updated_relation.state_history
    ) == 1


    assert (
        updated_relation.state_history[0]
        .previous_state
        == RelationState.ACTIVE
    )


    # ------------------------------------------------------------------------
    # Yatay küme ilişkisi
    # ------------------------------------------------------------------------


    cluster_relation = motor.add_cluster_relation(
        relation_id="cluster-relation-001",
        source_cluster_id="cluster-root",
        target_cluster_id="cluster-child",
        relation_type=ClusterRelationType.CONTINUATION,
        state=RelationState.ACTIVE,
    )


    assert (
        cluster_relation.state
        == RelationState.ACTIVE
    )


    # ------------------------------------------------------------------------
    # Küme lifecycle
    # ------------------------------------------------------------------------


    closed = motor.close_cluster(
        "cluster-root",
        changed_at=datetime(
            2026,
            1,
            5,
        ),
        reason="Reference event closed.",
    )


    assert (
        closed.state
        == ClusterState.CLOSED
    )


    assert len(
        closed.lifecycle_history
    ) == 1


    reopened = motor.reopen_cluster(
        "cluster-root",
        changed_at=datetime(
            2026,
            1,
            6,
        ),
        reason="Directly related information arrived.",
    )


    assert (
        reopened.state
        == ClusterState.REOPENED
    )


    assert len(
        reopened.lifecycle_history
    ) == 2


    # ------------------------------------------------------------------------
    # Integrity
    # ------------------------------------------------------------------------


    motor.validate_integrity()


    # ------------------------------------------------------------------------
    # 6 -> 7 output
    # ------------------------------------------------------------------------


    state = motor.state()


    assert len(state.clusters) == 2
    assert len(state.relations) == 1
    assert len(state.cluster_relations) == 1
    assert len(state.memberships) == 3


    # ------------------------------------------------------------------------
    # Provenance pass-through
    # ------------------------------------------------------------------------


    provenance = motor.provenance_for_information(
        "info-001"
    )


    assert (
        provenance["information_id"]
        == "info-001"
    )




# ============================================================================
# 17. FINAL ARCHITECTURAL PRINCIPLE
# ============================================================================




YOGURMA_FINAL_PRINCIPLE = (
    "Yoğurma Motoru, bilgiyi değiştirmeden; kaynak kökenini, "
    "statüsünü, zamanını ve bağlamını koruyarak bilgileri anlamlı "
    "kümeler ve ilişkisel yapılar hâline getirir. Bilgiyi tek bir "
    "kümeye hapsetmez; gerektiğinde çoklu üyeliği, ana/alt yapıları "
    "ve yatay ilişkili kümeleri korur. Zaman içinde gelişen olayların "
    "sürekliliğini ve kümelerin yaşam döngüsünü izler; kapanan veya "
    "değişen yapıları silmez. İlişkilerin mevcut ve geçmiş durumlarını "
    "korur ancak bunların gücünü, doğruluğunu, güvenilirliğini veya "
    "önemini değerlendirmez. Yoğurma Motoru bilgiyi analiz etmez, "
    "hesaplamaz, sentezlemez, tahmin etmez ve karar üretmez. Çıktısı, "
    "7. Bölüm — Analiz / Hesaplama / Değerlendirme için analize hazır "
    "ilişkili ve bağlamsal bilgi yapılarıdır."
)




# ============================================================================
# 18. MAIN
# ============================================================================




if __name__ == "__main__":
    validate_6()


    print(
        "6. BÖLÜM — YOĞURMA MOTORU"
    )
    print("=" * 72)


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÜRETMEZ"
    )


    print(
        "Validation: PASSED"
    )


    print(
        "=" * 72
    )


    print(
        YOGURMA_FINAL_PRINCIPLE
    )


