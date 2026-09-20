import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS cv_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    sha256 TEXT NOT NULL UNIQUE,
    page_count INTEGER,
    extractor TEXT NOT NULL,
    ingested_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS candidate_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    profile_json TEXT NOT NULL,
    missing_fields_json TEXT NOT NULL,
    extraction_status TEXT NOT NULL,
    extraction_error TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    FOREIGN KEY(document_id) REFERENCES cv_documents(id)
);

CREATE TABLE IF NOT EXISTS evidence_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    extracted_value_json TEXT,
    claim TEXT,
    source_text TEXT,
    source_location TEXT,
    status TEXT NOT NULL,
    confidence REAL,
    extraction_method TEXT NOT NULL,
    FOREIGN KEY(profile_id) REFERENCES candidate_profiles(id)
);
"""


class SQLiteStore:
    def __init__(self, db_path: str | Path = "data/job_agent.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)
        self._migrate_legacy_document_columns()
        self.conn.commit()

    def _migrate_legacy_document_columns(self) -> None:
        """Remove persisted source content/path columns from legacy databases.

        SQLite cannot drop columns safely on every supported version, so rebuild the
        table when an older schema contains file_path/raw_text. Existing structured
        metadata and hashes are retained; source document content is deliberately
        discarded.
        """
        columns = {
            row[1]
            for row in self.conn.execute("PRAGMA table_info(cv_documents)")
        }

        if "file_path" not in columns and "raw_text" not in columns:
            return

        self.conn.execute(
            "ALTER TABLE cv_documents RENAME TO cv_documents_legacy"
        )

        self.conn.execute("""
            CREATE TABLE cv_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                sha256 TEXT NOT NULL UNIQUE,
                page_count INTEGER,
                extractor TEXT NOT NULL,
                ingested_at TEXT NOT NULL
            )
        """)

        self.conn.execute("""
            INSERT INTO cv_documents(
                id,
                file_name,
                file_type,
                sha256,
                page_count,
                extractor,
                ingested_at
            )
            SELECT
                id,
                file_name,
                file_type,
                sha256,
                page_count,
                extractor,
                ingested_at
            FROM cv_documents_legacy
        """)

        self.conn.execute("DROP TABLE cv_documents_legacy")

    def deactivate_profiles(self) -> None:
        self.conn.execute(
            "UPDATE candidate_profiles SET is_active=0 WHERE is_active=1"
        )
        self.conn.commit()

    def get_document_by_sha256(
        self,
        sha256: str,
    ) -> dict[str, Any] | None:
        row = self.conn.execute(
            """
            SELECT
                id,
                file_name,
                file_type,
                sha256,
                page_count,
                extractor,
                ingested_at
            FROM cv_documents
            WHERE sha256 = ?
            """,
            (sha256,),
        ).fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "file_name": row[1],
            "file_type": row[2],
            "sha256": row[3],
            "page_count": row[4],
            "extractor": row[5],
            "ingested_at": row[6],
        }

    def add_document(
        self,
        *,
        file_name: str,
        file_type: str,
        sha256: str,
        page_count: int | None,
        extractor: str,
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()

        cur = self.conn.execute(
            """
            INSERT INTO cv_documents(
                file_name,
                file_type,
                sha256,
                page_count,
                extractor,
                ingested_at
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                file_name,
                file_type,
                sha256,
                page_count,
                extractor,
                now,
            ),
        )

        self.conn.commit()
        return int(cur.lastrowid)

    def add_profile(
        self,
        document_id: int,
        profile: dict[str, Any],
        missing_fields: list[str],
        status: str = "COMPLETE",
        error: str | None = None,
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()

        cur = self.conn.execute(
            """
            INSERT INTO candidate_profiles(
                document_id,
                profile_json,
                missing_fields_json,
                extraction_status,
                extraction_error,
                is_active,
                created_at
            )
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                document_id,
                json.dumps(profile, ensure_ascii=False),
                json.dumps(missing_fields),
                status,
                error,
                1,
                now,
            ),
        )

        self.conn.commit()
        return int(cur.lastrowid)

    def add_evidence(self, profile_id: int, items: list[Any]) -> None:
        for item in items:
            self.conn.execute(
                """
                INSERT INTO evidence_items(
                    profile_id,
                    field_name,
                    extracted_value_json,
                    claim,
                    source_text,
                    source_location,
                    status,
                    confidence,
                    extraction_method
                )
                VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    profile_id,
                    item.field_name,
                    json.dumps(
                        item.extracted_value,
                        ensure_ascii=False,
                    ),
                    item.claim,
                    item.source_text,
                    item.source_location,
                    item.status,
                    item.confidence,
                    item.extraction_method,
                ),
            )

        self.conn.commit()

    def close(self) -> None:
        self.conn.close()