import argparse
import json
import os
import tempfile
from pathlib import Path

from backend.candidate.extractor import (
    build_extraction_prompt,
    chunk_markdown,
    merge_profiles,
    normalize_missing,
    parse_profile_json,
)
from backend.candidate.ingestion import sha256_file
from backend.candidate.markitdown_adapter import convert_to_markdown, read_markdown
from backend.candidate.ollama import OllamaProvider
from backend.database.sqlite import SQLiteStore
from backend.evidence.service import apply_evidence_gate, normalize_evidence


def convert_cv_to_markdown(path: str, output: str | None = None) -> dict:
    """Convert a document with the external MarkItDown repo/tool."""
    source = Path(path).expanduser().resolve()
    target = (
        Path(output).expanduser().resolve()
        if output
        else source.with_suffix(".md")
    )

    result = convert_to_markdown(source, target)
    result["processing_representation"] = "external_markitdown_markdown"
    return result


def _extract_chunks(markdown: str, provider: OllamaProvider) -> list[dict]:
    """Build a reliable baseline profile, with optional LLM enrichment."""
    from backend.candidate.extractor import extract_deterministic_profile

    baseline = extract_deterministic_profile(markdown)
    profiles = [baseline]

    # CPU-only machines should not block ingestion on an optional LLM call.
    # Enable explicitly with ENABLE_LLM_EXTRACTION=1.
    if os.getenv("ENABLE_LLM_EXTRACTION", "").lower() not in {"1", "true", "yes"}:
        print("Candidate extraction: deterministic baseline complete; LLM enrichment disabled", flush=True)
        return profiles

    chunks = chunk_markdown(markdown)
    print(f"Candidate extraction: {len(chunks)} chunks queued for optional LLM enrichment", flush=True)

    for index, chunk in enumerate(chunks, start=1):
        prompt = build_extraction_prompt(chunk, chunk_index=index, total_chunks=len(chunks))
        try:
            print(f"[chunk {index}/{len(chunks)}] optional LLM enrichment...", flush=True)
            parsed = parse_profile_json(provider.generate_json(prompt))
            profiles.append(normalize_missing(parsed))
            print(f"[chunk {index}/{len(chunks)}] enrichment completed", flush=True)
        except Exception as exc:
            print(f"[chunk {index}/{len(chunks)}] enrichment skipped: {exc}", flush=True)

    return profiles


def ingest_markdown(
    path: str,
    db_path: str = "data/job_agent.db",
    model: str | None = None,
    document_sha256: str | None = None,
) -> dict:
    """Ingest an already-created Markdown artifact."""
    markdown_path = Path(path).expanduser().resolve()

    markdown = read_markdown(markdown_path)

    document_sha256 = (
        document_sha256
        or sha256_file(markdown_path)
    )

    print(
        f"Candidate ingestion: read {len(markdown):,} "
        f"Markdown characters",
        flush=True,
    )

    provider = OllamaProvider(model=model)

    chunk_profiles = _extract_chunks(
        markdown,
        provider,
    )

    print(
        "Candidate extraction: merging knowledge...",
        flush=True,
    )

    parsed = merge_profiles(chunk_profiles)

    print(
        "Candidate extraction: validating evidence...",
        flush=True,
    )

    evidence = normalize_evidence(
        parsed.get("evidence", []),
        markdown,
        markdown_path.name,
    )

    gated, evidence_missing = apply_evidence_gate(
        parsed,
        evidence,
    )

    gated.pop("evidence", None)

    gated["missing_fields"] = sorted(
        set(evidence_missing)
    )

    print(
        "Candidate ingestion: saving structured knowledge...",
        flush=True,
    )

    store = SQLiteStore(db_path)

    try:
        store.deactivate_profiles()

        doc_id = store.add_document(
            file_name=markdown_path.name,
            file_type="md",
            sha256=document_sha256,
            page_count=None,
            extractor="external-markitdown",
        )

        profile_id = store.add_profile(
            doc_id,
            gated,
            gated["missing_fields"],
        )

        store.add_evidence(
            profile_id,
            evidence,
        )

    finally:
        store.close()

    print(
        "Candidate ingestion: complete",
        flush=True,
    )

    return {
        "document_id": doc_id,
        "profile_id": profile_id,
        "active_profile_rebuilt": True,
        "chunks_processed": len(chunk_profiles),
        "markdown_persisted": True,
        "profile": gated,
        "evidence_count": len(evidence),
        "verified": sum(
            e.status == "VERIFIED"
            for e in evidence
        ),
        "user_confirmed": sum(
            e.status == "USER_CONFIRMED"
            for e in evidence
        ),
        "inferred": sum(
            e.status == "INFERRED"
            for e in evidence
        ),
        "unknown": sum(
            e.status == "UNKNOWN"
            for e in evidence
        ),
        "missing_fields": gated["missing_fields"],
    }


