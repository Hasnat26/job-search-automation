import json
from typing import Any

PROFILE_KEYS = [
    "full_name", "email", "phone", "current_location", "work_authorization",
    "visa_status", "willing_to_relocate", "preferred_countries", "preferred_regions",
    "preferred_industries", "preferred_job_titles", "languages", "skills",
    "certifications", "education", "experiences", "projects"
]

SYSTEM_PROMPT = """You extract a candidate profile from CV text. Use ONLY facts explicitly supported by the CV. Never infer visa status, work authorization, sponsorship, nationality, qualifications, dates, employers, skills, or experience. Missing information MUST be null or []. For every non-empty scalar, list item, education, experience, project, skill, certification, or language claim, attach an evidence object containing an exact verbatim supporting snippet from the CV. If a claim has no exact snippet, do not output it as a fact. Return JSON only. Do not wrap JSON in markdown fences."""


def build_extraction_prompt(cv_text: str) -> str:
    keys = ", ".join(PROFILE_KEYS)
    return f"{SYSTEM_PROMPT}\n\nRequired top-level keys: {keys}\n\nCV TEXT:\n{cv_text}"


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
    result = dict(profile)
    for key in PROFILE_KEYS:
        if key not in result or result[key] is None:
            result[key] = [] if key.endswith("s") or key in {"education", "experiences", "projects"} else None
    return result
