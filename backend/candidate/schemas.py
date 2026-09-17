from dataclasses import dataclass, field
from typing import Any, Literal

EvidenceStatus = Literal["VERIFIED", "INFERRED", "UNKNOWN", "USER_CONFIRMED", "CONFLICT"]

@dataclass
class EvidenceItem:
    field_name: str
    extracted_value: Any = None
    claim: str = ""
    source_file: str | None = None
    source_section: str | None = None
    source_text: str | None = None
    source_location: str | None = None
    status: EvidenceStatus = "UNKNOWN"
    confidence: float | None = None
    extraction_method: str = "llm"

@dataclass
class CandidateProfile:
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    current_location: str | None = None
    work_authorization: str | None = None
    visa_status: str | None = None
    willing_to_relocate: bool | None = None
    preferred_countries: list[str] = field(default_factory=list)
    preferred_regions: list[str] = field(default_factory=list)
    preferred_industries: list[str] = field(default_factory=list)
    preferred_job_titles: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    education: list[dict[str, Any]] = field(default_factory=list)
    experiences: list[dict[str, Any]] = field(default_factory=list)
    projects: list[dict[str, Any]] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)

CRITICAL_FIELDS = (
    "work_authorization", "visa_status", "willing_to_relocate",
)
