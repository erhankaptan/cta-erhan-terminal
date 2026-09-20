ERHAN / CTA TERMINALI


"""
ERHAN / CTA TERMINAL
6. BÃ–LÃœM â€” YOÄžURMA MOTORU
FINAL CODE


READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ


AmaÃ§
-----
5. BÃ¶lÃ¼m â€” Bilgi Havuzu iÃ§inde korunmuÅŸ InformationPiece kayÄ±tlarÄ±nÄ±:


- anlamlÄ± baÄŸlamsal kÃ¼meler halinde yapÄ±landÄ±rmak,
- Ã§oklu Ã¼yeliÄŸi korumak,
- ana / alt kÃ¼me iliÅŸkilerini korumak,
- yatay iliÅŸkili kÃ¼meleri korumak,
- bilgi parÃ§alarÄ± arasÄ±ndaki iliÅŸkileri yapÄ±landÄ±rmak,
- provenance / bilgi kÃ¶kÃ¼nÃ¼ korumak,
- zaman ve baÄŸlam sÃ¼rekliliÄŸini korumak,
- iliÅŸki ve kÃ¼me yaÅŸam dÃ¶ngÃ¼sÃ¼ geÃ§miÅŸini korumak,
- 7. BÃ¶lÃ¼m iÃ§in analize hazÄ±r yapÄ±lar Ã¼retmek


amacÄ±yla kullanÄ±r.


Bu modÃ¼l:


- analiz yapmaz,
- hesaplama yapmaz,
- deÄŸerlendirme yapmaz,
- confidence Ã¼retmez,
- trust score Ã¼retmez,
- truth score Ã¼retmez,
- evidence strength Ã¼retmez,
- weighting yapmaz,
- ranking yapmaz,
- consensus Ã¼retmez,
- forecast Ã¼retmez,
- prediction Ã¼retmez,
- piyasa yÃ¶nÃ¼ tahmin etmez,
- BUY / SELL Ã¼retmez,
- trade signal Ã¼retmez,
- final CTA bias Ã¼retmez,
- risk kararÄ± Ã¼retmez,
- kullanÄ±cÄ± adÄ±na nihai karar vermez.


Ã–NEMLÄ°
-------
Bu modÃ¼l 5. BÃ¶lÃ¼m'deki InformationPiece sÄ±nÄ±fÄ±nÄ± yeniden tanÄ±mlamaz.
5. BÃ¶lÃ¼mden gelen bilgi nesnelerini doÄŸrudan kullanÄ±r.


6. BÃ¶lÃ¼mde kÃ¼me sÄ±nÄ±rÄ± "yeni bir tahmin/puanlama metodolojisi"
ile hesaplanmaz. KÃ¼me Ã¼yeliÄŸi, saÄŸlanan baÄŸlamsal sÃ¼reklilik
eksenlerinin kaydedilmesi ve korunmasÄ± Ã¼zerinden yapÄ±landÄ±rÄ±lÄ±r.


7. BÃ¶lÃ¼m:
    Analiz / Hesaplama / DeÄŸerlendirme


8. BÃ¶lÃ¼m:
    CTA Synthesis / SonuÃ§


9. BÃ¶lÃ¼m:
    TarihÃ§e / HafÄ±za
"""


from __future__ import annotations


from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, Tuple




# ============================================================================
# 1. Ä°LÄ°ÅžKÄ° DURUMLARI
# ============================================================================




class RelationState(str, Enum):
    """
    Ä°liÅŸkinin mevcut / tarihsel durumu.


    Bunlar:
        - confidence
        - trust
        - truth
        - reliability
        - evidence strength


    deÄŸildir.
    """


    ACTIVE = "active"
    UNCERTAIN = "uncertain"
    DISPUTED = "disputed"
    WEAKENED = "weakened"
    INVALIDATED = "invalidated"
    UNRESOLVED = "unresolved"




# ============================================================================
# 2. KÃœME YAÅžAM DÃ–NGÃœSÃœ
# ============================================================================




class ClusterState(str, Enum):
    """
    KÃ¼menin yaÅŸam dÃ¶ngÃ¼sÃ¼.
    """


    FORMING = "forming"
    DEVELOPING = "developing"
    UPDATED = "updated"
    CLOSED = "closed"
    REOPENED = "reopened"




