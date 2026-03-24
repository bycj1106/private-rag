import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Optional, Generator
from contextlib import contextmanager
from app.config import get_settings


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                content TEXT NOT NULL,
                chunk_count INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        """)
        conn.commit()


def create_document(file_name: str, content: str, chunk_count: int) -> dict:
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
        "content": content,
        "chunk_count": chunk_count,
        "created_at": created_at
    }


def get_document(doc_id: str) -> Optional[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
    
    if row:
        return dict(row)
    return None


def get_all_documents() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, file_name, chunk_count, created_at FROM documents ORDER BY created_at DESC")
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]


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
