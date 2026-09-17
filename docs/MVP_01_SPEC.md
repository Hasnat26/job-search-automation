# MVP-01 — Candidate Intelligence

## Definition of done
`CV → Candidate Profile → Evidence → SQLite` is executable, testable, and candidate-independent.

## Supported CV formats
- PDF
- DOCX
- TXT
- Markdown

## Evidence states
- VERIFIED — exact source snippet supports the claim.
- INFERRED — model interpretation; never treated as verified fact.
- UNKNOWN — source does not support the fact.
- USER_CONFIRMED — explicitly confirmed by the candidate.
- CONFLICT — contradictory source evidence.

## Hard rules
- No evidence → no supported claim.
- LLM cannot promote a claim to VERIFIED.
- `UNKNOWN != YES`.
- Visa/work authorization/sponsorship must not be inferred from country, employer, or job history.
- Candidate-specific data is never hard-coded.

## Failure cases
1. Unsupported file → reject.
2. Empty/near-empty extraction → fail loudly.
3. Invalid LLM JSON → retry once, then persist extraction failure.
4. Evidence snippet not found verbatim in source → not VERIFIED.
5. Missing immigration data → UNKNOWN.
6. Contradictory source data → CONFLICT in a later evidence reconciliation step.