# ============================================================================
# 3. KÃœME SINIRI EKSENLERÄ°
# ============================================================================




class ClusterAxis(str, Enum):
    """
    AnlamlÄ± baÄŸlamsal sÃ¼reklilik eksenleri.


    Bu eksenlerin bulunmasÄ±, kÃ¼menin Ã¶nemini veya doÄŸruluÄŸunu
    gÃ¶stermez.


    Kelime benzerliÄŸi bu enum iÃ§inde bilinÃ§li olarak bulunmaz.
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
# 4. Ä°LÄ°ÅžKÄ° TÄ°PLERÄ°
# ============================================================================




class RelationType(str, Enum):
    """
    6. BÃ¶lÃ¼mde korunabilecek iliÅŸki tÃ¼rleri.


    Ä°liÅŸkinin varlÄ±ÄŸÄ± ile iliÅŸkinin analitik anlamÄ± birbirinden
    ayrÄ±dÄ±r. Analitik deÄŸerlendirme 7. BÃ¶lÃ¼me aittir.
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
# 5. KÃœME Ä°LÄ°ÅžKÄ° TÄ°PLERÄ°
# ============================================================================




class ClusterRelationType(str, Enum):
    """
    HiyerarÅŸik olmayan kÃ¼meler arasÄ±ndaki yatay iliÅŸki.


    Ana/alt iliÅŸkisi deÄŸildir.
    """


    RELATED = "related"
    CONTINUATION = "continuation"
    DIFFERENT_ANGLE = "different_angle"
    CONNECTED_EVENT = "connected_event"
    RELATED_CONTEXT = "related_context"




# ============================================================================
# 6. KÃœME YAÅžAM DÃ–NGÃœSÃœ GEÃ‡MÄ°ÅžÄ°
# ============================================================================




@dataclass(frozen=True)
class ClusterLifecycleEvent:
    """
    KÃ¼menin yaÅŸam dÃ¶ngÃ¼sÃ¼ndeki tarihsel bir durum deÄŸiÅŸimi.


    Eski durum silinmez.
    """


    event_id: str
    cluster_id: str


    previous_state: Optional[ClusterState]
    new_state: ClusterState


    occurred_at: datetime
    reason: Optional[str] = None




# ============================================================================
# 7. Ä°LÄ°ÅžKÄ° DURUM GEÃ‡MÄ°ÅžÄ°
# ============================================================================




@dataclass(frozen=True)
class RelationStateEvent:
    """
    Bir iliÅŸkinin durum deÄŸiÅŸiminin tarihsel kaydÄ±.
    """


    event_id: str
    relation_id: str


    previous_state: Optional[RelationState]
    new_state: RelationState


    occurred_at: datetime
    reason: Optional[str] = None




# ============================================================================
# 8. BÄ°LGÄ° PARÃ‡ASI Ä°LÄ°ÅžKÄ°SÄ°
# ============================================================================




@dataclass(frozen=True)
class Relation:
    """
    Ä°ki InformationPiece arasÄ±ndaki iliÅŸkisel baÄŸ.


    Burada yalnÄ±zca iliÅŸki ve onun tarihsel durumu korunur.


    Ä°liÅŸkinin:
        - gÃ¼cÃ¼,
        - doÄŸruluÄŸu,
        - gÃ¼venilirliÄŸi,
        - Ã¶nemi,
        - aÄŸÄ±rlÄ±ÄŸÄ±


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
# 9. KÃœME Ä°LÄ°ÅžKÄ°SÄ°
# ============================================================================




@dataclass(frozen=True)
class ClusterRelation:
    """
    Ä°ki kÃ¼me arasÄ±ndaki yatay iliÅŸki.


    Bu iliÅŸki ana/alt hiyerarÅŸi deÄŸildir.


    HiyerarÅŸik olmayan iliÅŸkili kÃ¼meleri zorla ana/alt yapÄ±ya
    sokmamak iÃ§in kullanÄ±lÄ±r.
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
# 10. KÃœME
# ============================================================================




