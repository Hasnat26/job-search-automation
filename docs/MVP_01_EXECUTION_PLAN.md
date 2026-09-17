# MVP-01 Execution Plan

## Goal
Build the first executable Universal Job Agent path:

`CV → text + metadata → local Ollama/Qwen JSON → evidence gate → candidate profile → SQLite`

## Components
- PDF: PyMuPDF
- DOCX: python-docx
- TXT/MD: standard library
- LLM: Ollama HTTP API, default `qwen3:8b`
- Persistence: SQLite
- Tests: pytest-compatible tests

## Trust model
- The LLM proposes structured facts and evidence.
- Code verifies that each evidence snippet is an exact substring of the source text.
- Only claims with verified snippets can remain as supported facts.
- Unsupported claims are cleared and recorded as missing.
- Missing immigration/work-authorization information remains UNKNOWN; it is never treated as permission to work.

## Retry/failure
- LLM JSON is requested with Ollama's JSON mode.
- Parse/validation gets one retry.
- Persistent failure is stored as an extraction failure and no candidate facts are created.
- Empty/near-empty CV extraction fails loudly.

## CLI
`python -m backend.cli ingest-cv ./data/cv.pdf`

Optional:
`--db data/job_agent.db --model qwen3:8b`

## Next increments
1. Add a richer Pydantic JSON schema and field-level evidence validation.
2. Add adapter mapping to existing Career Knowledge / Master CV entities.
3. Inspect and wrap the existing job-search implementation rather than replacing it.
4. Add normalized Job schema and source adapters.
5. Add deterministic immigration hard blockers and GO/CONDITIONAL/NO-GO scoring.
6. Add evidence-aware tailored CV generation.
7. Connect n8n only for orchestration/notifications/workflows; core truth and screening stay in Python.
