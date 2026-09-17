from pathlib import Path
from typing import Any


def build_master_cv_markdown(
    *,
    source_path: str | Path,
    raw_text: str,
    metadata: dict[str, Any],
) -> str:
    """Build the transient canonical Markdown representation of an uploaded CV.

    The Markdown is an in-memory processing artifact. The original PDF/DOCX is not
    copied into the application workspace, and this function does not persist the
    Markdown to disk. Downstream processing must use this returned string.
    """
    source = Path(source_path)
    lines = [
        "# Master CV — Extracted Markdown",
        "",
        "> Transient ingestion representation. The original source document is not stored.",
        "> Content must not be invented, summarized away, or silently removed at this stage.",
        "",
        "## Source Metadata",
        "",
        f"- **Original file name:** `{source.name}`",
        f"- **File type:** `{source.suffix.lower().lstrip('.')}`",
        f"- **Extractor:** `{metadata.get('extractor', 'unknown')}`",
        f"- **Page count:** `{metadata.get('page_count') if metadata.get('page_count') is not None else 'unknown'}`",
        "",
        "## Source Text",
        "",
        raw_text.rstrip(),
        "",
    ]
    return "\n".join(lines)
