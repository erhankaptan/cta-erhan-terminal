# ============================================================


from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple


from .access_channel import AccessChannel
from .master_source import MasterSource
from .source_identity_status import SourceIdentityStatus
from .source_type import SourceType


class AccessMethod(str, Enum):
    API = "API"
    CSV = "CSV"
    PDF = "PDF"
    HTML = "HTML"
    X = "X"
    OTHER = "OTHER"


class AccessMode(str, Enum):
    AUTOMATED = "AUTOMATED"
    PROGRAMMATIC_PARTIAL = "PROGRAMMATIC_PARTIAL"
    MANUAL = "MANUAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"


class InformationContentType(str, Enum):
    TEXT = "TEXT"
    NUMERIC = "NUMERIC"
    TABLE = "TABLE"
    CHART = "CHART"
    SCREENSHOT = "SCREENSHOT"
    PHOTO = "PHOTO"
    INFOGRAPHIC = "INFOGRAPHIC"
    DIAGRAM = "DIAGRAM"
    MAP = "MAP"
    VISUAL_PANEL = "VISUAL_PANEL"


@dataclass(frozen=True)
class SourceAccess:
    source_id: str
    access_method: AccessMethod
    access_mode: AccessMode
    endpoint: Optional[str] = None
    verified: bool = False


@dataclass(frozen=True)
class MultimodalContent:
    content_types: Tuple[InformationContentType, ...] = ()
    source_id: Optional[str] = None
    provenance_preserved: bool = True


@dataclass(frozen=True)
class DataSource:
    master_source: MasterSource
    access_methods: Tuple[AccessMethod, ...] = ()
    access_modes: Tuple[AccessMode, ...] = ()
    scope: Tuple[str, ...] = ()
    content_types: Tuple[InformationContentType, ...] = ()
    accesses: Tuple[SourceAccess, ...] = ()
    multimodal: Optional[MultimodalContent] = None


# ============================================================
