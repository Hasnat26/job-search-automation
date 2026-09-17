# Universal AI Job Search Platform — Architecture

## Product direction
`Hasnat26/job-search-automation` is the primary product repository. Existing Career Knowledge / Master CV / evidence assets remain authoritative; the Universal Job Agent is an adapter-driven layer around them.

## Runtime flow

`CV → Candidate Profile → Evidence → Job Sources → Normalized Job → Requirement Matrix → Eligibility → Shortlist → Tailored CV → Application → Tracking`

## Core rules
1. Candidate data is data/configuration, not hard-coded application logic.
2. Master CV remains the source of truth for application generation.
3. Evidence gates factual claims.
4. LLMs extract/interpret; deterministic code makes hard-gate decisions.
5. `UNKNOWN` never satisfies a hard requirement.
6. Immigration/eligibility conclusions retain source evidence.
7. Job connectors are modular: DIRECT, ASSISTED, or MANUAL.
8. No CAPTCHA/MFA/authentication bypass and no deliberate platform restriction bypass.

## Supporting components
- MarkItDown fork: document ingestion option.
- PyMuPDF/python-docx: deterministic extraction fallback.
- Ollama + local Qwen: semantic extraction/matching/tailoring.
- Existing LinkedIn jobs-guest search code: to be wrapped after inspection.
- n8n: orchestration, scheduling, notifications, email workflows; not the source of truth.
- browser-use: later permitted browser assistance.
- Open WebUI: optional local AI workspace.
- Hermes Agent: optional orchestration layer, not the primary domain runtime.

## Delivery order
1. Candidate intelligence.
2. Job intelligence and normalization.
3. Eligibility and immigration gates.
4. Shortlist/reporting.
5. Evidence-gated tailored CV and cover letter.
6. Application preparation/tracking.
7. Optional permitted browser/email automation.
8. Multi-user/cloud deployment.
