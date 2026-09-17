import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS cv_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    sha256 TEXT NOT NULL UNIQUE,
    raw_text TEXT NOT NULL,
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
        self.conn.commit()

    def add_document(self, *, file_name: str, file_path: str, file_type: str, sha256: str, raw_text: str, page_count: int | None, extractor: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        cur = self.conn.execute("INSERT INTO cv_documents(file_name,file_path,file_type,sha256,raw_text,page_count,extractor,ingested_at) VALUES (?,?,?,?,?,?,?,?)", (file_name,file_path,file_type,sha256,raw_text,page_count,extractor,now))
        self.conn.commit()
        return int(cur.lastrowid)

    def add_profile(self, document_id: int, profile: dict[str, Any], missing_fields: list[str], status: str = "COMPLETE", error: str | None = None) -> int:
        now = datetime.now(timezone.utc).isoformat()
        cur = self.conn.execute("INSERT INTO candidate_profiles(document_id,profile_json,missing_fields_json,extraction_status,extraction_error,created_at) VALUES (?,?,?,?,?,?)", (document_id,json.dumps(profile,ensure_ascii=False),json.dumps(missing_fields),status,error,now))
        self.conn.commit()
        return int(cur.lastrowid)

    def add_evidence(self, profile_id: int, items: list[Any]) -> None:
        for item in items:
            self.conn.execute("INSERT INTO evidence_items(profile_id,field_name,extracted_value_json,claim,source_text,source_location,status,confidence,extraction_method) VALUES (?,?,?,?,?,?,?,?,?)", (profile_id,item.field_name,json.dumps(item.extracted_value,ensure_ascii=False),item.claim,item.source_text,item.source_location,item.status,item.confidence,item.extraction_method))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
