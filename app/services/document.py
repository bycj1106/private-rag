from app.db import sqlite, chroma


def ensure_file_name_has_md_extension(file_name: str) -> str:
    if not file_name.endswith(".md"):
        file_name += ".md"
    return file_name


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> list[str]:
    if chunk_size is None:
        chunk_size = 500
    if chunk_overlap is None:
        chunk_overlap = 50
    
    separator = "\n\n"
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        chunk = text[start:end]
        sep_pos = chunk.rfind(separator)
        if sep_pos != -1:
            chunk = chunk[:sep_pos]
        
        chunks.append(chunk)
        start = start + len(chunk) - chunk_overlap if chunk_overlap > 0 else start + len(chunk)
    
    return chunks


def create_document(file_content: str, file_name: str) -> dict:
    if not file_content or not file_content.strip():
        raise ValueError("Document content cannot be empty")
    
    file_name = ensure_file_name_has_md_extension(file_name)
    
    chunks = chunk_text(file_content)
    chunk_count = len(chunks)
    
    doc = sqlite.create_document(file_name, file_content, chunk_count)
    
    chroma.add_chunks(doc["id"], chunks, file_name)
    
    return doc


def get_document(doc_id: str) -> dict | None:
    return sqlite.get_document(doc_id)


def get_all_documents() -> list[dict]:
    return sqlite.get_all_documents()


def delete_document(doc_id: str) -> bool:
    if not sqlite.document_exists(doc_id):
        return False
    
    chroma.delete_chunks(doc_id)
    return sqlite.delete_document(doc_id)
