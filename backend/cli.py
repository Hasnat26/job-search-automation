import argparse
import json

from backend.candidate.extractor import build_extraction_prompt, normalize_missing, parse_profile_json, validate_profile
from backend.candidate.ingestion import extract_text, sha256_file, validate_cv_path
from backend.candidate.markdown import build_master_cv_markdown
from backend.candidate.ollama import OllamaProvider
from backend.database.sqlite import SQLiteStore
from backend.evidence.service import apply_evidence_gate, normalize_evidence


def convert_cv_to_markdown(path: str) -> dict:
    """Convert an uploaded CV to transient Markdown without writing the Markdown to disk."""
    candidate = validate_cv_path(path)
    raw_text, meta = extract_text(candidate)
    if len(raw_text.strip()) < 50:
        raise RuntimeError("CV conversion failed: extracted text is empty or too short")
    markdown = build_master_cv_markdown(source_path=candidate, raw_text=raw_text, metadata=meta)
    return {
        "source_file": str(candidate),
        "markdown_persisted": False,
        "processing_representation": "in_memory_markdown",
        "file_type": candidate.suffix.lower().lstrip("."),
        "page_count": meta.get("page_count"),
        "extractor": meta.get("extractor"),
        "source_characters": len(raw_text),
        "markdown_characters": len(markdown),
    }


def ingest_cv(path: str, db_path: str = "data/job_agent.db", model: str | None = None) -> dict:
    candidate = validate_cv_path(path)
    raw_text, meta = extract_text(candidate)
    if len(raw_text.strip()) < 50:
        raise RuntimeError("CV ingestion failed: extracted text is empty or too short")

    # Markdown is the only downstream document representation and exists only in memory.
    markdown = build_master_cv_markdown(source_path=candidate, raw_text=raw_text, metadata=meta)

    provider = OllamaProvider(model=model)
    prompt = build_extraction_prompt(markdown)
    last_error: Exception | None = None
    for _ in range(2):
        try:
            parsed = normalize_missing(parse_profile_json(provider.generate_json(prompt)))
            missing = validate_profile(parsed)
            break
        except Exception as exc:
            last_error = exc
    else:
        store = SQLiteStore(db_path)
        doc_id = store.add_document(file_name=candidate.name, file_path="", file_type=candidate.suffix.lower().lstrip('.'), sha256=sha256_file(candidate), raw_text="", page_count=meta.get('page_count'), extractor=meta['extractor'])
        store.add_profile(doc_id, {}, [], status="FAILED", error=str(last_error))
        store.close()
        raise RuntimeError(f"Candidate extraction failed after retry: {last_error}") from last_error

    raw_evidence = parsed.get("evidence", [])
    evidence = normalize_evidence(raw_evidence, markdown, candidate.name)
    gated, evidence_missing = apply_evidence_gate(parsed, evidence)
    gated.pop("evidence", None)
    gated["missing_fields"] = sorted(set(missing + evidence_missing))

    store = SQLiteStore(db_path)
    doc_id = store.add_document(file_name=candidate.name, file_path="", file_type=candidate.suffix.lower().lstrip('.'), sha256=sha256_file(candidate), raw_text="", page_count=meta.get('page_count'), extractor=meta['extractor'])
    profile_id = store.add_profile(doc_id, gated, gated['missing_fields'])
    store.add_evidence(profile_id, evidence)
    store.close()
    return {"document_id": doc_id, "profile_id": profile_id, "markdown_persisted": False, "profile": gated, "evidence_count": len(evidence), "verified": sum(e.status == 'VERIFIED' for e in evidence), "inferred": sum(e.status == 'INFERRED' for e in evidence), "unknown": sum(e.status == 'UNKNOWN' for e in evidence), "missing_fields": gated['missing_fields']}


def main() -> None:
    parser = argparse.ArgumentParser(prog="job-agent")
    sub = parser.add_subparsers(dest="command", required=True)

    convert = sub.add_parser("convert-cv", help="Convert an uploaded CV to transient in-memory Markdown")
    convert.add_argument("path")

    ingest = sub.add_parser("ingest-cv", help="Convert a CV to transient Markdown and build an evidence-aware candidate profile")
    ingest.add_argument("path")
    ingest.add_argument("--db", default="data/job_agent.db")
    ingest.add_argument("--model", default=None)

    args = parser.parse_args()
    if args.command == "convert-cv":
        result = convert_cv_to_markdown(args.path)
    elif args.command == "ingest-cv":
        result = ingest_cv(args.path, args.db, args.model)
    else:
        raise RuntimeError(f"Unsupported command: {args.command}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
