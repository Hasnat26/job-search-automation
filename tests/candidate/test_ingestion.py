from pathlib import Path
import pytest
from backend.candidate.ingestion import extract_text, sha256_file, validate_cv_path


def test_text_ingestion_and_hash(tmp_path: Path):
    cv = tmp_path / "cv.txt"
    cv.write_text("John Doe\nProject Manager\n10 years experience", encoding="utf-8")
    text, meta = extract_text(cv)
    assert "Project Manager" in text
    assert meta["extractor"] == "plain_text"
    assert len(sha256_file(cv)) == 64


def test_unsupported_extension(tmp_path: Path):
    bad = tmp_path / "cv.exe"
    bad.write_text("x")
    with pytest.raises(ValueError):
        validate_cv_path(bad)


def test_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        validate_cv_path(tmp_path / "missing.pdf")
