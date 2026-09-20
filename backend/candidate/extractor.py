import json
from typing import Any

PROFILE_KEYS = [
    "full_name", "email", "phone", "current_location", "work_authorization",
    "visa_status", "willing_to_relocate", "preferred_countries", "preferred_regions",
    "preferred_industries", "preferred_job_titles", "languages", "skills",
    "certifications", "education", "experiences", "projects"
]

# Ollama commonly runs with a 4K-token context on local machines. Keep each
# extraction request comfortably below that limit so a 30-40 page CV is not
# silently truncated.
DEFAULT_CHUNK_CHARS = 4000
DEFAULT_OVERLAP_CHARS = 200

SYSTEM_PROMPT = """Extract candidate facts from the supplied CV section using ONLY explicit text. Never infer visa status, work authorization, sponsorship, nationality, qualifications, dates, employers, skills, or experience.

Return ONLY one compact JSON object with exactly these keys: full_name, email, phone, current_location, work_authorization, visa_status, willing_to_relocate, preferred_countries, preferred_regions, preferred_industries, preferred_job_titles, languages, skills, certifications, education, experiences, projects, evidence.

Use null for unavailable scalar fields and [] for unavailable list fields. Keep list values concise. Do not repeat the same fact. Keep evidence compact: maximum one evidence object per extracted field and maximum 20 evidence objects total. Each evidence object MUST contain field_name, extracted_value, claim, raw_snippet, source_location, and confidence. raw_snippet MUST be an exact verbatim substring of this CV section. Use null for unavailable source_location. Keep claim short. Use confidence 1.0 only when raw_snippet exactly supports the value; otherwise do not create the evidence item. Do not invent snippets. Do not output markdown, explanations, query, response, or any other keys."""


def build_extraction_prompt(cv_text: str, *, chunk_index: int = 1, total_chunks: int = 1) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"CV SECTION {chunk_index} OF {total_chunks}:\n"
        f"{cv_text}"
    )


def chunk_markdown(markdown: str, *, max_chars: int = DEFAULT_CHUNK_CHARS, overlap: int = DEFAULT_OVERLAP_CHARS) -> list[str]:
    """Split transient Markdown into bounded overlapping chunks."""
    if max_chars <= overlap:
        raise ValueError("max_chars must be greater than overlap")
    if not markdown.strip():
        return []
    chunks: list[str] = []
    start = 0
    length = len(markdown)
    while start < length:
        end = min(start + max_chars, length)
        if end < length:
            boundary = markdown.rfind("\n", start, end)
            if boundary > start + max_chars // 2:
                end = boundary
        chunks.append(markdown[start:end])
        if end >= length:
            break
        start = max(0, end - overlap)
    return chunks


def parse_profile_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Candidate extraction must return a JSON object")
    return value


def validate_profile(profile: dict[str, Any]) -> list[str]:
    return [key for key in PROFILE_KEYS if key not in profile]


def normalize_missing(profile: dict[str, Any]) -> dict[str, Any]:
    result = {key: profile.get(key) for key in PROFILE_KEYS}
    for key in PROFILE_KEYS:
        if result[key] is None and key in {"education", "experiences", "projects", "skills", "certifications", "languages", "preferred_countries", "preferred_regions", "preferred_industries", "preferred_job_titles"}:
            result[key] = []
    result["evidence"] = profile.get("evidence", [])
    return result


def merge_profiles(profiles: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge chunk-level extractions without allowing one chunk to erase another."""
    merged: dict[str, Any] = {key: None for key in PROFILE_KEYS}
    list_fields = {"preferred_countries", "preferred_regions", "preferred_industries", "preferred_job_titles", "languages", "skills", "certifications", "education", "experiences", "projects"}
    for key in list_fields:
        merged[key] = []
    merged["evidence"] = []

    for profile in profiles:
        profile = normalize_missing(profile)
        for key in PROFILE_KEYS:
            value = profile.get(key)
            if value in (None, "", []):
                continue
            if key in list_fields:
                existing = merged[key]
                for item in value:
                    if item not in existing:
                        existing.append(item)
            elif merged[key] in (None, ""):
                merged[key] = value
        evidence = profile.get("evidence", [])
        if isinstance(evidence, list):
            merged["evidence"].extend(item for item in evidence if isinstance(item, dict))

    return normalize_missing(merged)
