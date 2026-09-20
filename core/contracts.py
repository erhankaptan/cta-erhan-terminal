from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime

@dataclass(frozen=True)
class RawEvidence:
    source_id: str
    timestamp: str
    raw_content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class StructuredInformation:
    evidence_id: str
    timestamp: str
    extracted_data: Dict[str, Any]
    provenance: str

@dataclass(frozen=True)
class CanonicalRecord:
    record_id: str
    timestamp: str
    canonical_data: Dict[str, Any]
    provenance: str
    version: int

@dataclass(frozen=True)
class PipelineContext:
    execution_id: str
    point_in_time: str
    read_only: bool = True