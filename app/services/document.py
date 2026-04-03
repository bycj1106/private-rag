from app.db import sqlite, chroma
from app.db.sqlite import DocumentDetailRecord, DocumentRecord
from app.config import get_settings


def _normalize_non_empty_text(value: str, error_message: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(error_message)
    return normalized


def ensure_file_name_has_md_extension(file_name: str) -> str:
    if not file_name.endswith(".md"):
        file_name += ".md"
    return file_name


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> list[str]:
    settings = get_settings()
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if chunk_overlap is None:
        chunk_overlap = settings.chunk_overlap

    if not text or not text.strip():
        return []
    
    separator = "\n\n"
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end >= len(text):
            chunk = text[start:]
            if chunk.strip():
                chunks.append(chunk)
            break
        
        chunk = text[start:end]
        
        sep_pos = chunk.rfind(separator)
        if sep_pos > 0:
            end = start + sep_pos + len(separator)
            chunk = text[start:end]
        
        if chunk.strip():
            chunks.append(chunk)
        
        effective_overlap = min(chunk_overlap, chunk_size - 1) if chunk_overlap > 0 else 0
        next_start = end - effective_overlap if effective_overlap > 0 else end
        start = next_start if next_start > start else end
    
    return chunks


def create_document(file_content: str, file_name: str) -> DocumentRecord:
    _normalize_non_empty_text(file_content, "Document content cannot be empty")
    file_name = _normalize_non_empty_text(file_name, "File name cannot be empty")
    file_name = ensure_file_name_has_md_extension(file_name)
    chunks = chunk_text(file_content)
    chunk_count = len(chunks)
    doc = sqlite.create_document(file_name, file_content, chunk_count)

    try:
        chroma.add_chunks(doc["id"], chunks, file_name)
    except Exception:
        sqlite.delete_document(doc["id"])
        raise
    
    return doc


def get_document(doc_id: str) -> DocumentDetailRecord | None:
    return sqlite.get_document(doc_id)


def get_all_documents(limit: int = None, offset: int = None) -> list[DocumentRecord]:
    return sqlite.get_all_documents(limit=limit, offset=offset)


def get_documents_count() -> int:
    return sqlite.get_documents_count()


def delete_document(doc_id: str) -> bool:
    chroma.delete_chunks(doc_id)
    return sqlite.delete_document(doc_id)