@dataclass(frozen=True)
class Cluster:
    """
    6. BÃ¶lÃ¼m bilgi kÃ¼mesi.


    KÃ¼me:
        - baÄŸlamsal sÃ¼reklilik taÅŸÄ±r,
        - InformationPiece ID'lerini referanslar,
        - Ã§oklu Ã¼yeliÄŸi destekler,
        - ana/alt yapÄ±yÄ± destekler,
        - yatay iliÅŸkileri destekler,
        - yaÅŸam dÃ¶ngÃ¼sÃ¼ geÃ§miÅŸini korur.


    KÃ¼me bir Ã¶nem, doÄŸruluk veya gÃ¼ven sÄ±ralamasÄ± deÄŸildir.
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
# 11. Ã‡OKLU ÃœYELÄ°K
# ============================================================================




@dataclass(frozen=True)
class Membership:
    """
    InformationPiece -> Cluster Ã¼yeliÄŸi.


    AynÄ± InformationPiece birden fazla Cluster iÃ§inde bulunabilir.


    InformationPiece kopyalanmaz.
    """


    information_id: str
    cluster_id: str


    assigned_at: Optional[datetime] = None


    context_note: Optional[str] = None




# ============================================================================
# 12. YOÄžURMA DURUMU
# ============================================================================




@dataclass(frozen=True)
class YogurmaState:
    """
    YoÄŸurma Motoru'nun mevcut yapÄ±sal durumu.


    Buradaki nesneler analiz sonucu deÄŸildir.
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
# 13. YOÄžURMA MOTORU
# ============================================================================




