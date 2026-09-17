from typing import Any
from backend.candidate.schemas import EvidenceItem


def _snippet_is_supported(snippet: Any, source_text: str) -> bool:
    return isinstance(snippet, str) and bool(snippet.strip()) and snippet.strip() in source_text


def normalize_evidence(raw_evidence: Any, source_text: str, source_file: str, method: str = "llm") -> list[EvidenceItem]:
    if not isinstance(raw_evidence, list):
        return []
    result: list[EvidenceItem] = []
    for item in raw_evidence:
        if not isinstance(item, dict):
            continue
        field_name = item.get("field_name") or item.get("field")
        snippet = item.get("raw_snippet") or item.get("source_text") or item.get("evidence")
        value = item.get("extracted_value", item.get("value"))
        if not field_name:
            continue
        supported = _snippet_is_supported(snippet, source_text)
        status = "VERIFIED" if supported else ("INFERRED" if value not in (None, "", []) else "UNKNOWN")
        confidence = item.get("confidence")
        if not isinstance(confidence, (int, float)):
            confidence = 1.0 if supported else 0.0
        result.append(EvidenceItem(field_name=str(field_name), extracted_value=value, claim=str(item.get("claim") or ""), source_file=source_file, source_text=snippet if supported else None, source_location=item.get("source_location"), status=status, confidence=float(confidence), extraction_method=method))
    return result


def apply_evidence_gate(profile: dict[str, Any], evidence: list[EvidenceItem]) -> tuple[dict[str, Any], list[str]]:
    """Remove unsupported material claims; missing data stays UNKNOWN/null."""
    verified_fields = {e.field_name for e in evidence if e.status in {"VERIFIED", "USER_CONFIRMED"}}
    gated = dict(profile)
    missing: list[str] = []
    for field, value in list(gated.items()):
        if field == "evidence" or value in (None, "", []):
            continue
        if field not in verified_fields:
            gated[field] = [] if isinstance(value, list) else None
            missing.append(field)
    return gated, sorted(set(missing))
