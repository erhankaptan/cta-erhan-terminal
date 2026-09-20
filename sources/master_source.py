# ============================================================


from __future__ import annotations


from dataclasses import dataclass, field
from typing import Dict, Tuple


from .access_channel import AccessChannel
from .source_identity_status import SourceIdentityStatus
from .source_role import SourceRole
from .source_type import SourceType


@dataclass(frozen=True)
class MasterSource:
    master_source_id: str
    name: str
    source_type: SourceType
    source_identity_status: SourceIdentityStatus = (
        SourceIdentityStatus.UNRESOLVED
    )
    access_channels: Tuple[AccessChannel, ...] = ()
    source_roles: Tuple[SourceRole, ...] = ()
    metadata: Dict[str, str] = field(default_factory=dict)


# ============================================================
