# MVP-02 — Candidate Knowledge Extraction

## Purpose

Convert the transient Markdown representation of an uploaded Master CV into a persistent, evidence-aware Candidate Knowledge Base.

## Storage rule

- The uploaded PDF/DOCX/TXT is an input only.
- Markdown exists only in memory during processing.
- No original CV bytes, raw CV text, or `.md` artifact are stored by the application.
- Persistent storage contains structured candidate knowledge, evidence, metadata, and hashes needed for traceability/deduplication.

## Update rule

A user may upload a replacement Master CV at any time. The newly extracted candidate knowledge becomes the active profile. The system must not require a CV upload for every job request.

## Evidence policy

- `VERIFIED`: directly supported by an exact source snippet.
- `USER_CONFIRMED`: explicitly confirmed by the user.
- `INFERRED`: model interpretation; never automatically used as a factual CV claim.
- `UNKNOWN`: not supported by the source.
- `CONFLICT`: contradictory source evidence requiring review.

Generated CVs may use only `VERIFIED` and `USER_CONFIRMED` claims unless the user explicitly reviews and confirms another claim.

## Required behavior

1. Extract from the transient Markdown, not directly from the source binary.
2. Preserve supported facts; do not summarize away potentially useful information.
3. Do not invent immigration/work authorization, nationality, sponsorship, dates, employers, qualifications, skills, or achievements.
4. Keep exact evidence snippets for important claims.
5. Mark unsupported fields as `UNKNOWN`.
6. Separate candidate knowledge from job-specific tailoring.
7. Support both workflows: user-provided JD and system-discovered jobs.