class YogurmaMotoru:
    """
    6. BÃ¶lÃ¼m â€” YoÄŸurma Motoru.


    5. BÃ¶lÃ¼mdeki InformationPiece nesnelerini doÄŸrudan referanslar.


    SorumluluklarÄ±:
        - baÄŸlamsal kÃ¼meler,
        - Ã§oklu Ã¼yelik,
        - ana/alt kÃ¼meler,
        - yatay iliÅŸkili kÃ¼meler,
        - bilgi parÃ§alarÄ± arasÄ± iliÅŸkiler,
        - provenance referanslarÄ±nÄ±n korunmasÄ±,
        - iliÅŸki geÃ§miÅŸi,
        - kÃ¼me yaÅŸam dÃ¶ngÃ¼sÃ¼.


    SorumluluklarÄ± DEÄžÄ°LDÄ°R:
        - analiz,
        - hesaplama,
        - deÄŸerlendirme,
        - skor,
        - aÄŸÄ±rlÄ±k,
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
        # 5. BÃ¶lÃ¼mden gelen gerÃ§ek bilgi parÃ§alarÄ±.
        #
        # Burada InformationPiece yeniden tanÄ±mlanmaz.
        self._pieces: dict[str, Any] = {}


        self._clusters: dict[str, Cluster] = {}


        self._relations: dict[str, Relation] = {}


        self._cluster_relations: dict[
            str,
            ClusterRelation,
        ] = {}


        self._memberships: set[tuple[str, str]] = set()


    # ========================================================================
    # INFORMATION PIECES â€” 5 -> 6
    # ========================================================================


    def register_information_piece(
        self,
        piece: Any,
    ) -> None:
        """
        5. BÃ¶lÃ¼m InformationPiece nesnesini 6. BÃ¶lÃ¼me baÄŸlar.


        AynÄ± information ID ikinci kez gelirse eski kayÄ±t sessizce
        ezilmez.


        Bu modÃ¼l InformationPiece iÃ§eriÄŸini deÄŸiÅŸtirmez.
        """


        information_id = self._extract_information_id(piece)


        if information_id in self._pieces:
            existing = self._pieces[information_id]


            if existing is piece:
                return


            raise ValueError(
                f"Duplicate information_id in 6. BÃ¶lÃ¼m: "
                f"{information_id}"
            )


        self._pieces[information_id] = piece


    def register_information_pieces(
        self,
        pieces: Iterable[Any],
    ) -> None:
        """
        Birden fazla 5. BÃ¶lÃ¼m InformationPiece kaydÄ±nÄ± ekler.
        """


        for piece in pieces:
            self.register_information_piece(piece)


    def get_information_piece(
        self,
        information_id: str,
    ) -> Any:
        """
        KayÄ±tlÄ± InformationPiece dÃ¶ndÃ¼rÃ¼r.
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
        Yeni kÃ¼me oluÅŸturur.


        parent_cluster_id verilmiÅŸse parent'Ä±n gerÃ§ekten mevcut olmasÄ±
        gerekir.


        Bu metod yalnÄ±zca saÄŸlanan baÄŸlamsal eksenleri kaydeder.
        Kelime benzerliÄŸine dayalÄ± otomatik kÃ¼meleme yapmaz.
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
        InformationPiece'i kÃ¼meye baÄŸlar.


        AynÄ± InformationPiece farklÄ± kÃ¼melere baÄŸlanabilir.


        AynÄ± information_id + cluster_id Ã§ifti ikinci kez eklenmez.
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
        Bir InformationPiece'in tÃ¼m kÃ¼me Ã¼yeliklerini dÃ¶ndÃ¼rÃ¼r.
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
        Bir InformationPiece'in ait olduÄŸu tÃ¼m kÃ¼meler.
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
        InformationPiece'ler arasÄ±ndaki iliÅŸkiyi kaydeder.


        Kaynak ve hedef bilgi parÃ§alarÄ± gerÃ§ekten mevcut olmalÄ±dÄ±r.


        Bu metod iliÅŸkinin doÄŸruluÄŸunu veya gÃ¼cÃ¼nÃ¼ deÄŸerlendirmez.
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
        Ä°liÅŸki durumunu deÄŸiÅŸtirir.


        Ã–nceki durum silinmez.
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
        KÃ¼menin yaÅŸam dÃ¶ngÃ¼sÃ¼nÃ¼ deÄŸiÅŸtirir.


        Ã–nceki durum silinmez.


        CLOSED:
            KÃ¼me silinmez.


        REOPENED:
            KapanmÄ±ÅŸ bir kÃ¼menin yeniden aktif baÄŸlama alÄ±nmasÄ±nÄ±
            temsil eder.


        Bu iÅŸlem hiÃ§bir analitik Ã¶nem veya deÄŸer anlamÄ± taÅŸÄ±maz.
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
    # CLUSTER RELATIONS â€” YATAY YAPILAR
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
        HiyerarÅŸik olmayan iki kÃ¼me arasÄ±ndaki iliÅŸkiyi kaydeder.


        Ä°liÅŸkili kÃ¼meler zorla ana/alt yapÄ±ya sokulmaz.
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
        KÃ¼me iliÅŸkisinin durumunu deÄŸiÅŸtirir.


        Ã–nceki durum korunur.
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
        KÃ¼me iÃ§in mevcut baÄŸlamsal sÃ¼reklilik eksenlerini kaydeder.


        Bu metod yeni bir analiz veya skor Ã¼retmez.
        Sadece saÄŸlanan baÄŸlamsal yapÄ±yÄ± korur.


        Kelime benzerliÄŸi burada kullanÄ±lmaz.
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
        KÃ¼meye kaydedilmiÅŸ en az bir anlamlÄ± baÄŸlamsal sÃ¼reklilik
        ekseni bulunup bulunmadÄ±ÄŸÄ±nÄ± kontrol eder.


        Bu bir gÃ¼ven / Ã¶nem / doÄŸruluk skoru deÄŸildir.
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
        5. BÃ¶lÃ¼m InformationPiece iÃ§indeki provenance / source
        bilgilerini deÄŸiÅŸtirmeden dÄ±ÅŸarÄ± verir.


        FarklÄ± 5. BÃ¶lÃ¼m modellerinin isimleri iÃ§in gÃ¼venli eriÅŸim
        yardÄ±mcÄ±larÄ± kullanÄ±lÄ±r.


        Burada provenance hakkÄ±nda yeni yorum Ã¼retilmez.
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
        7. BÃ¶lÃ¼me devredilecek analize hazÄ±r iliÅŸkisel yapÄ±.


        Bu metod:
            - analiz yapmaz,
            - hesaplama yapmaz,
            - deÄŸerlendirme yapmaz,
            - aÄŸÄ±rlÄ±klandÄ±rma yapmaz,
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
        YapÄ±sal bÃ¼tÃ¼nlÃ¼k kontrolÃ¼.


        Bu kontrol:
            - truth,
            - confidence,
            - reliability,
            - evidence strength,
            - ranking,
            - weighting


        hesaplamaz.


        YalnÄ±zca referanslarÄ±n ve yapÄ±larÄ±n tamamlÄ±ÄŸÄ±nÄ± kontrol eder.
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
        5. BÃ¶lÃ¼mdeki InformationPiece'in ID alanÄ±nÄ± okur.


        Desteklenen ana biÃ§imler:
            information_id
            id


        Burada yeni bilgi Ã¼retilmez.
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
                "5. BÃ¶lÃ¼m InformationPiece must expose "
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
        Deterministik olmayan fakat yalnÄ±zca tarihsel olay kaydÄ± iÃ§in
        kullanÄ±lan lokal ID Ã¼retimi.


        Bu ID herhangi bir epistemik anlam taÅŸÄ±maz.
        """


        import uuid


        return f"{prefix}:{uuid.uuid4().hex}"




# ============================================================================
# 14. YASAKLI 6. BÃ–LÃœM SORUMLULUKLARI
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
    6. BÃ¶lÃ¼mÃ¼n karar Ã¼retmeyen sÄ±nÄ±rÄ±nÄ± doÄŸrular.


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
                    f"Forbidden 6. BÃ¶lÃ¼m field found in "
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
            "Forbidden 6. BÃ¶lÃ¼m operations exposed: "
            f"{sorted(leaked_operations)}"
        )




# ============================================================================
# 16. SELF TEST
# ============================================================================




def validate_6() -> None:
    """
    6. BÃ¶lÃ¼m yapÄ±sal validation.


    Testler yalnÄ±zca yapÄ±sal bÃ¼tÃ¼nlÃ¼ÄŸÃ¼ kontrol eder.
    """


    validate_6_boundary()


    motor = YogurmaMotoru()


    # ------------------------------------------------------------------------
    # 5. BÃ¶lÃ¼mden Ã¶rnek InformationPiece yerine basit test nesnesi.
    #
    # GerÃ§ek Ã§alÄ±ÅŸma sÄ±rasÄ±nda 5. BÃ¶lÃ¼m InformationPiece nesnesi doÄŸrudan
    # register_information_piece() ile kullanÄ±lacaktÄ±r.
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
    # Ana kÃ¼me
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
    # Alt kÃ¼me
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
    # Ã‡oklu Ã¼yelik
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
    # Ä°liÅŸki
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
    # Ä°liÅŸki durum deÄŸiÅŸikliÄŸi
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
    # Yatay kÃ¼me iliÅŸkisi
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
    # KÃ¼me lifecycle
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
    "YoÄŸurma Motoru, bilgiyi deÄŸiÅŸtirmeden; kaynak kÃ¶kenini, "
    "statÃ¼sÃ¼nÃ¼, zamanÄ±nÄ± ve baÄŸlamÄ±nÄ± koruyarak bilgileri anlamlÄ± "
    "kÃ¼meler ve iliÅŸkisel yapÄ±lar hÃ¢line getirir. Bilgiyi tek bir "
    "kÃ¼meye hapsetmez; gerektiÄŸinde Ã§oklu Ã¼yeliÄŸi, ana/alt yapÄ±larÄ± "
    "ve yatay iliÅŸkili kÃ¼meleri korur. Zaman iÃ§inde geliÅŸen olaylarÄ±n "
    "sÃ¼rekliliÄŸini ve kÃ¼melerin yaÅŸam dÃ¶ngÃ¼sÃ¼nÃ¼ izler; kapanan veya "
    "deÄŸiÅŸen yapÄ±larÄ± silmez. Ä°liÅŸkilerin mevcut ve geÃ§miÅŸ durumlarÄ±nÄ± "
    "korur ancak bunlarÄ±n gÃ¼cÃ¼nÃ¼, doÄŸruluÄŸunu, gÃ¼venilirliÄŸini veya "
    "Ã¶nemini deÄŸerlendirmez. YoÄŸurma Motoru bilgiyi analiz etmez, "
    "hesaplamaz, sentezlemez, tahmin etmez ve karar Ã¼retmez. Ã‡Ä±ktÄ±sÄ±, "
    "7. BÃ¶lÃ¼m â€” Analiz / Hesaplama / DeÄŸerlendirme iÃ§in analize hazÄ±r "
    "iliÅŸkili ve baÄŸlamsal bilgi yapÄ±larÄ±dÄ±r."
)




# ============================================================================
# 18. MAIN
# ============================================================================




if __name__ == "__main__":
    validate_6()


    print(
        "6. BÃ–LÃœM â€” YOÄžURMA MOTORU"
    )
    print("=" * 72)


    print(
        "READ-ONLY INTELLIGENCE | KARAR ÃœRETMEZ"
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


