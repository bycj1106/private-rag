import chromadb
import threading
from app.config import get_settings


_client = None
_client_lock = threading.Lock()


def get_chroma_client():
    global _client
    if _client is None:
        with _client_lock:
            if _client is None:
                settings = get_settings()
                _client = chromadb.PersistentClient(path=settings.chroma_dir)
    return _client


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name="documents")


def add_chunks(document_id: str, chunks: list[str], file_name: str):
    collection = get_collection()
    
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_id": document_id, "file_name": file_name, "chunk_index": i}
        for i in range(len(chunks))
    ]
    
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )


def search_chunks(query: str, top_k: int) -> list[dict]:
    collection = get_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    chunks = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            chunks.append({
                "content": doc,
                "file_name": results["metadatas"][0][i]["file_name"],
                "relevance_score": float(results["distances"][0][i]) if results["distances"] else 0.0
            })
    
    return chunks


def delete_chunks(document_id: str):
    collection = get_collection()
    collection.delete(where={"document_id": document_id})


def get_collection_count() -> int:
    collection = get_collection()
    return collection.count()
