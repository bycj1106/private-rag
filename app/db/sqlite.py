import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Generator, Optional, TypedDict

from app.config import ensure_data_dirs, get_settings


class DocumentRecord(TypedDict):
    id: str
    file_name: str
    chunk_count: int
    created_at: str


class DocumentDetailRecord(DocumentRecord):
    content: str


def _create_connection() -> sqlite3.Connection:
    ensure_data_dirs()
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = _create_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                content TEXT NOT NULL,
                chunk_count INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documents_created_at
            ON documents(created_at DESC)
        """)
        conn.commit()


def create_document(file_name: str, content: str, chunk_count: int) -> DocumentRecord:
    doc_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO documents (id, file_name, content, chunk_count, created_at) VALUES (?, ?, ?, ?, ?)",
            (doc_id, file_name, content, chunk_count, created_at)
        )
        conn.commit()
    
    return {
        "id": doc_id,
        "file_name": file_name,
        "chunk_count": chunk_count,
        "created_at": created_at
    }


def get_document(doc_id: str) -> Optional[DocumentDetailRecord]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()

    return dict(row) if row else None


def get_all_documents(limit: int = None, offset: int = None) -> list[DocumentRecord]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT id, file_name, chunk_count, created_at FROM documents ORDER BY created_at DESC"
        params = []
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset is not None:
            query += " OFFSET ?"
            params.append(offset)
        cursor.execute(query, params)
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]


def get_documents_count() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        row = cursor.fetchone()
    
    return row[0] if row else 0


def delete_document(doc_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        affected = cursor.rowcount
        conn.commit()
    
    return affected > 0


def document_exists(doc_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM documents WHERE id = ?", (doc_id,))
        exists = cursor.fetchone() is not None
    
    return exists


def health_check() -> bool:
    with get_connection() as conn:
        conn.execute("SELECT 1")
    return True
