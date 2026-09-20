# ============================================================


from __future__ import annotations


from dataclasses import dataclass
from typing import Optional


from .access_channel import AccessChannel
from .claim_verification_status import ClaimVerificationStatus
from .information_class import InformationClass
from .source_role import SourceRole


@dataclass(frozen=True)
class Claim:
    claim_id: str
    master_source_id: str
    content: str
    information_class: InformationClass
    source_role: SourceRole
    claim_verification_status: ClaimVerificationStatus = (
        ClaimVerificationStatus.UNRESOLVED
    )
    access_channel: Optional[AccessChannel] = None
    evidence_notes: Optional[str] = None


# ============================================================
