import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

from backend.cli import ingest_cv


APP_DIR = Path(__file__).resolve().parent.parent
FRONTEND_INDEX = APP_DIR / "frontend" / "index.html"

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

app = FastAPI(title="Job Search Automation", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    if not FRONTEND_INDEX.is_file():
        raise HTTPException(status_code=500, detail="Frontend is missing")
    return HTMLResponse(FRONTEND_INDEX.read_text(encoding="utf-8"))


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/cv")
async def upload_cv(file: UploadFile = File(...)) -> dict:
    filename = Path(file.filename or "").name
    suffix = Path(filename).suffix.lower()

    if not filename:
        raise HTTPException(status_code=400, detail="A CV file is required")

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Supported CV formats: PDF, DOCX, TXT, MD",
        )

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded CV is empty")

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="CV exceeds the 10 MB upload limit",
        )

    db_path = os.getenv("JOB_AGENT_DB", "data/job_agent.db")
    model = os.getenv("OLLAMA_MODEL", "qwen3:8b")

    with tempfile.TemporaryDirectory(prefix="job-agent-upload-") as temp_dir:
        upload_path = Path(temp_dir) / filename
        upload_path.write_bytes(content)

        try:
            result = ingest_cv(
                str(upload_path),
                db_path=db_path,
                model=model,
            )
        except FileNotFoundError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"CV processing failed: {exc}",
            ) from exc

    return result
