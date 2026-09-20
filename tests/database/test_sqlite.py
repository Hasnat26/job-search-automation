from pathlib import Path

from backend.database.sqlite import SQLiteStore


def test_get_document_by_sha256(tmp_path: Path):
    db = tmp_path / "test.db"
    store = SQLiteStore(db)

    try:
        document_id = store.add_document(
            file_name="cv.md",
            file_type="md",
            sha256="abc123",
            page_count=None,
            extractor="external-markitdown",
        )

        document = store.get_document_by_sha256("abc123")

        assert document is not None
        assert document["id"] == document_id
        assert document["file_name"] == "cv.md"
        assert document["sha256"] == "abc123"
    finally:
        store.close()


def test_get_document_by_sha256_returns_none_for_unknown_hash(
    tmp_path: Path,
):
    db = tmp_path / "test.db"
    store = SQLiteStore(db)

    try:
        assert store.get_document_by_sha256("does-not-exist") is None
    finally:
        store.close()