def ingest_cv(
    path: str,
    db_path: str = "data/job_agent.db",
    model: str | None = None,
) -> dict:
    """End-to-end CV ingestion with duplicate protection."""

    source = Path(path).expanduser().resolve()

    if not source.is_file():
        raise FileNotFoundError(source)

    # Calculate the identity of the ORIGINAL CV.
    source_sha256 = sha256_file(source)

    # Check for an existing document BEFORE running
    # MarkItDown or Ollama.
    store = SQLiteStore(db_path)

    try:
        existing = store.get_document_by_sha256(
            source_sha256
        )
    finally:
        store.close()

    if existing is not None:
        print(
            "CV ingestion: duplicate detected; "
            "skipping conversion and extraction",
            flush=True,
        )

        return {
            "document_id": existing["id"],
            "profile_id": None,
            "active_profile_rebuilt": False,
            "chunks_processed": 0,
            "markdown_persisted": False,
            "profile": None,
            "evidence_count": 0,
            "verified": 0,
            "user_confirmed": 0,
            "inferred": 0,
            "unknown": 0,
            "missing_fields": [],
            "source_file": str(source),
            "source_persisted": False,
            "converter": None,
            "duplicate": True,
            "message": (
                "CV already ingested; "
                "skipped duplicate processing"
            ),
        }

    # Only new CVs reach MarkItDown/Ollama.
    with tempfile.TemporaryDirectory(
        prefix="job-agent-md-"
    ) as temp_dir:

        temporary_md = (
            Path(temp_dir)
            / f"{source.stem}.md"
        )

        print(
            "CV ingestion: converting with external MarkItDown...",
            flush=True,
        )

        conversion = convert_to_markdown(
            source,
            temporary_md,
        )

        print(
            "CV ingestion: Markdown ready "
            f"({conversion['markdown_characters']:,} characters)",
            flush=True,
        )

        result = ingest_markdown(
            str(temporary_md),
            db_path=db_path,
            model=model,
            document_sha256=source_sha256,
        )

        result["source_file"] = str(source)
        result["source_persisted"] = False
        result["markdown_persisted"] = False
        result["converter"] = "external-markitdown"
        result["duplicate"] = False

        return result


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="job-agent"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    convert = sub.add_parser(
        "convert-cv",
        help=(
            "Convert PDF/DOCX/etc. to Markdown "
            "using external MarkItDown"
        ),
    )

    convert.add_argument("path")
    convert.add_argument(
        "--output",
        default=None,
    )

    ingest_md = sub.add_parser(
        "ingest-markdown",
        help=(
            "Build candidate knowledge from "
            "an existing Markdown file"
        ),
    )

    ingest_md.add_argument("path")
    ingest_md.add_argument(
        "--db",
        default="data/job_agent.db",
    )
    ingest_md.add_argument(
        "--model",
        default=None,
    )

    ingest = sub.add_parser(
        "ingest-cv",
        help=(
            "Convert with MarkItDown, then "
            "ingest temporary Markdown"
        ),
    )

    ingest.add_argument("path")
    ingest.add_argument(
        "--db",
        default="data/job_agent.db",
    )
    ingest.add_argument(
        "--model",
        default=None,
    )

    args = parser.parse_args()

    if args.command == "convert-cv":
        result = convert_cv_to_markdown(
            args.path,
            args.output,
        )

    elif args.command == "ingest-markdown":
        result = ingest_markdown(
            args.path,
            args.db,
            args.model,
        )

    elif args.command == "ingest-cv":
        result = ingest_cv(
            args.path,
            args.db,
            args.model,
        )

    else:
        raise RuntimeError(
            f"Unsupported command: {args.command}"
        )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()