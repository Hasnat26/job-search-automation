from pathlib import Path
from typing import Any


def build_master_cv_markdown(
    *,
    source_path: str | Path,
    raw_text: str,
    metadata: dict[str, Any],
) -> str:
    """Create a lossless, processing-friendly Markdown representation of an uploaded CV.

    This stage intentionally does not summarize, tailor, or remove content. The extracted
    text is preserved verbatim inside a source section so later AI processing can work from
    a stable Markdown artifact while retaining provenance.
    """
    source = Path(source_path)
    lines = [
        "# Master CV — Extracted Markdown",
        "",
        "> Generated from the user's uploaded source document. This is an ingestion artifact,",
        "> not a tailored CV. Content must not be invented, summarized away, or silently removed.",
        "",
        "## Source Metadata",
        "",
        f"- **Original file:** `{source.name}`",
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


def write_master_cv_markdown(
    *,
    source_path: str | Path,
    raw_text: str,
    metadata: dict[str, Any],
    output_path: str | Path | None = None,
) -> Path:
    source = Path(source_path).expanduser().resolve()
    target = Path(output_path).expanduser().resolve() if output_path else source.with_suffix('.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        build_master_cv_markdown(source_path=source, raw_text=raw_text, metadata=metadata),
        encoding="utf-8",
    )
    return target
