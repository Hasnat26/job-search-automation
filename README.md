# Universal AI Job Search Automation

Primary repository for a candidate-independent, evidence-aware job search and application platform.

## Current MVP
CV → document ingestion → local Ollama/Qwen extraction → evidence gate → candidate profile → SQLite.

## Run
```bash
pip install -r requirements.txt
python -m backend.cli ingest-cv ./data/cv.pdf --model qwen3:8b
```

Ollama is expected at `http://127.0.0.1:11434`. Override with `OLLAMA_BASE_URL` and `OLLAMA_MODEL`.

## Product rule
`UNKNOWN != YES` and `INFERRED != VERIFIED`. The Master CV/evidence layer remains the source of truth; automation may prepare work but must not fabricate candidate facts or bypass CAPTCHA/MFA/authentication controls.
